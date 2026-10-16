package com.example.story;

public class Hero {
    private String name;

    public Hero(String name) {
        this.name = name;
    }

    public void save(Princess princess) {
        princess.release();
    }

    public void fight(Enemy enemy) {
        // combat logic
    }
}
