"""
Camera Module
Contains the Camera class for smooth player following
"""

import pygame
from game.settings import *
from game.utils import lerp


class Camera:
    """
    Camera system for smooth player following with scrolling
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize the camera

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Camera position (top-left corner of view)
        self.x = 0
        self.y = 0

        # Target position for smooth following
        self.target_x = 0
        self.target_y = 0

        # Camera bounds
        self.min_x = 0
        self.min_y = 0
        self.max_x = float("inf")
        self.max_y = float("inf")

        # Smoothing factor (lower = smoother but slower)
        self.smoothing = CAMERA_SMOOTHING

        # Dead zone - area where player can move without camera following
        self.dead_zone_x = CAMERA_SLACK_X
        self.dead_zone_y = 200  # Increased for larger player vertical movement

        # Screen shake
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_timer = 0

    def update(self, target):
        """
        Update camera position to follow target

        Args:
            target: Object to follow (must have rect attribute)
        """
        # Calculate target camera position
        # Keep player in the left-center area of the screen for a runner game
        target_center_x = target.rect.centerx - self.screen_width // 3
        target_center_y = target.rect.centery - self.screen_height // 2

        # Apply dead zone for x
        if abs(target_center_x - self.target_x) > self.dead_zone_x:
            if target_center_x > self.target_x:
                self.target_x = target_center_x - self.dead_zone_x
            else:
                self.target_x = target_center_x + self.dead_zone_x

        # For an endless runner, camera should mostly move forward
        # Prevent camera from going backwards
        self.target_x = max(self.target_x, target_center_x - self.dead_zone_x)

        # Apply dead zone for y
        if abs(target_center_y - self.target_y) > self.dead_zone_y:
            if target_center_y > self.target_y:
                self.target_y = target_center_y - self.dead_zone_y
            else:
                self.target_y = target_center_y + self.dead_zone_y

        # Smooth interpolation
        self.x = lerp(self.x, self.target_x, self.smoothing)
        self.y = lerp(self.y, self.target_y, self.smoothing)

        # Apply bounds
        self.x = max(self.min_x, min(self.x, self.max_x))
        self.y = max(self.min_y, min(self.y, self.max_y))

        # Update screen shake
        self._update_shake()

    def _update_shake(self):
        """Update screen shake effect"""
        if self.shake_duration > 0:
            self.shake_timer += 1
            if self.shake_timer >= self.shake_duration:
                self.shake_duration = 0
                self.shake_intensity = 0
                self.shake_timer = 0

    def shake(self, intensity=5, duration=10):
        """
        Apply screen shake effect

        Args:
            intensity: Maximum shake offset in pixels
            duration: Duration in frames
        """
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_timer = 0

    def get_offset(self):
        """
        Get the camera offset for rendering

        Returns:
            tuple: (x_offset, y_offset)
        """
        offset_x = self.x
        offset_y = self.y

        # Apply shake
        if self.shake_duration > 0:
            import random

            offset_x += random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y += random.randint(-self.shake_intensity, self.shake_intensity)

        return (offset_x, offset_y)

    def reset(self):
        """Reset camera to origin"""
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.shake_duration = 0
        self.shake_intensity = 0
