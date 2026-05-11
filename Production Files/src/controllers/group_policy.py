# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: GroupPolicyController (v3.2 - State-Integrated & Enhanced Auditing)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class is the definitive backend logic engine for all Group Policy operations.
# It is engineered to be completely decoupled from the UI, receiving commands from
# the PolicyFrame and executing them with military-grade precision. This version is
# integrated with the ApplicationStateController to persist its operational state
# and features an enhanced auditing protocol for forensic-level error analysis.
#
# OPERATIONAL FLOW:
#
#   [UI Layer (PolicyFrame)] --(command)--> [GroupPolicyController]
#         |                                        |
#         |                                        +-- 1. Pre-flight checks (Admin, LGPO.exe exists)
#         |                                        |
#         |                                        +-- 2. Execute operation (LGPO.exe / PowerShell)
#         |                                        |
#         | (feedback message) <-------------------+-- 3. Return success/failure message
#         |                                        |
#         '--(state update)--> [ApplicationStateController] <--+-- 4. On success, update persistent state
#
# CORE PRINCIPLES:
#   1. COMMAND DELEGATION: This class executes complex system commands using the
#      most reliable tools for the job: Microsoft's `LGPO.exe` for policy import
#      and a comprehensive PowerShell script for a true system reset.
#
#   2. STATE SYNCHRONIZATION: Upon the successful completion of an operation, it
#      issues a command to the `ApplicationStateController` to update the
#      persistent state flag in the registry, ensuring the application's state
#      is always synchronized with the system's.
#
#   3. FORENSIC AUDITING: The command runner has been enhanced to capture and log
#      the specific `stderr` output from failed subprocesses, providing a detailed
#      audit trail for rapid troubleshooting of any operational failures.
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


class GroupPolicyController:
    """
    Manages all Group Policy operations and integrates with the application's
    state controller to persist its state.
    """
    # The constructor now accepts an instance of the state controller.
    def __init__(self, state_controller: 'ApplicationStateController'):
        # --- Store a reference to the state management module passed via dependency injection.
        self.state_controller = state_controller
        # --- DYNAMIC PATH RESOLUTION: Determines the app's root directory at runtime.
        if getattr(sys, 'frozen', False):
            # --- Executing as a bundled executable (e.g., via PyInstaller). The base path is the executable's directory.
            self.base_path = os.path.dirname(sys.executable)
        else:
            # --- Executing as a standard Python script. The base path is the script's directory.
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        # --- RESOURCE PATHS ---
        # --- The absolute path to the LGPO utility, a critical dependency.
        self.lgpo_path = os.path.join(self.base_path, "assets", "tools", "group_policy", "LGPO.exe")
        # --- The absolute path to the PARENT FOLDER of the master GPO backup. LGPO targets this folder.
        self.backup_path = os.path.join(self.base_path, "assets", "tools", "group_policy", "MyLocalGPO_Backup")

    # A private, robust helper method to execute a given command-line operation.
    def _run_command(self, command_list: list) -> tuple[bool, str]:
        """The single, secure gateway for all subprocess execution, with enhanced error logging."""
        # --- PRE-FLIGHT CHECK 1: Mandate administrative privileges for all policy operations using the central PrivilegeManager.
        if not PrivilegeManager._is_admin():
            logging.error("FATAL: Administrative privileges are required for Group Policy operations.")
            return (False, "Error: Administrative privileges are required.")
        # --- PRE-FLIGHT CHECK 2: Verify existence of the critical LGPO.exe dependency if it's being called.
        if "LGPO.exe" in command_list[0] and not os.path.exists(self.lgpo_path):
            logging.error(f"FATAL: LGPO.exe not found at expected path: {self.lgpo_path}")
            return (False, "Error: LGPO.exe dependency not found.")
        try:
            # --- Execute the command silently (`CREATE_NO_WINDOW`), capturing all output for analysis.
            result = subprocess.run(
                command_list,
                capture_output=True, text=True, check=False, # `check=False` allows us to handle errors manually.
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # --- Evaluate the result based on the process's exit code.
            if result.returncode == 0:
                # --- A return code of 0 indicates absolute success.
                logging.info(f"Command succeeded: {' '.join(command_list)}")
                return (True, "Operation completed successfully.")
            else:
                # --- A non-zero return code indicates failure. Log the specific error for forensics.
                error_message = f"Command failed with return code {result.returncode}: {' '.join(command_list)}\nSTDERR: {result.stderr.strip()}"
                logging.error(error_message)
                return (False, f"Error: Operation failed. See application logs for details.")
        except Exception as e:
            # --- A final catch-all for unexpected low-level exceptions during process creation.
            logging.error(f"An unexpected exception occurred while running command: {e}", exc_info=True)
            return (False, "An unexpected system error occurred.")

    # [ENHANCED] Applies policies and updates the persistent state on success.
    def apply_optimized_policies(self) -> str:
        """Applies the optimized GPO backup and sets the state flag on success."""
        # --- Log the intention for clear system auditing.
        logging.info(f"Applying optimized GPO from backup path: {self.backup_path}")
        # --- Construct the command as a list of arguments for `subprocess`. /g imports a GPO backup.
        command = [self.lgpo_path, "/g", self.backup_path]
        # --- Execute the command via the robust runner.
        success, message = self._run_command(command)
        # --- If the operation was a success, command the state controller to set the "Applied" flag.
        if success:
            self.state_controller.set_status_applied()
            return "Optimized policies have been successfully applied."
        else:
            # --- If it failed, return the error message from the runner.
            return f"Failed to apply policies. {message}"

    # [ENHANCED] Resets policies and updates the persistent state on success.
    def reset_to_default(self) -> str:
        """Resets all local Group Policies to a clean slate and sets the state flag on success."""
        # --- Log the intention for clear system auditing.
        logging.info("Executing definitive reset of all Local Group Policies to Windows default state.")
        # --- This multi-stage PowerShell script performs a forensically clean reset.
        power_script = """
            # Set the error action to 'Stop' to ensure the script exits on any failure.
            $ErrorActionPreference = 'Stop'
            try {
                # 1. Stop the Group Policy Client service to unlock policy files.
                Stop-Service -Name "gpsvc" -Force -ErrorAction SilentlyContinue

                # 2. Delete the machine and user policy directories to remove all settings.
                Remove-Item -Path "$env:SystemRoot\\System32\\GroupPolicy" -Recurse -Force -ErrorAction SilentlyContinue
                Remove-Item -Path "$env:SystemRoot\\System32\\GroupPolicyUsers" -Recurse -Force -ErrorAction SilentlyContinue

                # 3. Re-apply the default Windows security template to reset security policies.
                secedit /configure /db "$env:windir\\security\\database\\secedit.sdb" /cfg "$env:windir\\inf\\defltbase.inf" /overwrite /quiet

                # 4. Restart the Group Policy Client service.
                Start-Service -Name "gpsvc" -ErrorAction SilentlyContinue

                # 5. Force an update of the Group Policies to apply the clean state immediately.
                gpupdate /force | Out-Null

                # 6. Exit with a success code.
                exit 0
            } catch {
                # In case of any error, ensure the service is restarted.
                Start-Service -Name "gpsvc" -ErrorAction SilentlyContinue
                # Exit with a failure code.
                exit 1
            }
        """
        # --- Construct the command list to execute the script without needing a .ps1 file.
        command_list = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", power_script]
        # --- Execute the command.
        success, message = self._run_command(command_list)
        # --- If the script exited successfully, command the state controller to set the "Reset" flag.
        if success:
            self.state_controller.set_status_reset()
            return "All Group Policies have been successfully reset to Windows default."
        else:
            # --- If it failed, return the error message.
            return f"Failed to reset policies. {message}"
