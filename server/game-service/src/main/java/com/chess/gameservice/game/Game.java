package com.chess.gameservice.game;

import com.chess.gameservice.exception.GameException;
import com.chess.gameservice.game.board.Board;
import com.chess.gameservice.game.board.CheckState;
import com.chess.gameservice.game.move.PlayerMove;
import com.chess.gameservice.game.piece.Piece;
import com.chess.gameservice.game.piece.PieceType;
import com.chess.gameservice.game.player.Player;
import com.chess.gameservice.game.player.PlayerColor;
import com.chess.gameservice.game.player.Players;
import com.chess.gameservice.game.position.Position;
import com.chess.gameservice.game.turn.CurrentTurn;
import com.chess.gameservice.game.turn.GameTurn;
import com.chess.gameservice.messages.payloads.PlayerMovePayload;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.Setter;

import java.lang.reflect.Array;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Optional;
import java.util.UUID;

@Getter
@Setter
public class Game {
    private Board board;
    private Players players;
    private CurrentTurn currentTurn;
    private GamePhase gamePhase;
    private PlayerMove latestMove;
    @JsonIgnore
    private LocalDateTime startTime;
    @JsonIgnore
    private UUID gameId;
    @JsonIgnore
    private boolean withAi;

    @JsonIgnore
    private ArrayList<GameTurn> gameTurns;

    public Game() {
        board = new Board();
        players = new Players();
        gameTurns = new ArrayList<>();
        gamePhase = GamePhase.WAITING_FOR_PLAYERS;
        currentTurn = new CurrentTurn();
        latestMove = new PlayerMove();
        startTime = LocalDateTime.now();
    }
    
}
