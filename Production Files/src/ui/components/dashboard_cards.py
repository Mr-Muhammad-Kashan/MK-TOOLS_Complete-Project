# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: _DashboardCard (v2.4 - With State Reset Protocol)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This version introduces a definitive, public-facing state reset protocol.
#
# CORRECTION PROTOCOL:
#  1. NEW PUBLIC API: A new method, `reset_state()`, has been engineered. Its
#     sole purpose is to forcibly revert the component to its default, non-hovered
#     visual state. It sets the internal `_is_mouse_inside` flag to False and
#     resets the border color to its default.
#
#  2. ENCAPSULATION: This method provides a clean, encapsulated interface for the
#     parent frame (`DashboardFrame`) to command a state change without needing
#     to know about the component's internal implementation details. This is the
#     cornerstone of the bug fix.
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


class _DashboardCard(ctk.CTkFrame):
    """A single, interactive, and perfectly aligned clickable card with a unified, stateful hover effect and precise auditory feedback."""

    # The constructor for the re-engineered _DashboardCard class.
    def __init__(
        self,
        master,
        fonts,
        icon_path: str, # Changed from 'icon' to 'icon_path'
        title: str,
        feature_count: int,
        command: Callable[[], None],
        sound_manager: Optional['SoundManager'] = None
    ):
        # --- Base Class Initialization & Theming ---
        super().__init__(
            master,
            fg_color=Theme.CARD,
            corner_radius=20,
            border_width=2,
            border_color=Theme.CARD,
        )
        # --- Property and State Storage ---
        self.command = command
        self.fonts = fonts
        self.sound_manager = sound_manager
        self.icon_path = icon_path # Store the path for rescaling
        self._is_mouse_inside = False
        self._leave_check_job = None

        # --- Internal Grid Configuration for perfect centering ---
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)

        # --- Widget Creation & Placement ---
        # --- [ICON REFACTOR] The icon is now a scalable CTkImage, not a text emoji.
        self.icon_image = None # Placeholder for the CTkImage object
        self.icon_lbl = ctk.CTkLabel(self, text="") # Create the label, image will be added
        self.icon_lbl.grid(row=1, column=0, pady=(10, 5))

        # --- The title label for the card.
        self.title_lbl = ctk.CTkLabel(self, text=title, font=self.fonts["h2"], text_color=Theme.TEXT)
        self.title_lbl.grid(row=2, column=0)

        # --- The feature count sub-label.
        self.feat_lbl = ctk.CTkLabel(self, text=f"{feature_count} Features", font=self.fonts["small"], text_color=Theme.TEXT_SECONDARY)
        self.feat_lbl.grid(row=3, column=0, pady=(5, 10))

        # --- Definitive Event Binding Protocol ---
        self._bind_events()

        # --- Initial Scaling Call ---
        # This sets the initial size of the icon correctly.
        self.update_ui_scaling(self.fonts)

    def _bind_events(self):
        """
        [RE-ENGINEERED] Binds events recursively to all widgets to create a
        unified interaction surface, with stateful handlers to prevent anomalies.
        """
        # --- Create a comprehensive list of all widgets that form this component.
        all_widgets = (self, self.icon_lbl, self.title_lbl, self.feat_lbl)

        # --- Bind all widgets to the same set of event handlers.
        for widget in all_widgets:
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_click)

    def _on_enter(self, event=None):
        """
        Handles the mouse entering ANY part of the card. This serves as the
        primary trigger for the hover-on action.
        """
        # --- Cancel any pending "leave" check. This is crucial for when the
        # --- mouse moves rapidly between child widgets.
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
            self._leave_check_job = None

        # --- Check the state to prevent re-triggering ---
        # If the mouse is not already considered inside, proceed.
        if not self._is_mouse_inside:
            # --- Update the state to reflect the mouse is now inside.
            self._is_mouse_inside = True

            # --- Dispatch Auditory Feedback ---
            # If a sound manager exists, play the 'hover' sound exactly once.
            if self.sound_manager:
                self.sound_manager.play_sound('hover')

            # --- Dispatch Visual Feedback ---
            # Change the border color to the theme's accent color for a highlight effect.
            self.configure(border_color=Theme.ACCENT)

    def _on_leave(self, event=None):
        """
        Handles the mouse leaving ANY part of the card. Schedules a delayed
        check to verify if the mouse has truly exited the component's boundary.
        """
        # --- Cancel any previously scheduled check to avoid redundant checks.
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)

        # --- Schedule the positional verification check to run after 1ms.
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    def _check_if_truly_left(self):
        """
        Performs a forensic check of the cursor's position. This is the definitive
        method for determining if the hover-off state should be triggered.
        """
        # --- Get the current absolute X and Y coordinates of the mouse pointer.
        pointer_x = self.winfo_pointerx()
        pointer_y = self.winfo_pointery()

        # --- Get the absolute screen coordinates and dimensions of this card's master frame.
        x1 = self.winfo_rootx()
        y1 = self.winfo_rooty()
        x2 = x1 + self.winfo_width()
        y2 = y1 + self.winfo_height()

        # --- The Core Logical Check ---
        # Determine if the pointer's coordinates are outside the card's bounding box.
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)

        # If the mouse is confirmed to be outside the boundary AND the component
        # still thinks the mouse is inside...
        if is_truly_outside and self._is_mouse_inside:
            # --- Update the state to reflect the mouse is now outside.
            self._is_mouse_inside = False
            # --- Revert the visual feedback.
            self.configure(border_color=Theme.CARD)

    def _on_click(self, event=None):
        """
        Executes the stored command when any part of the card is clicked.
        """
        # The click sound is handled by the parent DashboardFrame's _safe_nav method.
        self.command()

    def reset_state(self):
        """
        [NEW] Forcibly resets the card to its default, non-hovered visual state.
        This is the public API for the parent frame to call during navigation
        to prevent a persistent hover effect.
        """
        # --- Cancel any pending leave check to prevent race conditions.
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
            self._leave_check_job = None
        # --- Forcibly reset the internal hover state.
        self._is_mouse_inside = False
        # --- Forcibly revert the visual feedback to its default state.
        self.configure(border_color=Theme.CARD)

    def update_ui_scaling(self, fonts):
        """
        [NEW] Propagates font updates and dynamically rescales the icon PNG to
        maintain visual quality and layout integrity.
        """
        self.fonts = fonts
        if self.winfo_exists():
            # --- Update text fonts ---
            self.title_lbl.configure(font=self.fonts["h2"])
            self.feat_lbl.configure(font=self.fonts["small"])

            # --- Rescale the icon image ---
            try:
                # --- Calculate the new icon size relative to the scaled H2 font size.
                # --- This ensures the icon scales proportionally with the text.
                new_font_size = self.fonts["h2"].cget("size")
                new_icon_size = int(new_font_size * 2.5) # Scaling multiplier for visual balance

                # --- Create a new CTkImage object with the updated size.
                self.icon_image = ctk.CTkImage(
                    Image.open(self.icon_path),
                    size=(new_icon_size, new_icon_size)
                )
                # --- Apply the new, rescaled image to the label.
                self.icon_lbl.configure(image=self.icon_image)
            except Exception as e:
                logging.error(f"Failed to load or resize icon '{self.icon_path}': {e}")
                # --- If loading fails, display a fallback text to prevent crashing.
                self.icon_lbl.configure(image=None, text="⚠️")


# ===================================================================================
# CLASS: _ComingSoonCard (v1.0 - Non-Interactive Placeholder Component)
#
# ARCHITECTURAL BLUEPRINT:
# This class defines a static, non-interactive placeholder card for the dashboard.
# Its sole purpose is to visually communicate that more features are planned for
# the application, managing user expectations and hinting at future value.
#
# CORE PRINCIPLES:
#   1. VISUAL SUBORDINATION: The card is intentionally styled with muted colors
#      (a slightly darker background and secondary text color) to differentiate
#      it from the active, interactive `_DashboardCard` components. It does not
#      react to hovering.
#
#   2. NON-INTERACTIVITY BY DESIGN: The card has no command callback and no event
#      bindings for clicks or hovers. It is a purely presentational element,
#      preventing any user confusion about its function.
#
#   3. STRUCTURAL CONSISTENCY: It uses the exact same internal grid structure as
#      the `_DashboardCard` to ensure it aligns perfectly within the dashboard's
#      master grid, maintaining visual harmony.
# ===================================================================================
class _ComingSoonCard(ctk.CTkFrame):
    """A static, non-interactive placeholder card for future features."""

    # The constructor for the _ComingSoonCard class.
    def __init__(self, master, fonts):
        # --- Base Class Initialization & Muted Theming ---
        # Initialize the parent CTkFrame with a darker, more subdued background
        # to visually distinguish it as a non-interactive element.
        super().__init__(
            master,
            fg_color=Theme.CARD_DARK, # Use a slightly different card color for a dull effect.
            corner_radius=20,
            border_width=2,
            border_color=Theme.NAV_RAIL, # Use a darker border to complete the muted look.
        )
        # --- Store a reference to the application's global font system.
        self.fonts = fonts

        # --- Internal Grid Configuration for Alignment ---
        # This mirrors the grid in _DashboardCard to ensure perfect alignment.
        self.columnconfigure(0, weight=1) # Horizontally center content.
        self.rowconfigure(0, weight=1)    # Vertical centering spacer.
        self.rowconfigure(1, weight=0)    # Icon row.
        self.rowconfigure(2, weight=0)    # Text row.
        self.rowconfigure(3, weight=1)    # Vertical centering spacer.

        # --- Widget Creation & Placement ---
        # The icon for this card, styled to be subtle.
        self.icon_lbl = ctk.CTkLabel(
            self,
            text="✨", # A "sparkle" emoji to hint at new things.
            font=ctk.CTkFont(size=48),
            text_color=Theme.TEXT_SECONDARY, # Use secondary text color for a muted appearance.
        )
        # Place the icon in its dedicated grid row.
        self.icon_lbl.grid(row=1, column=0, pady=(10, 5))

        # The placeholder text message.
        self.title_lbl = ctk.CTkLabel(
            self,
            text="More features\ncoming soon...!", # The specified text.
            font=self.fonts["h3"], # Use H3 font for a slightly smaller title.
            text_color=Theme.TEXT_SECONDARY, # Use secondary text color for the muted effect.
        )
        # Place the text below the icon.
        self.title_lbl.grid(row=2, column=0, pady=(5, 20))
