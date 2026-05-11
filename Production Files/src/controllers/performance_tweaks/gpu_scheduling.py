# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: GPUSchedulingTweak (v2.1 - Enhanced State Reporting)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This version enhances the state-reporting protocol. The `check_status` method
# now returns a definitive, explicit state ('on', 'off', 'default') instead of a
# generic 'configured' status. This provides the UI layer with the precise
# information required to render the new three-state button (Turned On, Turned Off,
# Not Configured), fulfilling the user's requirement for enhanced clarity.
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


class GPUSchedulingTweak:
    """
    Manages the logic for Hardware-Accelerated GPU Scheduling, now with an enhanced
    state-checking mechanism that reports the precise 'on', 'off', or 'default' status.
    """
    def __init__(self):
        """
        Constructor for the GPUSchedulingTweak controller.
        Initializes all non-negotiable constants for registry interaction.
        """
        # --- CONFIGURATION: Registry Ground Truth ---
        # The absolute, non-negotiable path to the target registry key.
        self.REG_PATH = "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers"
        # The exact name of the DWORD value to be modified.
        self.REG_NAME = "HwSchMode"

        # --- CONFIGURATION: State Definitions ---
        # The precise decimal value representing the "Enabled" state.
        self.ENABLED_VALUE = 2
        # The precise decimal value representing the "Disabled" state.
        self.DISABLED_VALUE = 1
        # The finalization message, informing the user of the required next step.
        self.FINALIZATION_MESSAGE = "Change applied! A system restart is required for this change to take full effect."

    def _run_powershell(self, command: str, get_output: bool = False) -> tuple[bool, Optional[str]]:
        """
        A private, robust helper method to execute a given PowerShell command.
        This is the single, secure gateway for all registry interactions from this class.

        Args:
            command (str): The PowerShell command string to execute.
            get_output (bool): If True, the function will capture and return stdout.

        Returns:
            tuple[bool, Optional[str]]: A tuple containing a success flag and the captured stdout or None.
        """
        # --- Pre-flight check for mandatory administrative privileges using the central PrivilegeManager. ---
        if not PrivilegeManager._is_admin():
            # --- Log a critical failure if admin rights are not present. ---
            logging.error("MISSION CRITICAL FAILURE: Administrative privileges are required to modify GraphicsDrivers settings.")
            # --- Return a definitive failure state. ---
            return (False, None)

        try:
            # --- Execute the PowerShell command silently, with no profile loading for maximum speed and stealth. ---
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", command],
                capture_output=True, # --- Required to capture stdout and stderr. ---
                text=True,           # --- Decodes stdout/stderr as text. ---
                check=True,          # --- Raise an exception on non-zero exit codes. ---
                creationflags=subprocess.CREATE_NO_WINDOW # --- CRITICAL: Prevents console flash. ---
            )
            # --- Return success and the captured output if requested. ---
            return (True, result.stdout.strip() if get_output else None)
        # --- Handle cases where PowerShell is not installed or not in the system's PATH. ---
        except FileNotFoundError:
            logging.error("FATAL ERROR: powershell.exe not found. Is PowerShell installed and in the system PATH?")
            return (False, None)
        # --- Handle errors returned by the PowerShell command itself (e.g., access denied). ---
        except subprocess.CalledProcessError as e:
            logging.error(f"PowerShell command failed. Return Code: {e.returncode}\nError Output: {e.stderr.strip()}")
            return (False, None)
        # --- A final catch-all for any other unexpected exceptions. ---
        except Exception as e:
            logging.error(f"An unexpected error occurred while running PowerShell command: {e}")
            return (False, None)

    def check_status(self) -> dict:
        """
        [RE-ENGINEERED] Checks the registry for the HwSchMode value and returns
        a precise 'on', 'off', or 'default' state.

        Returns:
            dict: A dictionary containing the 'status' ('on', 'off', or 'default')
                  and the current 'value' if it exists.
        """
        # --- Define the command to get the property; -ErrorAction SilentlyContinue prevents errors if the key doesn't exist. ---
        command = f'(Get-ItemProperty -Path "{self.REG_PATH}" -Name "{self.REG_NAME}" -ErrorAction SilentlyContinue).{self.REG_NAME}'
        # --- Execute the command and request the output. ---
        success, output = self._run_powershell(command, get_output=True)

        # --- If the command fails to run or the key doesn't exist (no output), return 'default'. ---
        if not success or not output:
            logging.info("HwSchMode status check: Default (key not found or read error).")
            return {'status': 'default', 'value': None}

        try:
            # --- Attempt to convert the PowerShell output to an integer. ---
            current_value = int(output)
            # --- Compare against the known state values. ---
            if current_value == self.ENABLED_VALUE:
                logging.info(f"HwSchMode status check: ON (Value: {current_value}).")
                return {'status': 'on', 'value': current_value}
            elif current_value == self.DISABLED_VALUE:
                logging.info(f"HwSchMode status check: OFF (Value: {current_value}).")
                return {'status': 'off', 'value': current_value}
            else:
                # --- If the value is something unexpected, treat it as default for safety. ---
                logging.warning(f"HwSchMode status check: Found unexpected value {current_value}. Treating as default.")
                return {'status': 'default', 'value': None}
        # --- This catches cases where the output is not a number. ---
        except (ValueError, TypeError):
            logging.info(f"HwSchMode registry value does not exist or is invalid. Assuming default state.")
            return {'status': 'default', 'value': None}

    def turn_on(self) -> str:
        """
        Applies the tweak by setting the HwSchMode registry value to 2 (Enabled).

        Returns:
            str: A user-friendly message indicating the outcome of the operation.
        """
        # --- Log the apply action for traceability. ---
        logging.info(f"Executing TURN ON command for GPU Scheduling. Setting {self.REG_NAME} to {self.ENABLED_VALUE}.")
        # --- Construct the command to set the registry DWORD value to Enabled. ---
        command = f'Set-ItemProperty -Path "{self.REG_PATH}" -Name "{self.REG_NAME}" -Value {self.ENABLED_VALUE} -Type DWord -Force'
        # --- Execute the command. ---
        success, _ = self._run_powershell(command)
        # --- Return a descriptive string based on the operation's success for the UI pop-up. ---
        return self.FINALIZATION_MESSAGE if success else "Error: Failed to enable GPU Scheduling. Please ensure the app is running as administrator."

    def turn_off(self) -> str:
        """
        Disables the tweak by setting the HwSchMode registry value to 1 (Disabled).

        Returns:
            str: A user-friendly message indicating the outcome of the operation.
        """
        # --- Log the disable action for traceability. ---
        logging.info(f"Executing TURN OFF command for GPU Scheduling. Setting {self.REG_NAME} to {self.DISABLED_VALUE}.")
        # --- Construct the command to set the registry DWORD value to Disabled. ---
        command = f'Set-ItemProperty -Path "{self.REG_PATH}" -Name "{self.REG_NAME}" -Value {self.DISABLED_VALUE} -Type DWord -Force'
        # --- Execute the command. ---
        success, _ = self._run_powershell(command)
        # --- Return a descriptive string based on the operation's success for the UI pop-up. ---
        return self.FINALIZATION_MESSAGE if success else "Error: Failed to disable GPU Scheduling. Please ensure the app is running as administrator."

    def undo(self) -> str:
        """
        Resets the tweak to the Windows default by completely removing the HwSchMode registry key.
        This action is triggered by the "Reset" button.

        Returns:
            str: A user-friendly message indicating the outcome of the operation.
        """
        # --- Log the undo action for traceability. ---
        logging.info(f"Executing UNDO/RESET command for GPU Scheduling. Removing {self.REG_NAME} property.")
        # --- Construct the command to completely remove the property. -ErrorAction SilentlyContinue prevents errors if it's already gone. ---
        command = f'Remove-ItemProperty -Path "{self.REG_PATH}" -Name "{self.REG_NAME}" -ErrorAction SilentlyContinue -Force'
        # --- Execute the command. ---
        success, _ = self._run_powershell(command)
        # --- Return a descriptive string based on the operation's success for the UI pop-up. ---
        return self.FINALIZATION_MESSAGE if success else "Error: Failed to reset GPU Scheduling. Please ensure the app is running as administrator."
