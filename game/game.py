"""
Game Manager Module
Main game class that coordinates all game systems
"""

import pygame
from game.settings import *
from game.player import Player
from game.platforms import WorldGenerator
from game.enemies import EnemySpawner
from game.collectibles import CollectibleSpawner
from game.difficulty import DifficultyManager
from game.camera import Camera
from game.sound import SoundManager
from game.leaderboard import Leaderboard
from game.background import Background, VisualEffects
from game.ui import (
    HUD,
    MainMenu,
    PauseMenu,
    GameOverScreen,
    LeaderboardScreen,
    SettingsScreen,
    TutorialScreen,
)
from game.utils import ParticleSystem


class Game:
    """
    Main game class that manages all game systems and the game loop
    """

    def __init__(self):
        """Initialize the game"""
        # Initialize Pygame
        pygame.init()
        pygame.font.init()

        # Display setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        # Game state
        self.state = STATE_MENU
        self.running = True

        # Initialize all managers
        self._init_managers()

        # Initialize game objects
        self._init_game_objects()

        # Initialize UI
        self._init_ui()

        # Game statistics
        self.difficulty_level = 1
        self.last_difficulty_score = 0
        self.start_x = 0  # Track starting position for distance-based scoring

        # Player name for leaderboard
        self.player_name = "Player"

    def _init_managers(self):
        """Initialize all game managers"""
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.sound_manager = SoundManager()
        self.leaderboard = Leaderboard()
        self.world_generator = WorldGenerator(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.enemy_spawner = EnemySpawner(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.collectible_spawner = CollectibleSpawner(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.particle_system = ParticleSystem()
        self.background = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.visual_effects = VisualEffects(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Difficulty manager for smooth score-based scaling
        self.difficulty_manager = DifficultyManager()

        # Connect difficulty manager to spawner
        self.enemy_spawner.set_difficulty_manager(self.difficulty_manager)

        # Generate procedural sounds if no audio files exist
        self.sound_manager.create_procedural_sounds()

        # Start professional layered ambient audio (horror + pond ambience mix)
        self.sound_manager.start_ambient_audio()

        # Current game speed multiplier (increases with difficulty)
        self.game_speed = 1.0

    def _init_game_objects(self):
        """Initialize game object groups"""
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.grounds = pygame.sprite.Group()
        self.ceilings = pygame.sprite.Group()  # Ceiling surfaces for gravity flip
        self.enemies = pygame.sprite.Group()
        self.ceiling_enemies = pygame.sprite.Group()  # Enemies on ceiling
        self.coins = pygame.sprite.Group()
        self.health_packs = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        # Player
        self.player = Player(200, SCREEN_HEIGHT - GROUND_HEIGHT - 100)
        self.all_sprites.add(self.player)

    def _init_ui(self):
        """Initialize UI elements"""
        self.hud = HUD(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.main_menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.pause_menu = PauseMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.game_over_screen = GameOverScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.leaderboard_screen = LeaderboardScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.settings_screen = SettingsScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.tutorial_screen = TutorialScreen(SCREEN_WIDTH, SCREEN_HEIGHT)

    def new_game(self):
        """Start a new game"""
        # Reset player
        self.player.reset(200, SCREEN_HEIGHT - GROUND_HEIGHT - 100)

        # Clear all groups
        self.platforms.empty()
        self.grounds.empty()
        self.ceilings.empty()
        self.enemies.empty()
        self.ceiling_enemies.empty()
        self.coins.empty()
        self.health_packs.empty()
        self.powerups.empty()

        # Reset managers
        self.world_generator.reset()
        self.enemy_spawner.reset()
        self.collectible_spawner.reset()
        self.camera.reset()
        self.particle_system.clear()

        # Generate initial world (now includes ceiling)
        self.world_generator.generate_initial_world(
            self.platforms, self.grounds, self.coins, self.enemies, self.ceilings
        )

        # Reset statistics
        self.difficulty_level = 1
        self.last_difficulty_score = 0
        self.game_speed = 1.0
        self.start_x = self.player.rect.x  # Track starting position for scoring
        self.last_distance_score = 0  # Track last distance-based score separately

        # Reset difficulty manager
        self.difficulty_manager.reset()

        # Reset controls hint
        self.hud.reset_controls_hint()

        # Show tutorial before playing
        self.state = STATE_TUTORIAL

    def start_playing(self):
        """Called after tutorial to actually start the game"""
        self.state = STATE_PLAYING

    def run(self):
        """Main game loop"""
        while self.running:
            self.clock.tick(FPS)

            # Handle events
            self._handle_events()

            # Update based on state
            self._update()

            # Draw
            self._draw()

            # Update display
            pygame.display.flip()

        pygame.quit()

    def _handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

            elif event.type == pygame.KEYUP:
                self._handle_keyup(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mousedown(event)

    def _handle_mousedown(self, event):
        """Handle mouse button press events"""
        if self.state == STATE_PLAYING and event.button == 1:  # Left click
            # Check if clicked on invisibility button first
            if self.hud.check_invisibility_click(event.pos):
                self._activate_invisibility()
            else:
                # Otherwise shoot
                if self.player.shoot():
                    self.sound_manager.play_sound("shoot")
        elif self.state == STATE_PLAYING and event.button == 3:  # Right click
            self._activate_invisibility()
        elif self.state == STATE_TUTORIAL:
            self.start_playing()

    def _handle_keydown(self, event):
        """Handle key press events"""
        # Tutorial: any key starts the game
        if self.state == STATE_TUTORIAL:
            self.start_playing()
            return

        if event.key == pygame.K_ESCAPE:
            if self.state == STATE_PLAYING:
                self.state = STATE_PAUSED
                self.sound_manager.pause_music()
            elif self.state == STATE_PAUSED:
                self.state = STATE_PLAYING
                self.sound_manager.unpause_music()
            elif self.state in [STATE_LEADERBOARD, STATE_SETTINGS]:
                self.state = STATE_MENU
            elif self.state == STATE_GAME_OVER:
                self.state = STATE_MENU

        elif event.key == pygame.K_p:
            if self.state == STATE_PLAYING:
                self.state = STATE_PAUSED
                self.sound_manager.pause_music()
            elif self.state == STATE_PAUSED:
                self.state = STATE_PLAYING
                self.sound_manager.unpause_music()

        elif event.key == pygame.K_RETURN:
            if self.state == STATE_MENU:
                self.new_game()
            elif self.state == STATE_GAME_OVER:
                self.new_game()

        elif event.key in [pygame.K_x, pygame.K_z, pygame.K_LCTRL, pygame.K_RCTRL]:
            if self.state == STATE_PLAYING:
                if self.player.shoot():
                    self.sound_manager.play_sound("shoot")

        elif event.key in [pygame.K_g, pygame.K_c]:  # Ghost/Invisibility
            if self.state == STATE_PLAYING:
                self._activate_invisibility()

    def _activate_invisibility(self):
        """Activate player invisibility and play feedback if the charge is ready."""
        if self.player.activate_invisibility():
            self.sound_manager.play_sound("powerup")
            self.visual_effects.flash((100, 200, 255), 20)
            return True
        return False

    def _handle_keyup(self, event):
        """Handle key release events"""
        if self.state == STATE_PLAYING:
            if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]:
                self.player.release_jump()

    def _update(self):
        """Update game state"""
        if self.state == STATE_MENU:
            self._update_menu()
        elif self.state == STATE_TUTORIAL:
            self._update_tutorial()
        elif self.state == STATE_PLAYING:
            self._update_gameplay()
        elif self.state == STATE_PAUSED:
            self._update_paused()
        elif self.state == STATE_GAME_OVER:
            self._update_game_over()
        elif self.state == STATE_LEADERBOARD:
            self._update_leaderboard()
        elif self.state == STATE_SETTINGS:
            self._update_settings()

    def _update_tutorial(self):
        """Update tutorial screen"""
        self.tutorial_screen.update()

    def _update_menu(self):
        """Update main menu"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Update high score display on menu
        self.main_menu.set_high_score(self.leaderboard.get_high_score())

        action = self.main_menu.update(mouse_pos, mouse_pressed)

        if action == "play":
            self.sound_manager.play_sound("click")
            self.new_game()
        elif action == "leaderboard":
            self.sound_manager.play_sound("click")
            self.leaderboard_screen.set_entries(self.leaderboard.get_entries())
            self.state = STATE_LEADERBOARD
        elif action == "settings":
            self.sound_manager.play_sound("click")
            self.state = STATE_SETTINGS
        elif action == "quit":
            self.running = False

    def _update_gameplay(self):
        """Update main gameplay"""
        # Get input
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, self.game_speed)

        # Update player - pass both ground and ceiling surfaces for collision
        self.player.update(list(self.grounds), list(self.ceilings))

        # Update player bullets
        self.player.update_bullets(self.camera.x)
        self.player.update_ammo()  # Regenerate ammo over time
        self.player.update_invisibility()  # Update invisibility charge/timer
        self._check_bullet_enemy_collisions()

        # Update HUD for button hover
        mouse_pos = pygame.mouse.get_pos()
        dt = self.clock.get_time()  # Get actual delta time from clock
        self.hud.update(mouse_pos, dt)

        # Update camera
        self.camera.update(self.player)

        # Update background
        self.background.update(self.camera.x)

        # Update world generation (includes ceiling for gravity flip)
        self.world_generator.update(
            self.player.rect.x,
            self.platforms,
            self.grounds,
            self.coins,
            self.enemies,
            self.ceilings,
        )

        # Spawn and update enemies (ground, ceiling, and flying)
        self.enemy_spawner.update(
            self.player.rect.x, self.enemies, [], self.ceiling_enemies
        )

        # Update all ground/flying enemies
        for enemy in self.enemies:
            enemy.update(self.player, None)
            self._check_enemy_projectile_collisions(enemy)

        # Update ceiling enemies
        for enemy in self.ceiling_enemies:
            enemy.update(self.player, None)
            self._check_enemy_projectile_collisions(enemy)

        # Check enemy collisions (both ground and ceiling enemies)
        self._check_enemy_collisions()

        # Spawn and update collectibles (ground-based only)
        self.collectible_spawner.update(
            self.player.rect.x,
            self.coins,
            self.health_packs,
            self.powerups,
            [],  # No platforms - ground-based endless runner
        )

        self.coins.update()
        self.health_packs.update()
        self.powerups.update()

        # Check collectible collisions
        self._check_collectible_collisions()

        # Update particles and effects
        self.particle_system.update()
        self.visual_effects.update()

        # Update dynamic ambient audio based on game state (AAA-style reactive audio)
        health_percent = self.player.health / PLAYER_MAX_HEALTH
        # Check both ground and ceiling enemies for nearby threat detection
        enemies_nearby = any(
            abs(enemy.rect.x - self.player.rect.x) < 400
            for enemy in list(self.enemies) + list(self.ceiling_enemies)
            if not enemy.is_dead
        )
        difficulty = (
            self.difficulty_manager.difficulty_level / 10.0
        )  # Normalize to 0.1-1.0
        self.sound_manager.update_danger_level(
            health_percent, enemies_nearby, difficulty
        )
        self.sound_manager.update_ambient_audio(1 / FPS)

        # Add distance-based score (faster rate for more engaging gameplay)
        distance_traveled = max(0, (self.player.rect.x - self.start_x) / 25)
        distance_score = int(distance_traveled)
        score_diff = distance_score - self.last_distance_score
        if score_diff > 0:
            self.player.add_score(2 * score_diff)  # Give 2 points per distance unit
            self.last_distance_score = distance_score

        # Update difficulty
        self._update_difficulty()

        # Cleanup ground and ceiling enemies
        self.enemy_spawner.cleanup(self.player.rect.x, self.enemies)
        self.enemy_spawner.cleanup(self.player.rect.x, self.ceiling_enemies)
        self.collectible_spawner.cleanup(
            self.player.rect.x, self.coins, self.health_packs, self.powerups
        )

        # Check for death (fell off screen or health depleted)
        # With gravity flip, player shouldn't die from going off-screen vertically
        if self.player.is_dead:
            self._game_over()

    def _check_enemy_collisions(self):
        """Check collisions between player and enemies (ground, flying, and ceiling)"""
        # Skip collision check if player is invisible (ghost mode)
        if self.player.is_invisible:
            return

        # Combine all enemies for collision checking
        all_enemies = list(self.enemies) + list(self.ceiling_enemies)

        for enemy in all_enemies:
            if enemy.is_dead:
                continue

            if self.player.collision_rect.colliderect(enemy.rect):
                # Determine stomp conditions based on gravity state and enemy type
                is_ceiling_enemy = (
                    hasattr(enemy, "is_ceiling_enemy") and enemy.is_ceiling_enemy
                )

                can_stomp = False
                if self.player.gravity_flipped:
                    # When gravity is flipped, player is on ceiling
                    if is_ceiling_enemy:
                        # Stomp ceiling enemies from below (player moving up)
                        if (
                            self.player.velocity_y < 0
                            and self.player.collision_rect.top > enemy.rect.centery - 60
                        ):
                            can_stomp = True
                    else:
                        # Stomp ground enemies from above when jumping down (gravity flipped)
                        if (
                            self.player.velocity_y > 0
                            and self.player.collision_rect.bottom
                            < enemy.rect.centery + 60
                        ):
                            can_stomp = True
                else:
                    # Normal gravity - stomp ground enemies from above
                    if not is_ceiling_enemy:
                        if (
                            self.player.velocity_y > 0
                            and self.player.collision_rect.bottom
                            < enemy.rect.centery + 60
                        ):
                            can_stomp = True

                if can_stomp:
                    # Stomp enemy
                    enemy.take_damage()
                    # Bounce direction depends on gravity
                    bounce_power = (
                        PLAYER_JUMP_POWER * 0.6
                        if not self.player.gravity_flipped
                        else -PLAYER_JUMP_POWER * 0.6
                    )
                    self.player.velocity_y = bounce_power
                    self.player.add_score(50)
                    self.sound_manager.play_sound("enemy_death")
                    particle_color = (
                        CEILING_ENEMY_COLOR if is_ceiling_enemy else ENEMY_COLOR
                    )
                    self.particle_system.emit(
                        enemy.rect.centerx, enemy.rect.centery, particle_color, count=20
                    )
                else:
                    # Take damage
                    if self.player.take_damage(enemy.damage):
                        self.sound_manager.play_sound("hurt")
                        self.sound_manager.pulse_horror_audio()
                        self.camera.shake(10, 20)
                        self.visual_effects.flash(RED, 50)
                        self.particle_system.emit(
                            self.player.rect.centerx,
                            self.player.rect.centery,
                            RED,
                            count=15,
                        )

    def _check_enemy_projectile_collisions(self, enemy):
        """Apply damage from any enemy-owned projectiles."""
        if self.player.is_invisible or not hasattr(enemy, "projectiles"):
            return

        for proj in list(enemy.projectiles):
            if self.player.collision_rect.colliderect(proj.rect):
                if self.player.take_damage(proj.damage):
                    self.sound_manager.play_sound("hurt")
                    self.sound_manager.pulse_horror_audio()
                    self.camera.shake(8, 15)
                    self.visual_effects.flash(RED, 35)
                    self.particle_system.emit(
                        self.player.rect.centerx,
                        self.player.rect.centery,
                        RED,
                        count=15,
                    )

                proj.is_dead = True
                if proj in enemy.projectiles:
                    enemy.projectiles.remove(proj)

    def _check_bullet_enemy_collisions(self):
        """Check collisions between player bullets and enemies (all types)"""
        # Combine all enemies for bullet collision
        all_enemies = list(self.enemies) + list(self.ceiling_enemies)

        for bullet in list(self.player.bullets):
            for enemy in all_enemies:
                if enemy.is_dead:
                    continue

                if bullet.rect.colliderect(enemy.rect):
                    # Bullet hit enemy
                    enemy.take_damage(bullet.damage)
                    bullet.kill()

                    # Effects
                    self.sound_manager.play_sound("hit")
                    self.particle_system.emit(
                        bullet.rect.centerx, bullet.rect.centery, BULLET_COLOR, count=10
                    )

                    if enemy.is_dead:
                        self.player.add_score(75)  # Bonus for shooting kill
                        self.sound_manager.play_sound("enemy_death")
                        # Use appropriate color based on enemy type
                        is_ceiling_enemy = (
                            hasattr(enemy, "is_ceiling_enemy")
                            and enemy.is_ceiling_enemy
                        )
                        particle_color = (
                            CEILING_ENEMY_COLOR if is_ceiling_enemy else ENEMY_COLOR
                        )
                        self.particle_system.emit(
                            enemy.rect.centerx,
                            enemy.rect.centery,
                            particle_color,
                            count=20,
                        )
                    break  # Each bullet can only hit one enemy

    def _check_collectible_collisions(self):
        """Check collisions between player and collectibles"""
        # Coins - only collect matching type based on gravity state
        for coin in list(self.coins):
            if self.player.collision_rect.colliderect(coin.rect):
                # Check if coin type matches player's gravity state
                # Ceiling coins can only be collected when gravity is flipped
                # Ground coins can only be collected when gravity is normal
                if coin.is_ceiling == self.player.gravity_flipped:
                    coin.collect(self.player)
                    self.sound_manager.play_sound("coin")
                    self.particle_system.emit(
                        coin.rect.centerx, coin.rect.centery, COIN_COLOR, count=8
                    )

        # Health packs
        for hp in list(self.health_packs):
            if self.player.collision_rect.colliderect(hp.rect):
                hp.collect(self.player)
                self.sound_manager.play_sound("powerup")
                self.particle_system.emit(
                    hp.rect.centerx, hp.rect.centery, RED, count=12
                )

        # Power-ups
        for pu in list(self.powerups):
            if self.player.collision_rect.colliderect(pu.rect):
                pu.collect(self.player)
                self.sound_manager.play_sound("powerup")
                self.visual_effects.flash(WHITE, 30)
                self.particle_system.emit(
                    pu.rect.centerx, pu.rect.centery, CYAN, count=20
                )

    def _update_difficulty(self):
        """Update game difficulty using the smooth difficulty manager"""
        # Update difficulty manager with current score
        milestone_reached = self.difficulty_manager.update(self.player.score)

        # Get smooth game speed from difficulty manager
        self.game_speed = self.difficulty_manager.game_speed

        # Update legacy difficulty level for UI display
        self.difficulty_level = self.difficulty_manager.difficulty_level

        # Visual/audio feedback when milestone is reached
        if milestone_reached:
            # Brief screen flash to indicate difficulty increase
            self.visual_effects.flash((100, 50, 50), 20)

            # Update legacy systems that still use discrete difficulty
            self.world_generator.set_difficulty(self.difficulty_level)
            self.enemy_spawner.set_difficulty(self.difficulty_level)

    def _game_over(self):
        """Handle game over"""
        self.state = STATE_GAME_OVER

        # Save score
        high_score = self.leaderboard.get_high_score()
        self.leaderboard.add_entry(
            self.player_name,
            self.player.score,
            self.player.coins,
        )

        # Update game over screen
        self.game_over_screen.set_data(self.player.score, high_score, self.player.coins)

        self.sound_manager.play_sound("death")

    def _update_paused(self):
        """Update pause menu"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        action = self.pause_menu.update(mouse_pos, mouse_pressed)

        # Apply volume changes from pause menu
        self.sound_manager.set_music_volume(self.pause_menu.music_volume)
        self.sound_manager.set_sfx_volume(self.pause_menu.sfx_volume)
        # Sync with settings screen
        self.settings_screen.music_volume = self.pause_menu.music_volume
        self.settings_screen.sfx_volume = self.pause_menu.sfx_volume

        if action == "resume":
            self.sound_manager.play_sound("click")
            self.state = STATE_PLAYING
            self.sound_manager.unpause_music()
        elif action == "restart":
            self.sound_manager.play_sound("click")
            self.new_game()
        elif action == "menu":
            self.sound_manager.play_sound("click")
            self.state = STATE_MENU

    def _update_game_over(self):
        """Update game over screen"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        action = self.game_over_screen.update(mouse_pos, mouse_pressed)

        if action == "restart":
            self.sound_manager.play_sound("click")
            self.new_game()
        elif action == "leaderboard":
            self.sound_manager.play_sound("click")
            self.leaderboard_screen.set_entries(self.leaderboard.get_entries())
            self.state = STATE_LEADERBOARD
        elif action == "menu":
            self.sound_manager.play_sound("click")
            self.state = STATE_MENU

    def _update_leaderboard(self):
        """Update leaderboard screen"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        action = self.leaderboard_screen.update(mouse_pos, mouse_pressed)

        if action == "back":
            self.sound_manager.play_sound("click")
            self.state = STATE_MENU

    def _update_settings(self):
        """Update settings screen"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        action = self.settings_screen.update(mouse_pos, mouse_pressed)

        # Apply volume changes
        self.sound_manager.set_music_volume(self.settings_screen.music_volume)
        self.sound_manager.set_sfx_volume(self.settings_screen.sfx_volume)
        # Sync with pause menu
        self.pause_menu.music_volume = self.settings_screen.music_volume
        self.pause_menu.sfx_volume = self.settings_screen.sfx_volume

        if action == "back":
            self.sound_manager.play_sound("click")
            self.state = STATE_MENU

    def _draw(self):
        """Draw everything to the screen"""
        if self.state == STATE_MENU:
            self.main_menu.draw(self.screen)

        elif self.state == STATE_TUTORIAL:
            # Draw game scene in background for atmosphere
            self._draw_gameplay()
            self.tutorial_screen.draw(self.screen)

        elif self.state == STATE_PLAYING:
            self._draw_gameplay()
            self.hud.draw(
                self.screen,
                self.player,
                self.difficulty_level,
                self.leaderboard.get_high_score(),
            )

        elif self.state == STATE_PAUSED:
            self._draw_gameplay()
            self.hud.draw(
                self.screen,
                self.player,
                self.difficulty_level,
                self.leaderboard.get_high_score(),
            )
            self.pause_menu.draw(self.screen)

        elif self.state == STATE_GAME_OVER:
            self._draw_gameplay()
            self.game_over_screen.draw(self.screen)

        elif self.state == STATE_LEADERBOARD:
            self.leaderboard_screen.draw(self.screen)

        elif self.state == STATE_SETTINGS:
            self.settings_screen.draw(self.screen)

    def _draw_gameplay(self):
        """Draw the gameplay scene"""
        camera_offset = self.camera.get_offset()

        # Draw background
        self.background.draw(self.screen, self.camera.x)

        # Draw grounds
        for ground in self.grounds:
            ground.draw(self.screen, camera_offset)

        # Draw ceilings (for gravity flip mechanic)
        for ceiling in self.ceilings:
            ceiling.draw(self.screen, camera_offset)

        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen, camera_offset)

        # Draw collectibles
        for coin in self.coins:
            coin.draw(self.screen, camera_offset)
        for hp in self.health_packs:
            hp.draw(self.screen, camera_offset)
        for pu in self.powerups:
            pu.draw(self.screen, camera_offset)

        # Draw all enemies (ground, flying, and ceiling)
        for enemy in self.enemies:
            enemy.draw(self.screen, camera_offset)
        for enemy in self.ceiling_enemies:
            enemy.draw(self.screen, camera_offset)

        # Draw player
        self.player.draw(self.screen, camera_offset)

        # Draw player bullets
        self.player.draw_bullets(self.screen, camera_offset)

        # Draw particles
        self.particle_system.draw(self.screen, camera_offset)

        # Draw visual effects
        self.visual_effects.draw(self.screen)
