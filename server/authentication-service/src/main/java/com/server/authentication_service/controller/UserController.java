package com.server.authentication_service.controller;

import com.server.authentication_service.dto.UserDto;
import com.server.authentication_service.model.User;
import com.server.authentication_service.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@AllArgsConstructor
public class UserController {

    private final UserService userService;

    @PostMapping(value = "/authentication/register", consumes = "application/json", produces = "application/json")
    public ResponseEntity<UserDto> register(@RequestBody User user) {
        UserDto saveUser = userService.save(user);
        return ResponseEntity.ok().body(saveUser);
    }

    @PostMapping(value = "/authentication/login", consumes = "application/json", produces = "application/json")
    public ResponseEntity<UserDto> login(@RequestBody User user) {
        UserDto savedUser = userService.login(user);
        return ResponseEntity.ok().body(savedUser);
    }

    @PostMapping(value = "/authentication/authorize", consumes = "application/json", produces = "application/json")
    public ResponseEntity<UserDto> authorize(HttpServletRequest req) {
        UserDto user = userService.authorize(req.getRemoteUser());
        return ResponseEntity.ok().body(user);
    }
}
