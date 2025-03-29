package com.chess.queueservice.messages.kafka;

import com.chess.queueservice.models.User;
import lombok.*;

import java.util.ArrayList;
import java.util.UUID;
import com.chess.queueservice.models.AIDifficulty;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class StartGameMessage {
    UUID gameId;
    ArrayList<User> users;
    boolean withAi;
    AIDifficulty aiDifficulty; // Optional field for AI games
}
