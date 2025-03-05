package com.server.authentication_service.service.impl;

import com.server.authentication_service.dto.UserDto;
import com.server.authentication_service.model.User;
import com.server.authentication_service.service.UserService;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class UserServiceImpl implements UserService {
    @Override
    public UserDto save(User user) {
        return null;
    }

    @Override
    public UserDto login(User user) {
        return null;
    }

    @Override
    public UserDto authorize(String login) {
        return null;
    }
}
