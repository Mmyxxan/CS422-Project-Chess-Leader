package com.chess.gameservice.messages.external;

import lombok.*;

import java.util.ArrayList;
import java.util.UUID;

import com.chess.gameservice.game.ai.AIDifficulty;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class StartGameMessage {
    UUID gameId;
    ArrayList<User> users;
    boolean withAi;
    AIDifficulty aiDifficulty;
}
