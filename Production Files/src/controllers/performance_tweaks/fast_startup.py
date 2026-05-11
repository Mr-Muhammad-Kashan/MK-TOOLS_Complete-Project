# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: DisableFastStartupTweak (v1.0 - Zero-Defect Logic Controller)
#
# ARCHITECTURAL BLUEPRINT:
# This class is a self-contained, high-integrity logic module responsible for
# managing the "Fast Startup" feature in Windows. It exclusively interfaces with the
# registry via fault-tolerant PowerShell commands, completely decoupled from the UI.
#
# CORE PRINCIPLES:
#   1. INVERSE STATE LOGIC: The `check_status` method implements the required
#      inverse logic. It returns `True` (Tweak is ON) if Fast Startup is DISABLED
#      (value 0) in the registry, and `False` (Tweak is OFF) if Fast Startup is
#      ENABLED (value 1). This aligns the backend state with the UI's perspective.
#
#   2. ATOMIC OPERATIONS: The `apply` and `undo` methods execute single, atomic
#      PowerShell commands to set the registry key, ensuring clean state transitions.
#
#   3. ZERO-DEFECT COMMANDS: All PowerShell commands use `-Force` to prevent
#      confirmation prompts and handle potential errors gracefully. Administrative
#      privileges are programmatically checked before any write operation.
#
#   4. REBOOT AWARENESS: All state-changing methods return a clear, user-friendly
#      message indicating a system restart is mandatory, which the UI layer
#      is designed to display in a notification.
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


class DisableFastStartupTweak:
    """
    Manages the logic for enabling/disabling the Windows Fast Startup feature
    by modifying the 'HiberbootEnabled' registry value.
    """
    def __init__(self):
        """
        Constructor for the DisableFastStartupTweak controller.
        Initializes all non-negotiable constants for registry interaction.
        """
        # --- CONFIGURATION: Registry Ground Truth ---
        # The absolute, non-negotiable path to the target registry key.
        self.REG_PATH = "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power"
        # The exact name of the DWORD value to be modified.
        self.REG_NAME = "HiberbootEnabled"
        # The finalization message, informing the user of the required next step.
        self.FINALIZATION_MESSAGE = "Change applied! A full shutdown or restart is required for this change to take effect."

    def _run_powershell(self, command: str, get_output: bool = False) -> tuple[bool, Optional[str]]:
        """
        A private, robust helper method to execute a given PowerShell command.
        This is the single, secure gateway for all registry interactions.

        Args:
            command (str): The PowerShell command string to execute.
            get_output (bool): If True, the function will capture and return stdout.

        Returns:
            tuple[bool, Optional[str]]: A tuple containing a success flag and the captured output or None.
        """
        # --- Pre-flight check for mandatory administrative privileges for write operations using the central PrivilegeManager. ---
        if not get_output and not PrivilegeManager._is_admin():
            logging.error("MISSION CRITICAL FAILURE: Administrative privileges are required to modify this setting.")
            return (False, None)

        try:
            # --- Execute the PowerShell command silently, with no profile loading for maximum speed and stealth. ---
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", command],
                capture_output=True, text=True, check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # --- Return success and the captured output if requested. ---
            return (True, result.stdout.strip() if get_output else None)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # --- Log any errors for diagnostics and return a definitive failure state. ---
            logging.error(f"PowerShell command failed for Fast Startup Tweak. Error: {e}")
            return (False, None)

    def check_status(self) -> bool:
        """
        Checks if the 'Disable Fast Startup' tweak is active.

        Returns:
            bool: True if Fast Startup is DISABLED (tweak is ON).
                  False if Fast Startup is ENABLED (tweak is OFF).
        """
        # --- Define the command to get the property; -ErrorAction SilentlyContinue prevents errors if the key doesn't exist. ---
        command = f'(Get-ItemProperty -Path "{self.REG_PATH}" -Name "{self.REG_NAME}" -ErrorAction SilentlyContinue).{self.REG_NAME}'
        success, output = self._run_powershell(command, get_output=True)

        # --- If the command fails or the key doesn't exist (no output), assume Windows default (Fast Startup enabled). ---
        if not success or not output:
            logging.info("HiberbootEnabled status check: Default (key not found or enabled). Tweak is OFF.")
            return False # --- Tweak is considered OFF.

        # --- If the registry value is 0, Fast Startup is disabled, meaning our tweak is ON. ---
        is_tweak_on = output == '0'
        logging.info(f"HiberbootEnabled status check: Value is {output}. Tweak is {'ON' if is_tweak_on else 'OFF'}.")
        return is_tweak_on

    def apply(self) -> str:
        """
        Applies the tweak by disabling Fast Startup (setting HiberbootEnabled to 0).
        This corresponds to turning the tweak ON.

        Returns:
            str: A user-friendly message for the notification pop-up.
        """
        logging.info("Executing APPLY command for Fast Startup. Setting HiberbootEnabled to 0.")
        command = f'Set-ItemProperty -Path "{self.REG_PATH}" -Name "{self.REG_NAME}" -Value 0 -Type DWord -Force'
        success, _ = self._run_powershell(command)
        return self.FINALIZATION_MESSAGE if success else "Error: Failed to disable Fast Startup. Please run as administrator."

    def undo(self) -> str:
        """
        Reverts the tweak by enabling Fast Startup (setting HiberbootEnabled to 1).
        This corresponds to turning the tweak OFF or resetting to default.

        Returns:
            str: A user-friendly message for the notification pop-up.
        """
        logging.info("Executing UNDO/RESET for Fast Startup. Setting HiberbootEnabled to 1.")
        command = f'Set-ItemProperty -Path "{self.REG_PATH}" -Name "{self.REG_NAME}" -Value 1 -Type DWord -Force'
        success, _ = self._run_powershell(command)
        return self.FINALIZATION_MESSAGE if success else "Error: Failed to enable Fast Startup. Please run as administrator."
