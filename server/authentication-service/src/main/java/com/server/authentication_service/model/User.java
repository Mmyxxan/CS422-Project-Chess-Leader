package com.server.authentication_service.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotEmpty;
import lombok.Data;

@Entity
@Data
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;

    @NotEmpty(message = "Name cannot be empty.")
    @Column(nullable = false, unique = true)
    private String login;

    @Email(message = "Email must be valid")
    @Column(nullable = false, unique = true)
    private String email;

    @NotEmpty(message = "Password cannot be empty")
    private String password;

}
