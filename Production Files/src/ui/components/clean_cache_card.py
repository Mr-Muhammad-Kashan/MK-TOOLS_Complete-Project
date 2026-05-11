# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# DEFINITIVE CleanCacheCard Class (v2.7 - Feature-Specific Hover Sound)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component's auditory feedback protocol has been upgraded to provide a more
# distinct user experience.
#
# CORE ENHANCEMENTS:
#   1. FEATURE-SPECIFIC HOVER: The stateful hover protocol's `_on_enter` method
#      is now wired to dispatch the new 'feature_hover' sound event. This
#      distinguishes the hover sound for these cards from all other hoverable
#      elements in the application, fulfilling the user's directive for a unique
#      auditory cue.
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


class CleanCacheCard(ctk.CTkFrame):
    """
    An interactive card for a single cache category, re-architected to delegate
    all cleanup operations to its parent frame's master logic controller.
    """
    def __init__(self, master, fonts, task_data: dict, sound_manager: Optional['SoundManager'] = None):
        # --- Base Initialization: Set up the card's visual frame.
        super().__init__(master, fg_color=Theme.CARD, corner_radius=20, border_width=1, border_color=Theme.CARD)

        # --- Property and State Storage ---
        self.master_frame = master                      # --- Store a reference to the parent frame (CleanCacheFrame).
        self.fonts = fonts                              # --- Store the application's font dictionary.
        self.task_data = task_data                      # --- Store the dictionary containing all data for this specific cleanup task.
        self.sound_manager = sound_manager              # --- Store a reference to the global sound manager.
        self.is_info_expanded = False                   # --- State flag for the informational dropdown panel.
        self.info_frame = None                          # --- Placeholder for the info panel widget.
        self._is_mouse_inside = False                   # --- State flag for the robust hover detection protocol.
        self._leave_check_job = None                    # --- Placeholder for the scheduled hover-leave check.

        # --- UI Construction ---
        self.grid_columnconfigure(0, weight=1)          # --- Allow the content to center itself horizontally.
        self._setup_ui(task_data)                       # --- Build all the child widgets for the card.
        self._bind_events()                             # --- Bind all necessary mouse events for interactivity.

    def _setup_ui(self, task_data: dict):
        """Sets up the card's primary UI components from the task data dictionary."""
        # --- Create a transparent main frame to hold all content with consistent padding.
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(1, weight=1) # --- Allow the text column to expand.

        # --- Create the emoji label.
        self.emoji_label = ctk.CTkLabel(self.main_frame, text=task_data['emoji'], font=("Arial", 24))
        self.emoji_label.grid(row=0, rowspan=2, column=0, padx=15, pady=10)

        # --- Create the title label.
        self.title_label = ctk.CTkLabel(self.main_frame, text=task_data['title'], font=self.fonts["bold"], text_color=Theme.TEXT)
        self.title_label.grid(row=0, column=1, sticky="w")

        # --- Create the description label.
        self.desc_label = ctk.CTkLabel(self.main_frame, text=task_data['description'], font=self.fonts["small"], text_color=Theme.TEXT_SECONDARY)
        self.desc_label.grid(row=1, column=1, sticky="w")

        # --- Create a frame to hold the action buttons on the right side.
        self.controls_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.controls_frame.grid(row=0, rowspan=2, column=2, padx=15)
        self.controls_frame.grid_columnconfigure((0, 1), weight=1) # --- Allow buttons to have consistent spacing.

        # --- The clean button's command now delegates the action to the parent frame's logic controller.
        self.clean_button = ctk.CTkButton(self.controls_frame, text="Clean", font=self.fonts["button"], height=35, corner_radius=10, fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, border_color=Theme.SUCCESS_BORDER, border_width=2, command=self.start_cleanup)
        self.clean_button.grid(row=0, column=0, padx=2, pady=5, sticky="ew")

        # --- The info button toggles the visibility of the info panel.
        self.info_button = ctk.CTkButton(self.controls_frame, text="What is it?", font=self.fonts["button"], height=35, corner_radius=10, fg_color=Theme.RESET_BUTTON_FG, text_color=Theme.RESET_BUTTON_TEXT, hover_color=Theme.RESET_BUTTON_HOVER, border_width=2, border_color=Theme.BORDER, command=self.toggle_info_panel)
        self.info_button.grid(row=0, column=1, padx=2, pady=5, sticky="ew")

    def start_cleanup(self):
        """Plays the click sound and delegates the cleanup operation to the parent frame."""
        # --- Play the sound for a manual, single-item clean action.
        if self.sound_manager: self.sound_manager.play_sound('manual_clean')
        # --- Command the parent frame to execute the cleanup for the task associated with this card.
        self.master_frame.start_manual_cleanup(self)

    def _bind_events(self):
        """Binds events recursively to all child widgets for a unified interaction surface."""
        # --- This list ensures that hovering over any part of the card triggers the hover effect.
        all_widgets = [self, self.main_frame, self.emoji_label, self.title_label, self.desc_label, self.controls_frame, self.clean_button, self.info_button]
        for widget in all_widgets:
            widget.bind("<Enter>", self._on_enter, add="+")
            widget.bind("<Leave>", self._on_leave, add="+")

    def _on_enter(self, event=None):
        """Handles the mouse entering ANY part of the card, triggering the hover-on action exactly once."""
        # --- If a "leave" check is pending, cancel it, as the mouse is still inside the component.
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        # --- Only trigger the hover-on effect if the mouse is not already flagged as being inside.
        if not self._is_mouse_inside:
            # --- Set the state flag to True to prevent sound/visual spam.
            self._is_mouse_inside = True
            # --- Play the specific hover sound for this feature type.
            if self.sound_manager: self.sound_manager.play_sound('feature_hover')
            # --- Activate the visual border highlight.
            self.configure(border_color=Theme.GLASS_BORDER_HOVER)

    def _on_leave(self, event=None):
        """Schedules a delayed check to verify if the mouse has truly exited the component's boundary."""
        # --- Cancel any previously scheduled check to avoid redundant calls.
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        # --- Schedule the forensic check to run after 1 millisecond.
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    def _check_if_truly_left(self):
        """Performs a definitive check of the cursor's position to trigger the hover-off state correctly."""
        # --- Get the absolute screen coordinates of the mouse pointer.
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        # --- Get the absolute screen coordinates of the card's bounding box.
        x1, y1 = self.winfo_rootx(), self.winfo_rooty()
        x2, y2 = x1 + self.winfo_width(), y1 + self.winfo_height()
        # --- Determine if the pointer is outside the bounding box.
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)
        # --- If the mouse is confirmed outside and the state is still 'inside', reset the state.
        if is_truly_outside and self._is_mouse_inside:
            self._is_mouse_inside = False
            self.configure(border_color=Theme.CARD)

    def toggle_info_panel(self):
        """Notifies the parent frame to manage panels, then toggles this card's info panel."""
        # --- Step 1: Notify the parent frame (CleanCacheFrame) that this card is being toggled.
        # --- The parent frame will handle closing any other open panels.
        self.master_frame.manage_info_panels(self)

        # --- Step 2: Play the "what is it" sound only if the panel is about to be opened.
        if not self.is_info_expanded and self.sound_manager:
            self.sound_manager.play_sound('what_is_it')

        # --- Step 3: Lazily create the info frame if it doesn't exist.
        if self.info_frame is None:
            self._create_info_panel()

        # --- Step 4: Toggle the internal state flag.
        self.is_info_expanded = not self.is_info_expanded

        # --- Step 5: Show or hide the info frame based on the new state.
        if self.is_info_expanded:
            self.info_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        else:
            self.info_frame.grid_forget()

    def _create_info_panel(self):
        """Lazily creates the rich-text info panel from the task's data dictionary."""
        # --- Create the panel frame.
        self.info_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        self.info_frame.grid_columnconfigure(0, weight=1)
        # --- Define helper functions to populate the panel with styled text.
        def add_info_label(text, font_key="bold", color_key="TEXT"): ctk.CTkLabel(self.info_frame, text=text, font=self.fonts[font_key], text_color=getattr(Theme, color_key)).pack(padx=20, pady=(15, 5), anchor="w")
        def add_info_detail(text, wraplength=400, color_key="TEXT_SECONDARY"): ctk.CTkLabel(self.info_frame, text=text, font=self.fonts["normal"], text_color=getattr(Theme, color_key), wraplength=wraplength, justify="left").pack(padx=20, pady=2, anchor="w")
        # --- Get the info dictionary from the main task data.
        info = self.task_data.get('info', {})
        # --- Populate the panel.
        add_info_label("Details"); add_info_detail(info.get('details', 'No details available.'))
        add_info_label("Pros", color_key="SUCCESS");
        for pro in info.get('pros', ['Not applicable.']): add_info_detail(f"• {pro}", color_key="SUCCESS")
        add_info_label("Cons", color_key="STATE_OFF_FG");
        for con in info.get('cons', ['None.']): add_info_detail(f"• {con}", color_key="STATE_OFF_FG")
        add_info_label(f"Safety Rating: {info.get('safety_rating', 'Unknown')}")

    def close_info_panel(self):
        """A direct, non-toggling command to forcibly close the info panel."""
        # --- This is a direct command, not a toggle. It only acts if the panel is currently open.
        if self.is_info_expanded:
            # --- Hide the info frame widget from the grid.
            if self.info_frame:
                self.info_frame.grid_forget()
            # --- Set the internal state flag to closed.
            self.is_info_expanded = False

    def revert_button_state(self):
        """Resets the 'Clean' button to its default state after a timed 'Cleaned' message."""
        if self.winfo_exists():
            self.clean_button.configure(fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, text="Clean", state="normal")
