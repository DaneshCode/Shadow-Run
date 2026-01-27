"""
Utility Functions and Helper Classes
Contains reusable functions and classes for the game
"""

import pygame
import math
import random
from game.settings import *


def load_image(path, scale=None, colorkey=None):
    """
    Load an image from file with optional scaling and transparency

    Args:
        path: Path to the image file
        scale: Tuple (width, height) to scale to, or None
        colorkey: Color to use as transparency, or -1 for top-left pixel

    Returns:
        pygame.Surface: The loaded and processed image
    """
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        return image
    except pygame.error as e:
        print(f"Unable to load image: {path}")
        print(e)
        # Return a placeholder surface
        surface = pygame.Surface((32, 32))
        surface.fill(PURPLE)
        return surface


def create_placeholder_surface(width, height, color, border_color=None, border_width=2):
    """
    Create a simple colored surface (used when sprites aren't available)

    Args:
        width: Surface width
        height: Surface height
        color: Fill color
        border_color: Optional border color
        border_width: Border width in pixels

    Returns:
        pygame.Surface: The created surface
    """
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(color)

    if border_color:
        pygame.draw.rect(surface, border_color, surface.get_rect(), border_width)

    return surface


def create_gradient_surface(width, height, color1, color2, vertical=True):
    """
    Create a gradient surface between two colors

    Args:
        width: Surface width
        height: Surface height
        color1: Starting color
        color2: Ending color
        vertical: True for vertical gradient, False for horizontal

    Returns:
        pygame.Surface: The gradient surface
    """
    surface = pygame.Surface((width, height))

    if vertical:
        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    else:
        for x in range(width):
            ratio = x / width
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (x, 0), (x, height))

    return surface


def clamp(value, min_val, max_val):
    """Clamp a value between min and max"""
    return max(min_val, min(value, max_val))


def lerp(start, end, t):
    """Linear interpolation between start and end"""
    return start + (end - start) * t


def distance(pos1, pos2):
    """Calculate distance between two points"""
    return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)


def draw_text(
    surface, text, font, color, x, y, center=True, shadow=False, shadow_color=BLACK
):
    """
    Draw text on a surface with optional centering and shadow

    Args:
        surface: Surface to draw on
        text: Text string to draw
        font: Pygame font object
        color: Text color
        x, y: Position
        center: If True, center text at position
        shadow: If True, draw shadow behind text
        shadow_color: Color of the shadow
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)

    if shadow:
        shadow_surface = font.render(text, True, shadow_color)
        shadow_rect = shadow_surface.get_rect()
        shadow_rect.topleft = (text_rect.x + 2, text_rect.y + 2)
        surface.blit(shadow_surface, shadow_rect)

    surface.blit(text_surface, text_rect)
    return text_rect


class Timer:
    """Simple timer class for tracking time-based events"""

    def __init__(self, duration):
        """
        Initialize timer

        Args:
            duration: Duration in milliseconds
        """
        self.duration = duration
        self.start_time = 0
        self.active = False

    def start(self):
        """Start the timer"""
        self.start_time = pygame.time.get_ticks()
        self.active = True

    def stop(self):
        """Stop the timer"""
        self.active = False

    def is_finished(self):
        """Check if timer has finished"""
        if not self.active:
            return True
        return pygame.time.get_ticks() - self.start_time >= self.duration

    def get_elapsed(self):
        """Get elapsed time in milliseconds"""
        if not self.active:
            return 0
        return pygame.time.get_ticks() - self.start_time

    def get_remaining(self):
        """Get remaining time in milliseconds"""
        if not self.active:
            return 0
        remaining = self.duration - (pygame.time.get_ticks() - self.start_time)
        return max(0, remaining)


class Animation:
    """
    Animation class for handling sprite animations
    """

    def __init__(self, frames, frame_duration=ANIMATION_SPEED, loop=True):
        """
        Initialize animation

        Args:
            frames: List of pygame surfaces (frames)
            frame_duration: Time per frame in milliseconds
            loop: Whether to loop the animation
        """
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.finished = False

    def update(self):
        """Update the animation frame"""
        now = pygame.time.get_ticks()

        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True

    def get_current_frame(self):
        """Get the current animation frame"""
        return self.frames[self.current_frame]

    def reset(self):
        """Reset animation to first frame"""
        self.current_frame = 0
        self.finished = False
        self.last_update = pygame.time.get_ticks()


class ParticleSystem:
    """
    Particle system for visual effects
    """

    def __init__(self):
        self.particles = []

    def emit(
        self,
        x,
        y,
        color,
        count=PARTICLE_COUNT,
        speed=PARTICLE_SPEED,
        lifetime=PARTICLE_LIFETIME,
    ):
        """
        Emit particles from a position

        Args:
            x, y: Emission position
            color: Particle color
            count: Number of particles
            speed: Particle speed
            lifetime: Particle lifetime in ms
        """
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            vel_x = math.cos(angle) * random.uniform(0.5, 1) * speed
            vel_y = math.sin(angle) * random.uniform(0.5, 1) * speed
            size = random.randint(2, 6)

            self.particles.append(
                {
                    "x": x,
                    "y": y,
                    "vel_x": vel_x,
                    "vel_y": vel_y,
                    "size": size,
                    "color": color,
                    "lifetime": lifetime,
                    "birth_time": pygame.time.get_ticks(),
                }
            )

    def update(self):
        """Update all particles"""
        current_time = pygame.time.get_ticks()

        for particle in self.particles[:]:
            # Update position
            particle["x"] += particle["vel_x"]
            particle["y"] += particle["vel_y"]
            particle["vel_y"] += 0.2  # Gravity

            # Remove dead particles
            if current_time - particle["birth_time"] > particle["lifetime"]:
                self.particles.remove(particle)

    def draw(self, surface, camera_offset=(0, 0)):
        """Draw all particles"""
        current_time = pygame.time.get_ticks()

        for particle in self.particles:
            age = current_time - particle["birth_time"]
            alpha = 255 * (1 - age / particle["lifetime"])

            # Calculate screen position
            screen_x = particle["x"] - camera_offset[0]
            screen_y = particle["y"] - camera_offset[1]

            # Create particle surface with alpha
            size = max(1, int(particle["size"] * (1 - age / particle["lifetime"])))
            pygame.draw.circle(
                surface, particle["color"], (int(screen_x), int(screen_y)), size
            )

    def clear(self):
        """Clear all particles"""
        self.particles.clear()
