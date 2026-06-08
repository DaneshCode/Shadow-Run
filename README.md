<p align="center">
  <img src="https://img.shields.io/badge/SHADOW%20RUN-Endless%20Nightmare-8B0000?style=for-the-badge&labelColor=1a1a2e" alt="Shadow Run">
</p>

<h1 align="center">🌑 SHADOW RUN: Endless Nightmare 🌑</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20With-Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Engine-Pygame-brightgreen?style=flat-square&logo=python" alt="Pygame">
  <img src="https://img.shields.io/badge/Genre-Horror%20Runner-8B0000?style=flat-square" alt="Genre">
  <img src="https://img.shields.io/badge/Status-Playable-success?style=flat-square" alt="Status">
</p>

<p align="center">
  <b>🎮 An intense endless runner with horror atmosphere, gravity-defying mechanics, and nightmarish enemies! 🎮</b>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-gameplay">Gameplay</a> •
  <a href="#-controls">Controls</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-enemies">Enemies</a> •
  <a href="#-screenshots">Screenshots</a>
</p>

---

## 🎯 Overview

**Shadow Run: Endless Nightmare** is a fast-paced, atmospheric endless runner that plunges you into a dark, horror-themed world. Run, jump, flip gravity, and shoot your way through an ever-increasing nightmare as you try to survive as long as possible!

The game features smooth progressive difficulty scaling that makes the experience more challenging the further you go—without sudden spikes that break your flow.

---

## ⚔️ Features

### 🕹️ Core Mechanics

- **Gravity Flip System** — Defy physics! Switch between running on the ground and ceiling at will
- **Shooting System** — Blast through enemies with your weapon (5 ammo with auto-regeneration)
- **Invisibility Power** — Charge up and become invisible to pass through dangers
- **Double Jump** — Unlock the ability to jump in mid-air
- **Smooth Auto-Run** — The game runs automatically; you focus on survival!

### 🌙 Horror Atmosphere

- **Dark, moody visuals** with fog effects and eerie color palette
- **Nightmarish enemy designs** that get more terrifying as you progress
- **Haunting background** with dead trees, blood moon, and creeping shadows

### 📈 Progressive Difficulty

- **Smooth scaling** — Difficulty increases gradually based on your score
- **Enemy evolution** — New enemy types unlock as you progress:
  - Basic Enemies (Start)
  - Chasers (500+ score)
  - Shooters (1500+ score)
  - Berserkers (3000+ score)
  - Swarm Patterns (5000+ score)

### 🎨 Rich Content

- **10+ Enemy Types** — Including ground, ceiling, flying, ghost, teleporter, and spider enemies
- **Power-Ups & Collectibles** — Coins, health packs, and special abilities
- **Leaderboard System** — Compete for the highest score
- **Full Menu System** — Main menu, pause, settings, tutorial, and game over screens

---

## 🎮 Gameplay

Your goal is simple: **survive as long as possible** and rack up the highest score!

- Run automatically through an endless nightmare landscape
- Jump over obstacles and pits
- Flip gravity to run on the ceiling and dodge enemies
- Shoot enemies to clear your path
- Collect coins for bonus points
- Grab health packs to stay alive
- Use invisibility to phase through danger

---

## 🎹 Controls

| Action           | Key                 |
| ---------------- | ------------------- |
| **Jump**         | `SPACE` / `W` / `↑` |
| **Flip Gravity** | `F` / `G`           |
| **Shoot**        | `Left Click` / `X`  |
| **Invisibility** | `Right Click` / `C` |
| **Pause**        | `ESC` / `P`         |

---

## 💻 Installation

### Prerequisites

- Python 3.8+
- Pygame library

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/shadow-run.git
   cd shadow-run
   ```

2. **Install dependencies**

   ```bash
   pip install pygame
   ```

3. **Run the game**
   ```bash
   python unigame.py
   ```

---

## 👹 Enemies

| Enemy             | Description                     | Unlocks At |
| ----------------- | ------------------------------- | ---------- |
| **Basic Enemy**   | Patrols back and forth          | Start      |
| **Chaser**        | Aggressively pursues the player | 500 pts    |
| **Shooter**       | Fires projectiles at you        | 1500 pts   |
| **Berserker**     | Fast and deals heavy damage     | 3000 pts   |
| **Ceiling Enemy** | Lurks on the ceiling            | Various    |
| **Flying Enemy**  | Hovers and attacks from above   | Various    |
| **Ghost**         | Phases through obstacles        | Various    |
| **Teleporter**    | Blinks around unpredictably     | Various    |
| **Spider**        | Fast and deadly                 | Various    |

---

## 🏆 Scoring System

- **Distance** — The further you run, the more points you earn
- **Coins** — Each coin adds 10 points
- **Survival** — Stay alive to keep multiplying your score
- **Leaderboard** — Your top 10 scores are saved locally

---

## ⚙️ Technical Details

- **Resolution:** 1280 × 720
- **Frame Rate:** 60 FPS
- **Language:** Python 3
- **Engine:** Pygame
- **Architecture:** Modular OOP design with separate systems for player, enemies, UI, camera, sound, and more

---

## 📁 Project Structure

```
Shadow-Run/
├── unigame.py          # Main entry point
├── assets/
│   ├── audio/          # Sound effects and music
│   └── sprites/        # Player and enemy sprites
│       └── player/
│           ├── idle/
│           ├── walk/
│           ├── jump/
│           └── Dash2/
├── data/
│   └── leaderboard.json
└── game/
    ├── __init__.py
    ├── game.py         # Main game manager
    ├── player.py       # Player class
    ├── enemies.py      # All enemy types
    ├── platforms.py    # Ground and world generation
    ├── collectibles.py # Coins, health, power-ups
    ├── difficulty.py   # Progressive difficulty system
    ├── camera.py       # Camera system
    ├── background.py   # Visual effects
    ├── sound.py        # Audio manager
    ├── ui.py           # All UI screens
    ├── leaderboard.py  # Score tracking
    ├── settings.py     # Game configuration
    └── utils.py        # Helper utilities
```

---

## 🌟 Tips & Tricks

1. **Master gravity flipping** — It's your best tool for dodging enemies
2. **Save your ammo** — Bullets regenerate slowly, use them wisely
3. **Charge invisibility early** — Have it ready for emergencies
4. **Watch the ceiling** — Ceiling enemies are just as deadly as ground ones
5. **Don't panic at swarms** — Use gravity flip to escape large groups

---

## 📜 License

This project is open source and available under the MIT License.

---

## 🙏 Credits

- **Developer:** Danesh khodadadzadeh
- **Engine:** Pygame Community
- **Inspiration:** Classic endless runners with a horror twist

---

<p align="center">
  <b>⚡ Can you survive the endless nightmare? ⚡</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/GOOD%20LUCK-You'll%20Need%20It-8B0000?style=for-the-badge&labelColor=000000" alt="Good Luck">
</p>

---

<p align="center">
  <a href="README.fa.md">🇮🇷 نسخه فارسی</a>
</p>
