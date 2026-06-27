package com.example.chat;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ChatService {
    private final RestTemplate restTemplate = new RestTemplate();
    private final String chatUrl;

    public ChatService(@Value("${ai.service.chat-url:http://localhost:8000/chat}") String chatUrl) {
        this.chatUrl = chatUrl;
    }

    public String chat(ChatRequest request) {
        Map<String, Object> aiRequest = new HashMap<>();
        aiRequest.put("message", request.getMessage());

        putIfPresent(aiRequest, "model", request.getModel());

        String result = restTemplate.postForObject(
                chatUrl,
                aiRequest,
                String.class);

        return result;
    }

    private void putIfPresent(Map<String, Object> request, String key, Object value) {
        if (value != null) {
            request.put(key, value);
        }
    }
}
