"""
Sound Manager Module
Handles all game audio including music and sound effects
"""

import pygame
import os
from game.settings import *


class SoundManager:
    """
    Manages all game audio
    """

    def __init__(self):
        """Initialize the sound manager"""
        # Initialize pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Volume settings
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME

        # Sound effect cache
        self.sounds = {}

        # Music state
        self.current_music = None
        self.music_paused = False

        # Load sounds
        self._load_sounds()

    def _load_sounds(self):
        """Load all sound effects"""
        # Define sound effects to load
        sound_files = {
            "jump": "assets/sounds/jump.wav",
            "coin": "assets/sounds/coin.wav",
            "hurt": "assets/sounds/hurt.wav",
            "death": "assets/sounds/death.wav",
            "powerup": "assets/sounds/powerup.wav",
            "click": "assets/sounds/click.wav",
            "enemy_death": "assets/sounds/enemy_death.wav",
        }

        for name, path in sound_files.items():
            self._load_sound(name, path)

    def _load_sound(self, name, path):
        """
        Load a single sound effect

        Args:
            name: Name to reference the sound
            path: Path to the sound file
        """
        if os.path.exists(path):
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.sfx_volume)
                self.sounds[name] = sound
            except pygame.error as e:
                print(f"Could not load sound {path}: {e}")
                self.sounds[name] = None
        else:
            # Create a silent placeholder
            self.sounds[name] = None

    def play_sound(self, name, volume=None):
        """
        Play a sound effect

        Args:
            name: Name of the sound to play
            volume: Optional volume override (0.0 to 1.0)
        """
        if name in self.sounds and self.sounds[name]:
            sound = self.sounds[name]
            if volume is not None:
                sound.set_volume(volume * self.sfx_volume)
            else:
                sound.set_volume(self.sfx_volume)
            sound.play()

    def pause_music(self):
        """Pause the current music"""
        pygame.mixer.music.pause()
        self.music_paused = True

    def unpause_music(self):
        """Unpause the current music"""
        pygame.mixer.music.unpause()
        self.music_paused = False

    def set_music_volume(self, volume):
        """
        Set music volume

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """
        Set sound effects volume

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))

        # Update all loaded sounds
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.sfx_volume)

    def create_procedural_sounds(self):
        """
        Create simple procedural sound effects when no audio files exist
        This provides basic audio feedback without external files
        """
        import array
        import math

        sample_rate = 44100

        # Jump sound (rising tone)
        duration = 0.15
        samples = int(sample_rate * duration)
        jump_array = array.array("h")
        for i in range(samples):
            t = i / sample_rate
            freq = 300 + (i / samples) * 400
            value = int(10000 * math.sin(2 * math.pi * freq * t) * (1 - t / duration))
            jump_array.append(value)

        try:
            self.sounds["jump"] = pygame.mixer.Sound(buffer=jump_array)
            self.sounds["jump"].set_volume(self.sfx_volume * 0.5)
        except:
            pass

        # Coin sound (pleasant ding)
        duration = 0.2
        samples = int(sample_rate * duration)
        coin_array = array.array("h")
        for i in range(samples):
            t = i / sample_rate
            freq = 800
            value = int(8000 * math.sin(2 * math.pi * freq * t) * math.exp(-t * 10))
            coin_array.append(value)

        try:
            self.sounds["coin"] = pygame.mixer.Sound(buffer=coin_array)
            self.sounds["coin"].set_volume(self.sfx_volume * 0.4)
        except:
            pass

        # Hurt sound (low buzz)
        duration = 0.3
        samples = int(sample_rate * duration)
        hurt_array = array.array("h")
        for i in range(samples):
            t = i / sample_rate
            freq = 150 + math.sin(t * 50) * 50
            value = int(8000 * math.sin(2 * math.pi * freq * t) * (1 - t / duration))
            hurt_array.append(value)

        try:
            self.sounds["hurt"] = pygame.mixer.Sound(buffer=hurt_array)
            self.sounds["hurt"].set_volume(self.sfx_volume * 0.5)
        except:
            pass

        # Click sound
        duration = 0.05
        samples = int(sample_rate * duration)
        click_array = array.array("h")
        for i in range(samples):
            t = i / sample_rate
            value = int(5000 * math.sin(2 * math.pi * 600 * t) * (1 - t / duration))
            click_array.append(value)

        try:
            self.sounds["click"] = pygame.mixer.Sound(buffer=click_array)
            self.sounds["click"].set_volume(self.sfx_volume * 0.3)
        except:
            pass

        # Shoot sound (sharp pew)
        duration = 0.1
        samples = int(sample_rate * duration)
        shoot_array = array.array("h")
        for i in range(samples):
            t = i / sample_rate
            freq = 500 - (i / samples) * 300
            value = int(8000 * math.sin(2 * math.pi * freq * t) * (1 - t / duration))
            shoot_array.append(value)

        try:
            self.sounds["shoot"] = pygame.mixer.Sound(buffer=shoot_array)
            self.sounds["shoot"].set_volume(self.sfx_volume * 0.4)
        except:
            pass

        # Hit sound (impact thud)
        duration = 0.08
        samples = int(sample_rate * duration)
        hit_array = array.array("h")
        for i in range(samples):
            t = i / sample_rate
            freq = 200
            noise = int((i % 7 - 3) * 500)
            value = (
                int(6000 * math.sin(2 * math.pi * freq * t) * (1 - t / duration))
                + noise
            )
            hit_array.append(max(-32767, min(32767, value)))

        try:
            self.sounds["hit"] = pygame.mixer.Sound(buffer=hit_array)
            self.sounds["hit"].set_volume(self.sfx_volume * 0.4)
        except:
            pass

        # Enemy death sound
        duration = 0.25
        samples = int(sample_rate * duration)
        death_array = array.array("h")
        for i in range(samples):
            t = i / sample_rate
            freq = 400 - (i / samples) * 300
            value = int(7000 * math.sin(2 * math.pi * freq * t) * (1 - t / duration))
            death_array.append(value)

        try:
            self.sounds["enemy_death"] = pygame.mixer.Sound(buffer=death_array)
            self.sounds["enemy_death"].set_volume(self.sfx_volume * 0.4)
        except:
            pass

        # Death sound (low descending)
        duration = 0.5
        samples = int(sample_rate * duration)
        player_death_array = array.array("h")
        for i in range(samples):
            t = i / sample_rate
            freq = 300 - (i / samples) * 200
            value = int(8000 * math.sin(2 * math.pi * freq * t) * (1 - t / duration))
            player_death_array.append(value)

        try:
            self.sounds["death"] = pygame.mixer.Sound(buffer=player_death_array)
            self.sounds["death"].set_volume(self.sfx_volume * 0.5)
        except:
            pass

        # Powerup sound (rising melody)
        duration = 0.3
        samples = int(sample_rate * duration)
        powerup_array = array.array("h")
        for i in range(samples):
            t = i / sample_rate
            freq = 400 + (i / samples) * 600
            value = int(7000 * math.sin(2 * math.pi * freq * t) * math.exp(-t * 3))
            powerup_array.append(value)

        try:
            self.sounds["powerup"] = pygame.mixer.Sound(buffer=powerup_array)
            self.sounds["powerup"].set_volume(self.sfx_volume * 0.4)
        except:
            pass

    def create_procedural_music(self):
        """
        Create procedural background music for the game
        This generates a dark ambient loop that plays continuously
        """
        import array
        import math
        import random
        import tempfile
        import wave

        sample_rate = 44100
        duration = 8  # 8 second loop
        samples = int(sample_rate * duration)

        # Create stereo audio data
        audio_data = []

        for i in range(samples):
            t = i / sample_rate
            loop_t = t / duration  # 0 to 1 over the loop

            # Base drone (low frequency)
            drone = 0.3 * math.sin(2 * math.pi * 55 * t)
            drone += 0.2 * math.sin(2 * math.pi * 82.5 * t)

            # Eerie pad (slow modulated tone)
            mod = 0.5 + 0.5 * math.sin(2 * math.pi * 0.1 * t)
            pad = 0.15 * math.sin(2 * math.pi * 110 * t) * mod
            pad += 0.1 * math.sin(2 * math.pi * 165 * t) * (1 - mod)

            # Heartbeat-like pulse
            pulse_freq = 1.2  # beats per second
            pulse_phase = (t * pulse_freq) % 1
            if pulse_phase < 0.1:
                pulse = (
                    0.4 * math.exp(-pulse_phase * 30) * math.sin(2 * math.pi * 40 * t)
                )
            elif pulse_phase < 0.25 and pulse_phase > 0.15:
                pulse = (
                    0.25
                    * math.exp(-(pulse_phase - 0.15) * 30)
                    * math.sin(2 * math.pi * 35 * t)
                )
            else:
                pulse = 0

            # Subtle high frequency shimmer
            shimmer = (
                0.05
                * math.sin(2 * math.pi * 880 * t)
                * (0.3 + 0.7 * math.sin(2 * math.pi * 0.5 * t))
            )

            # Combine all elements
            sample = drone + pad + pulse + shimmer

            # Apply soft envelope at loop boundaries for seamless looping
            if loop_t < 0.05:
                sample *= loop_t / 0.05
            elif loop_t > 0.95:
                sample *= (1 - loop_t) / 0.05

            # Convert to 16-bit integer
            value = int(sample * 16000)
            value = max(-32767, min(32767, value))
            audio_data.append(value)

        # Create a temporary WAV file for the music
        try:
            temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp_path = temp_file.name
            temp_file.close()

            # Write WAV file
            with wave.open(temp_path, "w") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(array.array("h", audio_data).tobytes())

            # Load and play the music
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # Loop infinitely
            self.current_music = "procedural"
            self.music_paused = False

        except Exception as e:
            print(f"Could not create procedural music: {e}")
