# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: FontManager (v2.0 - Zero-Defect Typographic Asset Protocol)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class is the definitive, self-contained authority for all custom font
# loading operations. It has been re-engineered for absolute robustness. The new
# protocol includes a pre-flight file existence check for precise error reporting
# and a more granular exception handling sequence. This ensures that in a failure
# scenario, the system can provide a forensically accurate reason for termination
# (e.g., "file missing" vs. "file corrupt"), which is critical for rapid
# diagnostics and field support. The synchronous nature of this operation is
# intentional and mandatory to prevent visual integrity failures during UI rendering.
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


class FontManager:
    """A static utility class for managing and registering custom application fonts."""

    # --- FONT MANIFEST ---
    # The definitive, exclusive list of all critical typographic assets required
    # for the application's visual and functional integrity.
    REQUIRED_FONTS: List[str] = [
        "assets", "fonts", "NotoColorEmoji-Regular.ttf"
    ]

    # ===============================================================================
    # METHOD: _load_single_font (v1.0 - Atomic Font Loader)
    # This private helper method encapsulates the logic for loading a single font file.
    # It performs pre-flight checks and handles exceptions for a single asset.
    # ===============================================================================
    @staticmethod
    def _load_single_font(font_filename: str):
        """
        Loads a single font file into memory with pre-flight checks and granular error handling.

        Args:
            font_filename (str): The filename of the font to load from the asset directory.

        Raises:
            FileNotFoundError: If the font file does not exist at the resolved path.
            Exception: For any other errors during the font loading process (e.g., file is corrupt).
        """
        # --- Resolve the absolute path to the font asset using the universal pathing utility.
        font_path = resource_path(font_filename)

        # --- Pre-flight Check: Verify the physical existence of the file before attempting to load.
        # --- This provides a more precise error message than a generic loading failure.
        if not os.path.exists(font_path):
            # --- Raise a specific, informative exception if the file is missing.
            raise FileNotFoundError(f"Required font asset is missing from path: {font_path}")

        # --- Attempt to add the font file to the application's in-memory font directory.
        # --- This makes the font available to all UI components. This can fail if the file is corrupt.
        pyglet.font.add_file(font_path)

        # --- Log the successful registration of the individual font file for auditing.
        logging.info(f"Successfully registered font: {font_filename}")

    # ===============================================================================
    # METHOD: register_fonts (v2.0 - Hardened Registration Protocol)
    # The sole public interface for this class. It orchestrates the loading of all
    # fonts listed in the manifest and manages the critical failure path.
    # ===============================================================================
    @staticmethod
    def register_fonts():
        """
        The definitive public method to load and register all required fonts.
        This method iterates through the REQUIRED_FONTS manifest and loads each one.
        """
        # --- Log the initiation of the font registration sequence for auditing.
        logging.info("FontManager: Initiating font registration protocol.")

        # --- Iterate through each font file specified in the manifest.
        for font_filename in FontManager.REQUIRED_FONTS:
            try:
                # --- Delegate the loading of the font to the atomic helper method.
                FontManager._load_single_font(font_filename)

            # --- Granular Exception Handling ---
            # This sequence provides precise, actionable error information upon failure.
            except FileNotFoundError as e:
                # --- This block executes if the pre-flight check fails (file is missing).
                logging.critical(f"FATAL: {e}", exc_info=True)
                root = tk.Tk()
                root.withdraw() # --- Hide the empty root window.
                tk.messagebox.showerror("Critical Asset Error", f"Required font '{font_filename}' is missing. The application cannot start.")
                sys.exit(1) # --- Terminate with a non-zero exit code.
            except Exception as e:
                # --- This block executes for any other failure, such as a corrupt or unsupported font file.
                logging.critical(f"FATAL: Could not load required font file '{font_filename}'. It may be corrupt. Error: {e}", exc_info=True)
                root = tk.Tk()
                root.withdraw() # --- Hide the empty root window.
                tk.messagebox.showerror("Critical Font Error", f"Required font '{font_filename}' is corrupt or unsupported. The application cannot start.")
                sys.exit(1) # --- Terminate with a non-zero exit code.
