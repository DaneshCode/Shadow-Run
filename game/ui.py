"""
User Interface Module
Contains menus, HUD, buttons, and UI elements
"""

import pygame
from game.settings import *
from game.utils import draw_text


class Button:
    """
    Interactive button class for menus
    """

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font,
        color=BUTTON_COLOR,
        hover_color=BUTTON_HOVER,
        text_color=BUTTON_TEXT,
    ):
        """
        Initialize a button

        Args:
            x, y: Button position (center)
            width, height: Button dimensions
            text: Button text
            font: Pygame font object
            color: Normal button color
            hover_color: Color when hovered
            text_color: Text color
        """
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)

        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

        self.is_hovered = False
        self.is_pressed = False
        self.was_clicked = False

    def update(self, mouse_pos, mouse_pressed):
        """
        Update button state

        Args:
            mouse_pos: Current mouse position
            mouse_pressed: Mouse button state

        Returns:
            bool: True if button was clicked this frame
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Check for click (press and release)
        clicked = False
        if self.is_hovered and mouse_pressed[0]:
            self.is_pressed = True
        elif self.is_pressed and not mouse_pressed[0]:
            if self.is_hovered:
                clicked = True
            self.is_pressed = False

        self.was_clicked = clicked
        return clicked

    def draw(self, surface):
        """Draw the button"""
        # Determine color
        if self.is_pressed and self.is_hovered:
            current_color = tuple(max(0, c - 30) for c in self.hover_color)
        elif self.is_hovered:
            current_color = self.hover_color
        else:
            current_color = self.color

        # Draw button background
        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)

        # Draw border
        border_color = UI_HIGHLIGHT if self.is_hovered else UI_ACCENT
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=8)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Slight offset when pressed
        if self.is_pressed:
            text_rect.y += 2

        surface.blit(text_surface, text_rect)


class HUD:
    """
    Heads-Up Display showing player stats during gameplay
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize the HUD

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        # Health bar settings
        self.health_bar_width = 200
        self.health_bar_height = 25
        self.health_bar_x = 20
        self.health_bar_y = 20

        # Ammo bar settings
        self.ammo_bar_width = 200
        self.ammo_bar_height = 20
        self.ammo_bar_x = 20
        self.ammo_bar_y = 52  # Right below health bar

        # Score display
        self.score_x = screen_width - 20
        self.score_y = 20

        # Coin display
        self.coin_x = screen_width - 20
        self.coin_y = 60

        # Best score display position
        self.best_score_x = screen_width - 20
        self.best_score_y = 100

    def draw(self, surface, player, difficulty=1, high_score=0):
        """
        Draw the HUD

        Args:
            surface: Surface to draw on
            player: Player object
            difficulty: Current difficulty level
            high_score: Current high score
        """
        # Health bar background
        health_bg_rect = pygame.Rect(
            self.health_bar_x,
            self.health_bar_y,
            self.health_bar_width,
            self.health_bar_height,
        )
        pygame.draw.rect(surface, DARK_GRAY, health_bg_rect, border_radius=5)

        # Health bar fill
        health_ratio = player.health / player.max_health
        health_width = int(self.health_bar_width * health_ratio)

        if health_width > 0:
            health_rect = pygame.Rect(
                self.health_bar_x,
                self.health_bar_y,
                health_width,
                self.health_bar_height,
            )

            # Color based on health level
            if health_ratio > 0.6:
                health_color = UI_SUCCESS
            elif health_ratio > 0.3:
                health_color = ORANGE
            else:
                health_color = UI_DANGER

            pygame.draw.rect(surface, health_color, health_rect, border_radius=5)

        # Health bar border
        pygame.draw.rect(surface, WHITE, health_bg_rect, 2, border_radius=5)

        # Health text
        health_text = f"{int(player.health)}/{player.max_health}"
        draw_text(
            surface,
            health_text,
            self.font_small,
            WHITE,
            self.health_bar_x + self.health_bar_width // 2,
            self.health_bar_y + self.health_bar_height // 2,
            center=True,
            shadow=True,
        )

        # Health label
        draw_text(
            surface,
            "HP",
            self.font_small,
            WHITE,
            self.health_bar_x + self.health_bar_width + 40,
            self.health_bar_y + self.health_bar_height // 2,
            center=True,
            shadow=True,
        )

        # Ammo bar background
        ammo_bg_rect = pygame.Rect(
            self.ammo_bar_x,
            self.ammo_bar_y,
            self.ammo_bar_width,
            self.ammo_bar_height,
        )
        pygame.draw.rect(surface, AMMO_EMPTY_COLOR, ammo_bg_rect, border_radius=4)

        # Ammo bar fill
        ammo_ratio = player.ammo / player.max_ammo
        ammo_width = int(self.ammo_bar_width * ammo_ratio)

        if ammo_width > 0:
            ammo_rect = pygame.Rect(
                self.ammo_bar_x,
                self.ammo_bar_y,
                ammo_width,
                self.ammo_bar_height,
            )
            pygame.draw.rect(surface, AMMO_COLOR, ammo_rect, border_radius=4)

        # Ammo bar border
        pygame.draw.rect(surface, WHITE, ammo_bg_rect, 2, border_radius=4)

        # Ammo text
        ammo_text = f"{player.ammo}/{player.max_ammo}"
        draw_text(
            surface,
            ammo_text,
            self.font_small,
            WHITE,
            self.ammo_bar_x + self.ammo_bar_width // 2,
            self.ammo_bar_y + self.ammo_bar_height // 2,
            center=True,
            shadow=True,
        )

        # Ammo label with bullet icon
        draw_text(
            surface,
            "AMMO",
            self.font_small,
            AMMO_COLOR,
            self.ammo_bar_x + self.ammo_bar_width + 40,
            self.ammo_bar_y + self.ammo_bar_height // 2,
            center=True,
            shadow=True,
        )

        # Score
        score_text = f"SCORE: {player.score}"
        score_surface = self.font_medium.render(score_text, True, COIN_COLOR)
        surface.blit(
            score_surface, (self.score_x - score_surface.get_width(), self.score_y)
        )

        # Coins
        coin_text = f"COINS: {player.coins}"
        coin_surface = self.font_medium.render(coin_text, True, YELLOW)
        surface.blit(
            coin_surface, (self.coin_x - coin_surface.get_width(), self.coin_y)
        )

        # Best score display
        best_text = f"BEST SCORE: {high_score}"
        best_surface = self.font_small.render(best_text, True, UI_HIGHLIGHT)
        surface.blit(
            best_surface,
            (self.best_score_x - best_surface.get_width(), self.best_score_y),
        )

        # High score (if beating it)
        if player.score > high_score and high_score > 0:
            new_record_text = "NEW RECORD!"
            draw_text(
                surface,
                new_record_text,
                self.font_medium,
                YELLOW,
                self.screen_width // 2,
                55,
                center=True,
                shadow=True,
            )

        # Gravity indicator
        gravity_y = 90
        if hasattr(player, "gravity_flipped"):
            gravity_text = "CEILING" if player.gravity_flipped else "GROUND"
            gravity_color = PURPLE if player.gravity_flipped else UI_SUCCESS
            draw_text(
                surface,
                gravity_text,
                self.font_small,
                gravity_color,
                self.health_bar_x + self.health_bar_width // 2,
                gravity_y,
                center=True,
                shadow=True,
            )


class MainMenu:
    """
    Main menu screen
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize the main menu

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Fonts
        self.font_title = pygame.font.Font(None, 96)
        self.font_subtitle = pygame.font.Font(None, 36)
        self.font_button = pygame.font.Font(None, 30)

        # Buttons
        button_width = 250
        button_height = 60
        button_x = screen_width // 2

        self.buttons = {
            "play": Button(
                button_x, 350, button_width, button_height, "PLAY", self.font_button
            ),
            "leaderboard": Button(
                button_x,
                430,
                button_width,
                button_height,
                "LEADERBOARD",
                self.font_button,
            ),
            "settings": Button(
                button_x, 510, button_width, button_height, "SETTINGS", self.font_button
            ),
            "quit": Button(
                button_x,
                590,
                button_width,
                button_height,
                "QUIT",
                self.font_button,
                color=(100, 60, 60),
                hover_color=(140, 80, 80),
            ),
        }

        # Animation
        self.title_offset = 0
        self.animation_timer = 0

        # High score display
        self.high_score = 0

    def set_high_score(self, score):
        """Set the high score to display"""
        self.high_score = score

    def update(self, mouse_pos, mouse_pressed):
        """
        Update menu state

        Args:
            mouse_pos: Mouse position
            mouse_pressed: Mouse button state

        Returns:
            str or None: Action if button clicked
        """
        # Update animation
        self.animation_timer += 0.05
        self.title_offset = pygame.math.Vector2(0, 0)

        # Update buttons
        for name, button in self.buttons.items():
            if button.update(mouse_pos, mouse_pressed):
                return name

        return None

    def draw(self, surface):
        """Draw the main menu"""
        # Background
        surface.fill(MENU_BG)

        # Draw decorative elements
        self._draw_background_decorations(surface)

        # Title
        title_y = 150 + int(
            pygame.math.Vector2(0, 5).y
            * abs(
                pygame.math.Vector2(0, 1).y
                * (1 + 0.1 * abs(self.animation_timer % 2 - 1))
            )
        )

        draw_text(
            surface,
            "SHADOW RUNNER",
            self.font_title,
            UI_HIGHLIGHT,
            self.screen_width // 2,
            title_y,
            center=True,
            shadow=True,
        )

        # Subtitle
        draw_text(
            surface,
            "Escape the Darkness...",
            self.font_subtitle,
            LIGHT_GRAY,
            self.screen_width // 2,
            220,
            center=True,
        )

        # High Score display
        if self.high_score > 0:
            draw_text(
                surface,
                f" BEST SCORE: {self.high_score} ",
                self.font_subtitle,
                YELLOW,
                self.screen_width // 2,
                265,
                center=True,
                shadow=True,
            )

        # Draw buttons
        for button in self.buttons.values():
            button.draw(surface)

        # Instructions
        draw_text(
            surface,
            "Auto-Run • SPACE to jump • Click to shoot (Limited Ammo!)",
            self.font_subtitle,
            GRAY,
            self.screen_width // 2,
            self.screen_height - 50,
            center=True,
        )

    def _draw_background_decorations(self, surface):
        """Draw animated background decorations"""
        import math

        # Floating particles
        for i in range(20):
            x = (i * 73 + int(self.animation_timer * 20)) % self.screen_width
            y = (i * 47 + int(self.animation_timer * 10)) % self.screen_height
            size = 2 + (i % 3)
            alpha = 50 + (i * 7) % 100

            pygame.draw.circle(surface, (100, 150, 200), (x, y), size)


class PauseMenu:
    """
    Pause menu overlay
    """

    def __init__(self, screen_width, screen_height):
        """Initialize pause menu"""
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 42)
        self.font_option = pygame.font.Font(None, 32)

        button_width = 220
        button_height = 55
        button_x = screen_width // 2

        self.buttons = {
            "resume": Button(
                button_x, 420, button_width, button_height, "RESUME", self.font_button
            ),
            "restart": Button(
                button_x, 490, button_width, button_height, "RESTART", self.font_button
            ),
            "menu": Button(
                button_x,
                560,
                button_width,
                button_height,
                "MAIN MENU",
                self.font_button,
            ),
        }

        # Volume controls
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME

        # Volume control buttons
        self.music_down = Button(button_x - 100, 280, 40, 35, "-", self.font_option)
        self.music_up = Button(button_x + 100, 280, 40, 35, "+", self.font_option)

        self.sfx_down = Button(button_x - 100, 340, 40, 35, "-", self.font_option)
        self.sfx_up = Button(button_x + 100, 340, 40, 35, "+", self.font_option)

        # Semi-transparent overlay
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

    def update(self, mouse_pos, mouse_pressed):
        """Update pause menu"""
        for name, button in self.buttons.items():
            if button.update(mouse_pos, mouse_pressed):
                return name

        # Volume controls
        if self.music_down.update(mouse_pos, mouse_pressed):
            self.music_volume = max(0, self.music_volume - 0.1)
        if self.music_up.update(mouse_pos, mouse_pressed):
            self.music_volume = min(1, self.music_volume + 0.1)

        if self.sfx_down.update(mouse_pos, mouse_pressed):
            self.sfx_volume = max(0, self.sfx_volume - 0.1)
        if self.sfx_up.update(mouse_pos, mouse_pressed):
            self.sfx_volume = min(1, self.sfx_volume + 0.1)

        return None

    def draw(self, surface):
        """Draw pause menu"""
        # Overlay
        surface.blit(self.overlay, (0, 0))

        # Title
        draw_text(
            surface,
            "PAUSED",
            self.font_title,
            WHITE,
            self.screen_width // 2,
            180,
            center=True,
            shadow=True,
        )

        # Music volume
        draw_text(
            surface,
            "Music:",
            self.font_option,
            WHITE,
            self.screen_width // 2 - 150,
            280,
            center=True,
        )
        self.music_down.draw(surface)
        self.music_up.draw(surface)

        # Music volume bar
        bar_rect = pygame.Rect(self.screen_width // 2 - 55, 270, 110, 20)
        pygame.draw.rect(surface, DARK_GRAY, bar_rect, border_radius=5)
        fill_width = int(110 * self.music_volume)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.screen_width // 2 - 55, 270, fill_width, 20)
            pygame.draw.rect(surface, UI_ACCENT, fill_rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, bar_rect, 2, border_radius=5)

        draw_text(
            surface,
            f"{int(self.music_volume * 100)}%",
            self.font_option,
            WHITE,
            self.screen_width // 2,
            280,
            center=True,
        )

        # SFX volume
        draw_text(
            surface,
            "SFX:",
            self.font_option,
            WHITE,
            self.screen_width // 2 - 150,
            340,
            center=True,
        )
        self.sfx_down.draw(surface)
        self.sfx_up.draw(surface)

        # SFX volume bar
        bar_rect = pygame.Rect(self.screen_width // 2 - 55, 330, 110, 20)
        pygame.draw.rect(surface, DARK_GRAY, bar_rect, border_radius=5)
        fill_width = int(110 * self.sfx_volume)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.screen_width // 2 - 55, 330, fill_width, 20)
            pygame.draw.rect(surface, UI_ACCENT, fill_rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, bar_rect, 2, border_radius=5)

        draw_text(
            surface,
            f"{int(self.sfx_volume * 100)}%",
            self.font_option,
            WHITE,
            self.screen_width // 2,
            340,
            center=True,
        )

        # Buttons
        for button in self.buttons.values():
            button.draw(surface)


class GameOverScreen:
    """
    Game over screen with score display
    """

    def __init__(self, screen_width, screen_height):
        """Initialize game over screen"""
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.font_title = pygame.font.Font(None, 96)
        self.font_score = pygame.font.Font(None, 48)
        self.font_button = pygame.font.Font(None, 30)

        button_width = 220
        button_height = 55
        button_x = screen_width // 2

        self.buttons = {
            "restart": Button(
                button_x,
                480,
                button_width,
                button_height,
                "PLAY AGAIN",
                self.font_button,
            ),
            "leaderboard": Button(
                button_x,
                550,
                button_width,
                button_height,
                "LEADERBOARD",
                self.font_button,
            ),
            "menu": Button(
                button_x,
                620,
                button_width,
                button_height,
                "MAIN MENU",
                self.font_button,
            ),
        }

        # Overlay
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 200))

        # Score data
        self.final_score = 0
        self.high_score = 0
        self.is_new_record = False
        self.coins = 0

    def set_data(self, score, high_score, coins):
        """Set the game over data"""
        self.final_score = score if score is not None else 0
        self.high_score = high_score if high_score is not None else 0
        self.is_new_record = self.final_score > self.high_score
        self.coins = coins if coins is not None else 0

    def update(self, mouse_pos, mouse_pressed):
        """Update game over screen"""
        for name, button in self.buttons.items():
            if button.update(mouse_pos, mouse_pressed):
                return name
        return None

    def draw(self, surface):
        """Draw game over screen"""
        # Overlay
        surface.blit(self.overlay, (0, 0))

        # Title
        draw_text(
            surface,
            "GAME OVER",
            self.font_title,
            UI_DANGER,
            self.screen_width // 2,
            120,
            center=True,
            shadow=True,
        )

        # New record indicator
        if self.is_new_record:
            draw_text(
                surface,
                " NEW HIGH SCORE! ",
                self.font_score,
                YELLOW,
                self.screen_width // 2,
                200,
                center=True,
                shadow=True,
            )

        # Stats
        stats_y = 260
        stats_spacing = 45

        draw_text(
            surface,
            f"Final Score: {int(self.final_score)}",
            self.font_score,
            WHITE,
            self.screen_width // 2,
            stats_y,
            center=True,
            shadow=True,
        )

        draw_text(
            surface,
            f"Coins Collected: {int(self.coins)}",
            self.font_score,
            COIN_COLOR,
            self.screen_width // 2,
            stats_y + stats_spacing,
            center=True,
        )

        # Show best score with emphasis
        best_score = max(int(self.final_score), int(self.high_score))
        draw_text(
            surface,
            f" BEST SCORE: {best_score} ",
            self.font_score,
            YELLOW,
            self.screen_width // 2,
            stats_y + stats_spacing * 2,
            center=True,
            shadow=True,
        )

        # Buttons
        for button in self.buttons.values():
            button.draw(surface)


class LeaderboardScreen:
    """
    Leaderboard display screen
    """

    def __init__(self, screen_width, screen_height):
        """Initialize leaderboard screen"""
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.font_title = pygame.font.Font(None, 72)
        self.font_entry = pygame.font.Font(None, 36)
        self.font_button = pygame.font.Font(None, 42)

        self.back_button = Button(
            screen_width // 2, screen_height - 80, 180, 50, "BACK", self.font_button
        )

        self.entries = []

    def set_entries(self, entries):
        """
        Set leaderboard entries

        Args:
            entries: List of (name, score) tuples
        """
        self.entries = entries[:MAX_LEADERBOARD_ENTRIES]

    def update(self, mouse_pos, mouse_pressed):
        """Update leaderboard screen"""
        if self.back_button.update(mouse_pos, mouse_pressed):
            return "back"
        return None

    def draw(self, surface):
        """Draw leaderboard screen"""
        surface.fill(MENU_BG)

        # Title
        draw_text(
            surface,
            "LEADERBOARD",
            self.font_title,
            UI_HIGHLIGHT,
            self.screen_width // 2,
            80,
            center=True,
            shadow=True,
        )

        # Column headers
        headers_y = 150
        draw_text(surface, "RANK", self.font_entry, GRAY, 150, headers_y, center=True)
        draw_text(surface, "PLAYER", self.font_entry, GRAY, 400, headers_y, center=True)
        draw_text(surface, "SCORE", self.font_entry, GRAY, 700, headers_y, center=True)

        # Separator line
        pygame.draw.line(
            surface,
            GRAY,
            (100, headers_y + 20),
            (self.screen_width - 100, headers_y + 20),
            2,
        )

        # Entries
        if self.entries:
            entry_y = 200
            entry_spacing = 45

            for i, entry in enumerate(self.entries):
                rank = i + 1
                name = entry.get("name", "Player")
                score = entry.get("score", 0)

                # Highlight top 3
                if rank == 1:
                    color = YELLOW
                elif rank == 2:
                    color = LIGHT_GRAY
                elif rank == 3:
                    color = (205, 127, 50)  # Bronze
                else:
                    color = WHITE

                y = entry_y + (i * entry_spacing)

                draw_text(
                    surface, f"#{rank}", self.font_entry, color, 150, y, center=True
                )
                draw_text(surface, name, self.font_entry, color, 400, y, center=True)
                draw_text(
                    surface, str(score), self.font_entry, color, 700, y, center=True
                )
        else:
            draw_text(
                surface,
                "No scores yet!",
                self.font_entry,
                GRAY,
                self.screen_width // 2,
                300,
                center=True,
            )
            draw_text(
                surface,
                "Play a game to set a high score",
                self.font_entry,
                GRAY,
                self.screen_width // 2,
                350,
                center=True,
            )

        # Back button
        self.back_button.draw(surface)


class SettingsScreen:
    """
    Settings/options screen
    """

    def __init__(self, screen_width, screen_height):
        """Initialize settings screen"""
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.font_title = pygame.font.Font(None, 72)
        self.font_option = pygame.font.Font(None, 36)
        self.font_button = pygame.font.Font(None, 42)

        self.back_button = Button(
            screen_width // 2, screen_height - 80, 180, 50, "BACK", self.font_button
        )

        # Settings values
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME

        # Volume sliders (simplified as buttons for now)
        self.music_down = Button(450, 250, 50, 40, "-", self.font_option)
        self.music_up = Button(750, 250, 50, 40, "+", self.font_option)

        self.sfx_down = Button(450, 320, 50, 40, "-", self.font_option)
        self.sfx_up = Button(750, 320, 50, 40, "+", self.font_option)

    def update(self, mouse_pos, mouse_pressed):
        """Update settings screen"""
        if self.back_button.update(mouse_pos, mouse_pressed):
            return "back"

        # Volume controls
        if self.music_down.update(mouse_pos, mouse_pressed):
            self.music_volume = max(0, self.music_volume - 0.1)
        if self.music_up.update(mouse_pos, mouse_pressed):
            self.music_volume = min(1, self.music_volume + 0.1)

        if self.sfx_down.update(mouse_pos, mouse_pressed):
            self.sfx_volume = max(0, self.sfx_volume - 0.1)
        if self.sfx_up.update(mouse_pos, mouse_pressed):
            self.sfx_volume = min(1, self.sfx_volume + 0.1)

        return None

    def draw(self, surface):
        """Draw settings screen"""
        surface.fill(MENU_BG)

        # Title
        draw_text(
            surface,
            "SETTINGS",
            self.font_title,
            UI_HIGHLIGHT,
            self.screen_width // 2,
            80,
            center=True,
            shadow=True,
        )

        # Music volume
        draw_text(
            surface, "Music Volume:", self.font_option, WHITE, 250, 250, center=True
        )
        self.music_down.draw(surface)
        self.music_up.draw(surface)

        # Volume bar
        bar_rect = pygame.Rect(510, 240, 220, 20)
        pygame.draw.rect(surface, DARK_GRAY, bar_rect, border_radius=5)
        fill_width = int(220 * self.music_volume)
        if fill_width > 0:
            fill_rect = pygame.Rect(510, 240, fill_width, 20)
            pygame.draw.rect(surface, UI_ACCENT, fill_rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, bar_rect, 2, border_radius=5)

        draw_text(
            surface,
            f"{int(self.music_volume * 100)}%",
            self.font_option,
            WHITE,
            600,
            250,
            center=True,
        )

        # SFX volume
        draw_text(
            surface, "SFX Volume:", self.font_option, WHITE, 250, 320, center=True
        )
        self.sfx_down.draw(surface)
        self.sfx_up.draw(surface)

        # Volume bar
        bar_rect = pygame.Rect(510, 310, 220, 20)
        pygame.draw.rect(surface, DARK_GRAY, bar_rect, border_radius=5)
        fill_width = int(220 * self.sfx_volume)
        if fill_width > 0:
            fill_rect = pygame.Rect(510, 310, fill_width, 20)
            pygame.draw.rect(surface, UI_ACCENT, fill_rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, bar_rect, 2, border_radius=5)

        draw_text(
            surface,
            f"{int(self.sfx_volume * 100)}%",
            self.font_option,
            WHITE,
            600,
            320,
            center=True,
        )

        # Controls info
        controls_y = 420
        draw_text(
            surface,
            "CONTROLS",
            self.font_option,
            UI_HIGHLIGHT,
            self.screen_width // 2,
            controls_y,
            center=True,
        )

        controls = [
            "Jump: SPACE / W / UP Arrow",
            "Flip Gravity: SHIFT / S / DOWN / F",
            "Shoot: LEFT CLICK / X / Z / CTRL",
            "Pause: ESC or P",
        ]

        for i, control in enumerate(controls):
            draw_text(
                surface,
                control,
                self.font_option,
                LIGHT_GRAY,
                self.screen_width // 2,
                controls_y + 40 + i * 35,
                center=True,
            )

        # Back button
        self.back_button.draw(surface)


class TutorialScreen:
    """
    Tutorial screen showing game controls before starting
    """

    def __init__(self, screen_width, screen_height):
        """Initialize tutorial screen"""
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.font_title = pygame.font.Font(None, 72)
        self.font_subtitle = pygame.font.Font(None, 42)
        self.font_control = pygame.font.Font(None, 36)
        self.font_hint = pygame.font.Font(None, 32)

        # Background overlay
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.overlay.fill((10, 5, 15, 240))

        # Animation timer for blinking text
        self.blink_timer = 0
        self.show_prompt = True

    def update(self):
        """Update tutorial screen animations"""
        self.blink_timer += 1
        if self.blink_timer >= 40:
            self.blink_timer = 0
            self.show_prompt = not self.show_prompt

    def draw(self, surface):
        """Draw the tutorial screen"""
        # Dark overlay
        surface.blit(self.overlay, (0, 0))

        # Title
        draw_text(
            surface,
            "HOW TO PLAY",
            self.font_title,
            UI_HIGHLIGHT,
            self.screen_width // 2,
            80,
            center=True,
            shadow=True,
        )

        # Subtitle
        draw_text(
            surface,
            "Survive the darkness...",
            self.font_subtitle,
            LIGHT_GRAY,
            self.screen_width // 2,
            140,
            center=True,
        )

        # Controls section
        controls_y = 200
        controls = [
            ("JUMP", "Space  /  W  /  Up Arrow", UI_ACCENT),
            ("FLIP GRAVITY", "Shift  /  S  /  Down  /  F", PURPLE),
            ("SHOOT", "Click  /  X  /  Z  /  Ctrl", BULLET_COLOR),
            ("PAUSE", "Escape  or  P", LIGHT_GRAY),
        ]

        for i, (action, keys, color) in enumerate(controls):
            y = controls_y + i * 60

            # Action name
            draw_text(
                surface,
                action,
                self.font_control,
                color,
                self.screen_width // 2 - 140,
                y,
                center=True,
            )

            # Key binding
            draw_text(
                surface,
                keys,
                self.font_control,
                WHITE,
                self.screen_width // 2 + 100,
                y,
                center=True,
            )

        # Tips
        tips_y = 480
        tips = [
            "FLIP GRAVITY to switch between ground and ceiling!",
            "Enemies spawn on both surfaces • Time your flips wisely",
            "You have 5 bullets • Ammo regenerates over time",
        ]

        for i, tip in enumerate(tips):
            draw_text(
                surface,
                tip,
                self.font_hint,
                LIGHT_GRAY,
                self.screen_width // 2,
                tips_y + i * 30,
                center=True,
            )

        # Blinking prompt
        if self.show_prompt:
            draw_text(
                surface,
                "Press any key to start...",
                self.font_subtitle,
                WHITE,
                self.screen_width // 2,
                self.screen_height - 60,
                center=True,
                shadow=True,
            )
