# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: RepairSuccessPopup (v2.0 - Architecturally Compliant)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class has been re-engineered to inherit from the BaseModalDialog engine.
# All redundant, manually implemented logic for modality, centering, and focus
# management has been excised. The class now exclusively contains its unique UI
# content, delegating all core windowing behavior to its parent, ensuring
# architectural consistency and zero code duplication.
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


class RepairSuccessPopup(BaseModalDialog):
    """
    A centered, modal, and celebratory pop-up to confirm a successful repair,
    now built upon the definitive BaseModalDialog engine.
    """
    # ===============================================================================
    # METHOD: __init__
    # The constructor now inherits from BaseModalDialog for core functionality.
    # ===============================================================================
    def __init__(self, master, fonts, on_close_callback):
        # --- Base Class Initialization: Establishes the core modal window.
        super().__init__(master, "Repair Complete!")

        # --- Store the callback to execute upon closing (e.g., UI reset).
        self.on_close_callback = on_close_callback

        # --- Window & UI Configuration ---
        self.configure(fg_color=Theme.NAV_RAIL)      # --- Use a consistent, themed background color.

        # --- Layout & UI Creation ---
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # --- Display the celebratory success message to the user.
        message = "🎉 Hooray! Your PC has been successfully repaired. Feel free to use it."
        ctk.CTkLabel(main_frame, text=message, font=fonts["h3"], text_color=Theme.TEXT, wraplength=400, justify="center").pack(pady=(20, 30))

        # --- The single, large, centered action button for user confirmation.
        ok_button = GlassButton(main_frame, text="OK", emoji="✅", font=fonts["button"], command=self.close)
        ok_button.configure(fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, border_color=Theme.SUCCESS_BORDER)
        ok_button.pack(pady=(10, 20), padx=80, fill="x", ipady=10)

        # --- Allow closing with the Enter key for accessibility.
        self.bind("<Return>", lambda e: self.close())

    # ===============================================================================
    # METHOD: close
    # Overrides the base method to execute the specific callback before closing.
    # ===============================================================================
    def close(self):
        """Executes the on-close callback, then calls the parent close method."""
        # --- Execute the specific UI reset callback required by the parent frame.
        if self.on_close_callback:
            self.on_close_callback()
        # --- Call the base class's close method to handle window destruction and event unbinding.
        super().close()


# ===================================================================================
# CLASS: CleanAllSuccessPopup (v5.0 - Architecturally Compliant)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class now inherits from the BaseModalDialog engine, offloading all common
# modality and window management logic. It retains its unique UI construction
# and dynamic messaging capabilities while eliminating redundant code and ensuring
# adherence to the application's core architectural standard.
# ===================================================================================
class CleanAllSuccessPopup(BaseModalDialog):
    """
    A truly modal, DPI-aware, and anchored pop-up that displays a professional,
    randomized success message, now built upon the definitive BaseModalDialog engine.
    """
    # ===============================================================================
    # METHOD: __init__
    # Inherits from BaseModalDialog and orchestrates UI creation.
    # ===============================================================================
    def __init__(self, master, fonts, cleaned_size_str, on_close_callback):
        # --- Base Class Initialization: Establishes the core modal window.
        super().__init__(master, "Cleanup Complete!")

        # --- Store component-specific properties.
        self.on_close_callback = on_close_callback

        # --- Window & UI Configuration ---
        self.configure(fg_color=Theme.NAV_RAIL)
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self._create_widgets(main_frame, fonts, cleaned_size_str)

        # --- Allow closing with the Enter key for accessibility.
        self.bind("<Return>", lambda e: self.close())

    # ===============================================================================
    # METHOD: _create_widgets
    # Encapsulates the unique UI construction for this specific dialog.
    # ===============================================================================
    def _create_widgets(self, master_frame, fonts, cleaned_size_str):
        """Creates and lays out all the widgets inside the pop-up, ensuring DPI-aware text wrapping."""
        # --- DPI-Aware Wraplength Calculation for resilient layout.
        wraplength = self.master_window.winfo_width() * 0.4

        # --- Dynamic Messaging ---
        professional_messages = [
            ("Hooray! 🎉 Your PC is now fully clean.", "It’s now lighter, faster, and smoother than ever before."),
            ("Mission Accomplished! 🚀 All junk has been vaporized.", "Enjoy a more responsive and efficient system experience."),
            ("Cleanup Complete! ✨ Your system's cache has been purged.", "Your PC should now feel lighter and more agile.")
        ]
        header, sub_header = random.choice(professional_messages)
        final_message_header = f"{header}\n{sub_header}"

        # --- UI Element Creation ---
        ctk.CTkLabel(master_frame, text=final_message_header, font=fonts["h3"], text_color=Theme.TEXT, wraplength=wraplength, justify="center").pack(pady=(10, 15), padx=10)
        ctk.CTkFrame(master_frame, height=2, fg_color=Theme.BORDER).pack(fill="x", padx=50, pady=10)
        ctk.CTkLabel(master_frame, text=f"✅ Total space cleaned: {cleaned_size_str}", font=fonts["bold"], text_color=Theme.SUCCESS, wraplength=wraplength, justify="center").pack(pady=(15, 20), padx=10)
        ok_button = GlassButton(master_frame, text="OK", emoji="✅", font=fonts["button"], command=self.close)
        ok_button.configure(fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, border_color=Theme.SUCCESS_BORDER)
        ok_button.pack(pady=(10, 0), padx=100, fill="x")

    # ===============================================================================
    # METHOD: close
    # Overrides the base method to execute the specific callback before closing.
    # ===============================================================================
    def close(self):
        """Executes the on-close callback, then calls the parent close method."""
        if self.on_close_callback:
            self.on_close_callback()
        super().close()
