# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# PARADIGM SOLUTION: BaseModalDialog (v1.0 - Zero-Defect Modality Engine)
#
# ARCHITECTURAL BLUEPRINT:
# This new base class encapsulates all logic for creating a military-grade,
# truly modal dialog that is visually and functionally inseparable from its parent.
#
# CORE PRINCIPLES:
#   1. UNBREAKABLE MODALITY: Uses a combination of `transient`, `grab_set`, and
#      a forced-focus binding to ensure the dialog cannot be bypassed.
#   2. DYNAMIC CENTERING: Binds to the parent window's `<Configure>` event,
#      guaranteeing the dialog remains perfectly centered even if the parent is moved.
#   3. LIFECYCLE MANAGEMENT: Handles its own event unbinding and resource release
#      in a robust `close` method to prevent memory leaks.
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


class BaseModalDialog(ctk.CTkToplevel):
    """A base class for creating robust, perfectly centered, and truly modal dialogs."""

    def __init__(self, master, title: str):
        # --- Base Initialization & State Storage ---
        super().__init__(master)
        self.master_window = master
        self.configure_bind_id = None

        # --- Window Configuration: Unbreakable Modality & Stacking Protocol ---
        self.title(title)
        self.overrideredirect(True)      # Remove OS-level window decorations.
        self.transient(self.master_window) # Link this pop-up to its parent window.
        self.attributes("-topmost", True)  # Ensure the pop-up stays on top.
        self.protocol("WM_DELETE_WINDOW", self.close) # Handle attempts to close via OS.

        # --- Bind events to ensure perfect modality and positioning.
        self.after(10, self._initial_setup) # Delay setup to ensure parent is ready.

    def _initial_setup(self):
        """Finalizes setup after the event loop has started."""
        if not self.winfo_exists(): return
        self.grab_set() # CRITICAL: Block all interaction with the parent window.
        self._bind_events()
        self.update_idletasks()
        self._center_on_parent()
        self.focus_force()

    def _bind_events(self):
        """Binds events to keep the pop-up centered and focused."""
        # --- When the parent moves, re-center this pop-up. This makes it "stick".
        self.configure_bind_id = self.master_window.bind("<Configure>", self._on_parent_move, add="+")
        # --- If this window loses focus, force focus back immediately.
        self.bind("<FocusOut>", self._force_focus)
        # --- Allow closing with Escape key for accessibility.
        self.bind("<Escape>", lambda e: self.close())

    def _on_parent_move(self, event=None):
        """Callback to re-center the pop-up when the parent window is moved or resized."""
        if self.winfo_exists() and self.master_window.winfo_exists():
            self._center_on_parent()

    def _center_on_parent(self):
        """Calculates and sets the pop-up's geometry to be perfectly centered on its parent."""
        self.update_idletasks() # Ensure window dimensions are current.
        master_x = self.master_window.winfo_rootx()
        master_y = self.master_window.winfo_rooty()
        master_width = self.master_window.winfo_width()
        master_height = self.master_window.winfo_height()
        popup_width = self.winfo_width()
        popup_height = self.winfo_height()
        # --- Centering Calculation ---
        popup_x = master_x + (master_width - popup_width) // 2
        popup_y = master_y + (master_height - popup_height) // 2
        self.geometry(f"+{popup_x}+{popup_y}") # Apply the calculated centered position.
        self.lift() # Bring the window to the front of the stacking order.

    def _force_focus(self, event=None):
        """Prevents the pop-up from losing focus, ensuring unbreakable modality."""
        if self.winfo_exists():
            self.focus_force()
            self.grab_set()

    def close(self):
        """Safely closes the dialog, unbinds events, and destroys the window."""
        # --- CRITICAL: Unbind the <Configure> event from the parent to prevent memory leaks.
        if self.configure_bind_id and self.master_window.winfo_exists():
            try:
                self.master_window.unbind("<Configure>", self.configure_bind_id)
            except tk.TclError:
                pass # --- Ignore error if the binding is already gone.
        self.grab_release() # --- Release the modal grab.
        self.destroy()      # --- Destroy the pop-up window.
