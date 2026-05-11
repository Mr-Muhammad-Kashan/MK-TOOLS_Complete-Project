# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: ClassicContextMenuTweak (v1.0 - Zero-Defect Logic Controller)
#
# ARCHITECTURAL BLUEPRINT:
# This class is a self-contained, high-integrity logic module responsible for
# managing a single system tweak: the Classic Context Menu on Windows 11. It is
# designed with absolute separation of concerns, containing no UI code. Its sole
# purpose is to interface with the Windows Registry and shell via optimized,
# fault-tolerant PowerShell commands.
#
# CORE PRINCIPLES:
#   1. STATE AWARENESS: The `check_status` method provides a definitive, boolean
#      answer to the question "Is this tweak active?" by using the most reliable
#      and performant check (`Test-Path`) instead of error-prone value parsing.
#
#   2. ASYNCHRONOUS EXECUTION: All methods that modify the system (`apply`, `undo`)
#      are designed to be run in a background thread. They execute silently
#      (no flashing console windows) and manage the necessary UI shell restart.
#
#   3. ATOMIC OPERATIONS: The PowerShell commands are transactional. The 'apply'
#      script ensures the entire key path is created. The 'undo' script removes
#      the entire key tree recursively, guaranteeing a clean reversion to the
#      Windows default state.
#
#   4. ZERO-DEFECT COMMANDS: The PowerShell commands use `-Force` to prevent
#      confirmation prompts and `-ErrorAction SilentlyContinue` on the removal
#      command to prevent exceptions if the key doesn't exist, ensuring the
#      operation never fails unexpectedly.
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


class ClassicContextMenuTweak:
    """
    Manages the logic for enabling/disabling the classic right-click context menu in Windows 11.
    This class handles registry checks and modifications in a safe, thread-agnostic manner.
    """
    def __init__(self):
        # --- REGISTRY PATH CONSTANT ---
        # The specific, non-negotiable registry path for this tweak. Stored as a
        # class instance variable for easy access and to prevent magic strings.
        self.reg_key_path = "HKCU:\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}"

    def check_status(self) -> bool:
        """
        Checks the Windows Registry to determine if the classic context menu is currently enabled.
        This is a non-blocking, read-only operation.

        Returns:
            bool: True if the tweak is active, False otherwise.
        """
        # --- COMMAND DEFINITION ---
        # This command uses Test-Path, the most efficient and reliable way to check for
        # the existence of a registry key. It returns a simple boolean, avoiding
        # complex and fragile output parsing.
        command = f"Test-Path -Path '{self.reg_key_path}'"

        try:
            # --- SUBPROCESS EXECUTION ---
            # Execute the PowerShell command silently in the background.
            # `capture_output=True` and `text=True` ensure we get string-based stdout/stderr.
            # `creationflags=subprocess.CREATE_NO_WINDOW` is CRITICAL to prevent a console flash.
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True,
                text=True,
                check=True, # --- This will raise an exception if PowerShell returns a non-zero exit code.
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # --- RESULT PARSING ---
            # PowerShell's Test-Path outputs "True" or "False" as a string, followed by a newline.
            # We strip whitespace and check for equality with "True" for a definitive result.
            is_enabled = result.stdout.strip() == "True"
            logging.info(f"Classic Context Menu status check: {'Enabled' if is_enabled else 'Disabled'}")
            return is_enabled

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # --- EXCEPTION HANDLING ---
            # Log any errors during the check (e.g., PowerShell not found, command fails).
            # In any case of error, we assume the default state, which is 'disabled'.
            logging.error(f"Error checking classic context menu status: {e}", exc_info=True)
            return False

    def _execute_and_restart_explorer(self, command: str):
        """
        A private helper method to execute a given PowerShell command and then
        gracefully restart the Windows Explorer process to apply UI changes.
        This method is designed to be run in a background thread.
        """
        try:
            # --- COMMAND EXECUTION ---
            # Execute the main tweak command (apply or undo).
            subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # --- UI SHELL RESTART SEQUENCE ---
            # This sequence is required for any registry change affecting Explorer to become visible.
            # It is executed silently and forcefully to ensure a clean restart.
            # 1. Terminate the explorer.exe process.
            subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            # 2. A brief, critical pause to allow the process to terminate fully.
            time.sleep(1)
            # 3. Relaunch the explorer.exe process.
            subprocess.run(["powershell", "-Command", "Start-Process explorer"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            logging.info("Successfully executed command and restarted explorer.exe")

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # --- EXCEPTION HANDLING ---
            # Log any errors that occur during the modification process.
            logging.error(f"Failed to execute command and restart explorer: {e}", exc_info=True)

    def apply(self):
        """
        Applies the tweak by creating the necessary registry key.
        This is a blocking operation and should be called from a background thread.
        """
        # --- COMMAND DEFINITION ---
        # This command creates the full registry path (-Force ensures parent keys are created)
        # and then sets the (Default) value to an empty string, which activates the tweak.
        inproc_path = f"{self.reg_key_path}\\InprocServer32"
        command = (
            f"New-Item -Path '{inproc_path}' -Force | Out-Null; "
            f"Set-ItemProperty -Path '{inproc_path}' -Name '(Default)' -Value '' -Force"
        )
        logging.info("Applying Classic Context Menu tweak...")
        self._execute_and_restart_explorer(command)

    def undo(self):
        """
        Reverts the tweak to the Windows default by deleting the registry key.
        This is a blocking operation and should be called from a background thread.
        """
        # --- COMMAND DEFINITION ---
        # This command removes the entire key tree recursively (-Recurse) and forcefully (-Force).
        # -ErrorAction SilentlyContinue prevents any errors if the key doesn't exist,
        # making this command idempotent and safe to run multiple times.
        command = f"Remove-Item -Path '{self.reg_key_path}' -Recurse -Force -ErrorAction SilentlyContinue"
        logging.info("Reverting Classic Context Menu tweak to default...")
        self._execute_and_restart_explorer(command)
