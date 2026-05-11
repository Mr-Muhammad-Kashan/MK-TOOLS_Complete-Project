# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: TerminalWidget (v6.0 - Futuristic Glassy 3D Terminal)
#
# ARCHITECTURAL BLUEPRINT:
# The TerminalWidget class is a specialized, read-only CTkTextbox designed to emulate
# a futuristic, glassy, 3D terminal interface for displaying real-time command output.
# It leverages the customtkinter library for a modern, visually appealing UI with
# dynamic hover effects and thread-safe text operations. The class supports regex-based
# exact matching and fuzzy matching (via fuzzywuzzy) for analyzing command output,
# making it ideal for real-time system monitoring or command execution feedback.
# Key features include thread-safe text appending, auto-scrolling, dynamic font scaling,
# and robust error handling for text analysis. The widget is lifecycle-aware, ensuring
# stability during destruction, and adheres to a modular, reusable design paradigm.
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


class TerminalWidget(ctk.CTkTextbox):
    """A futuristic, glassy, 3D terminal widget for displaying real-time command output."""
    def __init__(self, master, fonts):
        super().__init__(
            master,
            font=fonts["normal"],
            fg_color=Theme.GLASS_BG_START,
            border_color=Theme.GLASS_BORDER,
            border_width=2,
            corner_radius=20,
            wrap="word",
            height=300,
            text_color=Theme.TEXT,
            state="disabled"  # Read-only
        )
        self.grid_columnconfigure(0, weight=1)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.is_accepting_input = True

    def _on_enter(self, event):
        """Apply hover effect with animated border."""
        self.configure(border_color=Theme.GLASS_BORDER_HOVER)

    def _on_leave(self, event):
        """Revert border on leave."""
        self.configure(border_color=Theme.GLASS_BORDER)

    def append_text(self, text):
        """Appends text to the terminal in a thread-safe manner."""
        if not self.is_accepting_input or not self.winfo_exists():
            return
        self.configure(state="normal")
        self.insert("end", text + "\n")
        self.see("end")  # Auto-scroll to the latest output
        self.configure(state="disabled")

    def clear(self):
        """Clears the terminal content."""
        if not self.winfo_exists():
            return
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.configure(state="disabled")

    def update_ui_scaling(self, fonts):
        """Updates font for the terminal."""
        self.configure(font=fonts["normal"])

    def exact_match(self, line: str) -> Optional[str]:
        """
        Performs an exact regex match for key phrases in a line.

        Args:
            line (str): The line to search.

        Returns:
            Optional[str]: The matching result key or None.
        """
        try:
            for result_key, pattern in self.compiled_patterns.items():
                if pattern.search(line):
                    return result_key
            return None
        except Exception as e:
            logging.error(f"Error in exact match for line '{line}': {e}", exc_info=True)
            return None

    def fuzzy_match(self, line: str, threshold: int = 90) -> Optional[str]:
        """
        Performs a fuzzy match for key phrases using fuzzywuzzy.

        Args:
            line (str): The line to search.
            threshold (int): Minimum score for a match (0-100).

        Returns:
            Optional[str]: The matching result key or None.
        """
        try:
            for result_key, phrase in self.key_phrases.items():
                score = fuzz.ratio(line, phrase)
                if score >= threshold:
                    logging.debug(f"Fuzzy match for '{line}' with '{phrase}' (score: {score})")
                    return result_key
            return None
        except Exception as e:
            logging.error(f"Error in fuzzy match for line '{line}': {e}", exc_info=True)
            return None
