# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: DisableCompressedMemoryTweak (v2.0 - DEFINITIVE MMAgent IMPLEMENTATION)
#
# ARCHITECTURAL BLUEPRINT (RE-ENGINEERING):
# This version represents a complete architectural overhaul based on the definitive
# ground truth provided. All previous, complex logic involving multi-vector checks
# (Task Scheduler, manual registry keys) is discarded in favor of the official,
# high-level PowerShell MMAgent (Memory Management Agent) module. This is the
# paradigm solution for managing this feature.
#
# NEW PARADIGM: MMAgent API ABSTRACTION
# The class now functions as a direct, robust interface to the MMAgent cmdlets.
#
# DATA FLOW & LOGICAL INVERSION:
#
#  [ check_status() ]
#         |
#         +--> [ PowerShell: (Get-MMAgent).MemoryCompression ]
#                     |
#                     +--> Returns 'True' if System Compression is ENABLED
#                     +--> Returns 'False' if System Compression is DISABLED
#                     |
#         +--> [ Python Logic: return not result ]
#                     |
#                     +--> Returns True (Tweak ON) if System is DISABLED
#                     +--> Returns False (Tweak OFF) if System is ENABLED
#
# This correctly implements the logical inversion required by the feature's name.
#
# CORE PRINCIPLES:
#   1. SIMPLICITY & RELIABILITY: By using the official Microsoft cmdlets
#      (`Get-MMAgent`, `Enable-MMAgent`, `Disable-MMAgent`), we rely on a stable and
#      supported API, eliminating the brittleness of manual registry/task edits.
#
#   2. LOGICAL PURITY: The `check_status` method now perfectly reflects your
#      directive. It returns `True` (Tweak ON) when system memory compression is
#      `Disabled`, and `False` (Tweak OFF) when it is `Enabled`.
#
#   3. ATOMIC & REVERSIBLE OPERATIONS: `apply()` calls a single, atomic cmdlet to
#      disable the feature. `undo()` calls a single, atomic cmdlet to re-enable
#      it, guaranteeing a perfect restoration to the Windows default state.
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


class DisableCompressedMemoryTweak:
    """
    Manages the logic for enabling/disabling Windows Compressed Memory using the
    official MMAgent PowerShell module for 100% accuracy and reliability.
    """
    # The constructor for the DisableCompressedMemoryTweak controller.
    def __init__(self):
        # --- CONFIGURATION: Ground Truth Constants ---
        # --- The finalization message, informing the user of the required next step.
        self.FINALIZATION_MESSAGE = "Change applied! A system restart is required for this change to take full effect."

    # A private, robust helper method to execute a given PowerShell command.
    # This is the _run_powershell method inside the DisableCompressedMemoryTweak class

    def _run_powershell(self, command: str, get_output: bool = False) -> tuple[bool, Optional[str]]:
        """A private, secure gateway for all system interactions from this class."""
        # --- [CRITICAL FIX] Use the new PrivilegeManager for the admin check.
        if not PrivilegeManager._is_admin():
            # --- Log a critical failure if admin rights are not present.
            logging.error("MISSION CRITICAL FAILURE: Administrative privileges are required.")
            return (False, None)
        try:
            # --- Execute the PowerShell command silently, with no profile loading for maximum speed and stealth.
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", command],
                capture_output=True, text=True, check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # --- Return success and the captured output if requested.
            return (True, result.stdout.strip() if get_output else None)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # --- Log any errors for diagnostics and return a definitive failure state.
            logging.error(f"PowerShell command failed for DisableCompressedMemoryTweak. Error: {e}")
            return (False, None)

    # [CORRECTED] Performs a direct, official check using Get-MMAgent and inverts the logic.
    def check_status(self) -> bool:
        """
        Checks if Memory Compression is enabled or disabled using the official
        Get-MMAgent cmdlet and returns the logically correct state for the UI.

        Returns:
            bool: True if Compressed Memory is DISABLED (meaning the tweak is ON).
                  False if Compressed Memory is ENABLED (meaning the tweak is OFF).
        """
        # --- This is the official, simplest, and most reliable command to get the current state.
        command = "(Get-MMAgent).MemoryCompression"

        # --- Execute the command and get the string output ("True" or "False").
        success, output = self._run_powershell(command, get_output=True)

        # --- If the command fails to execute (e.g., on a Windows version without MMAgent), safely return False.
        if not success:
            logging.error("Failed to execute Get-MMAgent. Assuming compressed memory is enabled.")
            return False

        # --- Convert the PowerShell string "True" or "False" to a Python boolean.
        # --- This variable reflects the RAW SYSTEM STATE.
        is_system_feature_enabled = output.lower() == "true"
        # --- [CRITICAL LOGIC] Invert the result for the UI.
        # --- Our feature is "Disable Compressed Memory". It is "ON" when the system feature is "OFF" (disabled).
        is_tweak_on = not is_system_feature_enabled

        logging.info(f"System Compressed Memory Enabled: {is_system_feature_enabled}. Tweak state is ON: {is_tweak_on}")
        return is_tweak_on

    # Applies the tweak by DISABLING compressed memory.
    def apply(self) -> str:
        """
        Applies the tweak by disabling system-wide Memory Compression.
        This corresponds to turning the UI toggle ON.

        Returns:
            str: A user-friendly message for the notification pop-up.
        """
        # --- This is the official cmdlet to disable the feature.
        command = "Disable-MMAgent -MemoryCompression"
        # --- Execute the command.
        success, _ = self._run_powershell(command)
        return self.FINALIZATION_MESSAGE if success else "Error: Failed to disable compressed memory. Please run as administrator."

    # Reverts the tweak by ENABLING compressed memory.
    def undo(self) -> str:
        """
        Reverts the tweak by enabling system-wide Memory Compression.
        This corresponds to turning the UI toggle OFF or resetting to default.

        Returns:
            str: A user-friendly message for the notification pop-up.
        """
        # --- This is the official cmdlet to re-enable the feature, restoring the system default.
        command = "Enable-MMAgent -MemoryCompression"
        # --- Execute the command.
        success, _ = self._run_powershell(command)
        return self.FINALIZATION_MESSAGE if success else "Error: Failed to enable compressed memory. Please run as administrator."
