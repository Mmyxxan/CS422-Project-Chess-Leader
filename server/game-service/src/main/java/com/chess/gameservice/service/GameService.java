package com.chess.gameservice.service;

import com.chess.gameservice.dto.AiMoveResponse;
import com.chess.gameservice.exception.GameException;
import com.chess.gameservice.game.Game;
import com.chess.gameservice.game.GamePhase;
import com.chess.gameservice.game.ai.MinMax;
import com.chess.gameservice.game.move.PlayerMove;
import com.chess.gameservice.game.piece.PieceType;
import com.chess.gameservice.game.player.Player;
import com.chess.gameservice.game.player.PlayerColor;
import com.chess.gameservice.game.position.Position;
import com.chess.gameservice.messages.events.GameOverEvent;
import com.chess.gameservice.messages.external.StartGameMessage;
import com.chess.gameservice.messages.external.User;
import com.chess.gameservice.messages.payloads.AvailableMovesPayload;
import com.chess.gameservice.messages.payloads.PlayerMovePayload;

import org.springframework.http.*;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;


@Service
public class GameService {

    private final HashMap<UUID, Game> games = new HashMap<>();
    private final MinMax minMax = new MinMax();
    private final ApplicationEventPublisher applicationEventPublisher;
    @Value("${ai.chess.move-url}")
    private String aiMovelUrl;
    private final RestTemplate rest;

    public GameService(ApplicationEventPublisher applicationEventPublisher, RestTemplate rest) {
        this.applicationEventPublisher = applicationEventPublisher;
        this.rest = rest;
    }

    public Optional<UUID> getGameWithUser(String playerName) {
        for (Game game : games.values()) {
            Optional<UUID> gameId = game.isPlayerPresentInGame(playerName);
            if (gameId.isPresent()) {
                return gameId;
            }
        }
        return Optional.empty();
    }

    public Game forfeitGame(UUID gameId, String playerName) throws GameException {
        Game game = games.get(gameId);
        if (game == null) {
            throw new GameException("Game is already over.");
        }
        Optional<UUID> response = game.isPlayerPresentInGame(playerName);
        if (response.isEmpty()) {
            throw new GameException("Player not in game.");
        }
        game.forfeit(playerName);
        gameFinished(gameId);
        return game;
    }

    public Optional<Game> connect(UUID gameId, String playerName) {
        synchronized (games) {
            try {
                while (!games.containsKey(gameId)) {
                    games.wait();
                }
            } catch (InterruptedException ignored) {
            }
            Game game = games.get(gameId);
            if (game == null) {
                return Optional.empty();
            }
            Optional<UUID> response = game.isPlayerPresentInGame(playerName);
            if (response.isEmpty()) {
                return Optional.empty();
            }
            return Optional.of(game);
        }
    }

    @KafkaListener(topics = "${kafka-topics.start-game}")
    public void initGame(@Payload StartGameMessage message) {
        UUID gameId = message.getGameId();
        Game game = new Game();
        ArrayList<User> players = message.getUsers();
        game.setGameId(gameId);
        game.setWithAi(message.isWithAi());
        game.setPlayer(new Player(players.get(0).getLogin()), PlayerColor.WHITE);
        game.setPlayer(new Player(players.get(1).getLogin()), PlayerColor.BLACK);
        game.initGame(gameId);
        games.put(gameId, game);
    }

    public AvailableMovesPayload getAvailableMoves(UUID gameId, Position position, String name) throws GameException {
        Game game = games.get(gameId);
        if (game == null) {
            throw new GameException("Game is already over");
        }
        Player player = new Player(name);
        AvailableMovesPayload availableMovesPayload = new AvailableMovesPayload();
        availableMovesPayload.setPosition(position);
        availableMovesPayload.setAvailableMoves(game.getAvailableMoves(position, player));
        return availableMovesPayload;
    }

    public Game makeMove(UUID gameId, PlayerMovePayload playerMovePayload, String playerName) throws GameException {
        Game game = games.get(gameId);
        Player player = new Player(playerName);
        game.makeMove(playerMovePayload, player);
        if (game.isOver()) {
            gameFinished(gameId);
        }
        return game;
    }

    public Game makePromotion(UUID gameId, Position playerMove, PieceType selectedPromotion, String playerName) throws GameException {
        Game game = games.get(gameId);
        Player player = new Player(playerName);
        game.makePromotion(playerMove, player, selectedPromotion);
        return game;
    }

    public Game playerOutOfTime(UUID gameId) {
        Game game = games.get(gameId);
        if (game == null) {
            return null;
        }
        game.playerTimedOutOrOutOfTime();
        gameFinished(gameId);
        return game;
    }

    public Game makeAiMove(UUID gameId) throws GameException {
        Game game = games.get(gameId);
        if (game == null) return null;

        if (game.getBoard().getPositionAwaitingPromotion() == null) {
            // build the JSON payload
            Map<String,String> payload = Map.of(
                "fen",        game.getFenString(),
                "difficulty", "easy"
            );

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String,String>> entity = new HttpEntity<>(payload, headers);

            // do the call
            ResponseEntity<AiMoveResponse> response = rest.exchange(
                aiMovelUrl,
                HttpMethod.POST,
                entity,
                AiMoveResponse.class
            );

            // log response
            if (response.getStatusCode() != HttpStatus.OK) {
                throw new GameException("AI service returned error: " + response.getStatusCode());
            }

            AiMoveResponse aiMove = response.getBody();
            if (aiMove == null) {
                throw new GameException("AI returned empty response");
            }

            var moveDto = aiMove.getPlayerMove();
            Position from = new Position(
                moveDto.getInitialPosition().getX(),
                moveDto.getInitialPosition().getY()
            );
            Position to = new Position(
                moveDto.getDestinationPosition().getX(),
                moveDto.getDestinationPosition().getY()
            );

            game.makeAiMove(new PlayerMovePayload(from, to), new Player("Computer"));
        }

        if (game.getGamePhase() == GamePhase.GAME_OVER) {
            gameFinished(gameId);
        }
        return game;
    }

    @Scheduled(fixedDelay = 3600000)
    public synchronized void removeInactiveGames() {
        ArrayList<UUID> gamesToRemove = new ArrayList<>();
        games.values().forEach(game -> {
            long minutes = ChronoUnit.MINUTES.between(game.getStartTime(), LocalDateTime.now());
            if (Math.abs(minutes) > 30) {
                gamesToRemove.add(game.getGameId());
            }
        });
        gamesToRemove.forEach(this::gameFinished);
    }


    public synchronized void gameFinished(UUID gameId) {
        Game game = games.get(gameId);
        applicationEventPublisher.publishEvent(new GameOverEvent(this, game));
        game.beforeDestroy();
        games.remove(gameId);
    }
}
