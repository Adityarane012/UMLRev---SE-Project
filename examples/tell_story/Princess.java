package com.example.story;

public class Princess {
    private String name;
    private boolean isCaptured;

    public Princess(String name) {
        this.name = name;
        this.isCaptured = false;
    }

    public void setCaptured(boolean captured) {
        this.isCaptured = captured;
    }

    public void release() {
        this.isCaptured = false;
    }

    public String getName() {
        return this.name;
    }
}
