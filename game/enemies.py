"""
Enemy Module
Contains enemy classes with different behaviors and patterns
"""

import pygame
import random
import math
from game.settings import *
from game.settings import SWARM_SPACING, BASE_SPAWN_INTERVAL


class Enemy(pygame.sprite.Sprite):
    """
    Base enemy class with basic patrol behavior
    """

    def __init__(self, x, y, width=ENEMY_WIDTH, height=ENEMY_HEIGHT):
        """
        Initialize an enemy

        Args:
            x: X position
            y: Y position
            width: Enemy width
            height: Enemy height
        """
        super().__init__()

        self.width = width
        self.height = height

        # Create enemy surface
        self.base_image = self._create_enemy_surface()
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement
        self.velocity_x = ENEMY_SPEED
        self.velocity_y = 0
        self.direction = -1  # -1 = left, 1 = right
        self.speed = ENEMY_SPEED

        # Patrol settings
        self.start_x = x
        self.patrol_range = 100

        # Combat
        self.damage = ENEMY_DAMAGE
        self.health = 1
        self.is_dead = False

        # Animation
        self.animation_timer = 0
        self.animation_frame = 0
        self.facing_right = False

    def _create_enemy_surface(self):
        """Create the enemy sprite surface"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Body (slime-like blob)
        body_color = ENEMY_COLOR
        pygame.draw.ellipse(
            surface, body_color, (0, self.height // 3, self.width, self.height * 2 // 3)
        )

        # Darker bottom
        pygame.draw.ellipse(
            surface,
            (body_color[0] - 40, body_color[1] - 20, body_color[2] - 20),
            (2, self.height // 2 + 5, self.width - 4, self.height // 2 - 5),
        )

        # Eyes
        eye_y = self.height // 2
        pygame.draw.circle(surface, WHITE, (self.width // 3, eye_y), 6)
        pygame.draw.circle(surface, WHITE, (2 * self.width // 3, eye_y), 6)

        # Pupils
        pygame.draw.circle(surface, BLACK, (self.width // 3 + 2, eye_y), 3)
        pygame.draw.circle(surface, BLACK, (2 * self.width // 3 + 2, eye_y), 3)

        # Angry eyebrows
        pygame.draw.line(
            surface,
            BLACK,
            (self.width // 3 - 5, eye_y - 8),
            (self.width // 3 + 5, eye_y - 5),
            2,
        )
        pygame.draw.line(
            surface,
            BLACK,
            (2 * self.width // 3 - 5, eye_y - 5),
            (2 * self.width // 3 + 5, eye_y - 8),
            2,
        )

        return surface

    def update(self, player=None, platforms=None):
        """
        Update enemy behavior

        Args:
            player: Player object for AI targeting
            platforms: Platforms for collision
        """
        if self.is_dead:
            return

        # Basic patrol movement
        self.rect.x += self.velocity_x * self.direction

        # Reverse at patrol limits
        if abs(self.rect.x - self.start_x) > self.patrol_range:
            self.direction *= -1
            self.facing_right = self.direction > 0

        # Update facing direction for image
        if self.direction > 0 and not self.facing_right:
            self.facing_right = True
            self.image = pygame.transform.flip(self.base_image, True, False)
        elif self.direction < 0 and self.facing_right:
            self.facing_right = False
            self.image = self.base_image

        # Simple animation (bobbing)
        self.animation_timer += 1
        if self.animation_timer > 10:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2

    def take_damage(self, amount=1):
        """
        Take damage

        Args:
            amount: Damage amount

        Returns:
            bool: True if enemy died
        """
        self.health -= amount
        if self.health <= 0:
            self.die()
            return True
        return False

    def die(self):
        """Handle enemy death"""
        self.is_dead = True
        self.kill()

    def draw(self, surface, camera_offset=(0, 0)):
        """Draw the enemy"""
        if self.is_dead:
            return

        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]

        # Add bobbing animation
        bob_offset = math.sin(pygame.time.get_ticks() * 0.01) * 2

        surface.blit(self.image, (screen_x, screen_y + bob_offset))


class ChaserEnemy(Enemy):
    """
    Enemy that chases the player when in range
    """

    def __init__(self, x, y):
        super().__init__(x, y)

        self.detection_range = 300
        self.chase_speed = ENEMY_SPEED * 2
        self.is_chasing = False

        # Higher damage
        self.damage = ENEMY_DAMAGE * 1.5

        # Recreate with different appearance
        self.base_image = self._create_chaser_surface()
        self.image = self.base_image

    def _create_chaser_surface(self):
        """Create chaser enemy surface"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Angular aggressive body
        points = [
            (self.width // 2, 0),
            (self.width, self.height // 3),
            (self.width, self.height),
            (0, self.height),
            (0, self.height // 3),
        ]
        pygame.draw.polygon(surface, FAST_ENEMY_COLOR, points)

        # Eyes (angry looking)
        eye_y = self.height // 2
        pygame.draw.circle(surface, WHITE, (self.width // 3, eye_y), 6)
        pygame.draw.circle(surface, WHITE, (2 * self.width // 3, eye_y), 6)
        pygame.draw.circle(surface, RED, (self.width // 3, eye_y), 3)
        pygame.draw.circle(surface, RED, (2 * self.width // 3, eye_y), 3)

        return surface

    def update(self, player=None, platforms=None):
        """Update with chase behavior"""
        if self.is_dead:
            return

        if player and not player.is_dead:
            # Check if player is in range
            distance = abs(player.rect.centerx - self.rect.centerx)

            if distance < self.detection_range:
                self.is_chasing = True

                # Move towards player
                if player.rect.centerx < self.rect.centerx:
                    self.direction = -1
                else:
                    self.direction = 1

                self.rect.x += self.chase_speed * self.direction
            else:
                self.is_chasing = False
                # Normal patrol behavior
                super().update(player, platforms)
        else:
            super().update(player, platforms)

        # Update image direction
        if self.direction > 0:
            self.image = pygame.transform.flip(self.base_image, True, False)
        else:
            self.image = self.base_image


class ShooterEnemy(Enemy):
    """
    Stationary enemy that shoots projectiles at the player
    """

    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_WIDTH + 10, ENEMY_HEIGHT + 10)

        self.shoot_cooldown = 2000  # ms between shots
        self.last_shot = 0
        self.projectiles = []
        self.detection_range = 400

        # Recreate appearance
        self.base_image = self._create_shooter_surface()
        self.image = self.base_image

        # Stationary
        self.velocity_x = 0

    def _create_shooter_surface(self):
        """Create shooter enemy surface with cannon pointing left (towards player)"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Turret-like body
        pygame.draw.rect(
            surface,
            (100, 100, 120),
            (5, self.height // 3, self.width - 10, self.height * 2 // 3),
        )
        pygame.draw.rect(surface, (80, 80, 100), (0, self.height - 10, self.width, 10))

        # Cannon pointing LEFT (towards player in endless runner)
        cannon_y = self.height // 2
        pygame.draw.rect(
            surface, (60, 60, 80), (0, cannon_y - 8, self.width // 2 + 10, 16)
        )
        # Cannon base (circle)
        pygame.draw.circle(surface, (60, 60, 80), (self.width // 2, cannon_y), 15)

        # Eye on top of turret
        pygame.draw.circle(surface, RED, (self.width // 2, self.height // 3), 8)
        pygame.draw.circle(
            surface, (255, 100, 100), (self.width // 2 - 2, self.height // 3 - 2), 3
        )

        return surface

    def update(self, player=None, platforms=None):
        """Update and shoot at player"""
        if self.is_dead:
            return

        current_time = pygame.time.get_ticks()

        if player and not player.is_dead:
            distance = abs(player.rect.centerx - self.rect.centerx)

            if (
                distance < self.detection_range
                and current_time - self.last_shot > self.shoot_cooldown
            ):
                self.shoot(player)
                self.last_shot = current_time

        # Update projectiles
        for proj in self.projectiles[:]:
            proj.update()
            if proj.is_dead:
                self.projectiles.remove(proj)

    def shoot(self, player):
        """Shoot a projectile at the player"""
        # Calculate direction to player - aim at player's center/body
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = max(1, math.sqrt(dx * dx + dy * dy))

        # Normalize and set speed
        speed = 6
        vel_x = (dx / distance) * speed
        vel_y = (dy / distance) * speed

        # Spawn projectile from enemy's center (not top)
        projectile = Projectile(self.rect.centerx, self.rect.centery, vel_x, vel_y)
        self.projectiles.append(projectile)

    def draw(self, surface, camera_offset=(0, 0)):
        """Draw enemy and projectiles"""
        super().draw(surface, camera_offset)

        for proj in self.projectiles:
            proj.draw(surface, camera_offset)


class BerserkerEnemy(Enemy):
    """
    Dangerous enemy that charges at high speed when it sees the player.
    Harder to dodge, deals more damage, and has more health.
    Unlocked at higher scores for increased challenge.
    """

    def __init__(self, x, y):
        super().__init__(x, y, int(ENEMY_WIDTH * 1.2), int(ENEMY_HEIGHT * 1.2))

        # Berserker stats - very dangerous
        self.detection_range = 500
        self.charge_speed = ENEMY_SPEED * 4  # Very fast charge
        self.normal_speed = ENEMY_SPEED * 1.5
        self.is_charging = False
        self.charge_windup = 0
        self.charge_windup_time = 30  # Frames of windup before charge
        self.charge_duration = 0
        self.max_charge_duration = 90  # Frames of sustained charge
        self.charge_cooldown = 0
        self.charge_cooldown_time = 60  # Frames before can charge again

        # Higher damage and health
        self.damage = ENEMY_DAMAGE * 2
        self.health = 3  # Takes 3 hits to kill

        # Visual
        self.base_image = self._create_berserker_surface()
        self.image = self.base_image
        self.flash_timer = 0

    def _create_berserker_surface(self):
        """Create berserker enemy surface - large, spiky, intimidating"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Main body - dark red, bulky
        body_color = (160, 30, 30)
        pygame.draw.ellipse(
            surface,
            body_color,
            (5, self.height // 4, self.width - 10, self.height * 3 // 4),
        )

        # Spikes on top
        spike_color = (80, 20, 20)
        spike_positions = [
            (self.width // 4, self.height // 4),
            (self.width // 2, self.height // 8),
            (3 * self.width // 4, self.height // 4),
        ]
        for sx, sy in spike_positions:
            points = [
                (sx, sy - 15),
                (sx - 8, sy + 10),
                (sx + 8, sy + 10),
            ]
            pygame.draw.polygon(surface, spike_color, points)

        # Angry eyes
        eye_y = self.height // 2
        pygame.draw.circle(surface, (255, 200, 0), (self.width // 3, eye_y), 8)
        pygame.draw.circle(surface, (255, 200, 0), (2 * self.width // 3, eye_y), 8)
        pygame.draw.circle(surface, BLACK, (self.width // 3, eye_y), 4)
        pygame.draw.circle(surface, BLACK, (2 * self.width // 3, eye_y), 4)

        # Angry mouth
        pygame.draw.arc(
            surface,
            BLACK,
            (self.width // 4, eye_y + 10, self.width // 2, 20),
            3.14,
            0,
            3,
        )

        return surface

    def _create_charging_surface(self):
        """Create a flashing/glowing surface for charging state"""
        surface = self.base_image.copy()

        # Add red glow overlay
        glow = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        glow.fill((255, 50, 50, 80))
        surface.blit(glow, (0, 0))

        return surface

    def update(self, player=None, platforms=None):
        """Update berserker with charge behavior"""
        if self.is_dead:
            return

        # Update cooldowns
        if self.charge_cooldown > 0:
            self.charge_cooldown -= 1

        if player and not player.is_dead:
            distance = abs(player.rect.centerx - self.rect.centerx)

            # Determine movement direction
            if player.rect.centerx < self.rect.centerx:
                target_direction = -1
            else:
                target_direction = 1

            # Charging behavior
            if self.is_charging:
                # Continue charge
                self.charge_duration += 1
                self.rect.x += self.charge_speed * self.direction

                # Flash effect
                self.flash_timer += 1
                if self.flash_timer % 4 < 2:
                    self.image = self._create_charging_surface()
                else:
                    self.image = (
                        self.base_image
                        if self.direction < 0
                        else pygame.transform.flip(self.base_image, True, False)
                    )

                # End charge after duration
                if self.charge_duration >= self.max_charge_duration:
                    self.is_charging = False
                    self.charge_cooldown = self.charge_cooldown_time
                    self.charge_duration = 0

            elif self.charge_windup > 0:
                # Windup - telegraph the attack
                self.charge_windup += 1
                self.flash_timer += 1

                # Shake effect during windup
                shake = (self.flash_timer % 4) - 2

                # Flash warning
                if self.flash_timer % 6 < 3:
                    self.image = self._create_charging_surface()

                if self.charge_windup >= self.charge_windup_time:
                    # Start charging
                    self.is_charging = True
                    self.charge_windup = 0
                    self.direction = target_direction

            elif distance < self.detection_range and self.charge_cooldown == 0:
                # Start windup
                self.charge_windup = 1
                self.direction = target_direction

            else:
                # Normal patrol behavior when not charging
                self.rect.x += self.normal_speed * self.direction

                # Reverse at patrol limits
                if abs(self.rect.x - self.start_x) > self.patrol_range:
                    self.direction *= -1

        else:
            # No player - patrol
            self.rect.x += self.normal_speed * self.direction
            if abs(self.rect.x - self.start_x) > self.patrol_range:
                self.direction *= -1

        # Update facing direction
        if not self.is_charging and self.charge_windup == 0:
            if self.direction > 0:
                self.image = pygame.transform.flip(self.base_image, True, False)
            else:
                self.image = self.base_image

    def draw(self, surface, camera_offset=(0, 0)):
        """Draw berserker with charge indicator"""
        if self.is_dead:
            return

        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]

        # Draw warning indicator during windup
        if self.charge_windup > 0:
            # Exclamation mark above head
            warning_y = screen_y - 30
            warning_size = int(10 + 10 * (self.charge_windup / self.charge_windup_time))
            pygame.draw.circle(
                surface,
                (255, 50, 50),
                (int(screen_x + self.width // 2), int(warning_y)),
                warning_size,
            )
            pygame.draw.circle(
                surface,
                (255, 200, 50),
                (int(screen_x + self.width // 2), int(warning_y)),
                warning_size - 3,
            )

        # Draw trail when charging
        if self.is_charging:
            trail_color = (255, 100, 50, 100)
            for i in range(3):
                trail_x = screen_x - (self.direction * 20 * (i + 1))
                trail_surface = pygame.Surface(
                    (self.width, self.height), pygame.SRCALPHA
                )
                trail_surface.fill((255, 100, 50, 50 - i * 15))
                surface.blit(trail_surface, (trail_x, screen_y))

        # Draw the enemy
        bob_offset = math.sin(pygame.time.get_ticks() * 0.01) * 2
        surface.blit(self.image, (screen_x, screen_y + bob_offset))


class Projectile:
    """
    Projectile class for shooter enemies
    """

    def __init__(self, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.radius = 6
        self.damage = ENEMY_DAMAGE // 2
        self.is_dead = False
        self.lifetime = 3000
        self.birth_time = pygame.time.get_ticks()

        # For collision
        self.rect = pygame.Rect(
            x - self.radius, y - self.radius, self.radius * 2, self.radius * 2
        )

    def update(self):
        """Update projectile position"""
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.center = (self.x, self.y)

        # Check lifetime
        if pygame.time.get_ticks() - self.birth_time > self.lifetime:
            self.is_dead = True

    def draw(self, surface, camera_offset=(0, 0)):
        """Draw the projectile"""
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])

        # Glowing effect
        pygame.draw.circle(
            surface, (255, 100, 100), (screen_x, screen_y), self.radius + 2
        )
        pygame.draw.circle(surface, (255, 200, 100), (screen_x, screen_y), self.radius)
        pygame.draw.circle(surface, WHITE, (screen_x, screen_y), self.radius - 2)


class CeilingEnemy(Enemy):
    """
    Enemy that moves along the ceiling. Player must flip gravity to reach/avoid them.
    Visual appearance is inverted to show they're on the ceiling.
    """

    def __init__(self, x, y):
        super().__init__(x, y)

        # Mark as ceiling enemy
        self.is_ceiling_enemy = True

        # Create ceiling-specific appearance (purple tint, inverted)
        self.base_image = self._create_ceiling_surface()
        self.image = self.base_image

        # Slightly faster than ground enemies
        self.speed = ENEMY_SPEED * 1.2
        self.velocity_x = self.speed

    def _create_ceiling_surface(self):
        """Create ceiling enemy surface - inverted blob hanging from ceiling"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Body (inverted slime - hanging from ceiling)
        body_color = CEILING_ENEMY_COLOR
        pygame.draw.ellipse(
            surface, body_color, (0, 0, self.width, self.height * 2 // 3)
        )

        # Darker bottom (now top since inverted)
        pygame.draw.ellipse(
            surface,
            (body_color[0] - 30, body_color[1] - 15, body_color[2] - 30),
            (2, 5, self.width - 4, self.height // 2 - 5),
        )

        # Eyes (positioned for ceiling view)
        eye_y = self.height // 3
        pygame.draw.circle(surface, WHITE, (self.width // 3, eye_y), 6)
        pygame.draw.circle(surface, WHITE, (2 * self.width // 3, eye_y), 6)

        # Pupils looking down at player
        pygame.draw.circle(surface, BLACK, (self.width // 3, eye_y + 2), 3)
        pygame.draw.circle(surface, BLACK, (2 * self.width // 3, eye_y + 2), 3)

        # Dripping tendrils from bottom
        for i in range(3):
            x_pos = self.width // 4 + (i * self.width // 4)
            tendril_len = random.randint(10, 20)
            pygame.draw.line(
                surface,
                (body_color[0] - 20, body_color[1] - 10, body_color[2] - 20),
                (x_pos, self.height * 2 // 3),
                (x_pos, self.height * 2 // 3 + tendril_len),
                3,
            )

        return surface

    def draw(self, surface, camera_offset=(0, 0)):
        """Draw the ceiling enemy with bob animation"""
        if self.is_dead:
            return

        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]

        # Inverted bobbing animation (bob downward instead of upward)
        bob_offset = math.sin(pygame.time.get_ticks() * 0.01) * 2

        surface.blit(self.image, (screen_x, screen_y - bob_offset))


class FlyingEnemy(Enemy):
    """
    Flying enemy that moves in a wave pattern between ground and ceiling.
    Forces player to time gravity flips carefully.
    """

    def __init__(self, x, y, screen_height):
        super().__init__(x, y)

        # Mark as flying enemy
        self.is_flying_enemy = True
        self.screen_height = screen_height

        # Wave motion parameters
        self.base_y = screen_height // 2  # Center of screen
        self.wave_amplitude = (screen_height - GROUND_HEIGHT - CEILING_HEIGHT) // 3
        self.wave_frequency = 0.003  # Speed of wave motion
        self.wave_offset = random.random() * math.pi * 2  # Random phase

        # Create flying enemy appearance
        self.base_image = self._create_flying_surface()
        self.image = self.base_image

        # Faster horizontal movement
        self.speed = FLYING_ENEMY_SPEED
        self.velocity_x = self.speed

    def _create_flying_surface(self):
        """Create flying enemy surface - bat/ghost-like creature"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        body_color = FLYING_ENEMY_COLOR

        # Wings
        wing_color = (body_color[0] - 20, body_color[1] + 20, body_color[2] - 10)
        # Left wing
        pygame.draw.polygon(
            surface,
            wing_color,
            [
                (self.width // 4, self.height // 2),
                (0, self.height // 4),
                (0, self.height * 3 // 4),
            ],
        )
        # Right wing
        pygame.draw.polygon(
            surface,
            wing_color,
            [
                (3 * self.width // 4, self.height // 2),
                (self.width, self.height // 4),
                (self.width, self.height * 3 // 4),
            ],
        )

        # Body (oval in center)
        pygame.draw.ellipse(
            surface,
            body_color,
            (self.width // 4, self.height // 4, self.width // 2, self.height // 2),
        )

        # Glowing eyes
        eye_y = self.height // 2 - 5
        pygame.draw.circle(surface, (255, 100, 100), (self.width // 3 + 5, eye_y), 6)
        pygame.draw.circle(
            surface, (255, 100, 100), (2 * self.width // 3 - 5, eye_y), 6
        )
        pygame.draw.circle(surface, WHITE, (self.width // 3 + 5, eye_y), 3)
        pygame.draw.circle(surface, WHITE, (2 * self.width // 3 - 5, eye_y), 3)

        return surface

    def update(self, player=None, platforms=None):
        """Update with wave movement pattern"""
        if self.is_dead:
            return

        # Horizontal patrol movement
        self.rect.x += self.velocity_x * self.direction

        # Reverse at patrol limits
        if abs(self.rect.x - self.start_x) > self.patrol_range * 2:
            self.direction *= -1
            self.facing_right = self.direction > 0

        # Wave motion for vertical position
        time_factor = pygame.time.get_ticks() * self.wave_frequency + self.wave_offset
        wave_y = math.sin(time_factor) * self.wave_amplitude
        self.rect.y = int(self.base_y + wave_y)

        # Update facing direction for image
        if self.direction > 0 and not self.facing_right:
            self.facing_right = True
            self.image = pygame.transform.flip(self.base_image, True, False)
        elif self.direction < 0 and self.facing_right:
            self.facing_right = False
            self.image = self.base_image

    def draw(self, surface, camera_offset=(0, 0)):
        """Draw the flying enemy with wing flap animation"""
        if self.is_dead:
            return

        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]

        # Wing flap animation (scale wings based on time)
        flap_scale = 0.8 + 0.2 * math.sin(pygame.time.get_ticks() * 0.02)

        # Draw with slight vertical oscillation for flight feel
        surface.blit(self.image, (screen_x, screen_y))


class EnemySpawner:
    """
    Manages enemy spawning for endless gameplay with smooth difficulty scaling.
    Uses DifficultyManager for all difficulty-related decisions.
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize the enemy spawner

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Spawning parameters
        self.spawn_distance = ENEMY_SPAWN_DISTANCE
        self.last_spawn_x = 0

        # Reference to difficulty manager (set by game)
        self.difficulty_manager = None

        # Legacy compatibility
        self.difficulty = 1
        self.spawn_rate_multiplier = 1.0

    def set_difficulty_manager(self, difficulty_manager):
        """Set the difficulty manager reference"""
        self.difficulty_manager = difficulty_manager

    def set_difficulty(self, difficulty):
        """Legacy method - still updates internal difficulty for compatibility"""
        self.difficulty = min(difficulty, MAX_DIFFICULTY_LEVEL)
        self.spawn_rate_multiplier = 1 + (difficulty - 1) * 0.1

    def update(self, player_x, enemies, platforms, ceiling_enemies=None):
        """
        Spawn enemies ahead of player using difficulty manager.

        Args:
            player_x: Player's x position
            enemies: Sprite group for ground enemies
            platforms: List of platforms to spawn enemies on
            ceiling_enemies: Sprite group for ceiling enemies (gravity flip)
        """
        spawn_until = player_x + self.spawn_distance

        # Get spawn parameters from difficulty manager or use legacy values
        if self.difficulty_manager:
            spawn_interval = self.difficulty_manager.spawn_interval
            spawn_chance = self.difficulty_manager.spawn_chance
            swarm_chance = self.difficulty_manager.get_swarm_chance()
        else:
            spawn_interval = BASE_SPAWN_INTERVAL / self.spawn_rate_multiplier
            spawn_chance = 0.6
            swarm_chance = 0.0

        while self.last_spawn_x < spawn_until:
            self.last_spawn_x += spawn_interval

            # Check if we spawn at this interval
            if random.random() < spawn_chance:
                # Check for swarm spawn
                if random.random() < swarm_chance:
                    self._spawn_swarm_at(self.last_spawn_x, enemies)
                else:
                    # Decide spawn location: ground, ceiling, or flying
                    spawn_location = self._choose_spawn_location()

                    if spawn_location == "ceiling" and ceiling_enemies is not None:
                        self._spawn_ceiling_enemy_at(self.last_spawn_x, ceiling_enemies)
                    elif spawn_location == "flying":
                        self._spawn_flying_enemy_at(self.last_spawn_x, enemies)
                    else:
                        self._spawn_enemy_at(self.last_spawn_x, enemies, platforms)

    def _choose_spawn_location(self):
        """
        Choose where to spawn the enemy: ground, ceiling, or flying.
        Distribution depends on difficulty.
        """
        if self.difficulty_manager:
            difficulty_percent = self.difficulty_manager.difficulty_percent
        else:
            difficulty_percent = min(100, self.difficulty * 10)

        # As difficulty increases, more ceiling and flying enemies
        # At low difficulty: mostly ground (80% ground, 15% ceiling, 5% flying)
        # At high difficulty: more varied (50% ground, 30% ceiling, 20% flying)
        ground_chance = 0.8 - (difficulty_percent / 100) * 0.3
        ceiling_chance = 0.15 + (difficulty_percent / 100) * 0.15
        # flying_chance = 1 - ground_chance - ceiling_chance

        roll = random.random()
        if roll < ground_chance:
            return "ground"
        elif roll < ground_chance + ceiling_chance:
            return "ceiling"
        else:
            return "flying"

    def _spawn_ceiling_enemy_at(self, x, ceiling_enemies):
        """
        Spawn a ceiling enemy at the given position.

        Args:
            x: X position to spawn at
            ceiling_enemies: Sprite group for ceiling enemies
        """
        # Ceiling enemies spawn at the top
        spawn_y = CEILING_HEIGHT
        spawn_x = x

        enemy = CeilingEnemy(spawn_x, spawn_y)

        # Apply difficulty scaling
        self._apply_difficulty_scaling(enemy)
        ceiling_enemies.add(enemy)

    def _spawn_flying_enemy_at(self, x, enemies):
        """
        Spawn a flying enemy at the given position.

        Args:
            x: X position to spawn at
            enemies: Sprite group for enemies
        """
        spawn_x = x
        # Flying enemies start in the middle area
        spawn_y = self.screen_height // 2

        enemy = FlyingEnemy(spawn_x, spawn_y, self.screen_height)

        # Apply difficulty scaling
        self._apply_difficulty_scaling(enemy)
        enemies.add(enemy)

    def _spawn_swarm_at(self, x, enemies):
        """
        Spawn a swarm of enemies at the given position.

        Args:
            x: X position to start swarm
            enemies: Sprite group
        """
        if not self.difficulty_manager:
            return

        swarm_size = self.difficulty_manager.get_swarm_size()

        for i in range(swarm_size):
            spawn_x = x + (i * SWARM_SPACING)
            spawn_y = self.screen_height - GROUND_HEIGHT - ENEMY_HEIGHT

            # Swarms are mostly basic enemies with occasional chasers
            if random.random() < 0.3 and self.difficulty_manager.is_enemy_unlocked(
                "chaser"
            ):
                enemy = ChaserEnemy(spawn_x, spawn_y)
            else:
                enemy = Enemy(spawn_x, spawn_y)

            # Apply difficulty scaling
            self._apply_difficulty_scaling(enemy)
            enemies.add(enemy)

        # Skip ahead so we don't spawn on top of swarm
        self.last_spawn_x = x + (swarm_size * SWARM_SPACING) + 200

    def _spawn_enemy_at(self, x, enemies, platforms):
        """
        Spawn an enemy at a given x position with difficulty-based type selection.

        Args:
            x: X position to spawn at
            enemies: Sprite group
            platforms: Platforms to place enemies on (unused - ground-based runner)
        """
        spawn_y = self.screen_height - GROUND_HEIGHT - ENEMY_HEIGHT
        spawn_x = x

        # Choose enemy type based on difficulty weights
        enemy_type = self._choose_enemy_type()

        if enemy_type == "basic":
            enemy = Enemy(spawn_x, spawn_y)
        elif enemy_type == "chaser":
            enemy = ChaserEnemy(spawn_x, spawn_y)
            # Apply detection range scaling
            if self.difficulty_manager:
                enemy.detection_range = int(
                    enemy.detection_range
                    * self.difficulty_manager.get_chaser_detection_multiplier()
                )
        elif enemy_type == "shooter":
            enemy = ShooterEnemy(spawn_x, spawn_y)
            # Apply cooldown scaling (faster shooting)
            if self.difficulty_manager:
                enemy.shoot_cooldown = int(
                    enemy.shoot_cooldown
                    * self.difficulty_manager.get_shooter_cooldown_multiplier()
                )
        elif enemy_type == "berserker":
            enemy = BerserkerEnemy(spawn_x, spawn_y)
        else:
            enemy = Enemy(spawn_x, spawn_y)

        # Apply general difficulty scaling
        self._apply_difficulty_scaling(enemy)
        enemies.add(enemy)

    def _apply_difficulty_scaling(self, enemy):
        """
        Apply difficulty-based scaling to an enemy.

        Args:
            enemy: Enemy instance to scale
        """
        if self.difficulty_manager:
            speed_mult = self.difficulty_manager.enemy_speed_multiplier
            health_bonus = self.difficulty_manager.get_enemy_health_bonus()

            # Scale speed
            enemy.speed = ENEMY_SPEED * speed_mult
            enemy.velocity_x = enemy.speed

            # Add bonus health at higher difficulties
            enemy.health += health_bonus

            # Scale patrol range based on difficulty progress
            enemy.patrol_range = 100 + int(self.difficulty_manager.difficulty_percent)
        else:
            # Legacy behavior
            enemy.patrol_range = 100 + self.difficulty * 20
            enemy.speed = ENEMY_SPEED * (1 + (self.difficulty - 1) * 0.1)

    def _choose_enemy_type(self):
        """Choose enemy type using weighted random selection from difficulty manager"""
        if not self.difficulty_manager:
            # Legacy behavior
            return self._choose_enemy_type_legacy()

        weights = self.difficulty_manager.get_enemy_weights()
        # weights = (basic, chaser, shooter, berserker)

        roll = random.random()
        cumulative = 0.0

        enemy_types = ["basic", "chaser", "shooter", "berserker"]

        for i, weight in enumerate(weights):
            cumulative += weight
            if roll < cumulative:
                # Check if enemy type is unlocked
                enemy_type = enemy_types[i]
                if self.difficulty_manager.is_enemy_unlocked(enemy_type):
                    return enemy_type
                else:
                    # Fall back to basic if not unlocked
                    return "basic"

        return "basic"

    def _choose_enemy_type_legacy(self):
        """Legacy enemy type selection for backwards compatibility"""
        roll = random.random()

        if self.difficulty < 3:
            return "basic"
        elif self.difficulty < 5:
            if roll < 0.7:
                return "basic"
            else:
                return "chaser"
        else:
            if roll < 0.4:
                return "basic"
            elif roll < 0.75:
                return "chaser"
            else:
                return "shooter"

    def cleanup(self, player_x, enemies):
        """
        Remove enemies far behind the player

        Args:
            player_x: Player's x position
            enemies: Sprite group
        """
        cleanup_x = player_x - self.screen_width

        for enemy in list(enemies):
            if enemy.rect.right < cleanup_x:
                enemy.kill()

    def reset(self):
        """Reset spawner state"""
        self.last_spawn_x = 0
        self.difficulty = 1
        self.spawn_rate_multiplier = 1.0
