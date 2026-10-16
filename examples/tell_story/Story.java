package com.example.story;

public class Story {
    private Hero hero;
    private Enemy enemy;
    private Princess princess;

    public Story() {
        this.hero = new Hero("Arthur");
        this.enemy = new Enemy("Dragon");
        this.princess = new Princess("Guinevere");
    }

    public void start() {
        enemy.capture(princess);
    }

    public void tell() {
        hero.fight(enemy);
        hero.save(princess);
    }
}
