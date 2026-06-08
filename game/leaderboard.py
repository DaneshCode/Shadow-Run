"""
Leaderboard Module
Handles high score saving and loading
"""

import json
import os
from game.settings import *


class Leaderboard:
    """
    Manages the game's leaderboard/high scores
    """

    def __init__(self, filepath=LEADERBOARD_FILE):
        """
        Initialize the leaderboard

        Args:
            filepath: Path to the leaderboard JSON file
        """
        self.filepath = filepath
        self.entries = []
        self.max_entries = MAX_LEADERBOARD_ENTRIES

        # Ensure data directory exists when the file path includes one.
        data_dir = os.path.dirname(filepath)
        if data_dir:
            os.makedirs(data_dir, exist_ok=True)

        # Load existing scores
        self.load()

    def load(self):
        """Load leaderboard from file"""
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.entries = data.get("entries", [])
            else:
                self.entries = []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading leaderboard: {e}")
            self.entries = []

    def save(self):
        """Save leaderboard to file"""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump({"entries": self.entries}, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving leaderboard: {e}")

    def add_entry(self, name, score, coins=0):
        """
        Add a new entry to the leaderboard

        Args:
            name: Player name
            score: Final score
            coins: Coins collected

        Returns:
            int: Rank of the new entry (1-based), or 0 if not in top entries
        """
        entry = {"name": name, "score": score, "coins": coins}

        # Add entry
        self.entries.append(entry)

        # Sort by score (descending)
        self.entries.sort(key=lambda x: x["score"], reverse=True)

        # Trim to max entries
        self.entries = self.entries[: self.max_entries]

        # Find rank of new entry
        rank = 0
        for i, e in enumerate(self.entries):
            if e["score"] == score and e["name"] == name:
                rank = i + 1
                break

        # Save to file
        self.save()

        return rank

    def get_high_score(self):
        """
        Get the current high score

        Returns:
            int: Highest score, or 0 if no entries
        """
        if self.entries:
            return self.entries[0]["score"]
        return 0

    def get_entries(self):
        """
        Get all leaderboard entries

        Returns:
            list: List of entry dictionaries
        """
        return self.entries.copy()
