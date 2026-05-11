# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: MenuShowDelayTweak (v1.0 - Zero-Defect Logic Controller)
#
# ARCHITECTURAL BLUEPRINT:
# This is a self-contained logic module for managing the Windows menu show delay.
# It interfaces directly with the registry to check and set the required value.
#
# CORE PRINCIPLES:
#   1. ROBUST STATE CHECKING: The `check_status` method uses a fault-tolerant
#      PowerShell command that safely retrieves the current delay value, or returns
#      the Windows default ('400') if the value does not explicitly exist. This
#      prevents errors and ensures a reliable state check every time.
#
#   2. REBOOT AWARENESS: Unlike other tweaks, this module understands that its
#      changes are not applied instantly via a shell restart. The `apply` and `undo`
#      methods are designed to simply set the registry value, with the knowledge
#      that the UI layer will be responsible for notifying the user of the need
#      to log off or reboot.
#
#   3. ATOMIC MODIFICATION: The `Set-ItemProperty` command is an atomic operation,
#      guaranteeing that the registry value is updated cleanly in a single step.
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


class MenuShowDelayTweak:
    """
    Manages the logic for modifying the MenuShowDelay registry value to remove
    the right-click menu animation delay.
    """
    def __init__(self):
        # --- REGISTRY CONSTANTS ---
        # Define the exact path and name for the registry value this class controls.
        self.reg_path = "HKCU:\\Control Panel\\Desktop"
        self.reg_name = "MenuShowDelay"
        self.default_value = "400" # The Windows default value.
        self.tweak_value = "0"     # The value that enables the tweak.

    def check_status(self) -> bool:
        """
        Checks the registry to determine if the menu delay is set to 0.

        Returns:
            bool: True if the tweak is active (delay is 0), False otherwise.
        """
        # --- COMMAND DEFINITION ---
        # This robust command attempts to get the property. If it fails (e.g., the
        # property doesn't exist), the catch block ensures we return the default
        # value, preventing the application from crashing.
        command = (
            f'$path = "{self.reg_path}"; $name = "{self.reg_name}"; '
            f'try {{ $value = (Get-ItemProperty -Path $path -Name $name -ErrorAction Stop).$name; Write-Output $value }} '
            f'catch {{ Write-Output "{self.default_value}" }}'
        )

        try:
            # --- SUBPROCESS EXECUTION ---
            # Execute the command silently with no flashing console window.
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # --- RESULT PARSING ---
            # The command outputs the delay value. We check if it matches our tweak's value.
            current_value = result.stdout.strip()
            is_enabled = current_value == self.tweak_value
            logging.info(f"MenuShowDelay status check: Value is {current_value}. Tweak enabled: {is_enabled}")
            return is_enabled

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # --- EXCEPTION HANDLING ---
            # If any error occurs, assume the default 'disabled' state for safety.
            logging.error(f"Error checking MenuShowDelay status: {e}", exc_info=True)
            return False

    def apply(self):
        """
        Applies the tweak by setting the menu delay to 0.
        This is a blocking operation and should be called from a background thread.
        """
        # --- COMMAND DEFINITION ---
        # A simple, direct command to set the registry property to the tweak value.
        command = f'Set-ItemProperty -Path "{self.reg_path}" -Name "{self.reg_name}" -Value "{self.tweak_value}"'
        logging.info("Applying MenuShowDelay tweak (setting value to 0)...")
        self._execute_command(command)
        # --- NOTE: No explorer restart here. Change requires logoff/reboot.

    def undo(self):
        """
        Reverts the tweak to the Windows default by setting the menu delay to 400.
        This is a blocking operation and should be called from a background thread.
        """
        # --- COMMAND DEFINITION ---
        # A simple, direct command to set the registry property to the default value.
        command = f'Set-ItemProperty -Path "{self.reg_path}" -Name "{self.reg_name}" -Value "{self.default_value}"'
        logging.info("Reverting MenuShowDelay tweak to default (setting value to 400)...")
        self._execute_command(command)
        # --- NOTE: No explorer restart here. Change requires logoff/reboot.

    def _execute_command(self, command: str):
        """A private helper to execute a PowerShell command silently."""
        try:
            # --- SUBPROCESS EXECUTION ---
            subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            logging.info(f"Successfully executed command: {command}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # --- EXCEPTION HANDLING ---
            logging.error(f"Failed to execute command '{command}': {e}", exc_info=True)
