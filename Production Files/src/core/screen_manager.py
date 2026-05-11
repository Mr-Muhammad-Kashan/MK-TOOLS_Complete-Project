# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# -----------------------------------------------------------------------------------
# ===================================================================================
# CLASS: ScreenManager (v3.0 - Definitive DPI Scaling & Centering Protocol)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This version is the definitive, military-grade authority for all screen and DPI-
# related operations. It establishes a new paradigm for UI scaling by acting as the
# single source of truth for the system's DPI scaling factor.
#
# CORE ENHANCEMENTS:
#   1. [DPI SCALING FACTOR] A new static method, `get_scaling_factor`, has been
#      engineered to directly query the Windows API for the primary monitor's DPI.
#      This provides the ground-truth scaling value (e.g., 1.0 for 100%, 1.5 for 150%)
#      that all other UI components will use for geometry and font size calculations.
#
#   2. [PERFORMANCE] The scaling factor is calculated once and cached in a class-
#      level variable (`_scaling_factor`). This zero-overhead approach ensures that
#      all subsequent calls to `get_scaling_factor` are instantaneous, preventing
#      redundant and costly API queries.
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


class ScreenManager:
    """
    A definitive utility class providing static methods for all screen-related
    operations, including DPI awareness, scaling factor retrieval, and window centering.
    """
    # --- A private, class-level cache for the scaling factor to ensure it's calculated only once.
    _scaling_factor: float = 0.0

    @staticmethod
    def set_dpi_awareness():
        """
        Sets the application's process to be DPI-aware. This is a critical
        step that must be called before any UI is initialized to ensure correct
        scaling and geometry calculations on high-resolution displays.
        """
        try:
            # --- Attempt to use the most modern API for DPI awareness (Windows 8.1+).
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            logging.info("DPI Awareness set to: PROCESS_PER_MONITOR_DPI_AWARE.")
        except (AttributeError, OSError):
            # --- If the modern API is not available, fall back to the older API (Windows Vista+).
            try:
                ctypes.windll.user32.SetProcessDPIAware()
                logging.info("DPI Awareness set to: SetProcessDPIAware().")
            except Exception as e:
                # --- Log an error if neither method is successful.
                logging.error(f"Failed to set DPI awareness: {e}", exc_info=True)

    @staticmethod
    def get_scaling_factor() -> float:
        """
        [NEW] Retrieves the system's UI scaling factor by querying the primary monitor's DPI.
        The result is cached for performance. This is the single source of truth for all UI scaling.

        Returns:
            float: The UI scaling factor (e.g., 1.0 for 100%, 1.25 for 125%).
        """
        # --- If the scaling factor has already been calculated, return the cached value instantly.
        if ScreenManager._scaling_factor > 0:
            return ScreenManager._scaling_factor

        try:
            # --- Call the Windows User32 API to get the DPI for the primary screen (HWND 0).
            # --- The default DPI is 96.
            dpi = ctypes.windll.user32.GetDpiForWindow(0)
            # --- Calculate the scaling factor relative to the 96 DPI baseline.
            scaling = dpi / 96.0
            # --- If the calculated scaling is nonsensical, default to a safe value of 1.0.
            if scaling <= 0:
                scaling = 1.0
            # --- Cache the calculated scaling factor.
            ScreenManager._scaling_factor = scaling
            logging.info(f"System DPI detected as {dpi}. UI scaling factor set to {scaling:.2f}.")
            return scaling
        except Exception as e:
            # --- In case of any error, log it and fall back to a default, unscaled factor.
            logging.error(f"Failed to get system DPI scaling factor. Defaulting to 1.0. Error: {e}")
            # --- Cache the fallback value to prevent repeated errors.
            ScreenManager._scaling_factor = 1.0
            return 1.0

    @staticmethod
    def center_window(window: ctk.CTk | ctk.CTkToplevel, width: int, height: int):
        """
        Calculates the precise x and y coordinates to center a window on the main display.
        This method will return accurate results only after `set_dpi_awareness()` has been called.

        Args:
            window (ctk.CTk | ctk.CTkToplevel): The window object to be centered.
            width (int): The target width of the window.
            height (int): The target height of the window.
        """
        # --- These methods now return true physical pixel dimensions thanks to DPI awareness.
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # --- Calculate the top-left corner coordinates for perfect centering.
        center_x = int((screen_width / 2) - (width / 2))
        center_y = int((screen_height / 2) - (height / 2))

        # --- Apply the calculated geometry to the window.
        window.geometry(f"{width}x{height}+{center_x}+{center_y}")


# ===================================================================================
# SECTION 3: DYNAMIC FONT & UI SCALING ENGINE
# This manager handles the intelligent resizing of all text and UI elements.
# ===================================================================================
class UIManager:
    """
    Manages dynamic scaling of fonts and UI elements based on window size.
    [v2.0 CORRECTION]: This class no longer creates its own fonts. It now directly
    references and modifies the master font dictionary from the Theme class,
    ensuring all components have access to the complete, correct set of fonts.
    """
    def __init__(self, app_instance):
        # --- Store a reference to the main application instance.
        self.app = app_instance

        # --- Define the dimensional parameters for scaling calculations.
        self.base_width = 1280
        self.min_width = 800
        self.max_width = 3840

        # --- [CRITICAL FIX] Get a direct reference to the master font dictionary from the Theme class.
        # --- This ensures the UIManager uses the single source of truth for all fonts, including custom emoji fonts.
        self.fonts = Theme.FONTS

        # --- Debounce timer to prevent performance issues during rapid resizing.
        self.debounce_timer = None

        # --- Bind the resize event to the debounced scaling handler.
        self.app.bind("<Configure>", self._on_resize_debounce)

    def _on_resize_debounce(self, event=None):
        """Debounces the resize event to prevent lag and excessive recalculations."""
        # --- If a timer is already scheduled, cancel it.
        if self.debounce_timer:
            self.app.after_cancel(self.debounce_timer)
        # --- Schedule the update_scaling method to run after a 100ms pause in resizing.
        self.debounce_timer = self.app.after(100, self.update_scaling)

    def update_scaling(self):
        """
        [RE-ENGINEERED] This method no longer calculates scaling factors. Font
        scaling is now handled definitively by the Theme class at startup. This
        method's sole responsibility is to propagate UI update notifications to
        all registered content frames during a resize event, allowing them to
        adjust their own geometry if necessary.
        """
        # --- Propagate the scaling update notification to all content frames and the navigation rail.
        # --- This allows child components to perform their own geometry updates without
        # --- re-calculating font sizes, eliminating the primary source of the scaling bug.
        for frame in self.app.content_frames.values():
            if hasattr(frame, "update_ui_scaling"):
                frame.update_ui_scaling(self.fonts)
        if hasattr(self.app.navigation_rail, "update_ui_scaling"):
            self.app.navigation_rail.update_ui_scaling(self.fonts)
