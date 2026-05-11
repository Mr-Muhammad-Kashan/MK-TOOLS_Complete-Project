# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: ForegroundPriorityController (v1.0 - ENHANCED FEEDBACK PROTOCOL)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This version of the controller has been upgraded to provide enhanced user
# feedback. Instead of returning a simple boolean success state, the `apply` and
# `undo` methods now return a definitive, user-friendly string message upon
# completion. This conforms to the universal data contract expected by the
# `AnimatedTweakCard`'s notification system, ensuring a consistent and
# informative user experience across all tweak components.
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


class ForegroundPriorityController:
    """
    Manages the logic for the 'Prioritized Foreground Applications' tweak by
    interacting with the Windows Registry via PowerShell in a safe, robust, and
    decoupled manner.
    """
    def __init__(self):
        """
        Constructor for the ForegroundPriorityController.
        This method initializes all non-negotiable constants and configuration
        values required for the class to operate.
        """
        # --- CONFIGURATION: Registry Ground Truth ---
        # The absolute, non-negotiable path to the target registry key. This is a constant.
        self.REG_PATH = "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl"
        # The exact name of the DWORD value that will be read from and written to.
        self.REG_NAME = "Win32PrioritySeparation"

        # --- CONFIGURATION: State Definitions ---
        # The precise decimal value representing the OPTIMIZED state (Hex: 0x26).
        self.OPTIMIZED_VALUE = 38
        # The precise decimal value representing the Windows DEFAULT state. This is the target for all reset operations.
        self.DEFAULT_VALUE = 45

    def _run_powershell(self, command: str, get_output: bool = False) -> tuple[bool, Optional[str]]:
        """
        A private, robust helper method to execute a given PowerShell command.
        This is the single, secure gateway for all registry interactions from this class.

        Args:
            command (str): The PowerShell command string to execute.
            get_output (bool): If True, the function will capture and return stdout.

        Returns:
            tuple[bool, Optional[str]]: A tuple containing a success flag (True/False) and
                                        the captured stdout as a string, or None if not requested or on failure.
        """
        # --- Mandate 1: Administrative Privilege Check ---
        # The mission requires modifying HKLM, which is impossible without elevation.
        # This check now calls the central PrivilegeManager for a definitive, reliable answer.
        if not PrivilegeManager._is_admin():
            # --- Log a critical failure if admin rights are not present. ---
            logging.error("MISSION CRITICAL FAILURE: Administrative privileges are required to run registry commands.")
            # --- Return a definitive failure state. ---
            return (False, None)

        try:
            # --- Mandate 2: Execute PowerShell command silently and robustly. ---
            # 'powershell.exe': The target executable.
            # '-NoProfile': Skips loading the user's PowerShell profile for faster, cleaner execution.
            # '-Command': Specifies that the next argument is a command string to be executed.
            # 'capture_output=True': Required to capture stdout and stderr from the process.
            # 'text=True': Decodes stdout/stderr as text using the system's default encoding.
            # 'check=True': Automatically raises a CalledProcessError if PowerShell returns a non-zero exit code (an error).
            # 'creationflags=subprocess.CREATE_NO_WINDOW': CRITICAL. Prevents the black PowerShell console from flashing on the user's screen.
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", command],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # --- If 'check=True' passes without raising an exception, the command was successful. ---
            # --- If output was requested, return the success flag and the cleaned-up stdout string. ---
            return (True, result.stdout.strip() if get_output else None)

        except FileNotFoundError:
            # --- This specific exception occurs if 'powershell.exe' is not found in the system's PATH. ---
            logging.error("FATAL ERROR: powershell.exe not found. Is PowerShell installed and in the system PATH?")
            # --- Return a definitive failure state. ---
            return (False, None)
        except subprocess.CalledProcessError as e:
            # --- This error is raised by 'check=True' when PowerShell returns an error (e.g., key not found, permissions issue). ---
            # --- We log the specific error message from PowerShell's stderr for precise diagnostics. ---
            logging.error(f"PowerShell command failed. Return Code: {e.returncode}\nError Output: {e.stderr.strip()}")
            # --- Return a definitive failure state. ---
            return (False, None)
        except Exception as e:
            # --- A final catch-all for any other unexpected exceptions during subprocess execution. ---
            logging.error(f"An unexpected error occurred while running PowerShell command: {e}")
            # --- Return a definitive failure state. ---
            return (False, None)

    def check_status(self) -> bool:
        """
        Checks the registry to determine if the tweak is currently active.
        This is a read-only, non-blocking operation (relative to UI thread).

        Returns:
            bool: True if the tweak is active (value is 38), False otherwise.
                  Returns False if the key is missing or an error occurs.
        """
        # --- Step 1: Define the PowerShell command to query the registry value. ---
        # --- This command attempts to retrieve the specific property from the defined registry path. ---
        command = f'(Get-ItemProperty -Path "{self.REG_PATH}" -Name "{self.REG_NAME}" -ErrorAction SilentlyContinue).{self.REG_NAME}'

        # --- Step 2: Execute the command using the robust, centralized runner. ---
        # --- We request the output to be returned for parsing. ---
        success, output = self._run_powershell(command, get_output=True)

        # --- Step 3: Analyze the result. ---
        # --- If the PowerShell execution failed for any reason, we cannot determine the state. ---
        if not success:
            # --- Log the failure and assume the default (disabled) state for safety. ---
            logging.warning("Could not retrieve registry value due to execution failure. Assuming DEFAULT state.")
            # --- Return False as the definitive state. ---
            return False

        try:
            # --- Attempt to convert the string output from PowerShell to an integer. ---
            current_value = int(output)
            # --- Log the successfully read value for auditing and debugging. ---
            logging.info(f"Successfully read registry value for Win32PrioritySeparation: {current_value}")
            # --- Compare the retrieved value with the defined OPTIMIZED value. ---
            # --- This comparison is the single source of truth for the tweak's status. ---
            return current_value == self.OPTIMIZED_VALUE
        except (ValueError, TypeError):
            # --- This block catches errors if the output is not a valid integer (e.g., empty or null). ---
            # --- This can happen if the registry value does not exist. ---
            logging.info(f"Could not parse registry value or value does not exist. Assuming DEFAULT state. Raw output: '{output}'")
            # --- In case of any parsing error, we safely assume the tweak is not active. ---
            return False

    def apply(self) -> str:
        """
        Applies the tweak by setting the registry value to the OPTIMIZED state (38).
        This is a state modification method designed to be run in a background thread.

        Returns:
            str: A user-friendly message indicating the outcome of the operation.
        """
        # --- Log the intention to apply the optimization for clear traceability. ---
        logging.info(f"Executing APPLY command. Setting {self.REG_NAME} to {self.OPTIMIZED_VALUE}.")
        # --- Construct the PowerShell command to set the registry value using the defined constants. ---
        command = f'Set-ItemProperty -Path "{self.REG_PATH}" -Name "{self.REG_NAME}" -Value {self.OPTIMIZED_VALUE} -Type DWord -Force'
        # --- Execute the command using the centralized runner and capture the success flag. ---
        success, _ = self._run_powershell(command)

        # --- [UPGRADE] Return a descriptive string based on the operation's success. ---
        if success:
            # --- This is the success message that will be displayed in the notification pop-up. ---
            return "Optimization applied! A system restart is required for this change to take full effect."
        else:
            # --- This is the failure message. ---
            return "Error: Failed to apply the optimization. Please ensure the app is running as administrator."

    def undo(self) -> str:
        """
        Resets the tweak to the DEFAULT state by setting the registry value to 45.
        This is a state modification method designed to be run in a background thread.

        Returns:
            str: A user-friendly message indicating the outcome of the operation.
        """
        # --- Log the intention to reset to default for clear traceability. ---
        logging.info(f"Executing UNDO/RESET command. Setting {self.REG_NAME} to {self.DEFAULT_VALUE}.")
        # --- Construct the PowerShell command to set the registry value to its default. ---
        command = f'Set-ItemProperty -Path "{self.REG_PATH}" -Name "{self.REG_NAME}" -Value {self.DEFAULT_VALUE} -Type DWord -Force'
        # --- Execute the command using the centralized runner and capture the success flag. ---
        success, _ = self._run_powershell(command)

        # --- [UPGRADE] Return a descriptive string based on the operation's success. ---
        if success:
            # --- This is the success message for resetting the setting. ---
            return "Settings successfully reset to default. A system restart is required for this change to take full effect."
        else:
            # --- This is the failure message. ---
            return "Error: Failed to reset settings. Please ensure the app is running as administrator."
