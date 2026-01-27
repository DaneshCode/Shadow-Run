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

        # Ensure data directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Load existing scores
        self.load()

    def load(self):
        """Load leaderboard from file"""
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, "r") as f:
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
            with open(self.filepath, "w") as f:
                json.dump({"entries": self.entries}, f, indent=2)
        except IOError as e:
            print(f"Error saving leaderboard: {e}")

    def add_entry(self, name, score, distance, coins=0):
        """
        Add a new entry to the leaderboard

        Args:
            name: Player name
            score: Final score
            distance: Distance traveled
            coins: Coins collected

        Returns:
            int: Rank of the new entry (1-based), or 0 if not in top entries
        """
        entry = {"name": name, "score": score, "distance": distance, "coins": coins}

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

    def is_high_score(self, score):
        """
        Check if a score would be a new high score

        Args:
            score: Score to check

        Returns:
            bool: True if score beats current high score
        """
        return score > self.get_high_score()

    def would_make_leaderboard(self, score):
        """
        Check if a score would make it onto the leaderboard

        Args:
            score: Score to check

        Returns:
            bool: True if score would be in top entries
        """
        if len(self.entries) < self.max_entries:
            return True
        return score > self.entries[-1]["score"]

    def get_rank(self, score):
        """
        Get the rank a score would achieve

        Args:
            score: Score to check

        Returns:
            int: Rank (1-based), or 0 if wouldn't make leaderboard
        """
        if not self.would_make_leaderboard(score):
            return 0

        for i, entry in enumerate(self.entries):
            if score > entry["score"]:
                return i + 1

        return len(self.entries) + 1

    def clear(self):
        """Clear all leaderboard entries"""
        self.entries = []
        self.save()
