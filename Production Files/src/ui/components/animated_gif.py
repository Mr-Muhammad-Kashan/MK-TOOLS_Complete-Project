# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# PARADIGM SOLUTION: AnimatedGIFLabel (v2.1 - Framework-Compliant Engine)
# ===================================================================================
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component has been upgraded for zero-defect integration with the customtkinter
# framework. The previous implementation used PIL's `PhotoImage`, which is not
# fully compatible with customtkinter's high-DPI scaling and theming engine,
# resulting in a `UserWarning`.
#
# NEW PARADIGM: NATIVE CTkImage INTEGRATION
#  1. The internal frame cache (`self.frames`) no longer stores `PhotoImage` objects.
#     It now exclusively stores `customtkinter.CTkImage` objects.
#  2. During the `_load_gif` process, each raw PIL frame extracted from the GIF
#     is used to instantiate a `CTkImage`, specifying it for both light and dark
#     modes and locking its size.
#
# This architecture eliminates the framework warning, ensures full compatibility with
# the customtkinter rendering pipeline, and leverages the previously implemented
# `resize_and_reload` method to maintain perfect dynamic scaling.
# =====================================================================================

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
import psutil
import logging
import requests
from typing import List, Dict, Optional, Callable, Any, Tuple

try:
    import winreg
except ImportError:
    pass

try:
    import wmi
except ImportError:
    pass


class AnimatedGIFLabel(ctk.CTkLabel):
    """
    A self-managing label that plays animated GIFs with correct frame timing
    and supports dynamic, on-the-fly resizing using native CTkImage objects.
    """
    def __init__(self, master, gif_path: str, size: Tuple[int, int]):
        # --- Base Class Initialization: Initialize as a standard CTkLabel.
        super().__init__(master, text="", fg_color="transparent")

        # --- State and Asset Storage ---
        self.gif_path = gif_path                                      # --- The file path to the animated GIF.
        self.size = size                                              # --- The target (width, height) to display the GIF.
        self.frames = []                                              # --- A list to hold all processed CTkImage frames of the GIF.
        self.frame_durations = []                                     # --- A list to hold the duration of each corresponding frame.
        self.frame_index = 0                                          # --- The index of the current frame being displayed.
        self._animation_job = None                                    # --- A handle for the scheduled .after() job to allow for cancellation.
        self._is_animating = False                                    # --- A state flag to track if the animation loop is active.

        # --- Load the GIF frames into memory upon instantiation.
        self._load_gif()

    def _load_gif(self):
        """Extracts all frames, converts them to CTkImage objects, and stores them."""
        # --- Use a try-except block to handle file loading errors gracefully.
        try:
            # --- Open the GIF file using the Pillow library.
            with Image.open(self.gif_path) as img:
                # --- Iterate through each frame available in the GIF file.
                for i in range(img.n_frames):
                    # --- Seek to the current frame index.
                    img.seek(i)
                    # --- Create a copy of the frame and resize it to the specified dimensions using a high-quality filter.
                    frame = img.copy().resize(self.size, Image.Resampling.LANCZOS)
                    # --- [CRITICAL FIX] Convert the Pillow frame into a CTkImage object that customtkinter can manage.
                    ctk_frame = ctk.CTkImage(light_image=frame, dark_image=frame, size=self.size)
                    self.frames.append(ctk_frame)
                    # --- Extract the duration for this specific frame from the GIF's metadata (in milliseconds).
                    duration = img.info.get('duration', 100)
                    self.frame_durations.append(duration if duration > 0 else 100)
        # --- Handle the case where the specified GIF file does not exist.
        except FileNotFoundError:
            logging.error(f"AnimatedGIFLabel Error: GIF file not found at '{self.gif_path}'")
            self.configure(text=f"Error:\nGIF not found.")
        # --- Handle any other exceptions during image processing.
        except Exception as e:
            logging.error(f"AnimatedGIFLabel Error: Failed to load GIF '{self.gif_path}'. Reason: {e}", exc_info=True)
            self.configure(text=f"Error:\nFailed to load GIF.")

    def _animate(self):
        """The core animation loop that cycles through the frames."""
        # --- Abort if no frames are loaded or if the animation has been stopped.
        if not self.frames or not self._is_animating:
            return

        # --- Set the label's image to the current CTkImage frame.
        self.configure(image=self.frames[self.frame_index])

        # --- Increment the frame index, looping back to the beginning.
        self.frame_index = (self.frame_index + 1) % len(self.frames)

        # --- Schedule the next call to this method after the duration of the current frame.
        self._animation_job = self.after(self.frame_durations[self.frame_index], self._animate)

    def start_animation(self):
        """Starts the animation loop."""
        # --- Prevent duplicate animation loops.
        if self._is_animating:
            return
        # --- Set the state flag to true.
        self._is_animating = True
        # --- Begin the animation sequence.
        self._animate()

    def stop_animation(self):
        """Stops the animation loop by cancelling the scheduled job."""
        # --- Set the state flag to false to terminate the loop.
        self._is_animating = False
        # --- Cancel any pending .after() call.
        if self._animation_job:
            self.after_cancel(self._animation_job)
            self._animation_job = None

    def resize_and_reload(self, new_size: Tuple[int, int]):
        """Resizes the GIF by reloading and re-caching all frames at the new dimensions."""
        # --- Record the animation's current state.
        was_animating = self._is_animating
        # --- Stop any current animation to prevent conflicts.
        self.stop_animation()

        # --- Update the size and clear the old frame cache.
        self.size = new_size
        self.frames.clear()
        self.frame_durations.clear()
        self.frame_index = 0

        # --- Reload all frames at the new size.
        self._load_gif()

        # --- Restart the animation if it was running before the resize.
        if was_animating:
            self.start_animation()
