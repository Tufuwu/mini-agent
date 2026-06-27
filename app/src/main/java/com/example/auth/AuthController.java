package com.example.auth;

import java.util.UUID;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.user.User;
import com.example.user.UserRepository;

@RestController
@RequestMapping("/api/auth")
public class AuthController {
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
    private final UserRepository userRepository;

    public AuthController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Transactional
    @PostMapping("/register")
    public ResponseEntity<LoginResponse> register(@RequestBody RegisterRequest request) {
        if (!isValidRegisterRequest(request)) {
            return ResponseEntity.badRequest()
                    .body(new LoginResponse(false, "Username is required and password must be at least 6 characters", null));
        }

        String username = request.getUsername().trim();
        if (userRepository.existsByUsername(username)) {
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .body(new LoginResponse(false, "Username already exists", null));
        }

        String passwordHash = passwordEncoder.encode(request.getPassword());
        userRepository.save(new User(username, passwordHash, "USER"));

        String token = UUID.randomUUID().toString();
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new LoginResponse(true, "Registration successful", token));
    }

    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@RequestBody LoginRequest request) {
        if (isValidUser(request)) {
            String token = UUID.randomUUID().toString();
            return ResponseEntity.ok(new LoginResponse(true, "Login successful", token));
        }

        return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body(new LoginResponse(false, "Invalid username or password", null));
    }

    private boolean isValidRegisterRequest(RegisterRequest request) {
        return request != null
                && request.getUsername() != null
                && !request.getUsername().trim().isEmpty()
                && request.getUsername().trim().length() <= 64
                && request.getPassword() != null
                && request.getPassword().length() >= 6;
    }

    private boolean isValidUser(LoginRequest request) {
        if (request == null || request.getUsername() == null || request.getPassword() == null) {
            return false;
        }

        return userRepository.findByUsername(request.getUsername().trim())
                .map(user -> passwordEncoder.matches(request.getPassword(), user.getPasswordHash()))
                .orElse(false);
    }
}
