"""
Platform and World Module
Contains Platform classes and world generation for endless gameplay
"""

import pygame
import random
from game.settings import *


class Platform(pygame.sprite.Sprite):
    """
    Basic platform class for static platforms
    """

    def __init__(self, x, y, width, height=PLATFORM_HEIGHT):
        """
        Initialize a platform

        Args:
            x: X position
            y: Y position
            width: Platform width
            height: Platform height
        """
        super().__init__()

        self.width = width
        self.height = height

        # Create platform surface with gradient and details
        self.image = self._create_platform_surface(width, height)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Track if this platform has been passed (for scoring)
        self.passed = False

    def _create_platform_surface(self, width, height):
        """
        Create a dark horror-themed platform surface

        Args:
            width: Platform width
            height: Platform height

        Returns:
            pygame.Surface: The platform surface
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Main body - dark stone/dirt
        pygame.draw.rect(surface, PLATFORM_COLOR, (0, 4, width, height - 4))

        # Top moss/dead surface layer
        pygame.draw.rect(surface, PLATFORM_TOP_COLOR, (0, 0, width, 8))

        # Add crack/texture lines
        for i in range(0, width, 20):
            pygame.draw.line(
                surface, (25, 20, 15), (i, height - 2), (i + 10, height - 2), 2
            )

        # Dark edges with weathered look
        pygame.draw.line(surface, (20, 15, 10), (0, 4), (0, height), 3)
        pygame.draw.line(surface, (20, 15, 10), (width - 1, 4), (width - 1, height), 3)

        # Dead grass/weeds (sparse and dark)
        for i in range(5, width - 5, 25):
            if random.random() > 0.4:  # Sparse dead vegetation
                grass_height = random.randint(2, 4)
                pygame.draw.line(surface, (40, 35, 25), (i, 0), (i, -grass_height), 1)

        return surface

    def draw(self, surface, camera_offset=(0, 0)):
        """
        Draw the platform

        Args:
            surface: Surface to draw on
            camera_offset: Camera offset (x, y)
        """
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]
        surface.blit(self.image, (screen_x, screen_y))


class MovingPlatform(Platform):
    """
    Moving platform that travels between two points
    """

    def __init__(self, x, y, width, move_range, speed=2, vertical=False):
        """
        Initialize a moving platform

        Args:
            x, y: Starting position
            width: Platform width
            move_range: Distance to move
            speed: Movement speed
            vertical: True for vertical movement, False for horizontal
        """
        super().__init__(x, y, width)

        self.start_x = x
        self.start_y = y
        self.move_range = move_range
        self.speed = speed
        self.vertical = vertical
        self.direction = 1
        self.position = 0

        # Recolor for distinction
        self.image = self._create_moving_platform_surface(width, PLATFORM_HEIGHT)

    def _create_moving_platform_surface(self, width, height):
        """Create a distinct surface for moving platforms"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Different color scheme for moving platforms
        pygame.draw.rect(surface, (70, 70, 100), (0, 4, width, height - 4))
        pygame.draw.rect(surface, (100, 100, 150), (0, 0, width, 8))

        # Arrow indicators
        arrow_color = (150, 150, 200)
        if self.vertical:
            # Vertical arrows
            pygame.draw.polygon(
                surface,
                arrow_color,
                [(width // 2, 10), (width // 2 - 5, 18), (width // 2 + 5, 18)],
            )
            pygame.draw.polygon(
                surface,
                arrow_color,
                [
                    (width // 2, height - 2),
                    (width // 2 - 5, height - 10),
                    (width // 2 + 5, height - 10),
                ],
            )
        else:
            # Horizontal arrows
            pygame.draw.polygon(
                surface,
                arrow_color,
                [(5, height // 2), (13, height // 2 - 5), (13, height // 2 + 5)],
            )
            pygame.draw.polygon(
                surface,
                arrow_color,
                [
                    (width - 5, height // 2),
                    (width - 13, height // 2 - 5),
                    (width - 13, height // 2 + 5),
                ],
            )

        return surface

    def update(self):
        """Update platform position"""
        self.position += self.speed * self.direction

        # Reverse direction at endpoints
        if abs(self.position) >= self.move_range:
            self.direction *= -1

        # Update position
        if self.vertical:
            self.rect.y = self.start_y + self.position
        else:
            self.rect.x = self.start_x + self.position


class CrumblingPlatform(Platform):
    """
    Platform that crumbles and falls after player stands on it
    """

    def __init__(self, x, y, width):
        """Initialize a crumbling platform"""
        super().__init__(x, y, width)

        self.touched = False
        self.crumble_timer = 0
        self.crumble_delay = 1000  # ms before crumbling
        self.is_crumbling = False
        self.fall_speed = 0
        self.original_y = y

        # Distinct appearance
        self.image = self._create_crumbling_surface(width, PLATFORM_HEIGHT)
        self.original_image = self.image.copy()

    def _create_crumbling_surface(self, width, height):
        """Create surface for crumbling platform - dark and unstable looking"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Cracked dark stone appearance
        pygame.draw.rect(surface, (35, 30, 25), (0, 4, width, height - 4))
        pygame.draw.rect(surface, (45, 38, 30), (0, 0, width, 8))

        # Prominent crack lines
        crack_color = (20, 15, 10)
        for i in range(4):
            x = random.randint(10, width - 10)
            pygame.draw.line(
                surface, crack_color, (x, 0), (x + random.randint(-15, 15), height), 2
            )

        return surface

    def touch(self):
        """Called when player touches the platform"""
        if not self.touched:
            self.touched = True
            self.crumble_timer = pygame.time.get_ticks()

    def update(self):
        """Update crumbling state"""
        if self.touched and not self.is_crumbling:
            elapsed = pygame.time.get_ticks() - self.crumble_timer

            # Shake effect before crumbling
            if elapsed > self.crumble_delay * 0.5:
                shake = random.randint(-2, 2)
                self.rect.x += shake

            if elapsed >= self.crumble_delay:
                self.is_crumbling = True

        if self.is_crumbling:
            self.fall_speed += GRAVITY
            self.rect.y += self.fall_speed

    def reset(self):
        """Reset platform to original state"""
        self.touched = False
        self.is_crumbling = False
        self.fall_speed = 0
        self.rect.y = self.original_y
        self.image = self.original_image.copy()


class Ground(pygame.sprite.Sprite):
    """
    Ground/floor segment for the level
    """

    def __init__(self, x, y, width):
        """
        Initialize ground segment

        Args:
            x: X position
            y: Y position (usually bottom of screen)
            width: Ground width
        """
        super().__init__()

        self.image = self._create_ground_surface(width, GROUND_HEIGHT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _create_ground_surface(self, width, height):
        """Create dark horror-themed ground surface"""
        surface = pygame.Surface((width, height))

        # Dark ground gradient (dead earth)
        for y in range(height):
            ratio = y / height
            r = int(30 * (1 - ratio * 0.3))
            g = int(25 * (1 - ratio * 0.3))
            b = int(20 * (1 - ratio * 0.3))
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

        # Top dead surface layer
        pygame.draw.rect(surface, PLATFORM_TOP_COLOR, (0, 0, width, 12))

        # Sparse dead grass/weeds
        for x in range(0, width, 20):
            if random.random() > 0.6:
                grass_height = random.randint(2, 5)
                pygame.draw.line(surface, (35, 30, 20), (x, 0), (x, -grass_height), 1)

        # Dirt/bone details
        for _ in range(width // 30):
            dx = random.randint(0, width)
            dy = random.randint(20, height - 10)
            pygame.draw.circle(surface, (25, 20, 15), (dx, dy), random.randint(2, 4))

        return surface

    def draw(self, surface, camera_offset=(0, 0)):
        """Draw the ground"""
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]
        surface.blit(self.image, (screen_x, screen_y))


class WorldGenerator:
    """
    Procedural world generator for endless gameplay
    Generates platforms, enemies, and collectibles as player progresses
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize the world generator

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Track generation position
        self.last_platform_x = 0
        self.last_platform_y = screen_height - GROUND_HEIGHT - 100

        # Difficulty settings
        self.difficulty = 1
        self.gap_multiplier = 1.0

        # Ground segments
        self.ground_segment_width = 800
        self.last_ground_x = 0

        # Track what's been generated
        self.generated_until_x = 0

    def set_difficulty(self, difficulty):
        """
        Set the current difficulty level

        Args:
            difficulty: Difficulty level (1-10)
        """
        self.difficulty = min(difficulty, MAX_DIFFICULTY_LEVEL)
        self.gap_multiplier = 1 + (difficulty - 1) * 0.05

    def generate_initial_world(self, platforms, grounds, coins, enemies):
        """
        Generate the initial world layout

        Args:
            platforms: Sprite group for platforms (unused - ground-based runner)
            grounds: Sprite group for ground
            coins: Sprite group for coins
            enemies: Sprite group for enemies
        """
        # Create initial ground - this is now the only surface
        for x in range(
            -self.ground_segment_width, self.screen_width * 2, self.ground_segment_width
        ):
            ground = Ground(
                x, self.screen_height - GROUND_HEIGHT, self.ground_segment_width
            )
            grounds.add(ground)
            self.last_ground_x = x + self.ground_segment_width

        # No elevated platforms - pure ground-based endless runner
        self.generated_until_x = self.screen_width * 2

    def generate_platforms_ahead(self, platforms, until_x):
        """
        Generate platforms up to a certain x position
        NOTE: Disabled for ground-based endless runner - no elevated platforms

        Args:
            platforms: Sprite group for platforms (unused)
            until_x: Generate until this x position (unused)
        """
        # No platforms generated - pure ground-based endless runner
        pass

    def generate_ground_ahead(self, grounds, until_x):
        """
        Generate ground segments ahead

        Args:
            grounds: Sprite group for ground
            until_x: Generate until this x position
        """
        while self.last_ground_x < until_x:
            ground = Ground(
                self.last_ground_x,
                self.screen_height - GROUND_HEIGHT,
                self.ground_segment_width,
            )
            grounds.add(ground)
            self.last_ground_x += self.ground_segment_width

    def update(self, player_x, platforms, grounds, coins, enemies):
        """
        Update world generation based on player position

        Args:
            player_x: Player's x position
            platforms: Sprite group for platforms
            grounds: Sprite group for ground
            coins: Sprite group for coins
            enemies: Sprite group for enemies
        """
        # Generate more world when player gets close to the edge
        look_ahead = self.screen_width * 2

        if player_x + look_ahead > self.generated_until_x:
            # Only generate ground - no elevated platforms in ground-based runner
            self.generate_ground_ahead(grounds, player_x + look_ahead)

            self.generated_until_x = player_x + look_ahead

        # Cleanup: Remove objects far behind player
        cleanup_x = player_x - self.screen_width

        for ground in list(grounds):
            if ground.rect.right < cleanup_x:
                ground.kill()

    def reset(self):
        """Reset the generator to initial state"""
        self.last_platform_x = 0
        self.last_platform_y = self.screen_height - GROUND_HEIGHT - 100
        self.last_ground_x = 0
        self.generated_until_x = 0
        self.difficulty = 1
        self.gap_multiplier = 1.0
