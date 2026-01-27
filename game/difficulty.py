"""
Difficulty Manager Module
Handles smooth, score-based difficulty scaling for the endless runner
"""

import math
from game.settings import (
    BASE_GAME_SPEED,
    MAX_GAME_SPEED,
    GAME_SPEED_CURVE_STEEPNESS,
    BASE_SPAWN_INTERVAL,
    MIN_SPAWN_INTERVAL,
    BASE_SPAWN_CHANCE,
    MAX_SPAWN_CHANCE,
    BASE_ENEMY_SPEED_MULTIPLIER,
    MAX_ENEMY_SPEED_MULTIPLIER,
    DIFFICULTY_MAX_SCORE,
    MAX_DIFFICULTY_MULTIPLIER,
    DIFFICULTY_MILESTONE_INTERVAL,
    CHASER_UNLOCK_SCORE,
    SHOOTER_UNLOCK_SCORE,
    BERSERKER_UNLOCK_SCORE,
    SWARM_UNLOCK_SCORE,
    ENEMY_WEIGHTS_EARLY,
    ENEMY_WEIGHTS_MID,
    ENEMY_WEIGHTS_HARD,
    ENEMY_WEIGHTS_EXPERT,
    ENEMY_WEIGHTS_NIGHTMARE,
    SWARM_CHANCE_BASE,
    SWARM_CHANCE_MAX,
    SWARM_MIN_SIZE,
    SWARM_MAX_SIZE,
)


class DifficultyManager:
    """
    Manages all difficulty scaling based on player score.
    Uses smooth mathematical curves instead of discrete difficulty levels.
    """

    def __init__(self):
        """Initialize the difficulty manager"""
        self.score = 0
        self.last_milestone = 0
        self.milestone_triggered = False

        # Cached values (updated when score changes)
        self._cached_score = -1
        self._game_speed = BASE_GAME_SPEED
        self._spawn_interval = BASE_SPAWN_INTERVAL
        self._spawn_chance = BASE_SPAWN_CHANCE
        self._enemy_speed_multiplier = BASE_ENEMY_SPEED_MULTIPLIER
        self._difficulty_progress = 0.0

    def update(self, new_score):
        """
        Update difficulty based on new score.

        Args:
            new_score: Current player score

        Returns:
            bool: True if a milestone was just reached
        """
        self.score = new_score

        # Check for milestone
        current_milestone = (
            new_score // DIFFICULTY_MILESTONE_INTERVAL
        ) * DIFFICULTY_MILESTONE_INTERVAL
        if current_milestone > self.last_milestone:
            self.last_milestone = current_milestone
            self.milestone_triggered = True
        else:
            self.milestone_triggered = False

        # Recalculate cached values if score changed significantly
        if abs(new_score - self._cached_score) >= 10:
            self._recalculate_difficulty()
            self._cached_score = new_score

        return self.milestone_triggered

    def _recalculate_difficulty(self):
        """Recalculate all difficulty parameters based on current score"""
        # Calculate difficulty progress (0.0 to 1.0, with soft cap beyond)
        self._difficulty_progress = self._calculate_progress(self.score)

        # Calculate each parameter using smooth interpolation
        self._game_speed = self._lerp(
            BASE_GAME_SPEED,
            MAX_GAME_SPEED,
            self._ease_out_quad(self._difficulty_progress),
        )

        self._spawn_interval = self._lerp(
            BASE_SPAWN_INTERVAL,
            MIN_SPAWN_INTERVAL,
            self._ease_in_quad(self._difficulty_progress),
        )

        self._spawn_chance = self._lerp(
            BASE_SPAWN_CHANCE,
            MAX_SPAWN_CHANCE,
            self._ease_out_cubic(self._difficulty_progress),
        )

        self._enemy_speed_multiplier = self._lerp(
            BASE_ENEMY_SPEED_MULTIPLIER,
            MAX_ENEMY_SPEED_MULTIPLIER,
            self._ease_out_quad(self._difficulty_progress),
        )

    def _calculate_progress(self, score):
        """
        Calculate difficulty progress from 0.0 to 1.0+ based on score.
        Uses a smooth curve that approaches 1.0 asymptotically.

        Args:
            score: Current score

        Returns:
            float: Progress value (0.0 = easy, 1.0 = max difficulty)
        """
        if score <= 0:
            return 0.0

        # Logarithmic curve that approaches 1.0 as score approaches DIFFICULTY_MAX_SCORE
        # Continues to increase slowly beyond max score
        normalized = score / DIFFICULTY_MAX_SCORE

        # Use a tanh-like curve for smooth progression
        # This gives fast early gains and slower late gains
        progress = 1.0 - math.exp(-2.5 * normalized)

        return min(progress, 1.2)  # Allow slight overshoot for very high scores

    def _lerp(self, start, end, t):
        """
        Linear interpolation between two values.

        Args:
            start: Start value
            end: End value
            t: Interpolation factor (0.0 to 1.0)

        Returns:
            float: Interpolated value
        """
        t = max(0.0, min(1.0, t))  # Clamp t to [0, 1]
        return start + (end - start) * t

    def _ease_out_quad(self, t):
        """Quadratic ease-out: fast start, slow end"""
        return 1.0 - (1.0 - t) * (1.0 - t)

    def _ease_in_quad(self, t):
        """Quadratic ease-in: slow start, fast end"""
        return t * t

    def _ease_out_cubic(self, t):
        """Cubic ease-out: faster start, slower end"""
        return 1.0 - pow(1.0 - t, 3)

    # =========================================================================
    # PUBLIC GETTERS - Use these to get current difficulty values
    # =========================================================================

    @property
    def game_speed(self):
        """Get current game speed multiplier"""
        return self._game_speed

    @property
    def spawn_interval(self):
        """Get current enemy spawn interval (distance in pixels)"""
        return self._spawn_interval

    @property
    def spawn_chance(self):
        """Get current chance to spawn an enemy when interval is reached"""
        return self._spawn_chance

    @property
    def enemy_speed_multiplier(self):
        """Get current enemy speed multiplier"""
        return self._enemy_speed_multiplier

    @property
    def difficulty_percent(self):
        """Get difficulty as a percentage (0-100+)"""
        return self._difficulty_progress * 100

    @property
    def difficulty_level(self):
        """Get difficulty as a discrete level (1-10) for legacy compatibility"""
        return min(10, max(1, int(self._difficulty_progress * 10) + 1))

    def get_enemy_weights(self):
        """
        Get enemy type spawn weights based on current score.

        Returns:
            tuple: (basic_weight, chaser_weight, shooter_weight, berserker_weight)
        """
        if self.score < CHASER_UNLOCK_SCORE:
            return ENEMY_WEIGHTS_EARLY
        elif self.score < SHOOTER_UNLOCK_SCORE:
            # Smooth transition from early to mid
            t = (self.score - CHASER_UNLOCK_SCORE) / (
                SHOOTER_UNLOCK_SCORE - CHASER_UNLOCK_SCORE
            )
            return self._interpolate_weights(ENEMY_WEIGHTS_EARLY, ENEMY_WEIGHTS_MID, t)
        elif self.score < BERSERKER_UNLOCK_SCORE:
            t = (self.score - SHOOTER_UNLOCK_SCORE) / (
                BERSERKER_UNLOCK_SCORE - SHOOTER_UNLOCK_SCORE
            )
            return self._interpolate_weights(ENEMY_WEIGHTS_MID, ENEMY_WEIGHTS_HARD, t)
        elif self.score < SWARM_UNLOCK_SCORE:
            t = (self.score - BERSERKER_UNLOCK_SCORE) / (
                SWARM_UNLOCK_SCORE - BERSERKER_UNLOCK_SCORE
            )
            return self._interpolate_weights(
                ENEMY_WEIGHTS_HARD, ENEMY_WEIGHTS_EXPERT, t
            )
        else:
            # Beyond swarm unlock, gradually shift to nightmare weights
            excess_score = self.score - SWARM_UNLOCK_SCORE
            t = min(1.0, excess_score / 5000)  # Full nightmare at score 10000
            return self._interpolate_weights(
                ENEMY_WEIGHTS_EXPERT, ENEMY_WEIGHTS_NIGHTMARE, t
            )

    def _interpolate_weights(self, w1, w2, t):
        """Interpolate between two weight tuples"""
        t = max(0.0, min(1.0, t))
        return tuple(w1[i] + (w2[i] - w1[i]) * t for i in range(len(w1)))

    def get_swarm_chance(self):
        """
        Get chance of spawning a swarm pattern instead of single enemy.

        Returns:
            float: Probability (0.0 to SWARM_CHANCE_MAX)
        """
        if self.score < SWARM_UNLOCK_SCORE:
            return 0.0

        # Gradually increase swarm chance after unlock
        excess_score = self.score - SWARM_UNLOCK_SCORE
        progress = min(1.0, excess_score / 5000)  # Max at score 10000
        return self._lerp(
            SWARM_CHANCE_BASE, SWARM_CHANCE_MAX, self._ease_out_quad(progress)
        )

    def get_swarm_size(self):
        """
        Get size of swarm based on difficulty.

        Returns:
            int: Number of enemies in swarm
        """
        if self.score < SWARM_UNLOCK_SCORE:
            return SWARM_MIN_SIZE

        # Larger swarms at higher difficulties
        excess_score = self.score - SWARM_UNLOCK_SCORE
        progress = min(1.0, excess_score / 8000)
        size = SWARM_MIN_SIZE + int((SWARM_MAX_SIZE - SWARM_MIN_SIZE) * progress)
        return size

    def is_enemy_unlocked(self, enemy_type):
        """
        Check if an enemy type is unlocked at current score.

        Args:
            enemy_type: String name of enemy type

        Returns:
            bool: True if enemy type can spawn
        """
        thresholds = {
            "basic": 0,
            "chaser": CHASER_UNLOCK_SCORE,
            "shooter": SHOOTER_UNLOCK_SCORE,
            "berserker": BERSERKER_UNLOCK_SCORE,
        }
        return self.score >= thresholds.get(enemy_type, 0)

    def get_shooter_cooldown_multiplier(self):
        """
        Get multiplier for shooter enemy cooldown (lower = shoots faster).

        Returns:
            float: Cooldown multiplier (1.0 at start, down to 0.5 at max)
        """
        return self._lerp(1.0, 0.5, self._difficulty_progress)

    def get_chaser_detection_multiplier(self):
        """
        Get multiplier for chaser enemy detection range.

        Returns:
            float: Detection range multiplier (1.0 at start, up to 1.8 at max)
        """
        return self._lerp(1.0, 1.8, self._ease_out_quad(self._difficulty_progress))

    def get_enemy_health_bonus(self):
        """
        Get bonus health for enemies at higher difficulties.

        Returns:
            int: Additional health points (0 at start)
        """
        if self.score < 3000:
            return 0
        return int(self._lerp(0, 2, (self.score - 3000) / 7000))

    def reset(self):
        """Reset difficulty to initial state"""
        self.score = 0
        self.last_milestone = 0
        self.milestone_triggered = False
        self._cached_score = -1
        self._recalculate_difficulty()
