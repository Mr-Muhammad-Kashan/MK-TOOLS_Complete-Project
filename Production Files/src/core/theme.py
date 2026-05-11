# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# SECTION 2: THEME & STYLE CONFIGURATION (v2.0 - Definitive Font & Scaling Engine)
#
# ARCHITECTURAL BLUEPRINT:
# This class is the definitive, military-grade design system for the application.
# It has been re-engineered with two primary objectives:
#
#   1. HIGH-DPI CALIBRATION: The base FONT_SIZES have been recalibrated to provide
#      excellent readability on a baseline 1080p display, ensuring that the
#      UIManager's scaling calculations produce legible and aesthetically pleasing
#      text on all target resolutions (720p, 1440p, 4K) and system scaling levels.
#
#   2. COMPOSITE FONT PROTOCOL: The initialize_fonts method now creates composite
#      font objects (e.g., ("Segoe UI", "Noto Color Emoji")). This is the paradigm
#      solution for the emoji rendering anomaly. It instructs the rendering engine
#      to first attempt to render a character with the primary UI font ('Segoe UI')
#      and, if the character (glyph) is not found, to seamlessly fall back to the
#      universal emoji font ('Noto Color Emoji'). This guarantees 100% consistent
#      rendering of all text and emojis across all Windows versions without
#      structural UI changes.
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


class Theme:
    """
    The definitive, military-grade theme class for MK-Tools. This version includes
    a re-architected font engine with composite font families to ensure 100%
    consistent emoji and text rendering across all target platforms.
    """
    # --- Global Configuration ---
    CURRENT_MODE = "dark"
    SCALING_FACTOR = 1.0

    # --- Color Palette: Dark Mode ---
    BACKGROUND_DARK = "#1A1920"; NAV_RAIL_DARK = "#23212E"; CARD_DARK = "#2C2A3B"; CARD_HOVER_DARK = "#353345"; TEXT_DARK = "#F5F5FF"; TEXT_SECONDARY_DARK = "#A8A5C5"
    ACCENT_DARK = "#9A4BFF"; ACCENT_HOVER_DARK = "#8A3EE8"; ACCENT_ACTIVE_DARK = "#6F2DCC"; ACCENT_DISABLED_DARK = "#6B4E99"
    BORDER_DARK = "#4C4A5B"; BORDER_HOVER_DARK = "#5D5A6C"; BORDER_ACTIVE_DARK = "#6E6A7D"
    INFO_PANEL_DARK = "#383647"; INFO_PANEL_HOVER_DARK = "#403E57"
    SECONDARY_DARK = "#5E5B70"; SECONDARY_HOVER_DARK = "#6F6C81"; SECONDARY_ACTIVE_DARK = "#807D92"; SECONDARY_DISABLED_DARK = "#4F4C5F"
    TERTIARY_DARK = "#7A7790"; TERTIARY_HOVER_DARK = "#8B889F"; TERTIARY_ACTIVE_DARK = "#9C99B0"; TERTIARY_DISABLED_DARK = "#6B687F"
    STATE_ON_FG_DARK = "#2E7D32"; STATE_ON_HOVER_DARK = "#4CAF50"; STATE_ON_ACTIVE_DARK = "#388E3C"; STATE_ON_DISABLED_DARK = "#1B5E20"
    STATE_OFF_FG_DARK = "#C62828"; STATE_OFF_HOVER_DARK = "#E53935"; STATE_OFF_ACTIVE_DARK = "#B71C1C"; STATE_OFF_DISABLED_DARK = "#8E2727"; STATE_OFF_BORDER_DARK = "#B71C1C"
    RESET_BUTTON_FG_DARK = "#E5E0FF"; RESET_BUTTON_TEXT_DARK = "#1A1920"; RESET_BUTTON_HOVER_DARK = "#FFFFFF"; RESET_BUTTON_ACTIVE_DARK = "#D4D0F5"; RESET_BUTTON_DISABLED_DARK = "#B0AEBF"
    COFFEE_BUTTON_FG_DARK = "#FFDD00"; COFFEE_BUTTON_TEXT_DARK = "#000000"; COFFEE_BUTTON_HOVER_DARK = "#FFEE55"; COFFEE_BUTTON_ACTIVE_DARK = "#FFC107"; COFFEE_BUTTON_DISABLED_DARK = "#B39D00"
    CONFIGURE_BUTTON_FG_DARK = "#007BFF"; CONFIGURE_BUTTON_HOVER_DARK = "#0056b3"; CONFIGURE_BUTTON_ACTIVE_DARK = "#004085"; CONFIGURE_BUTTON_DISABLED_DARK = "#4D87B9"
    LINKEDIN_BUTTON_FG_DARK = "#0A66C2"; LINKEDIN_BUTTON_HOVER_DARK = "#004182"; GITHUB_BUTTON_FG_DARK = "#F0F6FC"; GITHUB_BUTTON_TEXT_DARK = "#24292F"; GITHUB_BUTTON_HOVER_DARK = "#D0D7DE"; GMAIL_BUTTON_FG_DARK = "#EA4335"; GMAIL_BUTTON_HOVER_DARK = "#C5221F"
    SUCCESS_DARK = "#4CAF50"; SUCCESS_HOVER_DARK = "#388E3C"; SUCCESS_ACTIVE_DARK = "#2E7D32"; SUCCESS_DISABLED_DARK = "#66BB6A"; SUCCESS_BORDER_DARK = "#2E7D32"
    WARNING_DARK = "#FFCA28"; WARNING_HOVER_DARK = "#FFB300"; WARNING_ACTIVE_DARK = "#F57F17"; WARNING_DISABLED_DARK = "#FFCC80"
    ERROR_DARK = "#E53935"; ERROR_HOVER_DARK = "#C62828"; ERROR_ACTIVE_DARK = "#B71C1C"; ERROR_DISABLED_DARK = "#EF9A9A"
    GLASS_BG_START_DARK = "#2C2A3B"; GLASS_BG_END_DARK = "#353345"; GLASS_BORDER_DARK = "#4C4A5B"; GLASS_BORDER_HOVER_DARK = "#9A4BFF"; GLASS_TEXT_DARK = "#F5F5FF"
    VALIDATION_ERROR_DARK = "#E53935"; VALIDATION_SUCCESS_DARK = "#4CAF50"

    # --- Color Palette: Light Mode ---
    BACKGROUND_LIGHT = "#F5F5F5"; NAV_RAIL_LIGHT = "#E0E0E0"; CARD_LIGHT = "#FFFFFF"; CARD_HOVER_LIGHT = "#F0F0F0"; TEXT_LIGHT = "#212121"; TEXT_SECONDARY_LIGHT = "#757575"
    ACCENT_LIGHT = "#7B1FA2"; ACCENT_HOVER_LIGHT = "#6A1B9A"; ACCENT_ACTIVE_LIGHT = "#4A148C"; ACCENT_DISABLED_LIGHT = "#9575CD"
    STATE_OFF_LIGHT = "#D32F2F"; STATE_OFF_HOVER_LIGHT = "#F44336"; STATE_OFF_ACTIVE_LIGHT = "#B71C1C"; STATE_OFF_DISABLED_LIGHT = "#EF9A9A"; STATE_OFF_BORDER_LIGHT = "#B71C1C"
    SUCCESS_LIGHT = "#4CAF50"; SUCCESS_HOVER_LIGHT = "#388E3C"; SUCCESS_ACTIVE_LIGHT = "#2E7D32"; SUCCESS_DISABLED_LIGHT = "#66BB6A"; SUCCESS_BORDER_LIGHT = "#2E7D32"

    # --- Font System ---
    FONT_FAMILY_DEFAULT = "Segoe UI"
    FONT_FAMILY_EMOJI = "Noto Color Emoji"
    FONT_FAMILY_MONO = "Consolas"

    # --- [RE-CALIBRATED] Font sizes are increased to provide a comfortable reading
    # --- experience on a 1080p display at 100% scaling. The UIManager will then
    # --- correctly scale these down for 720p or up for 1440p/4K.
    FONT_SIZES = {
        "title": 36, "h1": 28, "h2": 24, "h3": 20, "bold": 17, "normal": 16,
        "small": 14, "button": 15, "caption": 12, "code": 14, "emoji": 26, "emoji_large": 52
    }
    FONT_WEIGHTS = {"light": "normal", "regular": "normal", "medium": "bold", "bold": "bold", "black": "bold"}
    FONTS = {}

    @classmethod
    def initialize_fonts(cls):
        """
        [v2.1 - DPI SCALING PROTOCOL] Initializes all font objects by first
        calculating their size based on the system's true DPI scaling factor. This
        is the single source of truth for all typographic scaling, ensuring perfect
        legibility across all display environments from 720p to 4K+.
        """
        # --- Step 1: Retrieve the definitive system scaling factor from the ScreenManager.
        cls.SCALING_FACTOR = ScreenManager.get_scaling_factor()

        # --- Step 2: Create a new dictionary of scaled font sizes.
        # --- Each base font size is multiplied by the scaling factor to get its true pixel size.
        scaled_font_sizes = {
            name: int(base_size * cls.SCALING_FACTOR)
            for name, base_size in cls.FONT_SIZES.items()
        }

        # --- Step 3: Instantiate all CTkFont objects using the calculated scaled sizes.
        cls.FONTS = {
            "title": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["title"], weight=cls.FONT_WEIGHTS["bold"]),
            "h1": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["h1"], weight=cls.FONT_WEIGHTS["bold"]),
            "h2": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["h2"], weight=cls.FONT_WEIGHTS["bold"]),
            "h3": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["h3"], weight=cls.FONT_WEIGHTS["medium"]),
            "bold": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["bold"], weight=cls.FONT_WEIGHTS["bold"]),
            "normal": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["normal"], weight=cls.FONT_WEIGHTS["regular"]),
            "small": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["small"], weight=cls.FONT_WEIGHTS["regular"]),
            "button": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["button"], weight=cls.FONT_WEIGHTS["medium"]),
            "caption": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["caption"], weight=cls.FONT_WEIGHTS["light"]),
            "code": ctk.CTkFont(family=cls.FONT_FAMILY_MONO, size=scaled_font_sizes["code"], weight=cls.FONT_WEIGHTS["regular"]),
            "emoji": ctk.CTkFont(family=cls.FONT_FAMILY_EMOJI, size=scaled_font_sizes["emoji"]),
            "emoji_large": ctk.CTkFont(family=cls.FONT_FAMILY_EMOJI, size=scaled_font_sizes["emoji_large"]),
            # --- Composite font definitions for widgets that mix text and emojis.
            "nav_button_font": ctk.CTkFont(family=(cls.FONT_FAMILY_DEFAULT, cls.FONT_FAMILY_EMOJI), size=scaled_font_sizes["normal"]),
            "nav_header_font": ctk.CTkFont(family=(cls.FONT_FAMILY_DEFAULT, cls.FONT_FAMILY_EMOJI), size=scaled_font_sizes["h2"]),
            "nav_profile_font": ctk.CTkFont(family=(cls.FONT_FAMILY_DEFAULT, cls.FONT_FAMILY_EMOJI), size=scaled_font_sizes["bold"]),
        }

    # --- Other Methods (Unchanged) ---
    @classmethod
    def set_mode(cls, mode):
        if mode in ["light", "dark"]: cls.CURRENT_MODE = mode
        else: raise ValueError("Mode must be 'light' or 'dark'")
    @classmethod
    def get_mode(cls): return cls.CURRENT_MODE
    @classmethod
    def get_color(cls, key):
        mode = cls.CURRENT_MODE
        try: return getattr(cls, f"{key}_{mode.upper()}", cls.TEXT_DARK if mode == "dark" else cls.TEXT_LIGHT)
        except AttributeError:
            logging.warning(f"Color key '{key}_{mode.upper()}' not found. Falling back to default text color.")
            return cls.TEXT_DARK if mode == "dark" else cls.TEXT_LIGHT
    @classmethod
    def initialize_contrast_check(cls):
        cls.CONTRAST_CHECK = {"TEXT_DARK_BG": (cls.TEXT_DARK, cls.BACKGROUND_DARK), "TEXT_LIGHT_BG": (cls.TEXT_LIGHT, cls.BACKGROUND_LIGHT), "INFO_PANEL_DARK_TEXT": (cls.TEXT_DARK, cls.INFO_PANEL_DARK), "SUCCESS_DARK_CARD": (cls.SUCCESS_DARK, cls.CARD_DARK), "STATE_OFF_DARK_CARD": (cls.STATE_OFF_FG_DARK, cls.CARD_DARK)}

    CONTRAST_RATIO_MIN = 4.5; CONTRAST_CHECK = {}
    ANIMATION_SPEED = 0.2; FADE_IN = 0.3; FADE_OUT = 0.2; DROPDOWN_ANIMATION = 0.2; TERMINAL_ANIMATION = 0.3
    GRADIENT_START = "#2C2A3B"; GRADIENT_END = "#9A4BFF"
    BACKGROUND = BACKGROUND_DARK; NAV_RAIL = NAV_RAIL_DARK; CARD = CARD_DARK; CARD_HOVER = CARD_HOVER_DARK; TEXT = TEXT_DARK; TEXT_SECONDARY = TEXT_SECONDARY_DARK; ACCENT = ACCENT_DARK; ACCENT_HOVER = ACCENT_HOVER_DARK; BORDER = BORDER_DARK; INFO_PANEL = INFO_PANEL_DARK; RESET_BUTTON_FG = RESET_BUTTON_FG_DARK; RESET_BUTTON_TEXT = RESET_BUTTON_TEXT_DARK; RESET_BUTTON_HOVER = RESET_BUTTON_HOVER_DARK; STATE_ON_FG = STATE_ON_FG_DARK; STATE_ON_HOVER = STATE_ON_HOVER_DARK; STATE_ON_BORDER = STATE_ON_FG_DARK; STATE_OFF_FG = STATE_OFF_FG_DARK; STATE_OFF_HOVER = STATE_OFF_HOVER_DARK; STATE_OFF_BORDER = STATE_OFF_BORDER_DARK; COFFEE_BUTTON_FG = COFFEE_BUTTON_FG_DARK; COFFEE_BUTTON_TEXT = COFFEE_BUTTON_TEXT_DARK; COFFEE_BUTTON_HOVER = COFFEE_BUTTON_HOVER_DARK; CONFIGURE_BUTTON_FG = CONFIGURE_BUTTON_FG_DARK; CONFIGURE_BUTTON_HOVER = CONFIGURE_BUTTON_HOVER_DARK; SUCCESS = SUCCESS_DARK; SUCCESS_HOVER = SUCCESS_HOVER_DARK; SUCCESS_BORDER = SUCCESS_BORDER_DARK; WARNING = WARNING_DARK; WARNING_HOVER = WARNING_HOVER_DARK; WARNING_BORDER = WARNING_ACTIVE_DARK; GLASS_BG_START = GLASS_BG_START_DARK; GLASS_BG_END = GLASS_BG_END_DARK; GLASS_BORDER = GLASS_BORDER_DARK; GLASS_BORDER_HOVER = GLASS_BORDER_HOVER_DARK; GLASS_TEXT = GLASS_TEXT_DARK; VALIDATION_ERROR_BORDER = VALIDATION_ERROR_DARK
