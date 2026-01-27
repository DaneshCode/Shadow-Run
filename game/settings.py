"""
Game Settings and Configuration
Contains all constants, colors, and game parameters
"""

import pygame

# =============================================================================
# DISPLAY SETTINGS
# =============================================================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "NIGHTMARE RUNNER - Endless Horror"

# =============================================================================
# COLORS - Dark Horror Theme
# =============================================================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (180, 0, 0)
BLOOD_RED = (139, 0, 0)
GREEN = (0, 100, 0)
BLUE = (0, 60, 120)
YELLOW = (200, 180, 50)
ORANGE = (180, 100, 30)
PURPLE = (80, 0, 80)
CYAN = (0, 150, 150)
GRAY = (80, 80, 80)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (120, 120, 120)

# Horror/Dark UI Colors
UI_BG = (10, 5, 15)
UI_ACCENT = (120, 40, 60)
UI_HIGHLIGHT = (180, 60, 80)
UI_DANGER = (200, 30, 30)
UI_SUCCESS = (40, 120, 40)
MENU_BG = (8, 5, 12)
BUTTON_COLOR = (40, 20, 30)
BUTTON_HOVER = (70, 30, 45)
BUTTON_TEXT = (200, 180, 180)

# Horror atmosphere colors
FOG_COLOR = (20, 15, 25)
NIGHT_SKY_TOP = (5, 5, 15)
NIGHT_SKY_BOTTOM = (15, 10, 25)
MOON_COLOR = (220, 220, 200)
DEAD_TREE_COLOR = (20, 15, 10)
GROUND_DARK = (25, 20, 15)
GROUND_TOP = (35, 30, 25)

# =============================================================================
# PHYSICS SETTINGS
# =============================================================================
GRAVITY = 0.8
MAX_FALL_SPEED = 18
FRICTION = 0.85

# =============================================================================
# PLAYER SETTINGS
# =============================================================================
PLAYER_WIDTH = 144  # 3x original (48 * 3)
PLAYER_HEIGHT = 192  # 3x original (64 * 3)
PLAYER_SPEED = 6
PLAYER_ACCELERATION = 0.5
PLAYER_JUMP_POWER = -20  # Increased to compensate for larger player height
PLAYER_MAX_HEALTH = 100
PLAYER_INVINCIBILITY_TIME = 1500  # milliseconds
PLAYER_COLOR = (100, 80, 120)

# =============================================================================
# SHOOTING SETTINGS
# =============================================================================
BULLET_SPEED = 18  # Increased for faster bullets
BULLET_DAMAGE = 50  # Increased damage to one-shot basic enemies
BULLET_SIZE = 20  # Larger for visual balance
BULLET_COOLDOWN = 250  # Faster shooting
BULLET_COLOR = (255, 150, 50)
BULLET_LIFETIME = 2000  # milliseconds

# Ammo system
MAX_AMMO = 10
AMMO_REGEN_TIME = 6000  # milliseconds to regenerate 1 bullet (6 seconds per bullet)
AMMO_COLOR = (80, 180, 255)
AMMO_EMPTY_COLOR = (60, 60, 80)

# Auto-run speed
AUTO_RUN_SPEED = 4

# =============================================================================
# PLATFORM SETTINGS - Dark Theme
# =============================================================================
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = (35, 25, 20)
PLATFORM_TOP_COLOR = (50, 40, 35)
GROUND_HEIGHT = 100

# =============================================================================
# ENEMY SETTINGS - Horror Theme
# =============================================================================
ENEMY_WIDTH = 100  # Scaled up for better visibility and shooting
ENEMY_HEIGHT = 100  # Scaled up proportionally
ENEMY_SPEED = 2
ENEMY_DAMAGE = 20
ENEMY_COLOR = (120, 30, 30)
ENEMY_SPAWN_DISTANCE = 800  # Distance ahead of player to spawn enemies
FAST_ENEMY_COLOR = (150, 50, 30)

# =============================================================================
# COLLECTIBLE SETTINGS
# =============================================================================
COIN_SIZE = 24
COIN_VALUE = 10
COIN_COLOR = (180, 160, 80)
HEALTH_PACK_SIZE = 28
HEALTH_PACK_VALUE = 25
HEALTH_PACK_COLOR = (150, 50, 50)

# =============================================================================
# DIFFICULTY SETTINGS - Smooth Progressive Scaling
# =============================================================================
# Difficulty uses a continuous score-based curve instead of discrete levels
# This creates smooth, imperceptible increases that feel natural

# Score thresholds for difficulty milestones (for UI/feedback only)
DIFFICULTY_MILESTONE_INTERVAL = 1000  # Show "difficulty increased" every 1000 points
MAX_DIFFICULTY_MULTIPLIER = (
    3.0  # Maximum scaling factor (game becomes 3x harder at peak)
)

# Score at which difficulty reaches maximum (soft cap - continues slowly after)
DIFFICULTY_MAX_SCORE = 10000

# =============================================================================
# GAME SPEED SCALING
# =============================================================================
# Base game speed and scaling
BASE_GAME_SPEED = 1.0
MAX_GAME_SPEED = 2.0  # Game can get up to 2x faster
GAME_SPEED_CURVE_STEEPNESS = 0.0003  # How fast speed ramps up (lower = slower ramp)

# =============================================================================
# ENEMY SPAWN SCALING
# =============================================================================
# Base spawn interval (pixels between enemy spawn checks)
BASE_SPAWN_INTERVAL = 500
MIN_SPAWN_INTERVAL = 150  # Minimum distance between enemies at max difficulty

# Base spawn chance (probability of spawning when interval reached)
BASE_SPAWN_CHANCE = 0.4  # 40% chance at start
MAX_SPAWN_CHANCE = 0.85  # 85% chance at max difficulty

# =============================================================================
# ENEMY SPEED SCALING
# =============================================================================
BASE_ENEMY_SPEED_MULTIPLIER = 1.0
MAX_ENEMY_SPEED_MULTIPLIER = 2.5  # Enemies can get 2.5x faster

# =============================================================================
# ENEMY TYPE SCALING (score thresholds for unlocking enemy types)
# =============================================================================
CHASER_UNLOCK_SCORE = 500  # Chasers start appearing
SHOOTER_UNLOCK_SCORE = 1500  # Shooters start appearing
BERSERKER_UNLOCK_SCORE = 3000  # Berserkers start appearing (new dangerous type)
SWARM_UNLOCK_SCORE = 5000  # Swarm patterns start appearing

# Enemy type weights at different score ranges (higher = more common)
# Format: (basic_weight, chaser_weight, shooter_weight, berserker_weight)
ENEMY_WEIGHTS_EARLY = (1.0, 0.0, 0.0, 0.0)  # Score 0-500
ENEMY_WEIGHTS_MID = (0.6, 0.4, 0.0, 0.0)  # Score 500-1500
ENEMY_WEIGHTS_HARD = (0.4, 0.35, 0.25, 0.0)  # Score 1500-3000
ENEMY_WEIGHTS_EXPERT = (0.25, 0.30, 0.25, 0.20)  # Score 3000-5000
ENEMY_WEIGHTS_NIGHTMARE = (0.15, 0.25, 0.30, 0.30)  # Score 5000+

# =============================================================================
# DANGEROUS PATTERNS (spawned at higher scores)
# =============================================================================
# Swarm: Multiple enemies spawned close together
SWARM_MIN_SIZE = 3
SWARM_MAX_SIZE = 6
SWARM_SPACING = 120  # Pixels between swarm enemies
SWARM_CHANCE_BASE = 0.0  # No swarms at start
SWARM_CHANCE_MAX = 0.25  # 25% chance of swarm spawn at max difficulty

# =============================================================================
# LEGACY COMPATIBILITY (for existing code)
# =============================================================================
DIFFICULTY_INCREASE_INTERVAL = DIFFICULTY_MILESTONE_INTERVAL
MAX_DIFFICULTY_LEVEL = 10

# =============================================================================
# GAME STATES
# =============================================================================
STATE_MENU = "menu"
STATE_TUTORIAL = "tutorial"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_LEADERBOARD = "leaderboard"
STATE_SETTINGS = "settings"

# =============================================================================
# ANIMATION SETTINGS
# =============================================================================
ANIMATION_SPEED = 100  # milliseconds per frame

# =============================================================================
# SOUND SETTINGS
# =============================================================================
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7

# =============================================================================
# CAMERA SETTINGS
# =============================================================================
CAMERA_SLACK_X = 400  # Increased to accommodate larger player size
CAMERA_SMOOTHING = 0.1  # Camera smoothing factor (lower = smoother)

# =============================================================================
# LEADERBOARD SETTINGS
# =============================================================================
LEADERBOARD_FILE = "data/leaderboard.json"
MAX_LEADERBOARD_ENTRIES = 10

# =============================================================================
# PARTICLE SETTINGS
# =============================================================================
PARTICLE_COUNT = 10
PARTICLE_LIFETIME = 500
PARTICLE_SPEED = 5
