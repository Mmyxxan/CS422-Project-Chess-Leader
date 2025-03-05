package com.server.authentication_service.dto;

import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Builder
@Data
public class UserDto {
    private final String login;
    private final String email;
    private final String token;
}
