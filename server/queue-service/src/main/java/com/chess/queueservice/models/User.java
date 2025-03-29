package com.chess.queueservice.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import com.chess.queueservice.models.AIDifficulty;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class User {
    private String login;
    private String sessionId;
    private AIDifficulty difficulty;
    
    // Constructor without difficulty for backward compatibility
    public User(String login, String sessionId) {
        this.login = login;
        this.sessionId = sessionId;
        this.difficulty = null;
    }
}

