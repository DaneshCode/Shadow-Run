"""
Sound Manager Module
Handles all game audio including music and sound effects
Professional AAA-style dynamic audio mixing system
"""

import pygame
import os
import math
from game.settings import *


class AmbientMixer:
    """
    Professional dynamic ambient audio mixer
    Handles crossfading and layered audio like AAA games (Dead Space, Limbo, Inside)
    """

    def __init__(self, sound_manager):
        self.sound_manager = sound_manager

        # Audio channels for layered mixing
        self.horror_channel = None
        self.pond_channel = None

        # Current volume levels for each layer
        self.horror_volume = 0.0
        self.pond_volume = 0.0

        # Target volumes for smooth transitions
        self.horror_target = 0.5
        self.pond_target = 0.3

        # Transition speed (lower = smoother)
        self.transition_speed = 0.02

        # Loaded sounds
        self.horror_sound = None
        self.pond_sound = None

        # State
        self.is_playing = False
        self.intensity = 0.5  # 0.0 = calm, 1.0 = intense

        # Dynamic mixing parameters
        self.base_horror_volume = 0.4
        self.base_pond_volume = 0.35

    def load_ambient_tracks(self):
        """Load ambient audio tracks"""
        if not self.sound_manager.audio_available:
            return

        audio_path = "assets/audio"

        # Load horror ambience (OGG format - compressed)
        horror_path = os.path.join(audio_path, "horror-ambience.ogg")
        if os.path.exists(horror_path):
            try:
                self.horror_sound = pygame.mixer.Sound(horror_path)
                print(f"[OK] Loaded: {horror_path}")
            except pygame.error as e:
                print(f"[ERROR] Could not load {horror_path}: {e}")

        # Load pond ambience (OGG format - compressed)
        pond_path = os.path.join(audio_path, "pond-ambience.ogg")
        if os.path.exists(pond_path):
            try:
                self.pond_sound = pygame.mixer.Sound(pond_path)
                print(f"[OK] Loaded: {pond_path}")
            except pygame.error as e:
                print(f"[ERROR] Could not load {pond_path}: {e}")

    def start_ambient_mix(self):
        """Start playing the layered ambient mix"""
        if not self.sound_manager.audio_available:
            return

        if not self.horror_sound and not self.pond_sound:
            return

        # Reserve channels for ambient audio
        pygame.mixer.set_num_channels(16)

        # Start horror ambience on channel 0 (looping)
        if self.horror_sound:
            self.horror_channel = pygame.mixer.Channel(0)
            self.horror_sound.set_volume(0)
            self.horror_channel.play(self.horror_sound, loops=-1)

        # Start pond ambience on channel 1 (looping)
        if self.pond_sound:
            self.pond_channel = pygame.mixer.Channel(1)
            self.pond_sound.set_volume(0)
            self.pond_channel.play(self.pond_sound, loops=-1)

        self.is_playing = True

        # Set initial targets
        self.horror_target = self.base_horror_volume
        self.pond_target = self.base_pond_volume

    def update(self, dt=1 / 60):
        """
        Update the ambient mix - call this every frame
        Smoothly transitions volumes for professional sound
        """
        if not self.is_playing:
            return

        master_volume = self.sound_manager.music_volume

        # Smooth volume transitions (exponential interpolation for natural feel)
        self.horror_volume = self._lerp(
            self.horror_volume, self.horror_target, self.transition_speed
        )
        self.pond_volume = self._lerp(
            self.pond_volume, self.pond_target, self.transition_speed
        )

        # Apply volumes to channels
        if self.horror_channel and self.horror_sound:
            self.horror_sound.set_volume(self.horror_volume * master_volume)

        if self.pond_channel and self.pond_sound:
            self.pond_sound.set_volume(self.pond_volume * master_volume)

    def set_intensity(self, intensity):
        """
        Set the intensity of the audio mix (0.0 to 1.0)
        Higher intensity = more horror, less calm pond ambience

        Use cases:
        - Low health: high intensity
        - Near enemies: high intensity
        - Calm exploration: low intensity
        - Boss fight: maximum intensity
        """
        self.intensity = max(0.0, min(1.0, intensity))

        # Dynamic mix based on intensity
        # At low intensity: pond dominant, subtle horror
        # At high intensity: horror dominant, minimal pond
        self.horror_target = self.base_horror_volume + (0.5 * self.intensity)
        self.pond_target = self.base_pond_volume * (1.0 - 0.6 * self.intensity)

        # Cap volumes
        self.horror_target = min(1.0, self.horror_target)
        self.pond_target = max(0.05, self.pond_target)

    def set_danger_level(self, health_percent, enemy_nearby=False, difficulty=1.0):
        """
        Automatically calculate intensity based on game state
        Like professional games that react to gameplay

        Args:
            health_percent: Player health (0.0 to 1.0)
            enemy_nearby: Whether enemies are close
            difficulty: Current difficulty multiplier
        """
        # Base intensity from health (low health = high intensity)
        health_intensity = 1.0 - health_percent

        # Enemy proximity boost
        enemy_intensity = 0.3 if enemy_nearby else 0.0

        # Difficulty scaling
        difficulty_intensity = (difficulty - 1.0) * 0.1

        # Combine factors
        total_intensity = (
            health_intensity * 0.5 + enemy_intensity + difficulty_intensity
        )
        total_intensity = max(0.0, min(1.0, total_intensity))

        self.set_intensity(total_intensity)

    def pulse_horror(self, duration=0.5):
        """
        Briefly spike horror intensity (for jump scares, damage, etc.)
        """
        # Quick spike
        old_target = self.horror_target
        self.horror_target = min(1.0, self.horror_target + 0.3)

        # Will naturally transition back on next update cycle

    def fade_out(self, speed=0.01):
        """Fade out all ambient audio"""
        self.horror_target = 0.0
        self.pond_target = 0.0
        self.transition_speed = speed

    def fade_in(self, speed=0.02):
        """Fade in ambient audio to default levels"""
        self.horror_target = self.base_horror_volume
        self.pond_target = self.base_pond_volume
        self.transition_speed = speed

    def pause(self):
        """Pause ambient audio"""
        if self.horror_channel:
            self.horror_channel.pause()
        if self.pond_channel:
            self.pond_channel.pause()

    def unpause(self):
        """Unpause ambient audio"""
        if self.horror_channel:
            self.horror_channel.unpause()
        if self.pond_channel:
            self.pond_channel.unpause()

    def stop(self):
        """Stop all ambient audio"""
        if self.horror_channel:
            self.horror_channel.stop()
        if self.pond_channel:
            self.pond_channel.stop()
        self.is_playing = False

    def _lerp(self, current, target, speed):
        """Linear interpolation for smooth transitions"""
        if abs(current - target) < 0.001:
            return target
        return current + (target - current) * speed


class SoundManager:
    """
    Manages all game audio with AAA-quality dynamic mixing
    """

    def __init__(self):
        """Initialize the sound manager"""
        # Volume settings are kept even when audio cannot initialize so menus still
        # behave consistently.
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME

        self.audio_available = True

        # Initialize pygame mixer with high quality settings
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except pygame.error as e:
            print(f"Audio disabled: {e}")
            self.audio_available = False

        # Sound effect cache
        self.sounds = {}

        # Music state
        self.current_music = None
        self.music_paused = False

        # Professional ambient mixer
        self.ambient_mixer = AmbientMixer(self)

        # Load sounds
        if self.audio_available:
            self._load_sounds()

        # Load and initialize ambient tracks
        self.ambient_mixer.load_ambient_tracks()

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
        if not self.audio_available:
            self.sounds[name] = None
            return

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
        if not self.audio_available:
            return

        if name in self.sounds and self.sounds[name]:
            sound = self.sounds[name]
            if volume is not None:
                sound.set_volume(volume * self.sfx_volume)
            else:
                sound.set_volume(self.sfx_volume)
            sound.play()

    def pause_music(self):
        """Pause the current music and ambient audio"""
        if not self.audio_available:
            self.music_paused = True
            return

        pygame.mixer.music.pause()
        self.ambient_mixer.pause()
        self.music_paused = True

    def unpause_music(self):
        """Unpause the current music and ambient audio"""
        if not self.audio_available:
            self.music_paused = False
            return

        pygame.mixer.music.unpause()
        self.ambient_mixer.unpause()
        self.music_paused = False

    def start_ambient_audio(self):
        """Start the professional layered ambient audio mix"""
        self.ambient_mixer.start_ambient_mix()

    def update_ambient_audio(self, dt=1 / 60):
        """Update ambient audio mix - call every frame for smooth transitions"""
        self.ambient_mixer.update(dt)

    def set_audio_intensity(self, intensity):
        """
        Set audio intensity (0.0 = calm, 1.0 = intense horror)
        Higher intensity = more horror ambience, less calm sounds
        """
        self.ambient_mixer.set_intensity(intensity)

    def update_danger_level(self, health_percent, enemy_nearby=False, difficulty=1.0):
        """
        Automatically adjust audio based on game state
        Like professional AAA games that react to gameplay
        """
        self.ambient_mixer.set_danger_level(health_percent, enemy_nearby, difficulty)

    def pulse_horror_audio(self):
        """Briefly spike horror intensity for damage/scary moments"""
        self.ambient_mixer.pulse_horror()

    def set_music_volume(self, volume):
        """
        Set music volume

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        if self.audio_available:
            pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """
        Set sound effects volume

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))

        if not self.audio_available:
            return

        # Update all loaded sounds
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.sfx_volume)

    def create_procedural_sounds(self):
        """
        Create simple procedural sound effects when no audio files exist
        This provides basic audio feedback without external files
        """
        if not self.audio_available:
            return

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
        except (pygame.error, ValueError):
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
        except (pygame.error, ValueError):
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
        except (pygame.error, ValueError):
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
        except (pygame.error, ValueError):
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
        except (pygame.error, ValueError):
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
        except (pygame.error, ValueError):
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
        except (pygame.error, ValueError):
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
        except (pygame.error, ValueError):
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
        except (pygame.error, ValueError):
            pass

    def create_procedural_music(self):
        """
        Create procedural background music for the game
        This generates a dark ambient loop that plays continuously
        """
        if not self.audio_available:
            return

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
