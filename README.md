# Shadow Run: Endless Nightmare

Shadow Run is a 2D endless horror runner built with Python and Pygame. The player auto-runs through an infinite nightscape, flips gravity between the ground and ceiling, shoots enemies, collects coins, and uses a charged ghost mode to pass through danger.

## Features

- Endless procedurally generated ground and ceiling lanes
- Gravity flip movement for ground and ceiling traversal
- Shooting with limited ammo and timed regeneration
- Charged ghost mode for temporary invisibility
- Ground, ceiling, flying, chasing, shooting, ghost, teleporter, spider, berserker, and swarm enemy patterns
- Score, coins, health packs, power-ups, and persistent local leaderboard
- Dynamic difficulty scaling based on score
- Parallax horror background, particles, screen shake, and reactive ambient audio
- Menu, tutorial, pause, settings, game over, and leaderboard screens

## Controls

| Action | Input |
| --- | --- |
| Jump | `Space` / `W` / `Up Arrow` |
| Flip gravity | `Shift` / `S` / `Down Arrow` / `F` |
| Shoot | `Left Click` / `X` / `Z` / `Ctrl` |
| Ghost mode | `Right Click` / `C` / `G` / HUD button |
| Pause | `Esc` / `P` |

## Installation

Requirements:

- Python 3.8+
- Pygame

Install and run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python unigame.py
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python unigame.py
```

## Project Structure

```text
Shadow-Run/
  unigame.py              Main entry point
  requirements.txt        Python dependency list
  assets/
    audio/                Ambient audio tracks
    sprites/              Player animation frames
  data/
    leaderboard.json      Local high score storage
  docs/
    gdd/                  English interactive GDD
    gdd-fa/               Persian interactive GDD
  game/
    game.py               Main game loop and state manager
    player.py             Player movement, shooting, ghost mode
    enemies.py            Enemy classes and spawning
    platforms.py          Ground, ceiling, and world generation
    collectibles.py       Coins, health packs, and power-ups
    difficulty.py         Score-based difficulty scaling
    camera.py             Camera follow and screen shake
    background.py         Parallax background and visual effects
    sound.py              Audio loading, fallback, and ambient mix
    ui.py                 HUD and screens
    leaderboard.py        High score persistence
    settings.py           Constants and tuning
    utils.py              Shared helpers
```

## Gameplay Notes

- Ghost mode must charge before use. Watch the circular HUD button.
- Enemy shooters can appear on both ground and ceiling.
- Swarms unlock at higher scores, so gravity flips and ammo timing matter more as the run continues.
- Ammo regenerates slowly; save shots for enemies that block your lane.

## Verification

Compile the game modules:

```bash
python -m compileall unigame.py game
```

## Credits

Developer: Danesh Khodadadzadeh
Engine: Pygame
