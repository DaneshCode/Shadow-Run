# Endless Runner - Ultimate Platformer 🎮

A complete, polished, and professional 2D endless platformer game built with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Features

### Core Gameplay

- **Endless Procedural World**: Infinitely generated platforms and terrain
- **Progressive Difficulty**: Game becomes harder as you score more points
- **Smooth Physics**: Realistic gravity, friction, and momentum
- **Responsive Controls**: Tight player movement with variable jump height

### Player Mechanics

- **Running & Walking**: Acceleration-based movement with friction
- **Jumping**: Variable height jump with double-jump power-up
- **Health System**: Damage, invincibility frames, and health pickups
- **Score System**: Points from distance, coins, and defeating enemies

### Enemies

- **Basic Enemies**: Patrolling ground enemies
- **Flying Enemies**: Sine-wave movement patterns
- **Chaser Enemies**: Aggressive enemies that pursue the player
- **Shooter Enemies**: Stationary turrets that fire projectiles

### Collectibles & Power-ups

- **Coins**: Score multipliers scattered throughout
- **Health Packs**: Restore player health
- **Power-ups**: Speed boost, invincibility, double jump, magnet

### Platform Types

- **Static Platforms**: Regular solid platforms
- **Moving Platforms**: Horizontal and vertical movement
- **Crumbling Platforms**: Fall apart after standing on them

### Visual Features

- **Parallax Background**: Multi-layer scrolling scenery
- **Particle Effects**: Dynamic particles for impacts and pickups
- **Camera System**: Smooth player-following with screen shake
- **Animations**: Player and enemy animations

### Audio

- **Procedural Sound Effects**: Auto-generated sounds when no audio files exist
- **Support for Custom Audio**: Place your own sound files in `/assets/sounds/`

### Menus & UI

- **Main Menu**: Clean, navigable main menu
- **Pause System**: Pause and resume gameplay
- **Game Over Screen**: Score summary and options
- **Leaderboard**: Persistent high scores saved to JSON
- **Settings Screen**: Volume controls and key bindings display
- **HUD**: Health bar, score, coins, distance, and difficulty display

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**

   ```bash
   cd ugme
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**

   ```bash
   pip install pygame
   ```

4. **Run the game**
   ```bash
   python unigame.py
   ```

## 🎮 Controls

| Action      | Keys                 |
| ----------- | -------------------- |
| Move Left   | `←` or `A`           |
| Move Right  | `→` or `D`           |
| Jump        | `Space`, `↑`, or `W` |
| Pause       | `Esc` or `P`         |
| Menu Select | `Enter` or Click     |

## 📁 Project Structure

```
ugme/
├── unigame.py           # Main entry point
├── game/
│   ├── __init__.py      # Package initialization
│   ├── settings.py      # Game configuration and constants
│   ├── utils.py         # Utility functions and helpers
│   ├── player.py        # Player class with movement and physics
│   ├── platforms.py     # Platform classes and world generation
│   ├── enemies.py       # Enemy types and spawning system
│   ├── collectibles.py  # Coins, health packs, and power-ups
│   ├── camera.py        # Camera following and effects
│   ├── sound.py         # Audio management
│   ├── background.py    # Parallax background and visual effects
│   ├── ui.py            # Menus, HUD, and UI elements
│   ├── leaderboard.py   # High score system
│   └── game.py          # Main game manager
├── assets/
│   ├── sprites/         # Player and enemy sprites
│   │   └── player/
│   │       ├── idle/
│   │       ├── walk/
│   │       ├── jump/
│   │       └── Dash2/
│   ├── sounds/          # Sound effects (optional)
│   └── fonts/           # Custom fonts (optional)
└── data/
    └── leaderboard.json # Saved high scores
```

## ⚙️ Configuration

Key settings can be adjusted in `game/settings.py`:

```python
# Display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Player Physics
PLAYER_SPEED = 6
PLAYER_JUMP_POWER = -16
GRAVITY = 0.8
FRICTION = 0.85

# Difficulty
DIFFICULTY_INCREASE_INTERVAL = 500
MAX_DIFFICULTY_LEVEL = 10
```

## 🎨 Customization

### Adding Custom Sprites

Place sprite images in the appropriate folders under `assets/sprites/player/`:

- `idle/` - Standing animation frames
- `walk/` - Walking animation frames
- `jump/` - Jumping animation frames
- `Dash2/` - Dashing animation frames

Images should be PNG format with transparency.

### Adding Sound Effects

Create an `assets/sounds/` folder and add WAV files:

- `jump.wav` - Jump sound
- `coin.wav` - Coin collection
- `hurt.wav` - Player damage
- `death.wav` - Game over
- `powerup.wav` - Power-up collection
- `click.wav` - Menu click
- `enemy_death.wav` - Enemy defeated

### Adding Background Music

Place a music file (MP3, OGG, or WAV) in `assets/sounds/` and load it in the game.

## 🏗️ Architecture

The game uses an object-oriented, modular architecture:

- **Game Manager** (`game.py`): Central coordinator for all systems
- **Entity System**: Player, enemies, and collectibles are all sprites
- **Spawner Pattern**: World, enemy, and collectible spawners generate content
- **State Machine**: Game states (menu, playing, paused, game over) control flow
- **Observer Pattern**: Camera follows player, UI observes player stats

## 🔧 Extending the Game

### Adding a New Enemy Type

1. Create a new class in `enemies.py` extending `Enemy`
2. Override `_create_enemy_surface()` for appearance
3. Override `update()` for behavior
4. Add to `_choose_enemy_type()` in `EnemySpawner`

### Adding a New Power-up

1. Add type to `PowerUp.TYPES` in `collectibles.py`
2. Update `_create_surface()` for appearance
3. Implement effect in `collect()` method

### Adding a New Platform Type

1. Create class in `platforms.py` extending `Platform`
2. Override `update()` for behavior
3. Add spawning logic in `WorldGenerator`

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Credits

- Built with [Pygame](https://www.pygame.org/)
- Inspired by classic endless runners

---

**Enjoy the game! 🎮**
