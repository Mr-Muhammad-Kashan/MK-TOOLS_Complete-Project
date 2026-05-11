# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: UpdateNotificationPopup (v1.0 - Zero-Defect Modality Engine)
#
# ARCHITECTURAL BLUEPRINT:
# This class defines a specialized, high-integrity modal dialog for presenting
# application update information to the user. It inherits its core unbreakable
# modality and dynamic centering from the `BaseModalDialog`, ensuring a consistent
# and professional user experience.
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


class UpdateNotificationPopup(BaseModalDialog):
    """A modal dialog to inform the user about an available application update."""

    def __init__(self, master, fonts, update_info: dict, sound_manager: Optional['SoundManager'] = None):
        super().__init__(master, "Application Update")

        self.fonts = fonts
        self.update_info = update_info
        self.sound_manager = sound_manager

        self.configure(fg_color=Theme.NAV_RAIL)
        self._create_widgets()

        if self.sound_manager:
            self.sound_manager.play_sound('notification')

    def _create_widgets(self):
        """Creates and lays out all the widgets inside the pop-up."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=20, padx=30, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(0, 15), sticky="ew")
        ctk.CTkLabel(header_frame, text="🚀", font=self.fonts["emoji_large"]).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header_frame, text="A New Version is Available!", font=self.fonts["h2"], text_color=Theme.TEXT).pack(side="left")

        version_text = f"MK-Tools v{self.update_info.get('version', 'N/A')} is ready to install."
        ctk.CTkLabel(main_frame, text=version_text, font=self.fonts["bold"], text_color=Theme.ACCENT).grid(row=1, column=0, pady=(0, 15), sticky="w")

        ctk.CTkLabel(main_frame, text="Release Notes:", font=self.fonts["bold"], text_color=Theme.TEXT_SECONDARY).grid(row=2, column=0, pady=(0, 5), sticky="w")

        notes_textbox = ctk.CTkTextbox(main_frame, font=self.fonts["normal"], fg_color=Theme.CARD, wrap="word", height=150, border_width=1, border_color=Theme.BORDER)
        notes_textbox.grid(row=3, column=0, sticky="ew", pady=(0, 20))

        release_notes = self.update_info.get('release_notes', ["No release notes provided."])
        notes_text = "\n".join([f"• {note.get('description', note) if isinstance(note, dict) else note}" for note in release_notes])
        notes_textbox.insert("end", notes_text)
        notes_textbox.configure(state="disabled")

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=4, column=0, sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # --- "Ignore" Button ---
        ctk.CTkButton(button_frame, text="Ignore", font=self.fonts["button"], command=self._on_ignore, fg_color=Theme.SECONDARY_DARK, hover_color=Theme.SECONDARY_HOVER_DARK, height=40).grid(row=0, column=0, padx=(0, 10), sticky="ew")

        # --- "Update Now" Button ---
        ctk.CTkButton(button_frame, text="Update Now", font=self.fonts["button"], command=self._on_update_now, fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, height=40).grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def _on_ignore(self):
        """Plays a sound and closes the dialog for the current session."""
        if self.sound_manager:
            self.sound_manager.play_sound('cancel_operation')
        self.close()

    def _on_update_now(self):
        """Plays a sound, opens the specific download page, and closes the dialog."""
        if self.sound_manager:
            self.sound_manager.play_sound('ok_click')

        # --- This URL now points to your specific download page as requested. ---
        download_url = "https://mr-muhammad-kashan.github.io/MK-Tools.github.io/download.html"
        webbrowser.open_new_tab(download_url)

        self.close()
