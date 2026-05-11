# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

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


class ConfigDialog(BaseModalDialog):
    """A modal dialog for user input with validation, refactored for architectural purity."""
    def __init__(self, master, fonts, title, prompt, callback, validation_type='numeric'):
        # --- Initialize the BaseModalDialog with core properties ---
        super().__init__(master, title)
        # --- Store class-specific properties ---
        self.callback = callback
        self.validation_type = validation_type

        # --- Window & UI Configuration ---
        self.configure(fg_color=Theme.NAV_RAIL)
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)

        # --- UI Elements ---
        ctk.CTkLabel(self, text=prompt, font=fonts["normal"]).pack(pady=(20, 10))

        vcmd = (self.register(self._validate_char), '%P')
        self.entry = ctk.CTkEntry(self, font=fonts["normal"], width=250, border_color=Theme.BORDER,
                                  validate='key', validatecommand=vcmd)
        self.entry.pack(pady=10)
        self.entry.focus()

        self.error_label = ctk.CTkLabel(self, text="", text_color=Theme.VALIDATION_ERROR_BORDER, font=fonts["small"])
        self.error_label.pack(pady=5)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Enter", font=fonts["button"], command=self._on_enter, width=120).pack(side="left", padx=10)

        ctk.CTkButton(button_frame, text="Close", font=fonts["button"],
                      fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER,
                      command=self.close, width=120).pack(side="left", padx=10)

        self.bind("<Return>", lambda event: self._on_enter())

        # --- This call ensures the final geometry is known before centering. ---
        self.update_idletasks()
        self.geometry(f"{max(450, self.winfo_reqwidth())}x{self.winfo_reqheight()+40}")

    def _on_enter(self):
        value = self.entry.get()
        if self._validate_final(value):
            self.callback(value)
            self.close()
        else:
            self._flash_error()

    def _validate_char(self, new_value):
        if new_value == "": return True
        try:
            num = int(new_value)
            if self.validation_type == 'percentage':
                if len(new_value) > 3 or num > 100: return False
            return True
        except ValueError:
            return False

    def _validate_final(self, value):
        if not value: return False
        try:
            num = int(value)
            if self.validation_type == 'percentage':
                return 1 <= num <= 100
            return True
        except ValueError:
            return False

    def _flash_error(self):
        self.entry.configure(border_color=Theme.VALIDATION_ERROR_BORDER)
        if self.validation_type == 'percentage':
            self.error_label.configure(text="Value must be between 1-100.")
        else:
            self.error_label.configure(text="Invalid input.")
        self.after(2000, lambda: [
            self.entry.configure(border_color=Theme.BORDER),
            self.error_label.configure(text="")
        ])
