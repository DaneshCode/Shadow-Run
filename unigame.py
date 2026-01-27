"""
 shadow-run
===============================
A professional 2D endless platformer game built with Pygame

Controls:
    - SPACE or UP or W: Jump
    - ESC or P: Pause

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
    print("  ENDLESS RUNNER - Ultimate Platformer")
    print("=" * 60)
    print()
    print("  Controls:")
    print("    - Arrow Keys or WASD: Move")
    print("    - Space/Up/W: Jump")
    print("    - ESC or P: Pause")
    print()
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
