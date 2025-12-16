# Pygame-Updated

A small arcade-style Pygame project where you control a paddle to catch falling cubes. This is an updated version of my first Pygame game, created to practice Python fundamentals, game loops, collision detection, and simple power-up systems.

## Gameplay
- Move the paddle left/right to catch falling red cubes.
- Catching a cube increases your **score** and respawns the cube near the top.
- Missing a cube (it falls off the bottom) normally costs **1 life**.
- When **lives reach 0**, the game ends.

## Features (Updated Version)
- **Lives + Score** tracking (HUD)
- **Second falling cube spawns at Score = 5**
- **Power-up: Paddle Width Boost (Green)**
  - Catch the green power-up to increase paddle width
- **Power-up: Shield (Blue)**
  - Catch the blue shield to turn **Shield ON**
  - Shield blocks the **next missed cube** (prevents losing a life once), then turns OFF
- **Restart support**
  - Press **R** on the Game Over screen to reset the game

## Controls
- **Left Arrow** — move left  
- **Right Arrow** — move right  
- **R** — restart (Game Over screen)  
- **Close Window** — quit  

## Requirements
- Python 3.x
- Pygame

## Installation
Install Pygame:
```bash
pip install pygame

