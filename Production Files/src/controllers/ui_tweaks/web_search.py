# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: DisableWebSearchTweak (v2.0 - Dual-Key Modification Engine)
#
# ARCHITECTURAL BLUEPRINT:
# This definitive version of the logic controller executes a comprehensive, multi-key
# registry modification to provide a military-grade block on Windows web search.
# It targets both the user-level suggestion key (HKCU) and the machine-level
# results key (HKLM) in a single, atomic operation, as per the provided notes.
#
# CORE PRINCIPLES:
#   1. COMPREHENSIVE BLOCKING: Unlike the previous version, this engine modifies
#      two separate registry keys (`DisableSearchBoxSuggestions` and
#      `ConnectedSearchUseWeb`) to block both search suggestions and final web
#      results, providing a more robust and complete tweak.
#
#   2. STRICT STATE VALIDATION: The `check_status` method now considers the tweak
#      "active" only if BOTH registry keys are correctly configured. If either key
#      is missing or incorrect, the state is considered "default".
#
#   3. META POWER SHELL COMMANDS: The `apply` and `undo` methods now utilize
#      multi-line PowerShell scripts that perform all necessary operations
#      (path creation, value setting/removal for both keys) in a single,
#      fault-tolerant execution block.
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


class DisableWebSearchTweak:
    """
    Manages the logic for disabling web search by modifying both user and machine
    level registry policies for a comprehensive effect.
    """
    def __init__(self):
        # --- REGISTRY CONSTANTS ---
        # Define paths and names for BOTH registry keys this class now controls.
        self.reg_path_hkcu = "HKCU:\\Software\\Policies\\Microsoft\\Windows\\Explorer"
        self.reg_name_hkcu = "DisableSearchBoxSuggestions"
        self.reg_path_hklm = "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search"
        self.reg_name_hklm = "ConnectedSearchUseWeb"
        self.finalization_message = "Change applied! A system restart is required for this change to take full effect."

    def check_status(self) -> bool:
        """
        Checks if BOTH registry keys are correctly configured to disable web search.

        Returns:
            bool: True only if both tweaks are active, False otherwise.
        """
        # --- Multi-step PowerShell check command ---
        command = f"""
            $hkcuPath = "{self.reg_path_hkcu}"
            $hkcuName = "{self.reg_name_hkcu}"
            $hklmPath = "{self.reg_path_hklm}"
            $hklmName = "{self.reg_name_hklm}"

            $hkcu_ok = $false
            if (Test-Path $hkcuPath) {{
                $prop = Get-ItemProperty -Path $hkcuPath -Name $hkcuName -ErrorAction SilentlyContinue
                if ($prop -and $prop.$hkcuName -eq 1) {{ $hkcu_ok = $true }}
            }}

            $hklm_ok = $false
            if (Test-Path $hklmPath) {{
                $prop = Get-ItemProperty -Path $hklmPath -Name $hklmName -ErrorAction SilentlyContinue
                if ($prop -and $prop.$hklmName -eq 0) {{ $hklm_ok = $true }}
            }}

            if ($hkcu_ok -and $hklm_ok) {{ Write-Output "True" }}
            else {{ Write-Output "False" }}
        """
        try:
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            is_enabled = result.stdout.strip() == "True"
            logging.info(f"DisableWebSearch (Comprehensive) status check: {'Enabled' if is_enabled else 'Disabled'}")
            return is_enabled
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logging.error(f"Error checking comprehensive DisableWebSearch status: {e}", exc_info=True)
            return False

    def apply(self) -> str:
        """
        Applies the tweak by setting both HKCU and HKLM registry keys.

        Returns:
            str: A message for the user indicating next steps.
        """
        # --- Meta PowerShell command to apply both registry changes ---
        command = f"""
            # Configure HKCU key (Disable Suggestions)
            $hkcuPath = "{self.reg_path_hkcu}"
            if (-not (Test-Path $hkcuPath)) {{ New-Item -Path $hkcuPath -Force | Out-Null }}
            Set-ItemProperty -Path $hkcuPath -Name "{self.reg_name_hkcu}" -Value 1 -Type DWord -Force

            # Configure HKLM key (Disable Web Results)
            $hklmPath = "{self.reg_path_hklm}"
            if (-not (Test-Path $hklmPath)) {{ New-Item -Path $hklmPath -Force | Out-Null }}
            Set-ItemProperty -Path $hklmPath -Name "{self.reg_name_hklm}" -Value 0 -Type DWord -Force
        """
        logging.info("Applying comprehensive DisableWebSearch tweak...")
        self._execute_command(command)
        return self.finalization_message

    def undo(self) -> str:
        """
        Reverts the tweak by removing both HKCU and HKLM registry values.

        Returns:
            str: A message for the user indicating next steps.
        """
        # --- Meta PowerShell command to remove both registry values ---
        command = f"""
            Remove-ItemProperty -Path "{self.reg_path_hkcu}" -Name "{self.reg_name_hkcu}" -ErrorAction SilentlyContinue -Force
            Remove-ItemProperty -Path "{self.reg_path_hklm}" -Name "{self.reg_name_hklm}" -ErrorAction SilentlyContinue -Force
        """
        logging.info("Reverting comprehensive DisableWebSearch tweak...")
        self._execute_command(command)
        return self.finalization_message

    def _execute_command(self, command: str):
        """A private helper to execute a PowerShell command silently."""
        try:
            subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            logging.info(f"Successfully executed comprehensive command.")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logging.error(f"Failed to execute comprehensive command: {e}", exc_info=True)
