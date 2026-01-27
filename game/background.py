"""
Background Module
Handles parallax scrolling backgrounds and visual effects
Dark Horror Night Theme
"""

import pygame
import random
import math
from game.settings import *


class Background:
    """
    Multi-layer parallax scrolling background - Dark Horror Theme
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize the background

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Create stars first (they go behind everything)
        self.stars = []
        self._create_stars()

        # Create background layers
        self.layers = self._create_layers()

        # Fog particles
        self.fog_particles = []
        self._create_fog()

        # Moon position
        self.moon_x = screen_width * 0.8
        self.moon_y = 80

    def _create_layers(self):
        """Create parallax background layers"""
        layers = []

        # Layer 1: Night sky gradient (no parallax)
        sky = pygame.Surface((self.screen_width, self.screen_height))
        self._draw_night_sky(sky)
        layers.append({"surface": sky, "speed": 0, "x": 0, "y": 0})

        # Layer 2: Far dark mountains/hills
        mountains_far = pygame.Surface((self.screen_width * 3, 200), pygame.SRCALPHA)
        self._draw_dark_mountains(mountains_far, (15, 12, 20), 180)
        layers.append(
            {
                "surface": mountains_far,
                "speed": 0.05,
                "x": 0,
                "y": self.screen_height - 380,
            }
        )

        # Layer 3: Mid mountains with dead trees silhouettes
        mountains_mid = pygame.Surface((self.screen_width * 3, 180), pygame.SRCALPHA)
        self._draw_dark_mountains(mountains_mid, (20, 15, 25), 150)
        self._draw_dead_trees_silhouette(mountains_mid, 180)
        layers.append(
            {
                "surface": mountains_mid,
                "speed": 0.1,
                "x": 0,
                "y": self.screen_height - 340,
            }
        )

        # Layer 4: Near dead forest
        forest = pygame.Surface((self.screen_width * 3, 200), pygame.SRCALPHA)
        self._draw_horror_forest(forest)
        layers.append(
            {
                "surface": forest,
                "speed": 0.25,
                "x": 0,
                "y": self.screen_height - 280,
            }
        )

        return layers

    def _draw_night_sky(self, surface):
        """Draw dark night sky gradient"""
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            r = int(NIGHT_SKY_TOP[0] * (1 - ratio) + NIGHT_SKY_BOTTOM[0] * ratio)
            g = int(NIGHT_SKY_TOP[1] * (1 - ratio) + NIGHT_SKY_BOTTOM[1] * ratio)
            b = int(NIGHT_SKY_TOP[2] * (1 - ratio) + NIGHT_SKY_BOTTOM[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (self.screen_width, y))

    def _draw_dark_mountains(self, surface, color, max_height):
        """Draw dark mountain silhouettes"""
        width = surface.get_width()
        height = surface.get_height()

        points = [(0, height)]

        x = 0
        while x < width:
            peak_height = random.randint(int(max_height * 0.4), int(max_height * 0.9))
            peak_x = x + random.randint(80, 200)

            points.append((x, height - random.randint(30, 60)))
            points.append((peak_x, height - peak_height))

            x = peak_x + random.randint(50, 120)

        points.append((width, height - random.randint(30, 60)))
        points.append((width, height))

        if len(points) >= 3:
            pygame.draw.polygon(surface, color, points)

    def _draw_dead_trees_silhouette(self, surface, height):
        """Draw dead tree silhouettes on the mountains"""
        width = surface.get_width()

        x = 0
        while x < width:
            if random.random() < 0.3:
                tree_height = random.randint(40, 80)
                tree_y = height - tree_height - random.randint(20, 60)
                self._draw_dead_tree(surface, x, tree_y, tree_height, (10, 8, 12))

            x += random.randint(60, 150)

    def _draw_dead_tree(self, surface, x, y, height, color):
        """Draw a single dead tree silhouette"""
        # Main trunk
        trunk_width = max(2, height // 15)
        pygame.draw.line(surface, color, (x, y + height), (x, y), trunk_width)

        # Branches
        num_branches = random.randint(3, 6)
        for i in range(num_branches):
            branch_y = y + height * (0.2 + i * 0.15)
            branch_len = random.randint(15, 35)
            direction = 1 if random.random() > 0.5 else -1
            angle = random.uniform(0.3, 0.8)

            end_x = x + direction * branch_len
            end_y = branch_y - branch_len * angle

            pygame.draw.line(
                surface, color, (x, branch_y), (end_x, end_y), max(1, trunk_width - 1)
            )

            # Sub-branches
            if random.random() < 0.5:
                sub_len = branch_len * 0.5
                sub_end_x = end_x + direction * sub_len * 0.5
                sub_end_y = end_y - sub_len * 0.3
                pygame.draw.line(
                    surface, color, (end_x, end_y), (sub_end_x, sub_end_y), 1
                )

    def _draw_horror_forest(self, surface):
        """Draw a horror-style dark forest layer"""
        width = surface.get_width()
        height = surface.get_height()

        x = 0
        while x < width:
            tree_height = random.randint(100, 180)
            tree_color = (
                random.randint(15, 25),
                random.randint(10, 18),
                random.randint(12, 20),
            )
            self._draw_dead_tree(
                surface, x, height - tree_height, tree_height, tree_color
            )
            x += random.randint(30, 80)

    def _create_stars(self):
        """Create twinkling star objects"""
        for _ in range(150):
            star = {
                "x": random.randint(0, self.screen_width),
                "y": random.randint(0, self.screen_height // 2 + 100),
                "size": random.randint(1, 2),
                "brightness": random.uniform(0.3, 1.0),
                "twinkle_speed": random.uniform(0.02, 0.08),
                "twinkle_offset": random.uniform(0, math.pi * 2),
            }
            self.stars.append(star)

    def _create_fog(self):
        """Create fog/mist particles"""
        for _ in range(20):
            fog = {
                "x": random.randint(-200, self.screen_width + 200),
                "y": random.randint(self.screen_height - 300, self.screen_height - 50),
                "width": random.randint(200, 500),
                "height": random.randint(40, 100),
                "speed": random.uniform(0.1, 0.4),
                "alpha": random.randint(15, 40),
            }
            self.fog_particles.append(fog)

    def update(self, camera_x):
        """
        Update background positions

        Args:
            camera_x: Camera x position
        """
        # Update layer positions based on camera
        for layer in self.layers[1:]:  # Skip sky layer
            layer["x"] = -camera_x * layer["speed"]

        # Update fog
        for fog in self.fog_particles:
            fog["x"] -= fog["speed"]
            if fog["x"] + fog["width"] < -camera_x * 0.1 - 200:
                fog["x"] = self.screen_width + random.randint(0, 300)

    def draw(self, surface, camera_x=0):
        """
        Draw the background

        Args:
            surface: Surface to draw on
            camera_x: Camera x position
        """
        # Draw night sky (static)
        surface.blit(self.layers[0]["surface"], (0, 0))

        # Draw stars with twinkling effect
        current_time = pygame.time.get_ticks() / 1000.0
        for star in self.stars:
            twinkle = 0.5 + 0.5 * math.sin(
                current_time * star["twinkle_speed"] * 10 + star["twinkle_offset"]
            )
            brightness = int(star["brightness"] * twinkle * 255)
            color = (brightness, brightness, min(255, brightness + 20))
            pygame.draw.circle(surface, color, (star["x"], star["y"]), star["size"])

        # Draw moon
        self._draw_moon(surface)

        # Draw parallax layers (mountains, trees)
        for layer in self.layers[1:]:
            layer_width = layer["surface"].get_width()
            x = layer["x"] % layer_width
            y = layer.get("y", 0)

            # Draw the layer (twice for seamless scrolling)
            surface.blit(layer["surface"], (x - layer_width, y))
            surface.blit(layer["surface"], (x, y))

        # Draw fog overlay
        self._draw_fog(surface)

    def _draw_moon(self, surface):
        """Draw an eerie moon"""
        # Moon glow
        for i in range(5, 0, -1):
            glow_alpha = 15 - i * 2
            glow_size = 60 + i * 15
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                glow_surf,
                (100, 100, 80, glow_alpha),
                (glow_size, glow_size),
                glow_size,
            )
            surface.blit(
                glow_surf,
                (int(self.moon_x - glow_size), int(self.moon_y - glow_size)),
            )

        # Main moon
        pygame.draw.circle(
            surface, MOON_COLOR, (int(self.moon_x), int(self.moon_y)), 50
        )

        # Moon craters (darker spots)
        crater_color = (180, 180, 160)
        pygame.draw.circle(
            surface, crater_color, (int(self.moon_x - 15), int(self.moon_y - 10)), 8
        )
        pygame.draw.circle(
            surface, crater_color, (int(self.moon_x + 20), int(self.moon_y + 5)), 6
        )
        pygame.draw.circle(
            surface, crater_color, (int(self.moon_x - 5), int(self.moon_y + 20)), 10
        )

    def _draw_fog(self, surface):
        """Draw fog/mist effect"""
        for fog in self.fog_particles:
            fog_surf = pygame.Surface((fog["width"], fog["height"]), pygame.SRCALPHA)

            # Create gradient fog
            for i in range(fog["height"]):
                alpha = int(
                    fog["alpha"]
                    * (1 - abs(i - fog["height"] / 2) / (fog["height"] / 2))
                )
                pygame.draw.line(
                    fog_surf,
                    (FOG_COLOR[0], FOG_COLOR[1], FOG_COLOR[2], alpha),
                    (0, i),
                    (fog["width"], i),
                )

            surface.blit(fog_surf, (int(fog["x"]), int(fog["y"])))


class VisualEffects:
    """
    Visual effects manager for the game - Horror themed
    """

    def __init__(self, screen_width, screen_height):
        """Initialize visual effects"""
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Screen effects
        self.flash_alpha = 0
        self.flash_color = WHITE
        self.vignette = self._create_vignette()

        # Darkness overlay for horror atmosphere
        self.darkness_overlay = self._create_darkness_overlay()

    def _create_vignette(self):
        """Create a stronger vignette overlay for horror effect"""
        vignette = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )

        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        max_dist = math.sqrt(center_x**2 + center_y**2)

        for x in range(0, self.screen_width, 4):
            for y in range(0, self.screen_height, 4):
                dist = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                # Stronger vignette for horror
                alpha = int((dist / max_dist) ** 1.5 * 180)
                pygame.draw.rect(vignette, (0, 0, 0, alpha), (x, y, 4, 4))

        return vignette

    def _create_darkness_overlay(self):
        """Create subtle darkness overlay"""
        overlay = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 10, 30))
        return overlay

    def flash(self, color=WHITE, intensity=100):
        """
        Trigger a screen flash

        Args:
            color: Flash color
            intensity: Flash intensity (0-255)
        """
        self.flash_color = color
        self.flash_alpha = intensity

    def update(self):
        """Update visual effects"""
        # Fade out flash
        if self.flash_alpha > 0:
            self.flash_alpha = max(0, self.flash_alpha - 10)

    def draw(self, surface):
        """Draw visual effects"""
        # Draw subtle darkness overlay
        surface.blit(self.darkness_overlay, (0, 0))

        # Draw flash overlay
        if self.flash_alpha > 0:
            flash_surface = pygame.Surface(
                (self.screen_width, self.screen_height), pygame.SRCALPHA
            )
            flash_surface.fill((*self.flash_color[:3], self.flash_alpha))
            surface.blit(flash_surface, (0, 0))

        # Draw vignette for horror atmosphere
        surface.blit(self.vignette, (0, 0))
