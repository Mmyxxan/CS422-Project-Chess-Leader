package com.server.authentication_service.service;

import com.server.authentication_service.dto.UserDto;
import com.server.authentication_service.model.User;

public interface UserService {

    UserDto save(User user);

    UserDto login(User user);

    UserDto authorize(String login);
}
