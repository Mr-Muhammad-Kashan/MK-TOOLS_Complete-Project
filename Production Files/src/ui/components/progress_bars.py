# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# SNIPPET 1: New CleanAllProgressBar Class
# A dedicated progress bar widget styled to match the provided image specification.
# It includes a dynamic percentage label and a themed progress bar.
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


class CleanAllProgressBar(ctk.CTkFrame):
    """A progress bar widget with a percentage label, styled to specification."""
    def __init__(self, master, fonts):
        # --- Base Initialization ---
        # Initialize the parent frame. It's transparent to blend with the background.
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1) # Allow the progress bar to expand.

        # --- UI Components ---
        # The percentage label, positioned to the left of the bar as per the image.
        self.label = ctk.CTkLabel(self, text="0%", font=fonts["h2"], text_color=Theme.TEXT)
        self.label.grid(row=0, column=0, padx=(0, 15), sticky="w")

        # The progress bar, styled to match the visual reference.
        self.progress_bar = ctk.CTkProgressBar(
            self,
            orientation="horizontal",
            mode="determinate",
            height=30,
            corner_radius=15,  # Creates the pill shape.
            border_width=2,
            border_color=Theme.SUCCESS_BORDER, # Green border.
            fg_color=Theme.CARD, # Background of the bar.
            progress_color=Theme.SUCCESS # The green fill color.
        )
        self.progress_bar.set(0) # Start at 0%.
        self.progress_bar.grid(row=0, column=1, sticky="ew")

    def set_progress(self, value: float):
        """
        Updates the progress bar and percentage label.
        - value: A float between 0.0 and 1.0.
        """
        if self.winfo_exists():
            # Update the progress bar's visual fill.
            self.progress_bar.set(value)
            # Update the text label, formatted as an integer percentage.
            self.label.configure(text=f"{int(value * 100)}%")
