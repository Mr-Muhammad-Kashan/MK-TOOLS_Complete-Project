# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: JPEGQualityTweak (v1.0 - Zero-Defect Logic Controller)
#
# ARCHITECTURAL BLUEPRINT:
# This is a self-contained logic module for managing the Windows JPEG wallpaper
# import quality. It is more advanced than previous tweak controllers, as it
# reads and writes specific integer values rather than just checking for existence.
#
# CORE PRINCIPLES:
#   1. VALUE-AWARE STATE CHECKING: The `check_status` method is designed to
#      return not just a boolean, but a detailed dictionary containing the
#      tweak's state ('configured' or 'default') and the specific quality value
#      if it exists. It gracefully handles cases where the registry key is not set.
#
#   2. PARAMETERIZED APPLICATION: The `apply` method accepts an integer value,
#      allowing the UI to set a custom wallpaper quality from 0-100. It correctly
#      sets the registry key as a DWord type.
#
#   3. TRUE DEFAULT REVERSION: The `undo` method doesn't just set a default value;
#      it removes the registry key entirely, which is the true default state for
#      a fresh Windows installation.
#
#   4. USER ACTION NOTIFICATION: All state-changing methods return a clear,
#      user-friendly message detailing the next steps required (logoff/reboot
#      and re-applying the wallpaper), which the UI layer can then display.
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


class JPEGQualityTweak:
    """
    Manages the logic for setting a custom JPEG wallpaper import quality.
    """
    def __init__(self):
        # --- REGISTRY CONSTANTS ---
        self.reg_path = "HKCU:\\Control Panel\\Desktop"
        self.reg_name = "JPEGImportQuality"
        self.finalization_message = "Change applied! To see the effect, please log out and back in, or restart your PC, then re-apply your wallpaper."

    def check_status(self) -> dict:
        """
        Checks the registry for the JPEGImportQuality value.

        Returns:
            dict: A dictionary containing the 'status' ('configured' or 'default')
                  and the current 'value' if configured.
        """
        command = (
            f'$path = "{self.reg_path}"; $name = "{self.reg_name}"; '
            f'try {{ $value = (Get-ItemProperty -Path $path -Name $name -ErrorAction Stop).$name; Write-Output $value }} '
            f'catch {{ Write-Output "default" }}'
        )
        try:
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            output = result.stdout.strip()

            if output == "default":
                logging.info("JPEGImportQuality status check: Default (key not found).")
                return {'status': 'default', 'value': None}
            else:
                logging.info(f"JPEGImportQuality status check: Configured to {output}.")
                return {'status': 'configured', 'value': int(output)}
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as e:
            logging.error(f"Error checking JPEGImportQuality status: {e}", exc_info=True)
            return {'status': 'default', 'value': None}

    def apply(self, quality_value: int):
        """
        Applies the tweak by setting the JPEG quality to a specific value.
        This should be called from a background thread.

        Args:
            quality_value (int): The desired quality, from 0 to 100.

        Returns:
            str: A message for the user indicating next steps.
        """
        # --- Value Sanitation ---
        # Ensures the value is within the valid 0-100 range.
        clamped_value = max(0, min(100, quality_value))

        # --- COMMAND DEFINITION ---
        # Sets the registry property as a DWord type, which is required for this key.
        command = f'Set-ItemProperty -Path "{self.reg_path}" -Name "{self.reg_name}" -Type DWord -Value {clamped_value}'
        logging.info(f"Applying JPEGImportQuality tweak (setting value to {clamped_value})...")
        self._execute_command(command)
        return self.finalization_message

    def undo(self):
        """
        Reverts the tweak to the Windows default by deleting the registry key.
        This should be called from a background thread.

        Returns:
            str: A message for the user indicating next steps.
        """
        # --- COMMAND DEFINITION ---
        # Removes the property entirely. -ErrorAction SilentlyContinue prevents errors
        # if the key doesn't already exist, making it safe to run anytime.
        command = f'Remove-ItemProperty -Path "{self.reg_path}" -Name "{self.reg_name}" -ErrorAction SilentlyContinue'
        logging.info("Reverting JPEGImportQuality tweak to default (removing key)...")
        self._execute_command(command)
        return self.finalization_message

    def _execute_command(self, command: str):
        """A private helper to execute a PowerShell command silently."""
        try:
            subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            logging.info(f"Successfully executed command: {command}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logging.error(f"Failed to execute command '{command}': {e}", exc_info=True)
