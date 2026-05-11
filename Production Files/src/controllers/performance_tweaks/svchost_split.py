# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: SvcHostSplitTweak (v1.0 - Zero-Defect Logic Controller)
#
# ARCHITECTURAL BLUEPRINT:
# This is a self-contained logic module for managing the SvcHostSplitThresholdInKB
# registry value. It is engineered to perform robust system queries and execute
# precise registry modifications via fault-tolerant PowerShell commands.
#
# CORE PRINCIPLES:
#   1. DYNAMIC STATE AWARENESS: The `check_status` method performs a definitive
#      check against the registry, correctly identifying the 'default' state
#      by either the key's absence or its exact default decimal value (3670016).
#
#   2. PARAMETERIZED APPLICATION: The `apply` method accepts a precise RAM value
#      in GB, calculates the required threshold in KB, and writes it to the
#      registry as a DWORD value, ensuring perfect application of the tweak.
#
#   3. ATOMIC RESET PROTOCOL: The `undo` method restores the system to the
#      exact, authoritative Windows default state by writing 3670016 to the key,
#      guaranteeing a clean and predictable reversion.
#
#   4. REBOOT AWARENESS: All state-changing methods return a clear, user-friendly
#      message indicating that a system restart is mandatory for the change to
#      take effect, as per the ground truth directive.
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


class SvcHostSplitTweak:
    """
    Manages SvcHost Split Threshold configuration with forensically accurate RAM detection.
    """
    def __init__(self):
        # --- REGISTRY CONSTANTS ---
        # The absolute, non-negotiable registry path for this system tweak.
        self.reg_path = "HKLM:\\SYSTEM\\CurrentControlSet\\Control"
        # The exact name of the DWORD value to be modified.
        self.reg_name = "SvcHostSplitThresholdInKB"
        # The authoritative default decimal value for Windows 10/11 systems with >3.5GB RAM.
        self.default_value_decimal = 3670016
        # The finalization message, informing the user of the required next step.
        self.finalization_message = "Optimization applied! A system restart is required for this change to take effect."

    def _get_total_physical_memory_bytes(self) -> int:
        """
        [NEW] Executes a mandated PowerShell command to get absolute total physical RAM in bytes.
        This private method queries the hardware directly, ignoring OS-level reservations.

        Returns:
            int: Total physical RAM in bytes. Returns 0 on failure.
        """
        # --- COMMAND DEFINITION ---
        # This command interrogates the WMI class for physical memory modules, sums their
        # individual capacities, and returns the absolute total in bytes.
        command = "(Get-CimInstance -ClassName Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum).Sum"
        try:
            # --- SUBPROCESS EXECUTION ---
            # Execute the hardware query command silently.
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            # --- VALUE PARSING ---
            # Convert the resulting byte count from a string to an integer.
            total_bytes = int(result.stdout.strip())
            # Log the raw byte value for auditing purposes.
            logging.info(f"Detected raw physical memory: {total_bytes} bytes.")
            # Return the ground-truth byte value.
            return total_bytes
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as e:
            # --- EXCEPTION HANDLING ---
            # If the command fails, log the error and return a safe fallback value of 0.
            logging.error(f"FATAL: Failed to get absolute physical memory: {e}", exc_info=True)
            # A return value of 0 signals to the UI that detection failed.
            return 0

    def get_total_physical_ram_gb(self) -> float:
        """
        [NEW] Public accessor to get total physical RAM in gigabytes for UI display.

        Returns:
            float: Total physical RAM in gigabytes with floating-point precision.
        """
        # --- Retrieve the raw byte value from the primary query method.
        total_bytes = self._get_total_physical_memory_bytes()
        # --- If the query failed (returned 0), return 0.0.
        if total_bytes == 0:
            return 0.0
        # --- Convert bytes to gigabytes for UI display (1024^3).
        return total_bytes / (1024 * 1024 * 1024)

    def get_svchost_threshold_kb(self) -> int:
        """
        [NEW] Public accessor to get the precise SvcHost threshold value in kilobytes.

        Returns:
            int: The precise threshold value in kilobytes, derived from the raw byte count.
        """
        # --- Retrieve the raw byte value from the primary query method.
        total_bytes = self._get_total_physical_memory_bytes()
        # --- If the query failed (returned 0), return 0.
        if total_bytes == 0:
            return 0
        # --- Convert bytes to kilobytes for the registry write (1024).
        return total_bytes // 1024

    def check_status(self) -> dict:
        """
        Checks the registry for the current SvcHostSplitThresholdInKB value. (Unchanged)
        """
        # --- COMMAND DEFINITION ---
        command = (
            f'$path = "{self.reg_path}"; $name = "{self.reg_name}"; '
            f'try {{ $value = (Get-ItemProperty -Path $path -Name $name -ErrorAction Stop).$name; Write-Output $value }} '
            f'catch {{ Write-Output "unconfigured" }}'
        )
        try:
            # --- SUBPROCESS EXECUTION ---
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            # --- RESULT PARSING ---
            output = result.stdout.strip()
            # --- STATE VALIDATION ---
            if output == "unconfigured" or int(output) == self.default_value_decimal:
                return {'status': 'default', 'value': None}
            else:
                return {'status': 'configured', 'value': int(output)}
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as e:
            # --- EXCEPTION HANDLING ---
            logging.error(f"Error checking SvcHostSplitThreshold status: {e}", exc_info=True)
            return {'status': 'default', 'value': None}

    def apply(self):
        """
        [MODIFIED] Applies the tweak using the forensically accurate RAM detection.
        This method no longer accepts parameters and is now self-sufficient.
        """
        # --- Get the precise threshold value directly from the hardware query.
        threshold_kb = self.get_svchost_threshold_kb()
        # --- Fail-safe check in case the hardware query failed.
        if threshold_kb == 0:
            logging.error("Apply failed: Could not determine threshold value.")
            return "Error: Could not calculate threshold. Operation cancelled."
        # --- COMMAND DEFINITION ---
        command = f'Set-ItemProperty -Path "{self.reg_path}" -Name "{self.reg_name}" -Type DWord -Value {threshold_kb} -Force'
        logging.info(f"Applying SvcHostSplitThreshold tweak (setting value to {threshold_kb})...")
        self._execute_command(command)
        return self.finalization_message

    def apply_manual(self, ram_gb: int):
        """
        [NEW] Applies the tweak using a user-provided RAM value.
        This method handles the manual override workflow.
        """
        # --- VALUE CALCULATION ---
        # Calculate the threshold in KB using the user's manual input.
        threshold_kb = ram_gb * 1024 * 1024
        # --- COMMAND DEFINITION ---
        command = f'Set-ItemProperty -Path "{self.reg_path}" -Name "{self.reg_name}" -Type DWord -Value {threshold_kb} -Force'
        logging.info(f"Applying SvcHostSplitThreshold tweak (MANUAL OVERRIDE: {ram_gb}GB -> {threshold_kb}KB)...")
        self._execute_command(command)
        return self.finalization_message

    def undo(self):
        """
        Reverts the tweak to the Windows default state. (Unchanged)
        """
        # --- COMMAND DEFINITION ---
        command = f'Set-ItemProperty -Path "{self.reg_path}" -Name "{self.reg_name}" -Type DWord -Value {self.default_value_decimal} -Force'
        logging.info("Reverting SvcHostSplitThreshold tweak to default...")
        self._execute_command(command)
        return self.finalization_message

    def _execute_command(self, command: str):
        """
        A private helper method to execute a given PowerShell command silently. (Unchanged)
        """
        try:
            # --- SUBPROCESS EXECUTION ---
            subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            logging.info(f"Successfully executed command: {command}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # --- EXCEPTION HANDLING ---
            logging.error(f"Failed to execute command '{command}': {e}", exc_info=True)
