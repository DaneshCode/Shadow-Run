"""
Player Module
Contains the Player class with movement, physics, and animation handling
"""

import pygame
import os
from game.settings import *
from game.utils import Animation, create_placeholder_surface, clamp


class Player(pygame.sprite.Sprite):
    """
    Player class handling movement, jumping, physics, and animations
    """

    def __init__(self, x, y):
        """
        Initialize the player

        Args:
            x: Initial x position
            y: Initial y position
        """
        super().__init__()

        # Load or create animations
        self.animations = self._load_animations()
        self.current_animation = "idle"
        self.facing_right = True

        # Get initial image from animation
        self.image = self.animations["idle"].get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Collision rect (slightly smaller than sprite for better gameplay feel)
        # Scaled proportionally: original was (WIDTH-10, HEIGHT-4), now 3x
        self.collision_rect = pygame.Rect(0, 0, PLAYER_WIDTH - 30, PLAYER_HEIGHT)
        self.collision_rect.midbottom = self.rect.midbottom

        # Physics properties
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0
        self.on_ground = False
        self.can_jump = True

        # Player stats
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.score = 0
        self.coins = 0

        # State flags
        self.is_jumping = False
        self.is_falling = False
        self.is_running = False
        self.is_invincible = False
        self.is_dead = False

        # Invincibility timer
        self.invincibility_timer = 0
        self.blink_timer = 0
        self.visible = True

        # Double jump ability (optional - can be unlocked)
        self.can_double_jump = False
        self.double_jump_available = False

        # Shooting mechanics
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = 0
        self.can_shoot = True

        # Ammo system
        self.ammo = MAX_AMMO
        self.max_ammo = MAX_AMMO
        self.last_ammo_regen_time = 0

    def _load_animations(self):
        """
        Load all player animations or create placeholder frames

        Returns:
            dict: Dictionary of Animation objects
        """
        animations = {}

        # Try to load sprite sheets from assets folder
        sprite_folders = {
            "idle": "assets/sprites/player/idle",
            "walk": "assets/sprites/player/walk",
            "jump": "assets/sprites/player/jump",
            "dash": "assets/sprites/player/Dash2",
        }

        for anim_name, folder_path in sprite_folders.items():
            frames = self._load_frames_from_folder(folder_path)
            if frames:
                animations[anim_name] = Animation(frames, ANIMATION_SPEED)
            else:
                # Create placeholder animation
                animations[anim_name] = Animation(
                    self._create_placeholder_frames(anim_name), ANIMATION_SPEED
                )

        # Ensure we have fall animation (can reuse jump)
        if "fall" not in animations:
            animations["fall"] = animations["jump"]

        return animations

    def _load_frames_from_folder(self, folder_path):
        """
        Load all image frames from a folder

        Args:
            folder_path: Path to folder containing frame images

        Returns:
            list: List of pygame surfaces, or empty list if folder doesn't exist
        """
        frames = []

        if not os.path.exists(folder_path):
            return frames

        # Get all image files in folder
        valid_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
        files = sorted(
            [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]
        )

        for filename in files:
            try:
                image_path = os.path.join(folder_path, filename)
                image = pygame.image.load(image_path).convert_alpha()
                # Scale to player size
                image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                frames.append(image)
            except pygame.error as e:
                print(f"Error loading {filename}: {e}")

        return frames

    def _create_placeholder_frames(self, animation_name):
        """
        Create placeholder animation frames when no sprites are available

        Args:
            animation_name: Name of the animation

        Returns:
            list: List of placeholder surfaces
        """
        frames = []
        base_color = PLAYER_COLOR

        for i in range(4):  # 4 frames per animation
            surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)

            # Draw body
            body_rect = pygame.Rect(8, 10, PLAYER_WIDTH - 16, PLAYER_HEIGHT - 20)
            pygame.draw.rect(surface, base_color, body_rect, border_radius=8)

            # Draw head
            head_rect = pygame.Rect(12, 0, PLAYER_WIDTH - 24, 20)
            pygame.draw.rect(surface, base_color, head_rect, border_radius=6)

            # Draw eyes
            eye_color = WHITE
            pygame.draw.circle(surface, eye_color, (20, 10), 4)
            pygame.draw.circle(surface, eye_color, (PLAYER_WIDTH - 20, 10), 4)
            pygame.draw.circle(surface, BLACK, (22, 10), 2)
            pygame.draw.circle(surface, BLACK, (PLAYER_WIDTH - 18, 10), 2)

            # Animation-specific modifications
            if animation_name == "walk" or animation_name == "dash":
                # Animate legs
                leg_offset = (i % 2) * 6 - 3
                pygame.draw.rect(
                    surface, base_color, (14, PLAYER_HEIGHT - 14, 8, 14 + leg_offset)
                )
                pygame.draw.rect(
                    surface,
                    base_color,
                    (PLAYER_WIDTH - 22, PLAYER_HEIGHT - 14, 8, 14 - leg_offset),
                )
            elif animation_name == "jump":
                # Legs together, slightly bent
                pygame.draw.rect(
                    surface, base_color, (16, PLAYER_HEIGHT - 16, PLAYER_WIDTH - 32, 16)
                )
            else:
                # Idle - standing legs
                pygame.draw.rect(surface, base_color, (14, PLAYER_HEIGHT - 14, 8, 14))
                pygame.draw.rect(
                    surface, base_color, (PLAYER_WIDTH - 22, PLAYER_HEIGHT - 14, 8, 14)
                )

            frames.append(surface)

        return frames

    def handle_input(self, keys, game_speed=1.0):
        """
        Handle player input - Auto-run mode
        Only jumping is controlled by player, movement is automatic

        Args:
            keys: pygame key state
            game_speed: Current game speed multiplier for difficulty scaling
        """
        if self.is_dead:
            return

        # Auto-run: always running right with speed scaled by difficulty
        self.acceleration_x = PLAYER_ACCELERATION
        self.facing_right = True
        self.is_running = True
        self.velocity_x = AUTO_RUN_SPEED * game_speed  # Speed increases with difficulty

        # Jumping only
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump()

    def jump(self):
        """Perform a jump if allowed"""
        if self.is_dead:
            return

        if self.on_ground and self.can_jump:
            self.velocity_y = PLAYER_JUMP_POWER
            self.on_ground = False
            self.is_jumping = True
            self.can_jump = False
            self.double_jump_available = self.can_double_jump
            return True
        elif self.can_double_jump and self.double_jump_available and not self.on_ground:
            # Double jump
            self.velocity_y = PLAYER_JUMP_POWER * 0.85
            self.double_jump_available = False
            return True

        return False

    def release_jump(self):
        """Called when jump key is released"""
        self.can_jump = True

        # Variable jump height - cut jump short if released early
        if self.velocity_y < -5:
            self.velocity_y = -5

    def update(self, platforms):
        """
        Update player physics and state

        Args:
            platforms: Sprite group of platforms for collision
        """
        if self.is_dead:
            return

        # Apply acceleration and friction
        self.velocity_x += self.acceleration_x

        if not self.is_running:
            self.velocity_x *= FRICTION

        # Clamp horizontal velocity
        self.velocity_x = clamp(self.velocity_x, -PLAYER_SPEED, PLAYER_SPEED)

        # Stop if velocity is very small
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0

        # Apply gravity
        self.velocity_y += GRAVITY
        self.velocity_y = min(self.velocity_y, MAX_FALL_SPEED)

        # Update falling state
        self.is_falling = self.velocity_y > 0 and not self.on_ground

        # Move and check collisions
        self._move_and_collide(platforms)

        # Update invincibility
        if self.is_invincible:
            self.invincibility_timer -= 1000 / FPS
            self.blink_timer += 1
            self.visible = (self.blink_timer // 5) % 2 == 0

            if self.invincibility_timer <= 0:
                self.is_invincible = False
                self.visible = True

        # Update animation
        self._update_animation()

    def _move_and_collide(self, platforms):
        """
        Move player and handle platform collisions

        Args:
            platforms: Sprite group of platforms
        """
        # Store old position
        old_x = self.rect.x
        old_y = self.rect.y

        # Move horizontally
        self.rect.x += self.velocity_x
        self.collision_rect.midbottom = self.rect.midbottom

        # Check horizontal collisions
        for platform in platforms:
            if self.collision_rect.colliderect(platform.rect):
                if self.velocity_x > 0:  # Moving right
                    self.collision_rect.right = platform.rect.left
                elif self.velocity_x < 0:  # Moving left
                    self.collision_rect.left = platform.rect.right

                self.rect.midbottom = self.collision_rect.midbottom
                self.velocity_x = 0

        # Move vertically
        self.rect.y += self.velocity_y
        self.collision_rect.midbottom = self.rect.midbottom

        # Check vertical collisions
        self.on_ground = False

        for platform in platforms:
            if self.collision_rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Falling
                    self.collision_rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.is_jumping = False
                    self.velocity_y = 0
                elif self.velocity_y < 0:  # Rising
                    self.collision_rect.top = platform.rect.bottom
                    self.velocity_y = 0

                self.rect.midbottom = self.collision_rect.midbottom

    def _update_animation(self):
        """Update the current animation based on player state"""
        # Determine which animation to play
        if self.is_jumping or (self.velocity_y < 0 and not self.on_ground):
            new_animation = "jump"
        elif self.is_falling:
            new_animation = "fall"
        elif self.is_running and abs(self.velocity_x) > 0.5:
            new_animation = "walk"
        else:
            new_animation = "idle"

        # Switch animation if needed
        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.animations[self.current_animation].reset()

        # Update current animation
        self.animations[self.current_animation].update()

        # Get current frame and flip if needed
        frame = self.animations[self.current_animation].get_current_frame()

        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        self.image = frame

    def take_damage(self, amount):
        """
        Apply damage to the player

        Args:
            amount: Amount of damage to take

        Returns:
            bool: True if damage was applied, False if invincible
        """
        if self.is_invincible or self.is_dead:
            return False

        self.health -= amount
        self.health = max(0, self.health)

        # Start invincibility
        self.is_invincible = True
        self.invincibility_timer = PLAYER_INVINCIBILITY_TIME
        self.blink_timer = 0

        # Check for death
        if self.health <= 0:
            self.die()

        return True

    def heal(self, amount):
        """
        Heal the player

        Args:
            amount: Amount to heal
        """
        self.health += amount
        self.health = min(self.health, self.max_health)

    def add_score(self, points):
        """Add points to the score"""
        self.score += points

    def add_coins(self, amount=1):
        """Add coins to the player's collection"""
        self.coins += amount
        self.add_score(COIN_VALUE)

    def die(self):
        """Handle player death"""
        self.is_dead = True
        self.velocity_x = 0
        self.velocity_y = 0

    def reset(self, x, y):
        """
        Reset player to initial state

        Args:
            x, y: New spawn position
        """
        self.rect.x = x
        self.rect.y = y
        self.collision_rect.midbottom = self.rect.midbottom

        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0

        self.health = self.max_health
        self.score = 0
        self.coins = 0

        self.on_ground = False
        self.is_jumping = False
        self.is_falling = False
        self.is_running = False
        self.is_invincible = False
        self.is_dead = False
        self.visible = True

        self.facing_right = True
        self.current_animation = "idle"

        # Reset bullets
        self.bullets.empty()
        self.last_shot_time = 0

        # Reset ammo
        self.ammo = self.max_ammo
        self.last_ammo_regen_time = pygame.time.get_ticks()

    def draw(self, surface, camera_offset=(0, 0)):
        """
        Draw the player

        Args:
            surface: Surface to draw on
            camera_offset: Camera offset tuple (x, y)
        """
        if not self.visible:
            return

        # Calculate screen position
        screen_x = self.rect.x - camera_offset[0]
        screen_y = (
            self.rect.y - camera_offset[1] + 40
        )  # Offset to align feet with ground

        # Draw player
        surface.blit(self.image, (screen_x, screen_y))

        # Debug: Draw collision rect (uncomment for debugging)
        # debug_rect = self.collision_rect.copy()
        # debug_rect.x -= camera_offset[0]
        # debug_rect.y -= camera_offset[1]
        # pygame.draw.rect(surface, RED, debug_rect, 1)

    def shoot(self):
        """Attempt to shoot a bullet - requires ammo"""
        if self.is_dead:
            return False

        # Check if we have ammo
        if self.ammo <= 0:
            return False

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= BULLET_COOLDOWN:
            self.last_shot_time = current_time
            self.ammo -= 1  # Use one ammo

            # Create bullet at player's lower body (where enemies are)
            # Bullet spawn offset scaled for larger player
            bullet_x = self.rect.centerx + (60 if self.facing_right else -60)
            # Shoot at lower body height (closer to feet) to hit ground enemies
            bullet_y = self.rect.bottom - 60  # Near player's feet level
            direction = 1 if self.facing_right else -1

            bullet = Bullet(bullet_x, bullet_y, direction)
            self.bullets.add(bullet)
            return True
        return False

    def update_ammo(self):
        """Regenerate ammo over time"""
        if self.ammo < self.max_ammo:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_ammo_regen_time >= AMMO_REGEN_TIME:
                self.last_ammo_regen_time = current_time
                self.ammo = min(self.ammo + 1, self.max_ammo)

    def update_bullets(self, camera_x):
        """Update all player bullets"""
        self.bullets.update()

        # Remove bullets that are too far off screen
        for bullet in list(self.bullets):
            if (
                bullet.rect.x < camera_x - 100
                or bullet.rect.x > camera_x + SCREEN_WIDTH + 100
            ):
                bullet.kill()
            elif bullet.is_expired():
                bullet.kill()

    def draw_bullets(self, surface, camera_offset=(0, 0)):
        """Draw all bullets"""
        for bullet in self.bullets:
            bullet.draw(surface, camera_offset)


class Bullet(pygame.sprite.Sprite):
    """
    Bullet class for player shooting
    """

    def __init__(self, x, y, direction):
        """
        Initialize a bullet

        Args:
            x: Starting X position
            y: Starting Y position
            direction: 1 for right, -1 for left
        """
        super().__init__()

        self.direction = direction
        self.speed = BULLET_SPEED
        self.damage = BULLET_DAMAGE
        self.spawn_time = pygame.time.get_ticks()

        # Create bullet surface with glow effect
        self.image = self._create_bullet_surface()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def _create_bullet_surface(self):
        """Create a glowing bullet surface"""
        size = BULLET_SIZE * 3  # Extra space for glow
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2

        # Outer glow
        glow_color = (*BULLET_COLOR[:3], 50)
        pygame.draw.circle(surface, glow_color, (center, center), BULLET_SIZE + 4)

        # Inner glow
        inner_glow = (*BULLET_COLOR[:3], 100)
        pygame.draw.circle(surface, inner_glow, (center, center), BULLET_SIZE + 2)

        # Core
        pygame.draw.circle(surface, BULLET_COLOR, (center, center), BULLET_SIZE)

        # Bright center
        pygame.draw.circle(surface, (255, 220, 150), (center, center), BULLET_SIZE // 2)

        return surface

    def update(self):
        """Update bullet position"""
        self.rect.x += self.speed * self.direction

    def is_expired(self):
        """Check if bullet has exceeded its lifetime"""
        return pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME

    def draw(self, surface, camera_offset=(0, 0)):
        """Draw the bullet"""
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]
        surface.blit(self.image, (screen_x, screen_y))
