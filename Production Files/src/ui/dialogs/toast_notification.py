# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: InlineNotificationOverlay (v2.3 - Zero-Animation Protocol)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive version of the in-frame notification system. All scaling
# and fading animations have been completely excised and replaced with an
# instantaneous show/hide protocol. This guarantees a zero-stutter, high-performance
# user experience on all hardware tiers and eliminates visual artifacts during
# UI state transitions.
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


class InlineNotificationOverlay(ctk.CTkFrame):
    """
    A military-grade, in-frame modal notification overlay with a zero-animation
    protocol for maximum performance and stability.
    """
    def __init__(self, master, fonts: dict, title: str, message: str, emoji: str, buttons_config: list, on_close_callback: callable = None, gif_path: Optional[str] = None, rich_message: Optional[list] = None):
        # --- Base Initialization & Shield Configuration ---
        super().__init__(master, fg_color=Theme.BACKGROUND_DARK)
        # --- Store Core Properties ---
        self.master_frame = master
        self.fonts = fonts
        self.on_close_callback = on_close_callback
        # --- Central Dialog Box ---
        self.dialog_box = ctk.CTkFrame(self, fg_color=Theme.CARD, corner_radius=25, border_width=2, border_color=Theme.ACCENT)
        # --- Dialog Content Construction ---
        self._create_dialog_content(title, message, emoji, buttons_config, gif_path, rich_message)

    def _create_dialog_content(self, title: str, message: str, emoji: str, buttons_config: list, gif_path: Optional[str], rich_message: Optional[list]):
        """Dynamically creates and arranges the widgets inside the central dialog box."""
        content_frame = ctk.CTkFrame(self.dialog_box, fg_color="transparent")
        content_frame.pack(padx=40, pady=30, fill="both", expand=True)
        content_frame.grid_columnconfigure(0, weight=1)
        current_row = 0

        if gif_path:
            gif_widget = AnimatedGIFLabel(content_frame, gif_path=gif_path, size=(128, 128))
            gif_widget.grid(row=current_row, column=0, pady=(0, 15))
            gif_widget.start_animation()
            current_row += 1

        ctk.CTkLabel(content_frame, text=emoji, font=self.fonts["emoji_large"]).grid(row=current_row, column=0, pady=(0, 20))
        current_row += 1

        ctk.CTkLabel(content_frame, text=title, font=self.fonts["h2"], text_color=Theme.TEXT).grid(row=current_row, column=0, pady=(0, 10))
        current_row += 1

        if rich_message:
            message_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            message_frame.grid(row=current_row, column=0, pady=(0, 30))
            current_row += 1
            for i, (text, color) in enumerate(rich_message):
                ctk.CTkLabel(message_frame, text=text, font=self.fonts["normal"], text_color=color).pack(side="left")
        else:
            ctk.CTkLabel(content_frame, text=message, font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY, wraplength=450, justify="center").grid(row=current_row, column=0, pady=(0, 30))
            current_row += 1

        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=current_row, column=0, pady=(10, 0), sticky="ew")
        num_buttons = len(buttons_config)
        if num_buttons > 0:
            columns = tuple(range(num_buttons))
            button_frame.grid_columnconfigure(columns, weight=1)
        for i, config in enumerate(buttons_config):
            button = ctk.CTkButton(button_frame, text=config.get("text", "Button"), font=self.fonts["button"], height=40, corner_radius=15, command=lambda c=config: self._execute_button_action(c))
            self._apply_button_style(button, config.get("style", "default"))
            button.grid(row=0, column=i, padx=5, sticky="ew")

    def _apply_button_style(self, button: ctk.CTkButton, style: str):
        """Applies a predefined style to a button from the Theme class."""
        style_map = {
            "success": {"fg_color": Theme.SUCCESS, "hover_color": Theme.SUCCESS_HOVER, "border_color": Theme.SUCCESS_BORDER, "border_width": 2},
            "danger": {"fg_color": Theme.STATE_OFF_FG, "hover_color": Theme.STATE_OFF_HOVER, "border_color": Theme.STATE_OFF_BORDER, "border_width": 2},
            "warning": {"fg_color": Theme.WARNING, "hover_color": Theme.WARNING_HOVER, "border_color": Theme.WARNING_BORDER, "border_width": 2},
            "default": {"fg_color": Theme.SECONDARY_DARK, "hover_color": Theme.SECONDARY_HOVER_DARK}
        }
        button.configure(**style_map.get(style, style_map["default"]))

    def _execute_button_action(self, config: dict):
        """Executes the button's command and then closes the overlay."""
        command = config.get("command")
        if callable(command):
            command()
        self.close()

    def show(self):
        """[ZERO-ANIMATION] Instantly displays the overlay with its final geometry."""
        # --- Make the overlay visible and bring it to the front of the stacking order.
        self.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        self.lift()

        # --- Place the dialog box instantly at its final, centered position.
        # --- This eliminates the scaling animation that causes stutter.
        self.dialog_box.place(relx=0.5, rely=0.5, anchor="center")

    def _animate_entry(self):
        """
        [DEPRECATED] This method is now a placeholder and performs no action.
        The animation has been removed for performance and stability.
        """
        pass

    def close(self):
        """[ZERO-ANIMATION] Instantly destroys the widget and triggers callbacks."""
        # --- Immediately execute the on_close_callback if one was provided.
        if callable(self.on_close_callback):
            self.on_close_callback()

        # --- Instantly destroy the widget, preventing any fade-out animation.
        if self.winfo_exists():
            self.destroy()

    def _animate_exit(self):
        """
        [DEPRECATED] This method is now a placeholder and performs no action.
        The animation has been removed for performance and stability.
        """
        pass
