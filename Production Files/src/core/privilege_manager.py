# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# -----------------------------------------------------------------------------------
# Admin Privileges Check :
# -----------------------------------------------------------------------------------
# ===================================================================================
# CLASS: PrivilegeManager (v1.0 - Zero-Defect Elevation Protocol)
#
# ARCHITECTURAL BLUEPRINT:
# This class is the definitive, self-contained authority for all privilege-related
# operations. It encapsulates the necessary Windows API calls to provide a robust,
# fail-safe, and architecturally pure solution for ensuring the application runs
# with the required administrative rights.
#
# CORE PRINCIPLES:
#   1. ENCAPSULATION: All logic for checking and requesting administrator
#      privileges is contained within this class. No other part of the application
#      needs to be aware of the underlying OS-level implementation.
#
#   2. SINGLE POINT OF ENTRY: The static method `ensure_admin()` is the sole
#      public interface. This provides a clear, unambiguous command that is
#      executed at the application's entry point, guaranteeing that the entire
#      program runs in the correct security context from the very beginning.
#
#   3. SAFETY & RELIABILITY: The class uses the standard, Microsoft-approved
#      UAC elevation mechanism via the ShellExecuteEx API. It does not attempt
#      to bypass security features or modify system integrity. Error handling is
#      built-in to gracefully manage scenarios where elevation is denied or fails.
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


class PrivilegeManager:
    """A self-contained utility for managing and ensuring administrative privileges."""

    @staticmethod
    def _is_admin() -> bool:
        """
        Performs a direct check for administrative privileges using the Windows API.
        This is the most reliable and secure method to determine the current elevation state.

        Returns:
            bool: True if the process is running with admin rights, False otherwise.
        """
        try:
            # --- Use the 'IsUserAnAdmin' function from the shell32 library.
            # --- This is a direct query to the OS and is the ground truth for privilege level.
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            # --- In the unlikely event this API call fails, log the error and default to a safe, non-admin state.
            logging.error(f"Failed to check admin status: {e}", exc_info=True)
            return False

    @staticmethod
    def ensure_admin():
        """
        The definitive public method to ensure the application is running as an administrator.
        If not elevated, it triggers a UAC prompt to re-launch the application with elevated rights.
        """
        # --- Check the current privilege level using the internal helper method.
        if not PrivilegeManager._is_admin():
            logging.warning("Administrative privileges not detected. Attempting to re-launch with elevation.")
            try:
                # --- Use the ShellExecuteEx API to re-launch the script with the 'runas' verb.
                # --- This is the standard, user-facing method to request elevation via a UAC prompt.
                ShellExecuteEx(
                    nShow=win32con.SW_SHOWNORMAL,
                    lpVerb='runas',
                    lpFile=sys.executable,
                    # --- Pass the original script name and arguments to the new process.
                    lpParameters=' '.join([f'"{arg}"' for arg in sys.argv])
                )
                # --- After successfully requesting elevation, the current, non-elevated process must exit.
                logging.info("Elevation requested. Exiting current non-admin process.")
                sys.exit(0)
            except Exception as e:
                # --- If the elevation request fails (e.g., user clicks "No" on the UAC prompt),
                # --- log the error and terminate the application, as it cannot function correctly.
                logging.critical(f"Failed to elevate privileges: {e}", exc_info=True)
                # --- Display a user-friendly error message before exiting.
                root = tk.Tk()
                root.withdraw()
                tk.messagebox.showerror("Privilege Error", "This application requires administrative privileges to function correctly. Please restart as an administrator.")
                sys.exit(1)
        else:
            # --- If already running as admin, log the successful check and allow the application to proceed.
            logging.info("Administrative privileges confirmed.")
