# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: ResultPopup (v2.0 - Architecturally Compliant)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# Re-architected to inherit from BaseModalDialog. All duplicated modality and
# windowing logic has been removed, resulting in a cleaner, more maintainable
# component that conforms to the project's architectural standard.
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


class ResultPopup(BaseModalDialog):
    """
    A centered, modal pop-up for displaying scan results, now built upon the
    definitive BaseModalDialog engine.
    """
    # ===============================================================================
    # METHOD: __init__
    # Inherits from BaseModalDialog and orchestrates UI creation.
    # ===============================================================================
    def __init__(self, master, fonts, message, on_close_callback):
        # --- Base Class Initialization: Establishes the core modal window.
        super().__init__(master, "Scan Result")

        # --- Store component-specific properties.
        self.fonts = fonts
        self.on_close_callback = on_close_callback

        # --- Window & UI Configuration ---
        self.configure(fg_color="#353345")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Message Label ---
        label = ctk.CTkLabel(self, text=message, font=self.fonts["normal"], text_color=Theme.TEXT, wraplength=450, justify="center")
        label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="nsew")

        # --- OK Button ---
        ok_button = GlassButton(self, text="OK", emoji="", font=self.fonts["button"], command=self.close)
        ok_button.configure(fg_color="#4B0082", hover_color="#353345", text_color=Theme.GLASS_TEXT, border_color=Theme.GLASS_BORDER, border_width=8, corner_radius=8)
        ok_button.grid(row=1, column=0, pady=(0, 20), padx=50, sticky="ew")

        # --- Allow closing with the Enter key for accessibility.
        self.bind("<Return>", lambda e: self.close())

        # --- Finalize geometry before centering.
        self.update_idletasks()
        self.geometry(f"500x{self.winfo_reqheight()}")


    # ===============================================================================
    # METHOD: close
    # Overrides the base method to execute the specific callback before closing.
    # ===============================================================================
    def close(self):
        """Executes the on-close callback, then calls the parent close method."""
        if self.on_close_callback and callable(self.on_close_callback):
            self.on_close_callback()
        super().close()

    # ===============================================================================
    # METHOD: update_ui_scaling
    # Propagates font scaling updates to child widgets.
    # ===============================================================================
    def update_ui_scaling(self, fonts):
        """Updates font scaling for the pop-up’s UI elements."""
        self.fonts = fonts
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(font=fonts["normal"])
            elif isinstance(widget, GlassButton):
                widget.configure(font=fonts["button"])


# ===================================================================================
# CLASS: ResultPopupWithFix (v2.0 - Architecturally Compliant)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# Re-architected to inherit from BaseModalDialog. This version retains its unique
# dual-button layout and fix callback logic while delegating all core windowing
# behavior to the base class for architectural purity and maintainability.
# ===================================================================================
class ResultPopupWithFix(BaseModalDialog):
    """A modal dialog with a 'Fix Now' option, built on the BaseModalDialog engine."""

    # ===============================================================================
    # METHOD: __init__
    # Inherits from BaseModalDialog and orchestrates UI creation.
    # ===============================================================================
    def __init__(self, master, fonts, message, on_close_callback, fix_callback):
        # --- Base Class Initialization: Establishes the core modal window.
        super().__init__(master, "DISM Scan Result")

        # --- Store component-specific properties.
        self.fonts = fonts
        self.on_close_callback = on_close_callback
        self.fix_callback = fix_callback

        # --- Window & UI Configuration ---
        self.configure(fg_color="#353345")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Message Label ---
        label = ctk.CTkLabel(self, text=message, font=self.fonts["normal"], text_color=Theme.TEXT, wraplength=450, justify="center")
        label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="nsew")

        # --- Button Container Frame ---
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # --- Fix Now Button ---
        fix_button = GlassButton(button_frame, text="Fix Now", emoji="🛠️", font=self.fonts["button"], command=self._on_fix_now)
        fix_button.configure(fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, border_color=Theme.SUCCESS_BORDER)
        fix_button.grid(row=0, column=0, padx=10, sticky="ew")

        # --- Close Button ---
        close_button = GlassButton(button_frame, text="Close", emoji="❌", font=self.fonts["button"], command=self.close)
        close_button.configure(fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, border_color=Theme.STATE_OFF_BORDER)
        close_button.grid(row=0, column=1, padx=10, sticky="ew")

        # --- Finalize geometry before centering.
        self.update_idletasks()
        self.geometry(f"500x{self.winfo_reqheight()}")

    # ===============================================================================
    # METHOD: _on_fix_now
    # Executes the fix callback and then closes the dialog.
    # ===============================================================================
    def _on_fix_now(self):
        """Executes the repair action and closes the dialog."""
        if self.fix_callback:
            self.fix_callback()
        # --- Do not call super().close() here, call self.close() to ensure the on_close_callback also runs.
        self.close()

    # ===============================================================================
    # METHOD: close
    # Overrides the base method to execute the specific callback before closing.
    # ===============================================================================
    def close(self):
        """Executes the on-close callback, then calls the parent close method."""
        if self.on_close_callback and callable(self.on_close_callback):
            self.on_close_callback()
        super().close()

    # ===============================================================================
    # METHOD: update_ui_scaling
    # Propagates font scaling updates to child widgets.
    # ===============================================================================
    def update_ui_scaling(self, fonts):
        """Updates font scaling for the pop-up’s UI elements."""
        self.fonts = fonts
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(font=fonts["normal"])
            elif isinstance(widget, ctk.CTkFrame):
                for btn in widget.winfo_children():
                    if isinstance(btn, GlassButton):
                        btn.configure(font=fonts["button"])
