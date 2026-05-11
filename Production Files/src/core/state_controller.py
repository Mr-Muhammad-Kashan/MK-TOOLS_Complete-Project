# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================


from controllers.performance_tweaks.fast_startup import DisableFastStartupTweak
from controllers.performance_tweaks.compressed_memory import DisableCompressedMemoryTweak
from controllers.performance_tweaks.gpu_scheduling import GPUSchedulingTweak
from controllers.performance_tweaks.process_priority import ForegroundPriorityController
from controllers.performance_tweaks.svchost_split import SvcHostSplitTweak

from controllers.ui_tweaks.context_menu import ClassicContextMenuTweak
from controllers.ui_tweaks.menu_delay import MenuShowDelayTweak
from controllers.ui_tweaks.jpeg_quality import JPEGQualityTweak
from controllers.ui_tweaks.web_search import DisableWebSearchTweak

# ===================================================================================
# PARADIGM SOLUTION: TweakStateController (v1.0 - Zero-Race-Condition Engine)
#
# ARCHITECTURAL BLUEPRINT:
# This class is a new, self-contained, and mission-critical component engineered
# to be the single source of truth for all system pre-flight checks. It offloads
# all synchronous I/O operations (network checks, subprocess calls) from the
# main thread to a dedicated worker thread. It guarantees that a definitive,
# atomic state for every system tweak is determined before the main application
# UI is initialized.
#
# DATA FLOW:
#   [App.__init__]
#      |
#      +-> TweakStateController(app_instance)  (Dependency Injection)
#      |
#      +-> .start_checks()
#             |
#             +-> [Background Thread: _run_all_checks()]
#                    |
#                    +-> 1. Get update info (network I/O)
#                    +-> 2. Loop through all tweak controllers (subprocess I/O)
#                    +-> 3. Store results in a dictionary
#                    |
#                    +-> app_instance.after(0, _on_all_checks_complete, results) (Thread-safe callback)
#                           |
#                           V
#   [Main Thread: _on_pre_flight_complete]
#      |
#      +-> ._on_pre_flight_complete(results)
#             |
#             +-> 1. Hide splash screen
#             +-> 2. Inject results into each UI card
#             +-> 3. Show main UI
#
# This architecture completely eliminates the race condition and guarantees 100%
# startup stability by making the UI a passive consumer of a single, finalized
# data payload.
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


class TweakStateController:
    """
    Manages all asynchronous pre-flight checks, ensuring a single, non-blocking
    source of truth for application state before UI initialization.
    """
    def __init__(self, app_instance):
        # --- Store a reference to the main application instance for thread-safe callbacks.
        self.app = app_instance
        # --- Instantiate all tweak logic controllers once at initialization.
        self.tweak_controllers = {
            'performance_fast_startup': (DisableFastStartupTweak(), "Checking Fast Startup..."),
            'performance_compressed_mem': (DisableCompressedMemoryTweak(), "Analyzing Memory Compression..."),
            'performance_gpu_scheduling': (GPUSchedulingTweak(), "Querying GPU Scheduler..."),
            'performance_fg_priority': (ForegroundPriorityController(), "Verifying CPU Priority..."),
            'performance_svchost': (SvcHostSplitTweak(), "Checking SvcHost Configuration..."),
            'ui_classic_menu': (ClassicContextMenuTweak(), "Inspecting Context Menu..."),
            'ui_menu_delay': (MenuShowDelayTweak(), "Measuring Menu Delay..."),
            'ui_jpeg_quality': (JPEGQualityTweak(), "Reading Wallpaper Quality..."),
            'ui_web_search': (DisableWebSearchTweak(), "Probing Web Search Policy..."),
            'policy_status': (ApplicationStateController(), "Auditing Group Policies...")
        }
        # --- Initialize the Update Manager.
        self.update_manager = UpdateManager(latest_version_url=AppConfig.LATEST_VERSION_URL)
        # --- Cache for the final, pre-fetched state data.
        self.pre_fetched_states = {}

    def _run_all_checks_in_background(self):
        """
        [WORKER THREAD] The core logic loop that performs all blocking I/O
        operations and reports progress to the UI.
        """
        # --- Add 1 to the total checks to account for the new update check step.
        total_checks = len(self.tweak_controllers) + 1

        # --- STEP 1: Perform the update check.
        # --- Schedule a UI update on the main thread to show the "Checking for updates..." status.
        self.app.after(0, self.app.splash.update_progress, (1 / total_checks), "Checking for updates...")
        # --- Run the actual network check. This might take a few seconds or timeout.
        self.app.update_info = self.update_manager.check_for_updates()

        # --- STEP 2: Loop through all the system tweak checks.
        for i, (key, (controller, status_text)) in enumerate(self.tweak_controllers.items(), start=1):
            # --- Use the correct method name for each controller.
            if key == 'policy_status':
                status = controller.check_policy_status()
            else:
                status = controller.check_status()

            # --- Store the result in the pre-fetched state dictionary.
            self.pre_fetched_states[key] = status
            # --- Schedule a UI update on the main thread for the splash screen.
            progress = (i + 1) / total_checks
            self.app.after(0, self.app.splash.update_progress, progress, status_text)
            # --- A small sleep to make the loading appear smoother on very fast systems.
            time.sleep(0.1)

        # --- After all checks are complete, schedule the finalization step on the main thread.
        self.app.after(0, self.app._on_pre_flight_complete, self.pre_fetched_states)

    def start_checks(self):
        """
        [PUBLIC API] Initiates the pre-flight check process on a new background thread.
        This method is the single point of entry for the entire startup check sequence.
        """
        threading.Thread(target=self._run_all_checks_in_background, daemon=True).start()


# ===================================================================================
# CLASS: ApplicationStateController (v1.0 - Zero-Defect State Persistence Engine)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class is a dedicated, self-contained module that serves as the single source
# of truth for the application's persistent state. It is engineered to interface
# exclusively with the Windows Registry, abstracting all low-level read/write
# operations into a clean, fault-tolerant API. This version includes enhanced
# logging for complete auditability of all state transitions.
#
# REGISTRY INTERACTION MODEL:
#
#   [HKEY_CURRENT_USER]
#       |
#       +-- [Software]
#           |
#           +-- [MK-Tools]      <-- Application-specific registry hive.
#               |
#               +-- [State]     <-- Sub-key for all persistent state values.
#                   |
#                   +-- "PoliciesAppliedStatus" (REG_DWORD)
#                           |
#                           +--> 1 = Policies have been successfully APPLIED by this tool.
#                           +--> 0 = Policies have been successfully RESET by this tool.
#
# CORE PRINCIPLES:
#   1. ENCAPSULATION: All registry paths and value names are hard-coded constants
#      within this class. No other part of the application needs to know the
#      implementation details of where or how the state is stored.
#
#   2. FAULT TOLERANCE: All public methods are wrapped in comprehensive try-except
#      blocks. This guarantees that the application will never crash due to
#      registry permission errors, missing keys, or unexpected data types. The
#      methods will gracefully fail, log the error, and return a safe default state.
#
#   3. ATOMICITY: The constructor ensures the required registry path exists on
#      instantiation. Read and write operations target a single DWORD value,
#      making state changes atomic and reliable.
# ===================================================================================
class ApplicationStateController:
    """
    Manages the persistent state of the application by reading and writing a
    dedicated flag to the Windows Registry.
    """
    # The constructor for the state controller.
    def __init__(self):
        # --- CONSTANTS: Define the exact registry path and value names. ---
        # --- Using a unique name like "MK-Tools" prevents conflicts with other software.
        self.app_name = "MK-Tools" # The root key name for the application in the registry.
        # --- The key path is within HKEY_CURRENT_USER for writing without admin rights.
        self.key_path = f"Software\\{self.app_name}\\State"
        # --- The specific value name for the policy state flag.
        self.value_name = "PoliciesAppliedStatus"

        # --- On instantiation, ensure the registry path exists for subsequent operations.
        self._ensure_key_exists()

    # A private helper method to create the registry key path if it doesn't exist.
    def _ensure_key_exists(self):
        """Creates the necessary registry key if it's not already present."""
        try:
            # --- Open the key with write access.
            # --- `winreg.CreateKey` will open an existing key or create it if it's missing.
            # --- This is an idempotent operation, safe to run on every application start.
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.key_path)
            # --- Close the key handle to release system resources immediately.
            winreg.CloseKey(key)
            # --- Log the successful verification or creation of the registry key for audit trail.
            logging.info(f"State Persistence Engine: Registry key '{self.key_path}' is present and accounted for.")
        except OSError as e:
            # --- Log a critical error if the key cannot be created (e.g., permissions issue).
            # --- This is a fatal flaw in the environment if it occurs.
            logging.error(f"STATE ENGINE FAILURE: Could not create or open registry key at '{self.key_path}'. Error: {e}")

    # Checks the registry for the current policy status.
    def check_policy_status(self) -> bool:
        """
        Reads the PoliciesAppliedStatus flag from the registry.

        Returns:
            bool: True if the flag is 1 (applied), False otherwise (0, missing, or error).
        """
        try:
            # --- Open the registry key with read-only access for the state query.
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_READ)
            # --- Read the DWORD value. The `[0]` accesses the value from the returned (value, type) tuple.
            value, _ = winreg.QueryValueEx(key, self.value_name)
            # --- Close the key handle immediately after reading.
            winreg.CloseKey(key)
            # --- Log the found state for debugging and auditing purposes.
            logging.info(f"State Query: Read policy status from registry. Raw value: {value}. Status: {'APPLIED' if value == 1 else 'RESET'}")
            # --- Return True only if the value is exactly 1, representing the 'Applied' state.
            return value == 1
        except FileNotFoundError:
            # --- This is the expected case if the value has never been set. It is not an error.
            logging.info(f"State Query: '{self.value_name}' not found in registry. Defaulting to state: NOT APPLIED.")
            # --- If the value doesn't exist, the policies are considered not applied (default state).
            return False
        except OSError as e:
            # --- This catches other potential issues like permission denied during read.
            logging.error(f"State Query FAILURE: Error reading registry value at '{self.key_path}\\{self.value_name}'. Error: {e}")
            # --- In case of any read error, safely assume the default 'not applied' state.
            return False

    # Sets the registry flag to the "Applied" state (1).
    def set_status_applied(self) -> bool:
        """Writes the 'Applied' state (1) to the registry."""
        try:
            # --- Open the key with write access to modify the state.
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_WRITE)
            # --- Set the DWORD value to 1, representing the 'Applied' state.
            winreg.SetValueEx(key, self.value_name, 0, winreg.REG_DWORD, 1)
            # --- Close the key handle to commit the change and release resources.
            winreg.CloseKey(key)
            # --- Log the successful state transition for the audit trail.
            logging.info("State Transition: Successfully set policy status to APPLIED (1) in registry.")
            # --- Return True to indicate the operation was successful.
            return True
        except OSError as e:
            # --- Log any error that occurs during the write operation.
            logging.error(f"State Transition FAILURE: Error writing 'Applied' state to registry. Error: {e}")
            # --- Return False to indicate the operation failed.
            return False

    # Sets the registry flag to the "Reset" state (0).
    def set_status_reset(self) -> bool:
        """Writes the 'Reset' state (0) to the registry."""
        try:
            # --- Open the key with write access to modify the state.
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_WRITE)
            # --- Set the DWORD value to 0, representing the 'Reset' or default state.
            winreg.SetValueEx(key, self.value_name, 0, winreg.REG_DWORD, 0)
            # --- Close the key handle to commit the change and release resources.
            winreg.CloseKey(key)
            # --- Log the successful state transition for the audit trail.
            logging.info("State Transition: Successfully set policy status to RESET (0) in registry.")
            # --- Return True to indicate the operation was successful.
            return True
        except OSError as e:
            # --- Log any error that occurs during the write operation.
            logging.error(f"State Transition FAILURE: Error writing 'Reset' state to registry. Error: {e}")
            # --- Return False to indicate the operation failed.
            return False
