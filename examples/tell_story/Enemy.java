package com.example.story;

public class Enemy {
    private String name;

    public Enemy(String name) {
        this.name = name;
    }

    public void capture(Princess princess) {
        princess.setCaptured(true);
    }

    public void guard(Princess princess) {
        // guarding logic
    }
}
