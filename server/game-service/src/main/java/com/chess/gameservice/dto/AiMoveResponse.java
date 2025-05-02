package com.chess.gameservice.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

@Data
public class AiMoveResponse {
    @JsonProperty("PlayerMove")
    private PlayerMoveDto PlayerMove;

    @Data
    public static class PlayerMoveDto {
        private Position initialPosition;
        private Position destinationPosition;

        @Data
        public static class Position {
            private int x, y;
        }
    }
    
}
