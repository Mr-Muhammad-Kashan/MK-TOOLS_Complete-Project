# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# SECTION 4.5: AUDITORY FEEDBACK ENGINE (AFE) (v3.0 - Zero-Latency Startup)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive, military-grade implementation of the SoundManager. It is
# engineered for zero-latency application startup by offloading all blocking file
# I/O operations to a dedicated background thread. Its singleton architecture
# ensures a single, authoritative source for all auditory feedback, while its
# thread-safe command queue guarantees responsive and stable playback.
# ===================================================================================

import os
import sys
import ctypes
import time
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import pygame
from typing import List, Dict, Optional, Callable, Any, Tuple


class SoundManager:
    """
    A singleton class to manage UI sounds with global enable/disable functionality
    and a non-blocking, asynchronous asset loading protocol.
    """
    _instance = None # --- The single, shared instance of the class.

    # ===============================================================================
    # METHOD: __new__ (Singleton Instantiation Protocol)
    # Ensures that only one instance of the SoundManager is ever created.
    # ===============================================================================
    def __new__(cls, *args, **kwargs):
        # --- If no instance exists, create one.
        if not cls._instance:
            # --- Call the parent class's constructor to create the new instance.
            cls._instance = super(SoundManager, cls).__new__(cls)
        # --- Return the single, existing instance.
        return cls._instance

    # ===============================================================================
    # METHOD: __init__ (v3.1 - Hybrid Loading Protocol)
    #
    # ARCHITECTURAL BLUEPRINT (UPGRADE):
    # This version implements a hybrid asset loading model. It synchronously
    # pre-loads mission-critical assets (the startup sound) for instantaneous
    # availability, guaranteeing the application's initial auditory feedback.
    # All other non-essential assets remain offloaded to the non-blocking
    # background thread to ensure a zero-latency startup.
    # ===============================================================================
    def __init__(self):
        # --- Prevent re-initialization if the singleton is accessed again. ---
        if hasattr(self, '_initialized'):
            return
        # --- Set the initialization flag to prevent future re-runs of this constructor.
        self._initialized = True

        # --- Global Auditory State ---
        self.sound_enabled = True
        self._current_looping_sound = None
        self.sounds = {}

        # --- Core Audio Engine Initialization ---
        try:
            pygame.init()
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.looping_channel = pygame.mixer.Channel(0)
            logging.info("Auditory Feedback Engine (AFE) v3.1 initialized successfully.")
        except Exception as e:
            logging.error(f"AFE CRITICAL FAILURE: Could not initialize pygame.mixer. Error: {e}", exc_info=True)
            self.looping_channel = None
            return

        # --- [CRITICAL ASSET PRE-LOADING] ---
        # --- The startup sound is loaded synchronously on the main thread.
        # --- This is a single, small file, ensuring its impact on startup time is negligible
        # --- while guaranteeing its availability when the splash screen appears.
        try:
            startup_sound_path = resource_path(os.path.join("assets", "sounds", "Startup-Sound.mp3"))
            self.sounds['Startup-Sound.mp3'] = pygame.mixer.Sound(startup_sound_path)
            logging.info("AFE: Critical asset 'Startup-Sound.mp3' pre-loaded successfully.")
        except Exception as e:
            logging.error(f"AFE CRITICAL FAILURE: Could not pre-load 'Startup-Sound.mp3'. Error: {e}", exc_info=True)
            self.sounds['Startup-Sound.mp3'] = None

        # --- Asynchronous Asset Loading for all non-critical sounds ---
        self.loading_thread = threading.Thread(target=self._load_sounds_in_background, daemon=True)
        self.loading_thread.start()

        # --- Thread-Safe Command Queue & Playback Worker ---
        self.sound_queue = Queue()
        self._shutdown_event = threading.Event()
        self.playback_thread = threading.Thread(target=self._sound_playback_worker, daemon=True)
        self.playback_thread.start()

    # ===============================================================================
    # METHOD: _load_sounds_in_background (v1.1 - Non-Critical Asset Worker)
    #
    # ARCHITECTURAL BLUEPRINT (UPGRADE):
    # This worker's manifest has been updated to exclude any assets that are
    # pre-loaded by the constructor. It is now responsible for the asynchronous
    # loading of all non-essential, secondary sound assets.
    # ===============================================================================
    def _load_sounds_in_background(self):
        # --- Master Sound Asset Manifest (Non-Critical Assets Only) ---
        sound_files = [
            ('click', 'Mouse-Click.mp3'), ('hover', 'Mouse-Hover.mp3'),
            ('reset', 'Reset-Defaults.mp3'), ('turn_on', 'Turn-On.mp3'),
            ('turn_off', 'Turn-Off.mp3'), ('clean_all_click', 'Clean-all-button.mp3'),
            ('cleaning_loop', 'Cleaning.mp3'), ('manual_clean', 'Manual-Clean.mp3'),
            ('what_is_it', 'what-is-it.mp3'), ('money', 'Money.mp3'),
            ('linkedin_click', 'LinkedIn-Button-Click.mp3'), ('github_click', 'Github-Button-Click.mp3'),
            ('email_click', 'Email-Button-Click.mp3'), ('nav_click', 'Navigation-Sound.mp3'),
            ('fix_windows_hover', 'Fix-Windows-Hover-Effect.mp3'), ('question_mark', 'Questionmark.mp3'),
            ('scan_loop', 'Scan-Fix-Windows-Effect.mp3'), ('advanced_scan_loop', 'Advanced-Scan.mp3'),
            ('notification', 'Notification.mp3'), ('cancel_operation', 'Oh-No.mp3'),
            ('feature_hover', 'Feature-Hover.mp3'), ('warning_loop', 'Warning.mp3'),
            ('success_fanfare', 'Horray-No-Errors-Found.mp3'), ('error_sound', 'Error-404.mp3'),
            ('setup_unsuccessful', 'setup-unsuccessful.mp3'), ('success_loop', 'Horray-No-Errors-Found.mp3'),
            ('coin_hover', 'Coin.mp3'), ('ok_click', 'Mouse-Click-Ok.mp3'),
            # --- 'Startup-Sound.mp3' is now pre-loaded in __init__ and is omitted here.
            ('Nav_Sound_Click', 'Navigation-Click-Sound.mp3'),
            ('support_hover', "JUST DO IT - Sound Effect.mp3"),
            ('support_click', "Thanks-Coffee_Button.mp3")
        ]

        # --- Sequential Loading Loop ---
        for name, filename in sound_files:
            try:
                # --- Resolve the absolute path to the asset using the universal resource path resolver. ---
                path = resource_path(os.path.join("assets", "sounds", filename))
                # --- This is the blocking I/O operation. It loads the sound file from disk and decodes it. ---
                sound_object = pygame.mixer.Sound(path)
                # --- Atomically add the loaded sound object to the shared dictionary. ---
                self.sounds[name] = sound_object
                # --- Log the successful loading of the asset for auditing. ---
                logging.info(f"AFE Background Loader: Sound asset '{filename}' loaded successfully.")
            except pygame.error as e:
                # --- In case of a loading failure (e.g., file not found, corrupt file), log the specific error. ---
                logging.error(f"AFE Background Loader ERROR: Failed to load sound '{filename}'. Error: {e}", exc_info=True)
                # --- Place a None value in the dictionary to prevent KeyErrors if the UI tries to play a missing sound. ---
                self.sounds[name] = None

    # ===============================================================================
    # METHOD: _sound_playback_worker (v1.0 - Thread-Safe Command Processor)
    #
    # ARCHITECTURAL BLUEPRINT:
    # This is the core worker loop for the Auditory Feedback Engine. It runs on its
    # own dedicated thread, perpetually waiting for commands to be placed in the
    # thread-safe `sound_queue`. By processing all playback requests here, we
    # ensure that the main UI thread is never blocked by sound operations and that
    # all requests are handled sequentially and safely.
    # ===============================================================================
    def _sound_playback_worker(self):
        """Processes sound commands from the queue until a shutdown is signaled."""
        # --- This loop runs for the entire lifetime of the application until the shutdown event is set.
        while not self._shutdown_event.is_set():
            # --- The .get() call is blocking; the thread will sleep here until a command is available.
            command_tuple = self.sound_queue.get()
            # --- A 'None' object is the designated poison pill to signal thread termination.
            if command_tuple is None:
                # --- Exit the loop to allow the thread to terminate gracefully.
                break
            # --- Unpack the command tuple into the action and its argument (the sound name).
            command, argument = command_tuple
            try:
                # --- Process a 'play' command for one-shot sound effects.
                if command == 'play':
                    # --- Play the sound only if the global toggle is enabled OR if it's the specific nav_click sound.
                    if self.sound_enabled or argument == 'nav_click':
                        # --- Retrieve the pre-loaded sound object from the dictionary. .get() safely returns None if not found.
                        sound_to_play = self.sounds.get(argument)
                        if sound_to_play:
                            # --- Execute the sound playback.
                            sound_to_play.play()

                # --- Process a 'loop' command for continuous background sounds.
                elif command == 'loop':
                    # --- Only begin a new loop if sound is globally enabled.
                    if self.sound_enabled:
                        # --- Store the name of the looping sound for state restoration if sounds are toggled.
                        self._current_looping_sound = argument
                        if self.looping_channel:
                            sound_to_loop = self.sounds.get(argument)
                            if sound_to_loop:
                                # --- Stop any previously playing loop on the dedicated channel.
                                self.looping_channel.stop()
                                # --- Play the new sound indefinitely (loops=-1).
                                self.looping_channel.play(sound_to_loop, loops=-1)

                # --- Process a 'stop_loop' command.
                elif command == 'stop_loop':
                    # --- This command signifies the logical end of a looping operation (e.g., scan complete).
                    if self.looping_channel:
                        self.looping_channel.stop()
                    # --- [PARADIGM SOLUTION] Always clear the state variable to prevent incorrect resumption of the sound.
                    self._current_looping_sound = None

                # --- Process a 'stop_and_play' command to prevent sound overlap.
                elif command == 'stop_and_play':
                    if self.sound_enabled or argument == 'nav_click':
                        sound_to_play = self.sounds.get(argument)
                        if sound_to_play:
                            # --- Immediately stop any currently playing instances of this sound before starting a new one.
                            sound_to_play.stop()
                            sound_to_play.play()

                # --- Process a 'stop' command for a specific sound.
                elif command == 'stop':
                    sound_to_stop = self.sounds.get(argument)
                    if sound_to_stop:
                        sound_to_stop.stop()
                        # --- If we are stopping the sound that was considered the main loop, clear its state as a failsafe.
                        if argument == self._current_looping_sound:
                            self._current_looping_sound = None

            # --- Catch any low-level Pygame errors that might occur during playback.
            except pygame.error as e:
                logging.error(f"AFE PLAYBACK ERROR for command '({command}, {argument})': {e}", exc_info=True)

    # ===============================================================================
    # METHOD: Public API Methods (Play, Start Loop, Stop Loop, etc.)
    # These methods provide a clean, high-level interface for the rest of the
    # application to interact with the sound engine without needing to know about
    # the underlying threading model.
    # ===============================================================================
    def play_sound(self, name: str):
        """Places a 'play' command into the queue for a one-shot sound effect if enabled."""
        if hasattr(self, 'sound_queue'):
            self.sound_queue.put(('play', name))

    def start_looping_sound(self, name: str):
        """Places a 'loop' command into the queue to start a continuous sound if enabled."""
        if hasattr(self, 'sound_queue'):
            self.sound_queue.put(('loop', name))

    def stop_looping_sound(self):
        """Places a 'stop_loop' command into the queue to halt the continuous sound."""
        if hasattr(self, 'sound_queue'):
            self.sound_queue.put(('stop_loop', None))

    def stop_sound(self, name: str):
        """Places a 'stop' command into the queue to halt a specific one-shot sound."""
        if hasattr(self, 'sound_queue'):
            self.sound_queue.put(('stop', name))

    def stop_and_play_sound(self, name: str):
        """Places a 'stop_and_play' command into the queue to prevent sound overlap."""
        if hasattr(self, 'sound_queue'):
            self.sound_queue.put(('stop_and_play', name))

    def set_sound_enabled(self, enabled: bool):
        """
        Sets the global sound state with military-grade precision.
        ACTION: DISABLING SOUND - Terminates all active audio channels instantly.
        ACTION: ENABLING SOUND - Resumes the last known looping sound, if one was active.
        This ensures an instantaneous and seamless user experience upon toggling.
        """
        self.sound_enabled = enabled # --- Sets the new state for all future sound requests.
        if not enabled: # --- Executes if the sound is being toggled OFF.
            pygame.mixer.stop() # --- CRITICAL COMMAND: Ceases all audio playback on all channels immediately.
        elif enabled and self._current_looping_sound: # --- Executes if sound is toggled ON and a looping sound was previously active.
            # --- Resumes the last looping sound that was interrupted by the toggle-off action.
            self.sound_queue.put(('loop', self._current_looping_sound))

    def shutdown(self):
        """Gracefully shuts down the AFE worker thread and de-initializes Pygame."""
        logging.info("AFE: Shutdown initiated. Releasing audio resources.")
        if hasattr(self, '_shutdown_event'):
            self._shutdown_event.set()
            self.sound_queue.put(None) # --- Send the poison pill to the worker thread.
            self.playback_thread.join(timeout=1.0) # --- Wait for the thread to terminate.
        pygame.quit()
        logging.info("AFE: Pygame de-initialized. Audio resources released.")
