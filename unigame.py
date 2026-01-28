"""
 shadow-run
===============================
A professional 2D endless platformer game built with Pygame

Controls:
      "Jump: SPACE / W / UP Arrow",
      "Flip Gravity: SHIFT / S / DOWN Arrow / F",
      "Shoot: LEFT CLICK / X / Z / CTRL",
      "Pause: ESC or P",

Features:
    - Endless procedurally generated world
    - Progressive difficulty system
    - Multiple enemy types
    - Collectibles and power-ups
    - Health and score systems
    - Leaderboard with persistent high scores
    - Smooth camera following
    - Particle effects
    - Parallax background
"""

import sys
import os

# Ensure we can import from the game package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check for Pygame installation
try:
    import pygame
except ImportError:
    print("=" * 60)
    print("ERROR: Pygame is not installed!")
    print("Please install it using: pip install pygame")
    print("=" * 60)
    sys.exit(1)

from game.game import Game


def main():
    """Main entry point for the game"""
    print("=" * 60)
    print("  SHADOW RUN : endless nightmare")
    print("=" * 60)
    print("  Starting game...")
    print("=" * 60)

    # Create and run the game
    game = Game()
    game.run()

    print()
    print("Thanks for playing!")
    print("=" * 60)


if __name__ == "__main__":
    main()
