# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# SECTION 7: CONTENT FRAMES & PAGE DEFINITIONS
# Each class represents a different screen accessible from the navigation rail.
# ===================================================================================
# ===================================================================================
# CLASS: BaseContentFrame (v2.0 - Zero-Animation Stability Protocol)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class has been re-engineered to provide a paradigm solution for UI stability
# across all hardware configurations, from low-end legacy systems to high-performance
# workstations. The previous, resource-intensive animation protocol has been
# completely excised and replaced with an instantaneous widget placement model.
#
# CORE ENHANCEMENTS:
#   1. [STABILITY] Animation Elimination: The `run_entry_animation` method no longer
#      interfaces with the `AnimationEngine`. The logic that animated the `pady`
#      grid property—the direct cause of visual stutter and artifacts—has been
#      removed.
#
#   2. [PERFORMANCE] Instantaneous Placement: The new `run_entry_animation` method
#      now places all child 'card' widgets onto the grid instantly with their final,
#      static padding. This is a zero-cost rendering operation that guarantees a
#      flawless, flicker-free user experience.
#
#   3. [INHERITANCE] Universal Fix: By modifying the superclass, this stability
#      protocol is automatically inherited by all content frames (`PerformanceFrame`,
#      `UITweaksFrame`, `FixWindowsFrame`, etc.), solving the problem at its
#      foundational level.
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


class BaseContentFrame(ctk.CTkScrollableFrame):
    """A base class for content frames to handle shared functionality."""
    def __init__(self, master, fonts):
        # --- Initialize the parent CTkScrollableFrame with transparent background and no corner radius.
        super().__init__(master, fg_color="transparent", corner_radius=0)
        # --- Configure the first column (index 0) to expand and fill all available horizontal space.
        self.grid_columnconfigure(0, weight=1)
        # --- Store the application-wide font dictionary for use by child elements.
        self.fonts = fonts
        # --- Initialize an empty list to hold references to all child 'card' widgets.
        self.cards = []
        # --- Initialize a placeholder for the frame's main header label.
        self.header_label = None

    def run_entry_animation(self):
            """
            [RE-ARCHITECTED FOR UNIVERSAL STABILITY] Places all cards instantly
            without animation to guarantee zero flicker, stutter, or visual artifacts
            on all hardware tiers, from low-end to high-end systems. This is the
            definitive solution for maximum UI responsiveness and stability.
            """
            # --- Iterate through all registered card widgets in this frame's list.
            for card in self.cards:
                # --- Instantly place the card onto the grid with its final, static padding.
                # --- This bypasses any animation engine, eliminating all performance
                # --- overhead and potential rendering glitches.
                card.grid_configure(pady=10)

    def update_ui_scaling(self, fonts):
        """Propagates font updates to all child cards."""
        # --- Update the internal font dictionary with the new scaled font objects.
        self.fonts = fonts
        # --- If a header label exists, update its font.
        if self.header_label: self.header_label.configure(font=fonts["title"])
        # --- Iterate through all child cards.
        for card in self.cards:
            # --- Check if the card has an `update_ui_scaling` method and call it to propagate the change.
            if hasattr(card, "update_ui_scaling"): card.update_ui_scaling(fonts)
