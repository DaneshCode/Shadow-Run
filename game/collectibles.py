"""
Collectibles Module
Contains Coin, Health Pack, and Power-up classes
"""

import pygame
import math
import random
from game.settings import *


class Collectible(pygame.sprite.Sprite):
    """
    Base class for all collectible items
    """

    def __init__(self, x, y, width, height):
        """
        Initialize a collectible

        Args:
            x, y: Position
            width, height: Size
        """
        super().__init__()

        self.width = width
        self.height = height

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Animation
        self.animation_timer = random.uniform(0, math.pi * 2)
        self.collected = False

    def update(self):
        """Update animation"""
        self.animation_timer += 0.1

    def collect(self, player):
        """
        Called when player collects this item
        Override in subclasses

        Args:
            player: Player object
        """
        self.collected = True
        self.kill()

    def draw(self, surface, camera_offset=(0, 0)):
        """Draw with floating animation"""
        if self.collected:
            return

        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1] + math.sin(self.animation_timer) * 3

        surface.blit(self.image, (screen_x, screen_y))


class Coin(Collectible):
    """
    Coin collectible - adds score
    is_ceiling: True if this coin can only be collected from ceiling, False for ground only
    """

    def __init__(self, x, y, is_ceiling=False):
        super().__init__(x, y, COIN_SIZE, COIN_SIZE)

        self.value = COIN_VALUE
        self.is_ceiling = is_ceiling  # True = ceiling coin, False = ground coin
        self._create_surface()

    def _create_surface(self):
        """Create coin appearance - gold color for all coins"""
        self.image = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)

        center = COIN_SIZE // 2

        # All coins are gold color
        pygame.draw.circle(self.image, COIN_COLOR, (center, center), center)
        pygame.draw.circle(self.image, (218, 165, 32), (center, center), center - 2)
        pygame.draw.circle(self.image, (255, 223, 0), (center - 2, center - 2), 3)
        pygame.draw.circle(self.image, (200, 150, 0), (center, center), center // 2, 2)

    def collect(self, player):
        """Add coin value to player"""
        player.add_coins(1)
        super().collect(player)


class HealthPack(Collectible):
    """
    Health pack - restores player health
    """

    def __init__(self, x, y):
        super().__init__(x, y, HEALTH_PACK_SIZE, HEALTH_PACK_SIZE)

        self.heal_amount = HEALTH_PACK_VALUE
        self._create_surface()

    def _create_surface(self):
        """Create health pack appearance"""
        self.image = pygame.Surface(
            (HEALTH_PACK_SIZE, HEALTH_PACK_SIZE), pygame.SRCALPHA
        )

        # Box
        pygame.draw.rect(
            self.image,
            (255, 255, 255),
            (0, 0, HEALTH_PACK_SIZE, HEALTH_PACK_SIZE),
            border_radius=4,
        )
        pygame.draw.rect(
            self.image,
            HEALTH_PACK_COLOR,
            (2, 2, HEALTH_PACK_SIZE - 4, HEALTH_PACK_SIZE - 4),
            border_radius=3,
        )

        # Cross
        cross_color = WHITE
        center = HEALTH_PACK_SIZE // 2
        cross_size = HEALTH_PACK_SIZE // 3
        pygame.draw.rect(
            self.image,
            cross_color,
            (center - 2, center - cross_size, 4, cross_size * 2),
        )
        pygame.draw.rect(
            self.image,
            cross_color,
            (center - cross_size, center - 2, cross_size * 2, 4),
        )

    def collect(self, player):
        """Heal the player"""
        player.heal(self.heal_amount)
        super().collect(player)


class PowerUp(Collectible):
    """
    Power-up collectible - grants temporary abilities
    """

    TYPES = ["invincibility"]

    def __init__(self, x, y, power_type=None):
        super().__init__(x, y, 32, 32)

        self.power_type = power_type or random.choice(self.TYPES)
        self.duration = 5000  # 5 seconds
        self._create_surface()

    def _create_surface(self):
        """Create power-up appearance based on type"""
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)

        # Ghost shape for invincibility (white/gray like ghost icon)
        ghost_size = 24
        ghost_x = 16 - ghost_size // 2
        ghost_y = 16 - ghost_size // 2 - 2

        # Ghost body (rounded top, wavy bottom) - white color
        pygame.draw.ellipse(
            self.image, WHITE, (ghost_x, ghost_y, ghost_size, ghost_size)
        )
        pygame.draw.rect(
            self.image,
            WHITE,
            (ghost_x, ghost_y + ghost_size // 2, ghost_size, ghost_size // 2),
        )

        # Ghost eyes - gray color
        eye_color = (100, 100, 100)  # Dark gray for eyes
        eye_y = ghost_y + ghost_size // 3
        pygame.draw.circle(self.image, eye_color, (ghost_x + ghost_size // 3, eye_y), 3)
        pygame.draw.circle(
            self.image, eye_color, (ghost_x + 2 * ghost_size // 3, eye_y), 3
        )

    def collect(self, player):
        """Apply power-up effect"""
        if self.power_type == "invincibility":
            player.is_invincible = True
            player.invincibility_timer = self.duration

        super().collect(player)


class CollectibleSpawner:
    """
    Manages collectible spawning throughout the game
    Coins spawn in patterns - some require jumping, some are easy to collect
    """

    # Coin pattern types
    PATTERN_ARC = "arc"  # Arc pattern following jump trajectory
    PATTERN_LINE = "line"  # Horizontal line at jump height
    PATTERN_GROUND = "ground"  # Near ground level (easy)
    PATTERN_MIXED = "mixed"  # Mix of heights

    def __init__(self, screen_width, screen_height):
        """
        Initialize the collectible spawner

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.last_spawn_x = 0
        self.coin_interval = (
            500  # Interval between coin patterns (increased for fewer coins)
        )
        self.health_interval = 1000
        self.powerup_interval = 1500  # More frequent power-ups (was 2000)

        self.last_health_x = 0
        self.last_powerup_x = 0

        # Player stats for calculating reachable heights
        # Player height: 192px, standing on ground (100px from bottom)
        # Player top when standing: SCREEN_HEIGHT - 100 - 192 = 428px from top
        # Jump power: -20, gravity: 0.8
        # Max jump height: v²/(2g) = 400/1.6 = 250px
        # So player can reach up to: 428 - 250 = 178px from top
        #
        # For coins to require jumping but be reachable:
        # - Min height above ground for jump requirement: > 192 (player height)
        # - Max height above ground to be reachable: < 192 + 250 = 442px

        self.player_height = 192
        self.ground_height = 100
        self.max_jump_height = 250  # Based on physics

        # Heights relative to ground
        self.easy_coin_min = 20  # Just slightly above ground
        self.easy_coin_max = 150  # Still reachable without jump for tall player
        self.jump_coin_min = 200  # Requires small jump
        self.jump_coin_max = 320  # Requires good jump but still reachable

    def update(self, player_x, coins, health_packs, powerups, platforms):
        """
        Spawn collectibles ahead of player

        Args:
            player_x: Player's x position
            coins: Sprite group for coins
            health_packs: Sprite group for health packs
            powerups: Sprite group for power-ups
            platforms: List of platforms
        """
        spawn_until = player_x + self.screen_width * 2

        # Spawn coin patterns
        while self.last_spawn_x < spawn_until:
            self.last_spawn_x += self.coin_interval

            if random.random() < 0.6:
                self._spawn_coin_pattern(self.last_spawn_x, coins)

        # Spawn health packs (less frequent, still require jump)
        while self.last_health_x < spawn_until:
            self.last_health_x += self.health_interval

            if random.random() < 0.2:
                self._spawn_health_at(self.last_health_x, health_packs, platforms)

        # Spawn power-ups (more accessible now)
        while self.last_powerup_x < spawn_until:
            self.last_powerup_x += self.powerup_interval

            if random.random() < 0.20:  # 20% chance (was 10%)
                self._spawn_powerup_at(self.last_powerup_x, powerups, platforms)

    def _spawn_coin_pattern(self, x, coins):
        """Spawn coins in two rows - both require jumping to collect"""
        ground_y = self.screen_height - self.ground_height
        ceiling_y = self.ground_height  # Ceiling position

        num_coins = random.randint(2, 3)  # Reduced from 3-4 to 2-3
        spacing = 45

        # Ground row - coins high enough that player must jump from ground to get them
        # Player height is 192, so coins at 250px above ground require jumping
        ground_coin_height = ground_y - 240  # Requires jump from ground

        # Ceiling row - coins low enough that player must jump from ceiling to get them
        # When on ceiling, player hangs down, so coins need to be further from ceiling
        ceiling_coin_height = ceiling_y + 200  # Requires jump from ceiling

        for i in range(num_coins):
            coin_x = x + i * spacing

            # Spawn ground coin
            ground_coin = Coin(coin_x, ground_coin_height, is_ceiling=False)
            coins.add(ground_coin)

            # Spawn ceiling coin
            ceiling_coin = Coin(coin_x, ceiling_coin_height, is_ceiling=True)
            coins.add(ceiling_coin)

    def _spawn_health_at(self, x, health_packs, platforms):
        """Spawn a health pack - at reachable jump height"""
        ground_y = self.screen_height - self.ground_height
        # Health packs at medium height - requires small jump
        y = ground_y - random.randint(self.jump_coin_min, 300)

        health_pack = HealthPack(x, y)
        health_packs.add(health_pack)

    def _spawn_powerup_at(self, x, powerups, platforms):
        """Spawn a power-up - at good jump height but reachable"""
        ground_y = self.screen_height - self.ground_height
        # Power-ups require jumping but are reachable
        y = ground_y - random.randint(250, self.jump_coin_max)

        powerup = PowerUp(x, y)
        powerups.add(powerup)

    def cleanup(self, player_x, coins, health_packs, powerups):
        """Remove collectibles behind the player"""
        cleanup_x = player_x - self.screen_width

        for coin in list(coins):
            if coin.rect.right < cleanup_x:
                coin.kill()

        for hp in list(health_packs):
            if hp.rect.right < cleanup_x:
                hp.kill()

        for pu in list(powerups):
            if pu.rect.right < cleanup_x:
                pu.kill()

    def reset(self):
        """Reset spawner state"""
        self.last_spawn_x = 0
        self.last_health_x = 0
        self.last_powerup_x = 0
