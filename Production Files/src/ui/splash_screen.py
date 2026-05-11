# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: SplashScreen (v1.6 - Final Visual Synthesis)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This definitive version replaces the standard CTkProgressBar with a completely
# custom-drawn, animated progress bar on the tkinter.Canvas. The new design
# synthesizes the futuristic, segmented, and glowing aesthetics from the user-
# provided reference image while being meticulously optimized for low-end hardware.
#
# CORE ENHANCEMENTS:
#   1. [AESTHETICS] Custom-Drawn Segmented Progress Bar: The progress bar is no
#      longer a widget but a collection of canvas rectangles. This allows for a
#      pixel-perfect, sharp geometric design that faithfully captures the cyberpunk
#      aesthetic of the reference image.
#
#   2. [ANIMATION] Sequential Segment Illumination: The `update_progress` method
#      now calculates how many segments to "light up" based on the loading
#      percentage, filling the bar in discrete, visually satisfying steps.
#
#   3. [ANIMATION] Optimized Pulsing Glow: A low-frequency animation loop subtly
#      pulses the color of the active segments between two shades of purple. This
#      creates the illusion of a dynamic, "live" energy source without the
#      performance cost of a high-framerate animation.
#
#   4. [PERFORMANCE] Zero-Widget Progress Bar: By drawing the bar directly onto
#      the canvas, we eliminate the overhead of a CustomTkinter widget, further
#      reducing the component's resource footprint.
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


class SplashScreen(ctk.CTkToplevel):
    """
    A visually appealing, animated splash screen that masks background loading tasks.
    """
    def __init__(self, master):
        # --- Base Initialization & Window Configuration ---
        super().__init__(master)
        self.master = master

        # --- [DPI SCALING] Calculate scaled dimensions based on the system's DPI factor.
        scale_factor = ScreenManager.get_scaling_factor()
        self.width = int(700 * scale_factor)
        self.height = int(450 * scale_factor)

        # --- Configure the window to be borderless and stay on top.
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # --- Set the taskbar icon for the splash screen.
        try:
            # --- [MODIFIED] Use the resource_path function to locate the icon.
            self.iconbitmap(resource_path(os.path.join("assets", "icons", "Logo.ico")))
        except tk.TclError:
            logging.warning("Could not set splash screen icon. 'Logo.ico' may be missing.")

        # --- Delegate centering logic to the ScreenManager utility with scaled dimensions.
        ScreenManager.center_window(self, self.width, self.height)

        # --- Configure transparency for the floating effect.
        self.transparent_color = '#010101'
        self.wm_attributes('-transparentcolor', self.transparent_color)
        self.config(bg=self.transparent_color)
        self.attributes("-alpha", 0.0)

        # --- Animation & Particle System State ---
        self.particles = []
        self.animation_job = None
        self.glow_animation_job = None

        # --- Custom Progress Bar State ---
        self.progress_segments = []
        self.current_progress = 0.0

        # --- UI Construction Protocol ---
        self._create_widgets()
        # --- Start the animation loop immediately upon creation.
        self.start_animation()

    def _create_widgets(self):
        """Creates the canvas, text, custom progress bar, and status label with DPI scaling."""
        # --- Create the main canvas for drawing the animation, filling the scaled window.
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg=Theme.BACKGROUND_DARK, highlightthickness=0)
        self.canvas.pack()

        # --- [DPI SCALING] Scale the title font size based on the system's scaling factor.
        scale_factor = ScreenManager.get_scaling_factor()
        scaled_title_size = int(60 * scale_factor)

        # --- Create the central "MK-Tools 🚀" text element with the scaled font.
        self.title_text_id = self.canvas.create_text(
            self.width / 2, self.height / 2 - int(40 * scale_factor), # Scale vertical offset
            text="MK-Tools 🚀",
            font=("Segoe UI Black", scaled_title_size),
            fill=Theme.ACCENT_DARK
        )

        # --- Draw the custom, segmented progress bar which is now also scaled.
        self._create_custom_progress_bar()

        # --- Create a label to display status, using the pre-scaled font from the Theme class.
        self.status_label = ctk.CTkLabel(
            self,
            text="Initializing...",
            font=Theme.FONTS["normal"],
            fg_color=Theme.BACKGROUND_DARK,
            text_color=Theme.TEXT_SECONDARY
        )

        # --- Place the status label on the canvas below the progress bar with a scaled offset.
        self.canvas.create_window(self.width / 2, self.height - int(80 * scale_factor), window=self.status_label)

    def _create_custom_progress_bar(self):
        """Draws the static background and the individual segments of the progress bar on the canvas, scaled for DPI."""
        # --- [DPI SCALING] Calculate all progress bar dimensions based on the system scaling factor.
        scale_factor = ScreenManager.get_scaling_factor()
        bar_width = int(400 * scale_factor)
        bar_height = int(25 * scale_factor)
        num_segments = 20
        segment_width = bar_width / num_segments
        bar_x = (self.width - bar_width) / 2
        bar_y = self.height / 2 + int(50 * scale_factor)

        # --- Draw the dark background/container for the progress bar.
        self.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height, fill=Theme.NAV_RAIL_DARK, outline="")

        # --- Create each individual segment in an "off" state with a scaled gap.
        for i in range(num_segments):
            seg_x1 = bar_x + (i * segment_width)
            seg_x2 = seg_x1 + segment_width - int(2 * scale_factor) # Scale the gap between segments.
            seg_id = self.canvas.create_rectangle(seg_x1, bar_y, seg_x2, bar_y + bar_height, fill=Theme.CARD_DARK, outline="")
            self.progress_segments.append(seg_id)

    def _create_particles(self):
        """
        [PERFORMANCE TIERING] Generates a new batch of particles only if the
        hardware tier is not 'LOW'. On low-tier systems, this function exits
        immediately to prevent any performance impact.
        """
        # --- This check ensures no particles are ever created on low-end hardware.
        if self.master.hardware_tier == 'LOW':
            return

        if len(self.particles) < 50:
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            radius = random.uniform(1, 4)
            color = random.choice([Theme.ACCENT_DARK, Theme.ACCENT_HOVER_DARK, Theme.ACCENT_ACTIVE_DARK])
            dx = random.uniform(-0.5, 0.5)
            dy = random.uniform(-0.5, 0.5)
            orb_id = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline="")
            self.particles.append({'id': orb_id, 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'life': random.randint(150, 300)})

    def _update_animation(self):
        """
        [PERFORMANCE TIERING] The core particle animation loop. This entire
        method is bypassed on low-tier systems as it is never called by `start_animation`.
        """
        particles_to_keep = []
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['life'] -= 1
            if p['life'] > 0:
                self.canvas.move(p['id'], p['dx'], p['dy'])
                particles_to_keep.append(p)
            else:
                self.canvas.delete(p['id'])
        self.particles = particles_to_keep
        self._create_particles()
        self.animation_job = self.after(16, self._update_animation)

    def _animate_progress_bar_glow(self):
        """Creates a subtle, low-intensity pulsing glow on the active segments."""
        # --- The glow effect is a sine wave over time.
        glow_value = (math.sin(time.time() * 4) + 1) / 2 # --- Oscillates between 0 and 1.

        # --- Interpolate between two shades of purple to create the pulse.
        start_color = [int(Theme.ACCENT_HOVER_DARK[i:i+2], 16) for i in (1, 3, 5)]
        end_color = [int(Theme.ACCENT_DARK[i:i+2], 16) for i in (1, 3, 5)]

        current_color = [int(start_color[i] + (end_color[i] - start_color[i]) * glow_value) for i in range(3)]
        hex_color = f"#{current_color[0]:02x}{current_color[1]:02x}{current_color[2]:02x}"

        # --- Determine how many segments should be "on" based on the current progress.
        num_lit_segments = int(self.current_progress * len(self.progress_segments))

        # --- Apply the glowing color only to the active segments.
        for i, seg_id in enumerate(self.progress_segments):
            if i < num_lit_segments:
                self.canvas.itemconfig(seg_id, fill=hex_color)

        # --- Schedule the next frame of the glow animation.
        self.glow_animation_job = self.after(33, self._animate_progress_bar_glow)

    def start_animation(self):
        """
        Initiates the animation loops. The particle animation is conditionally
        disabled on low-tier hardware to conserve system resources.
        """
        # --- [PERFORMANCE TIERING] Only start the expensive particle animation
        # --- if the system is not classified as low-tier.
        if self.master.hardware_tier != 'LOW':
            self._update_animation()

        # --- The progress bar glow is a lightweight animation and runs on all tiers.
        self._animate_progress_bar_glow()
        self._fade_in()

    def _fade_in(self, alpha=0.0):
        """Animates the window's alpha channel from transparent to opaque."""
        if alpha < 1.0:
            alpha += 0.05
            self.attributes("-alpha", alpha)
            self.after(16, self._fade_in, alpha)

    def update_progress(self, value: float, text: str):
        """
        Public API method to update the progress bar and status text from the main App.
        """
        # --- Store the current progress value.
        self.current_progress = value
        # --- Determine how many segments should be lit.
        num_lit_segments = int(value * len(self.progress_segments))

        # --- Update the color of all segments based on the new progress.
        for i, seg_id in enumerate(self.progress_segments):
            if i < num_lit_segments:
                # --- This segment should be "on". The glow animation will handle its color.
                pass
            else:
                # --- This segment should be "off".
                self.canvas.itemconfig(seg_id, fill=Theme.CARD_DARK)

        # --- Update the status text label.
        self.status_label.configure(text=f"{text} ({int(value * 100)}%)")

    def close(self):
        """Public API method to initiate the fade-out and destruction of the splash screen."""
        # --- Stop all animation loops to conserve resources.
        if self.animation_job:
            self.after_cancel(self.animation_job)
            self.animation_job = None
        if self.glow_animation_job:
            self.after_cancel(self.glow_animation_job)
            self.glow_animation_job = None
        # --- Start the fade-out animation.
        self._fade_out()

    def _fade_out(self, alpha=1.0):
        """Animates the window's alpha channel from opaque to transparent, then destroys it."""
        if alpha > 0.0:
            alpha -= 0.05
            self.attributes("-alpha", alpha)
            self.after(16, self._fade_out, alpha)
        else:
            # --- Once fully transparent, destroy the splash screen window completely.
            self.destroy()
