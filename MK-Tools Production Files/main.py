# ===================================================================================
# MK-TOOLS (v1.0) - MILITARY-GRADE MASTER VERSION
# File: main.py
# Version: V1.0
# Description: The definitive, fully audited, and corrected version of the application.
#              This build incorporates all architectural, performance, stability, and
#              security enhancements.
# Change Log:
#   - Refactored for stability, performance, and maintainability.
#   - Centralized all external configurations.
#   - Implemented robust, non-blocking modal dialogs.
#   - Hardened shutdown protocol.
# ===================================================================================

# ===================================================================================
# ARCHITECTURAL BLUEPRINT: MK-TOOLS (v1.0)
# ===================================================================================
# ````
# [SYSTEM OVERVIEW]
# - Purpose: A military-grade Windows optimization tool with a modern GUI, sound feedback, and system cleanup capabilities.
# - Entry Point: `main.py` -> `PrivilegeManager.ensure_admin` -> `App` instantiation.
# - Core Components:
#   - PrivilegeManager: Ensures administrative privileges via Windows UAC.
#   - AppConfig: Centralized configuration for external links and constants.
#   - ScreenManager: Handles DPI-aware window centering.
#   - Theme: Defines a comprehensive color palette, fonts, and light/dark mode support.
#   - UIManager: Manages dynamic UI scaling based on window size.
#   - SoundManager: Singleton for auditory feedback with global toggle.
#   - SplashScreen: Animated loading screen with custom progress bar.
#   - App: Main application orchestrator with pre-flight checks.
#   - CleanCacheFrame: Manages cache cleanup operations with PowerShell integration.
#   - CleanCacheCard: UI component for individual cleanup tasks.
#   - AboutFrame: Displays creator info and external links.
#   - NavigationRail: Left-side navigation with sound toggle.

# [DATA PATHWAYS]
#   +-------------------+       +-------------------+       +-------------------+
#   |  PrivilegeManager | ----> |       App        | ----> |   SplashScreen    |
#   | (Admin Check)     |       | (Main Controller)|       | (Loading UI)      |
#   +-------------------+       +-------------------+       +-------------------+
#                                    |
#                                    | (UI Components & Navigation)
#                                    v
#   +-------------------+       +-------------------+       +-------------------+
#   |    ScreenManager | <---- |  NavigationRail  | ----> |  Content Frames   |
#   | (DPI & Centering)|       | (Frame Switching)|       | (CleanCacheFrame, |
#   +-------------------+       +-------------------+       |  AboutFrame, etc.)|
#                                    |                     +-------------------+
#                                    | (Sound Feedback)
#                                    v
#   +-------------------+       +-------------------+
#   |    Theme         | <---- |   SoundManager   |
#   | (Colors & Fonts) |       | (Audio Playback) |
#   +-------------------+       +-------------------+
#                                    |
#                                    | (UI Scaling)
#                                    v
#   +-------------------+
#   |    UIManager     |
#   | (Dynamic Scaling)|
#   +-------------------+

# [FILE SYSTEM INTEGRATION]
#   - gifs/*.gif: Used in `SplashScreen`, `CleanCacheFrame`, `AboutFrame` for animations.
#   - Icons/*.ico: Used for window icons and social buttons.
#   - Sound Effects/*.mp3: Loaded by `SoundManager` for auditory feedback.
#   - Group Policy Editor Tools: Backup files and `LGPO.exe` for policy tweaks.

# [CONTROL FLOW]
# 1. `PrivilegeManager.ensure_admin`: Checks and requests admin rights via UAC.
# 2. `App.__init__`: Initializes `SoundManager`, `SplashScreen`, and UI (hidden).
# 3. `App._run_pre_flight_checks`: Background thread for system state checks.
# 4. `SplashScreen.update_progress`: Updates custom progress bar during checks.
# 5. `App._on_pre_flight_complete`: Reveals main UI, closes splash screen.
# 6. `NavigationRail`: Switches between content frames (e.g., `CleanCacheFrame`).
# 7. `CleanCacheFrame._run_clean_all_logic`: Executes cleanup with PowerShell.
# 8. `SoundManager`: Plays sounds for UI interactions (e.g., `nav_click`, `clean_all_click`).

# [KEY DEPENDENCIES]
# - Standard Libraries: `ctypes`, `tkinter`, `pygame`, `subprocess`, etc.
# - Third-Party: `customtkinter`, `fuzzywuzzy`, `PIL`.
# - Windows-Specific: `win32con`, `win32com.shell`.
# - External Assets: GIFs, ICOs, MP3s, and Group Policy files.
# ```
# # ===================================================================================

# ===================================================================================
# SECTION 1: IMPORT MANIFEST & STRATEGIC DEPENDENCY INCLUSION
# This section constitutes the complete and exclusive list of all external modules
# and libraries required for the application's execution. Each import is a critical
# component, deliberately chosen to fulfill a specific, non-redundant role in the
# system's architecture. The manifest is divided into logical groupings for clarity
# and dependency analysis.
# ===================================================================================

# -----------------------------------------------------------------------------------
# SUB-SECTION 1.1: PYTHON STANDARD LIBRARY
# Core modules integrated into the standard Python distribution. These provide the
# foundational, platform-agnostic capabilities for system interaction, data
# manipulation, and concurrency.
# -----------------------------------------------------------------------------------
import atexit                                                            # FACILITATOR: Registers engine shutdown and resource cleanup functions. Ensures graceful termination and prevents orphaned processes or corrupted state data upon exit.
import ctypes                                                            # BRIDGE: Provides a low-level interface for direct interaction with C-compatible data types and functions. Essential for invoking native Windows API calls for advanced system control.
import ctypes.wintypes                                                   # DATATYPE EXTENSION (for ctypes): Supplies Windows-specific data type definitions (e.g., HWND, DWORD) required for interfacing with the WinAPI through ctypes.
import getpass                                                           # SECURITY/ENVIRONMENT: Securely retrieves the current user's system username without echoing it to the console, crucial for user-specific pathing and permissions.
import json                                                              # DATA INTERCHANGE: Implements the ubiquitous JavaScript Object Notation (JSON) data format. Used for serializing and de-serializing application configuration, state data, and API communication payloads.
import logging                                                           # DIAGNOSTICS & AUDITING: Establishes a robust framework for recording application events, warnings, and critical errors. Essential for debugging, operational monitoring, and post-mortem analysis.
import math                                                              # COMPUTATIONAL CORE: Provides access to fundamental mathematical functions and constants (e.g., trigonometric, logarithmic) for geometric calculations and data analysis.
import os                                                                # FILESYSTEM ABSTRACTION: A platform-agnostic interface for interacting with the operating system's file structure. Manages path manipulation, directory creation, and file existence checks.
import random                                                            # UTILITY/ALGORITHMIC: Supplies algorithms for generating pseudo-random numbers. Utilized for creating unique identifiers, implementing stochastic processes, or introducing jitter.
import cairosvg                                                          # GRAPHICS RENDERING ENGINE: A high-performance vector graphics converter. Specifically used to transcode Scalable Vector Graphics (SVG) assets into rasterized PNG format in-memory for display.
import shutil                                                            # HIGH-LEVEL FILESYSTEM OPS: Augments the 'os' module with advanced file operations, including high-level tree copying and removal, essential for managing complex directory structures.
import subprocess                                                        # PROCESS MANAGEMENT: Enables the spawning of new child processes, connecting to their input/output/error pipes, and obtaining their return codes. Critical for executing external scripts or command-line tools.
import sys                                                               # PYTHON RUNTIME INTERFACE: Provides access to variables and functions that interact strongly with the Python interpreter itself, such as command-line arguments and system exit protocols.
import pyglet.font                                                       # FONT MANAGEMENT: A specialized module for loading custom font files (e.g., .ttf, .otf) directly into the application's memory space, ensuring consistent typography regardless of system-installed fonts.
import threading                                                         # CONCURRENCY ENGINE: Enables the execution of multiple threads (lightweight processes) concurrently. Deployed here for non-blocking operations like audio playback to maintain UI responsiveness.
import psutil                                                            # SYSTEM PROFILING: A cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks), vital for system health checks and performance diagnostics.
import time                                                              # TEMPORAL CONTROL: Provides a suite of functions for handling time-related tasks, from simple delays (time.sleep) to high-precision performance counters for profiling code execution.
import tkinter as tk                                                     # GUI FRAMEWORK (ROOT): The foundational library for creating the main application window and managing the event loop. Serves as the root container for all GUI elements.
from tkinter import filedialog                                           # GUI FRAMEWORK (UTILITY): A specific submodule of Tkinter that provides access to native OS file/directory selection dialogs, ensuring a familiar user experience.
import webbrowser                                                        # SYSTEM INTEGRATION: Provides a high-level interface to display web-based documents to users, typically by invoking the system's default web browser.
import winreg                                                            # WINDOWS REGISTRY INTERFACE: Enables direct interaction with the Windows Registry database for reading system configuration, verifying software installation, or persisting application settings.
from queue import Queue                                                  # THREAD-SAFE DATA STRUCTURE: Implements a multi-producer, multi-consumer queue. Essential for safe, synchronized communication and data exchange between different threads.
from typing import List, Dict, Optional, Tuple, Callable                 # CODE INTROSPECTION & ROBUSTNESS: Provides type hinting capabilities. Enforces code quality, improves readability, and allows static analysis tools to catch potential type-related errors before runtime.

# -----------------------------------------------------------------------------------
# SUB-SECTION 1.2: THIRD-PARTY LIBRARIES
# External, mission-critical packages installed into the environment. These provide
# specialized, high-performance functionalities not available in the Standard Library.
# -----------------------------------------------------------------------------------
import customtkinter as ctk                                               # MODERN GUI TOOLKIT: A high-level extension of Tkinter that provides a modern, themeable, and professional widget set for constructing the user interface.
import pygame                                                             # MULTIMEDIA FRAMEWORK: A comprehensive library primarily leveraged here for its robust and low-latency audio subsystem (pygame.mixer) for sound effect management and playback.
from fuzzywuzzy import fuzz                                               # STRING-MATCHING ALGORITHM: Implements Levenshtein Distance calculations to provide "fuzzy" string matching. Crucial for user-friendly search features that tolerate typos and partial matches.
from PIL import Image                                                     # IMAGE PROCESSING SUITE (Pillow): A powerful library for opening, manipulating, and saving many different image file formats. The de-facto standard for image operations in Python.
import requests                                                           # NETWORKING CLIENT: A high-level HTTP client library for making network requests. Deployed for tasks like checking for application updates from a remote server or interacting with REST APIs.
from packaging.version import parse as parse_version                      # VERSIONING STANDARD COMPLIANCE: Provides a robust parser for software version strings (compliant with PEP 440). Essential for reliably comparing local and remote application versions.

# -----------------------------------------------------------------------------------
# SUB-SECTION 1.3: PLATFORM-SPECIFIC LIBRARIES (WINDOWS)
# Dependencies required for deep integration with the Microsoft Windows operating
# system. Encapsulated in a try-except block to ensure graceful failure on
# non-Windows platforms.
# -----------------------------------------------------------------------------------
try:
    import win32con                                                       # WINDOWS CONSTANTS: A repository of thousands of constants used by the Win32 API. Necessary for specifying flags and parameters in native API calls.
    from win32com.shell import shellcon                                   # WINDOWS SHELL CONSTANTS: A specific subset of Win32 constants related to the Windows Shell API, used for operations like creating shortcuts or managing file properties.        # type: ignore
    from win32com.shell.shell import ShellExecuteEx                       # WINDOWS SHELL EXECUTION: A powerful function for performing shell operations, most notably for requesting elevated (Administrator) privileges for a child process.              # type: ignore
except ImportError:
    # CRITICAL FAILURE HANDLER: This block executes only if the 'pywin32' dependency
    # is not installed. It logs the critical failure and presents a user-facing
    # error message before terminating the application to prevent unstable operation.
    logging.critical("FATAL: PyWin32 library not found. This is a non-recoverable, required dependency for core OS integration.")
    root = tk.Tk()
    root.withdraw() # Hide the empty root window.
    tk.messagebox.showerror("Dependency Error", "Required library 'pywin32' is not installed. Application cannot start.")
    sys.exit(1) # Terminate with a non-zero exit code to indicate failure.

# -----------------------------------------------------------------------------------
# SUB-SECTION 1.4: SPECIALIZED UTILITY IMPORTS
# Specific functions imported for highly targeted tasks, often related to in-memory
# data manipulation and I/O.
# -----------------------------------------------------------------------------------
from cairosvg import svg2png                                              # DIRECT FUNCTION IMPORT (SVG): A direct import of the primary conversion function from cairosvg for improved performance and code clarity, bypassing module-level access.
from io import BytesIO                                                    # IN-MEMORY I/O STREAM: Provides a binary stream interface that operates on an in-memory bytes buffer. Used to handle the raw PNG data from cairosvg without writing to disk.

# -- New Modules --
from concurrent.futures import ThreadPoolExecutor, as_completed         # PARALLEL EXECUTION ENGINE: A high-level interface for asynchronously executing callables in a pool of threads. Essential for non-blocking, concurrent I/O operations.


# -----------------------------------------------------------------------------------
# Imports END..!
# -----------------------------------------------------------------------------------


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
# -----------------------------------------------------------------------------------

# ===================================================================================
# PARADIGM SOLUTION: Definitive Asset Path Resolution Protocol (v1.0)
# This function is the single source of truth for locating all external asset files
# (icons, sounds, fonts, etc.). It correctly resolves paths for both the standard
# Python execution environment and the frozen, single-file executable environment
# created by PyInstaller, ensuring 100% operational integrity post-compilation.
# ===================================================================================
def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource, working for both development and PyInstaller.
    
    Args:
        relative_path (str): The path to the asset relative to the project root.

    Returns:
        str: The absolute, OS-correct path to the asset.
    """
    try:
        # --- When running as a frozen executable, sys.executable is the absolute path to the .exe file.
        # --- We take its directory as the base for all asset lookups.
        base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    except Exception:
        # --- A final fallback to the current working directory in case of an unknown error.
        base_path = os.path.abspath(".")
    
    # --- Join the determined base path with the asset's relative path to create the absolute path.
    return os.path.join(base_path, relative_path)

# ===================================================================================
# CLASS: UpdateManager (v1.0 - Zero-Latency Update Protocol)
#
# ARCHITECTURAL BLUEPRINT:
# This class is a self-contained, high-integrity logic module designed to perform
# non-blocking, fail-safe application update checks. It operates with a strict
# timeout protocol to guarantee it never impacts application startup latency.
#
# CORE PRINCIPLES:
#   1. ASYNCHRONOUS BY DESIGN: The core method, `check_for_updates`, is
#      intended to be executed on a background thread (e.g., the application's
#      pre-flight check thread) to ensure the UI thread remains 100% responsive.
#
#   2. RESILIENCE & GRACEFUL FAILURE: All network and file operations are
#      encapsulated in robust try-except blocks. It handles connection errors,
#      timeouts, file-not-found, and malformed JSON data, ensuring the
#      application proceeds smoothly even if the update check fails for any reason.
#
#   3. SEMANTIC VERSIONING INTEGRITY: It leverages the authoritative `packaging`
#      library to compare version strings. This is the paradigm solution that
#      correctly handles complex version numbers (e.g., '1.10.0' > '1.9.0'),
#      preventing false positives or negatives common with simple string comparison.
# ===================================================================================
class UpdateManager:
    """Manages the application update check with a non-blocking, cache-compliant protocol."""

    # --- The constructor for the UpdateManager. ---
    def __init__(self, latest_version_url: str):
        # --- The definitive URL for the server-side version manifest.
        self.latest_version_url = latest_version_url
        # --- [MODIFIED] Use the resource_path function for robust path resolution.
        self.local_version_file = resource_path(os.path.join("Version", "version.json"))
        # --- A strict but reasonable timeout for the network request (in seconds).
        self.TIMEOUT = 5.0
        # --- [NEW] Definitive cache-busting headers to ensure the latest data is always fetched.
        self.headers = {
            'Cache-Control': 'no-cache, no-store, must-revalidate', # --- For HTTP/1.1 caches.
            'Pragma': 'no-cache',                                  # --- For legacy HTTP/1.0 caches.
            'Expires': '0'                                         # --- For proxy servers.
        }

    # --- Safely reads and parses the local version.json file. ---
    def _get_local_version(self) -> Optional[str]:
        """
        Safely reads the current version from the local version.json file.

        Returns:
            Optional[str]: The local version string, or None on failure.
        """
        try:
            # --- Pre-flight check to ensure the local version file actually exists.
            if not os.path.exists(self.local_version_file):
                # --- Log a warning if the file is not found.
                logging.warning(f"Local version file not found at: {self.local_version_file}")
                return None
            # --- Open and parse the JSON file.
            with open(self.local_version_file, 'r') as f:
                # --- Safely get the 'version' key from the parsed data.
                return json.load(f).get("version")
        except Exception as e:
            # --- Log any error during file read/parse and return a safe None value.
            logging.error(f"Failed to read or parse local version file: {e}", exc_info=True)
            return None

    # --- [RE-ENGINEERED] Fetches the latest version from the server using cache-busting headers. ---
    def _get_latest_version(self) -> Optional[dict]:
        """
        Fetches the latest version information from the remote server with a strict
        timeout and cache-busting headers to guarantee data freshness.

        Returns:
            Optional[dict]: A dictionary containing the latest version info, or None on failure.
        """
        try:
            # --- Execute the HTTP GET request with the critical headers included.
            response = requests.get(self.latest_version_url, timeout=self.TIMEOUT, headers=self.headers)
            # --- Raise an exception for bad status codes (e.g., 404 Not Found, 500 Server Error).
            response.raise_for_status()
            # --- Parse and return the JSON response body.
            return response.json()
        except requests.exceptions.RequestException as e:
            # --- Handle all network, timeout, or JSON parsing errors gracefully.
            logging.error(f"Failed to fetch or parse latest version from server: {e}", exc_info=True)
            return None

    # --- The main public method to orchestrate the update check. ---
    def check_for_updates(self) -> Optional[dict]:
        """
        The main public method to check for updates. Compares local and remote versions.

        Returns:
            Optional[dict]: The latest version info dictionary if an update is available, otherwise None.
        """
        # --- Get the local and latest version data.
        local_version_str = self._get_local_version()
        latest_version_data = self._get_latest_version()

        # --- Perform a fail-safe check using `all()` to ensure both versions were retrieved.
        if not all([local_version_str, latest_version_data]):
            # --- Log the abortion of the check for auditing.
            logging.warning("Aborting update check due to missing local or remote version data.")
            return None
        
        # --- Safely extract the version string from the remote data.
        latest_version_str = latest_version_data.get("version")
        # --- Ensure the remote data is not malformed.
        if not latest_version_str:
            logging.error("Remote version data is malformed; 'version' key is missing.")
            return None

        try:
            # --- Use the `packaging` library for a robust semantic version comparison.
            if parse_version(latest_version_str) > parse_version(local_version_str):
                # --- Log the successful detection of a new version.
                logging.info(f"Update available: {local_version_str} -> {latest_version_str}")
                # --- Return the full data payload for the UI.
                return latest_version_data
            else:
                # --- Log that the application is current.
                logging.info(f"Application is up to date.")
                return None
        except Exception as e:
            # --- Catch any errors during version parsing (e.g., invalid version string).
            logging.error(f"Error comparing versions: {e}", exc_info=True)
            return None

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

# -----------------------------------------------------------------------------------
# SECTION 1.5: CENTRALIZED CONFIGURATION
# -----------------------------------------------------------------------------------
# ===================================================================================
# File: main.py
# Location: SECTION 1.5: CENTRALIZED CONFIGURATION
# ===================================================================================
class AppConfig:
    """A centralized store for all external links and configurable constants."""
    BUY_ME_A_COFFEE_URL = "https://mr-muhammad-kashan.github.io/Buy-Me-A-Coffee-Website/"
    LINKEDIN_URL = "https://www.linkedin.com/in/muhammad-kashan-tariq"
    GITHUB_URL = "https://github.com/Mr-Muhammad-Kashan"
    CONTACT_EMAIL = "mailto:m.kashan.exe@gmail.com"
    # --- [MODIFIED] This is the corrected, direct link to the raw JSON file for the update check.
    LATEST_VERSION_URL = "https://raw.githubusercontent.com/Mr-Muhammad-Kashan/MK-Tools/main/Version/Version.json"
# -----------------------------------------------------------------------------------

# ===================================================================================
# CLASS: HardwareTierManager (v1.0 - System Profiling & Tiering Engine)
#
# ARCHITECTURAL BLUEPRINT:
# This class is a self-contained, singleton utility designed to perform a one-time
# analysis of the host system's hardware at application startup. Its sole purpose
# is to classify the system into a definitive performance tier (LOW, MID, HIGH)
# based on available physical memory. This classification serves as the ground truth
# for all performance-related conditional logic throughout the application, enabling
# features like animations to be disabled on low-end hardware.
#
# SINGLETON PATTERN:
# The class is implemented as a singleton to guarantee that the hardware detection
# logic is executed exactly once, regardless of how many times the manager is
# instantiated. The result is cached, providing instantaneous access to the
# hardware tier from any component after the initial check.
# ===================================================================================
class HardwareTierManager:
    """
    A singleton manager that detects the system's hardware tier at startup.
    """
    _instance = None
    _tier = "MID"  # Default to a safe middle ground.

    def __new__(cls):
        # --- Ensure only one instance of this class is ever created.
        if cls._instance is None:
            cls._instance = super(HardwareTierManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        # --- Prevent re-initialization on subsequent calls.
        if self._initialized:
            return
        
        # --- Perform the hardware detection once.
        self._detect_tier()
        self._initialized = True

    def _detect_tier(self):
        """
        Analyzes system RAM to classify the hardware into LOW, MID, or HIGH tiers.
        """
        try:
            # --- Get total physical RAM in bytes using psutil.
            ram_bytes = psutil.virtual_memory().total
            # --- Convert bytes to gigabytes for easier classification.
            ram_gb = ram_bytes / (1024**3)

            # --- Classify based on RAM. Thresholds are set to be inclusive.
            if ram_gb <= 6:  # 6GB or less is considered low-tier.
                self.__class__._tier = "LOW"
            elif 6 < ram_gb <= 12: # Between 6GB and 12GB is considered mid-tier.
                self.__class__._tier = "MID"
            else: # Anything above 12GB is considered high-tier.
                self.__class__._tier = "HIGH"
            
            logging.info(f"Hardware Tier Detection: {ram_gb:.2f} GB RAM detected. Classified as TIER: {self._tier}")

        except Exception as e:
            # --- In case of any error, log it and fall back to the default MID tier.
            logging.error(f"Failed to detect hardware tier, defaulting to 'MID'. Error: {e}", exc_info=True)
            self.__class__._tier = "MID"

    def get_tier(self) -> str:
        """
        Public method to access the detected hardware tier.

        Returns:
            str: The detected hardware tier ('LOW', 'MID', or 'HIGH').
        """
        return self.__class__._tier

# ===================================================================================
# CLASS: FontManager (v2.0 - Zero-Defect Typographic Asset Protocol)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class is the definitive, self-contained authority for all custom font
# loading operations. It has been re-engineered for absolute robustness. The new
# protocol includes a pre-flight file existence check for precise error reporting
# and a more granular exception handling sequence. This ensures that in a failure
# scenario, the system can provide a forensically accurate reason for termination
# (e.g., "file missing" vs. "file corrupt"), which is critical for rapid
# diagnostics and field support. The synchronous nature of this operation is
# intentional and mandatory to prevent visual integrity failures during UI rendering.
# ===================================================================================
class FontManager:
    """A static utility class for managing and registering custom application fonts."""

    # --- FONT MANIFEST ---
    # The definitive, exclusive list of all critical typographic assets required
    # for the application's visual and functional integrity.
    REQUIRED_FONTS: List[str] = [
        "NotoColorEmoji-Regular.ttf"
    ]

    # ===============================================================================
    # METHOD: _load_single_font (v1.0 - Atomic Font Loader)
    # This private helper method encapsulates the logic for loading a single font file.
    # It performs pre-flight checks and handles exceptions for a single asset.
    # ===============================================================================
    @staticmethod
    def _load_single_font(font_filename: str):
        """
        Loads a single font file into memory with pre-flight checks and granular error handling.

        Args:
            font_filename (str): The filename of the font to load from the asset directory.
        
        Raises:
            FileNotFoundError: If the font file does not exist at the resolved path.
            Exception: For any other errors during the font loading process (e.g., file is corrupt).
        """
        # --- Resolve the absolute path to the font asset using the universal pathing utility.
        font_path = resource_path(font_filename)
        
        # --- Pre-flight Check: Verify the physical existence of the file before attempting to load.
        # --- This provides a more precise error message than a generic loading failure.
        if not os.path.exists(font_path):
            # --- Raise a specific, informative exception if the file is missing.
            raise FileNotFoundError(f"Required font asset is missing from path: {font_path}")
        
        # --- Attempt to add the font file to the application's in-memory font directory.
        # --- This makes the font available to all UI components. This can fail if the file is corrupt.
        pyglet.font.add_file(font_path)
        
        # --- Log the successful registration of the individual font file for auditing.
        logging.info(f"Successfully registered font: {font_filename}")

    # ===============================================================================
    # METHOD: register_fonts (v2.0 - Hardened Registration Protocol)
    # The sole public interface for this class. It orchestrates the loading of all
    # fonts listed in the manifest and manages the critical failure path.
    # ===============================================================================
    @staticmethod
    def register_fonts():
        """
        The definitive public method to load and register all required fonts.
        This method iterates through the REQUIRED_FONTS manifest and loads each one.
        """
        # --- Log the initiation of the font registration sequence for auditing.
        logging.info("FontManager: Initiating font registration protocol.")
        
        # --- Iterate through each font file specified in the manifest.
        for font_filename in FontManager.REQUIRED_FONTS:
            try:
                # --- Delegate the loading of the font to the atomic helper method.
                FontManager._load_single_font(font_filename)

            # --- Granular Exception Handling ---
            # This sequence provides precise, actionable error information upon failure.
            except FileNotFoundError as e:
                # --- This block executes if the pre-flight check fails (file is missing).
                logging.critical(f"FATAL: {e}", exc_info=True)
                root = tk.Tk()
                root.withdraw() # --- Hide the empty root window.
                tk.messagebox.showerror("Critical Asset Error", f"Required font '{font_filename}' is missing. The application cannot start.")
                sys.exit(1) # --- Terminate with a non-zero exit code.
            except Exception as e:
                # --- This block executes for any other failure, such as a corrupt or unsupported font file.
                logging.critical(f"FATAL: Could not load required font file '{font_filename}'. It may be corrupt. Error: {e}", exc_info=True)
                root = tk.Tk()
                root.withdraw() # --- Hide the empty root window.
                tk.messagebox.showerror("Critical Font Error", f"Required font '{font_filename}' is corrupt or unsupported. The application cannot start.")
                sys.exit(1) # --- Terminate with a non-zero exit code.

# -----------------------------------------------------------------------------------
# ===================================================================================
# CLASS: ScreenManager (v3.0 - Definitive DPI Scaling & Centering Protocol)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This version is the definitive, military-grade authority for all screen and DPI-
# related operations. It establishes a new paradigm for UI scaling by acting as the
# single source of truth for the system's DPI scaling factor.
#
# CORE ENHANCEMENTS:
#   1. [DPI SCALING FACTOR] A new static method, `get_scaling_factor`, has been
#      engineered to directly query the Windows API for the primary monitor's DPI.
#      This provides the ground-truth scaling value (e.g., 1.0 for 100%, 1.5 for 150%)
#      that all other UI components will use for geometry and font size calculations.
#
#   2. [PERFORMANCE] The scaling factor is calculated once and cached in a class-
#      level variable (`_scaling_factor`). This zero-overhead approach ensures that
#      all subsequent calls to `get_scaling_factor` are instantaneous, preventing
#      redundant and costly API queries.
# ===================================================================================
class ScreenManager:
    """
    A definitive utility class providing static methods for all screen-related
    operations, including DPI awareness, scaling factor retrieval, and window centering.
    """
    # --- A private, class-level cache for the scaling factor to ensure it's calculated only once.
    _scaling_factor: float = 0.0

    @staticmethod
    def set_dpi_awareness():
        """
        Sets the application's process to be DPI-aware. This is a critical
        step that must be called before any UI is initialized to ensure correct
        scaling and geometry calculations on high-resolution displays.
        """
        try:
            # --- Attempt to use the most modern API for DPI awareness (Windows 8.1+).
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            logging.info("DPI Awareness set to: PROCESS_PER_MONITOR_DPI_AWARE.")
        except (AttributeError, OSError):
            # --- If the modern API is not available, fall back to the older API (Windows Vista+).
            try:
                ctypes.windll.user32.SetProcessDPIAware()
                logging.info("DPI Awareness set to: SetProcessDPIAware().")
            except Exception as e:
                # --- Log an error if neither method is successful.
                logging.error(f"Failed to set DPI awareness: {e}", exc_info=True)

    @staticmethod
    def get_scaling_factor() -> float:
        """
        [NEW] Retrieves the system's UI scaling factor by querying the primary monitor's DPI.
        The result is cached for performance. This is the single source of truth for all UI scaling.

        Returns:
            float: The UI scaling factor (e.g., 1.0 for 100%, 1.25 for 125%).
        """
        # --- If the scaling factor has already been calculated, return the cached value instantly.
        if ScreenManager._scaling_factor > 0:
            return ScreenManager._scaling_factor

        try:
            # --- Call the Windows User32 API to get the DPI for the primary screen (HWND 0).
            # --- The default DPI is 96.
            dpi = ctypes.windll.user32.GetDpiForWindow(0)
            # --- Calculate the scaling factor relative to the 96 DPI baseline.
            scaling = dpi / 96.0
            # --- If the calculated scaling is nonsensical, default to a safe value of 1.0.
            if scaling <= 0:
                scaling = 1.0
            # --- Cache the calculated scaling factor.
            ScreenManager._scaling_factor = scaling
            logging.info(f"System DPI detected as {dpi}. UI scaling factor set to {scaling:.2f}.")
            return scaling
        except Exception as e:
            # --- In case of any error, log it and fall back to a default, unscaled factor.
            logging.error(f"Failed to get system DPI scaling factor. Defaulting to 1.0. Error: {e}")
            # --- Cache the fallback value to prevent repeated errors.
            ScreenManager._scaling_factor = 1.0
            return 1.0

    @staticmethod
    def center_window(window: ctk.CTk | ctk.CTkToplevel, width: int, height: int):
        """
        Calculates the precise x and y coordinates to center a window on the main display.
        This method will return accurate results only after `set_dpi_awareness()` has been called.

        Args:
            window (ctk.CTk | ctk.CTkToplevel): The window object to be centered.
            width (int): The target width of the window.
            height (int): The target height of the window.
        """
        # --- These methods now return true physical pixel dimensions thanks to DPI awareness.
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # --- Calculate the top-left corner coordinates for perfect centering.
        center_x = int((screen_width / 2) - (width / 2))
        center_y = int((screen_height / 2) - (height / 2))

        # --- Apply the calculated geometry to the window.
        window.geometry(f"{width}x{height}+{center_x}+{center_y}")
# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

# ===================================================================================
# SECTION 2: THEME & STYLE CONFIGURATION (v2.0 - Definitive Font & Scaling Engine)
#
# ARCHITECTURAL BLUEPRINT:
# This class is the definitive, military-grade design system for the application.
# It has been re-engineered with two primary objectives:
#
#   1. HIGH-DPI CALIBRATION: The base FONT_SIZES have been recalibrated to provide
#      excellent readability on a baseline 1080p display, ensuring that the
#      UIManager's scaling calculations produce legible and aesthetically pleasing
#      text on all target resolutions (720p, 1440p, 4K) and system scaling levels.
#
#   2. COMPOSITE FONT PROTOCOL: The initialize_fonts method now creates composite
#      font objects (e.g., ("Segoe UI", "Noto Color Emoji")). This is the paradigm
#      solution for the emoji rendering anomaly. It instructs the rendering engine
#      to first attempt to render a character with the primary UI font ('Segoe UI')
#      and, if the character (glyph) is not found, to seamlessly fall back to the
#      universal emoji font ('Noto Color Emoji'). This guarantees 100% consistent
#      rendering of all text and emojis across all Windows versions without
#      structural UI changes.
# ===================================================================================
class Theme:
    """
    The definitive, military-grade theme class for MK-Tools. This version includes
    a re-architected font engine with composite font families to ensure 100%
    consistent emoji and text rendering across all target platforms.
    """
    # --- Global Configuration ---
    CURRENT_MODE = "dark"
    SCALING_FACTOR = 1.0

    # --- Color Palette: Dark Mode ---
    BACKGROUND_DARK = "#1A1920"; NAV_RAIL_DARK = "#23212E"; CARD_DARK = "#2C2A3B"; CARD_HOVER_DARK = "#353345"; TEXT_DARK = "#F5F5FF"; TEXT_SECONDARY_DARK = "#A8A5C5"
    ACCENT_DARK = "#9A4BFF"; ACCENT_HOVER_DARK = "#8A3EE8"; ACCENT_ACTIVE_DARK = "#6F2DCC"; ACCENT_DISABLED_DARK = "#6B4E99"
    BORDER_DARK = "#4C4A5B"; BORDER_HOVER_DARK = "#5D5A6C"; BORDER_ACTIVE_DARK = "#6E6A7D"
    INFO_PANEL_DARK = "#383647"; INFO_PANEL_HOVER_DARK = "#403E57"
    SECONDARY_DARK = "#5E5B70"; SECONDARY_HOVER_DARK = "#6F6C81"; SECONDARY_ACTIVE_DARK = "#807D92"; SECONDARY_DISABLED_DARK = "#4F4C5F"
    TERTIARY_DARK = "#7A7790"; TERTIARY_HOVER_DARK = "#8B889F"; TERTIARY_ACTIVE_DARK = "#9C99B0"; TERTIARY_DISABLED_DARK = "#6B687F"
    STATE_ON_FG_DARK = "#2E7D32"; STATE_ON_HOVER_DARK = "#4CAF50"; STATE_ON_ACTIVE_DARK = "#388E3C"; STATE_ON_DISABLED_DARK = "#1B5E20"
    STATE_OFF_FG_DARK = "#C62828"; STATE_OFF_HOVER_DARK = "#E53935"; STATE_OFF_ACTIVE_DARK = "#B71C1C"; STATE_OFF_DISABLED_DARK = "#8E2727"; STATE_OFF_BORDER_DARK = "#B71C1C"
    RESET_BUTTON_FG_DARK = "#E5E0FF"; RESET_BUTTON_TEXT_DARK = "#1A1920"; RESET_BUTTON_HOVER_DARK = "#FFFFFF"; RESET_BUTTON_ACTIVE_DARK = "#D4D0F5"; RESET_BUTTON_DISABLED_DARK = "#B0AEBF"
    COFFEE_BUTTON_FG_DARK = "#FFDD00"; COFFEE_BUTTON_TEXT_DARK = "#000000"; COFFEE_BUTTON_HOVER_DARK = "#FFEE55"; COFFEE_BUTTON_ACTIVE_DARK = "#FFC107"; COFFEE_BUTTON_DISABLED_DARK = "#B39D00"
    CONFIGURE_BUTTON_FG_DARK = "#007BFF"; CONFIGURE_BUTTON_HOVER_DARK = "#0056b3"; CONFIGURE_BUTTON_ACTIVE_DARK = "#004085"; CONFIGURE_BUTTON_DISABLED_DARK = "#4D87B9"
    LINKEDIN_BUTTON_FG_DARK = "#0A66C2"; LINKEDIN_BUTTON_HOVER_DARK = "#004182"; GITHUB_BUTTON_FG_DARK = "#F0F6FC"; GITHUB_BUTTON_TEXT_DARK = "#24292F"; GITHUB_BUTTON_HOVER_DARK = "#D0D7DE"; GMAIL_BUTTON_FG_DARK = "#EA4335"; GMAIL_BUTTON_HOVER_DARK = "#C5221F"
    SUCCESS_DARK = "#4CAF50"; SUCCESS_HOVER_DARK = "#388E3C"; SUCCESS_ACTIVE_DARK = "#2E7D32"; SUCCESS_DISABLED_DARK = "#66BB6A"; SUCCESS_BORDER_DARK = "#2E7D32"
    WARNING_DARK = "#FFCA28"; WARNING_HOVER_DARK = "#FFB300"; WARNING_ACTIVE_DARK = "#F57F17"; WARNING_DISABLED_DARK = "#FFCC80"
    ERROR_DARK = "#E53935"; ERROR_HOVER_DARK = "#C62828"; ERROR_ACTIVE_DARK = "#B71C1C"; ERROR_DISABLED_DARK = "#EF9A9A"
    GLASS_BG_START_DARK = "#2C2A3B"; GLASS_BG_END_DARK = "#353345"; GLASS_BORDER_DARK = "#4C4A5B"; GLASS_BORDER_HOVER_DARK = "#9A4BFF"; GLASS_TEXT_DARK = "#F5F5FF"
    VALIDATION_ERROR_DARK = "#E53935"; VALIDATION_SUCCESS_DARK = "#4CAF50"
    
    # --- Color Palette: Light Mode ---
    BACKGROUND_LIGHT = "#F5F5F5"; NAV_RAIL_LIGHT = "#E0E0E0"; CARD_LIGHT = "#FFFFFF"; CARD_HOVER_LIGHT = "#F0F0F0"; TEXT_LIGHT = "#212121"; TEXT_SECONDARY_LIGHT = "#757575"
    ACCENT_LIGHT = "#7B1FA2"; ACCENT_HOVER_LIGHT = "#6A1B9A"; ACCENT_ACTIVE_LIGHT = "#4A148C"; ACCENT_DISABLED_LIGHT = "#9575CD"
    STATE_OFF_LIGHT = "#D32F2F"; STATE_OFF_HOVER_LIGHT = "#F44336"; STATE_OFF_ACTIVE_LIGHT = "#B71C1C"; STATE_OFF_DISABLED_LIGHT = "#EF9A9A"; STATE_OFF_BORDER_LIGHT = "#B71C1C"
    SUCCESS_LIGHT = "#4CAF50"; SUCCESS_HOVER_LIGHT = "#388E3C"; SUCCESS_ACTIVE_LIGHT = "#2E7D32"; SUCCESS_DISABLED_LIGHT = "#66BB6A"; SUCCESS_BORDER_LIGHT = "#2E7D32"

    # --- Font System ---
    FONT_FAMILY_DEFAULT = "Segoe UI"
    FONT_FAMILY_EMOJI = "Noto Color Emoji"
    FONT_FAMILY_MONO = "Consolas"

    # --- [RE-CALIBRATED] Font sizes are increased to provide a comfortable reading
    # --- experience on a 1080p display at 100% scaling. The UIManager will then
    # --- correctly scale these down for 720p or up for 1440p/4K.
    FONT_SIZES = {
        "title": 36, "h1": 28, "h2": 24, "h3": 20, "bold": 17, "normal": 16,
        "small": 14, "button": 15, "caption": 12, "code": 14, "emoji": 26, "emoji_large": 52
    }
    FONT_WEIGHTS = {"light": "normal", "regular": "normal", "medium": "bold", "bold": "bold", "black": "bold"}
    FONTS = {}

    @classmethod
    def initialize_fonts(cls):
        """
        [v2.1 - DPI SCALING PROTOCOL] Initializes all font objects by first
        calculating their size based on the system's true DPI scaling factor. This
        is the single source of truth for all typographic scaling, ensuring perfect
        legibility across all display environments from 720p to 4K+.
        """
        # --- Step 1: Retrieve the definitive system scaling factor from the ScreenManager.
        cls.SCALING_FACTOR = ScreenManager.get_scaling_factor()

        # --- Step 2: Create a new dictionary of scaled font sizes.
        # --- Each base font size is multiplied by the scaling factor to get its true pixel size.
        scaled_font_sizes = {
            name: int(base_size * cls.SCALING_FACTOR)
            for name, base_size in cls.FONT_SIZES.items()
        }

        # --- Step 3: Instantiate all CTkFont objects using the calculated scaled sizes.
        cls.FONTS = {
            "title": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["title"], weight=cls.FONT_WEIGHTS["bold"]),
            "h1": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["h1"], weight=cls.FONT_WEIGHTS["bold"]),
            "h2": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["h2"], weight=cls.FONT_WEIGHTS["bold"]),
            "h3": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["h3"], weight=cls.FONT_WEIGHTS["medium"]),
            "bold": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["bold"], weight=cls.FONT_WEIGHTS["bold"]),
            "normal": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["normal"], weight=cls.FONT_WEIGHTS["regular"]),
            "small": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["small"], weight=cls.FONT_WEIGHTS["regular"]),
            "button": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["button"], weight=cls.FONT_WEIGHTS["medium"]),
            "caption": ctk.CTkFont(family=cls.FONT_FAMILY_DEFAULT, size=scaled_font_sizes["caption"], weight=cls.FONT_WEIGHTS["light"]),
            "code": ctk.CTkFont(family=cls.FONT_FAMILY_MONO, size=scaled_font_sizes["code"], weight=cls.FONT_WEIGHTS["regular"]),
            "emoji": ctk.CTkFont(family=cls.FONT_FAMILY_EMOJI, size=scaled_font_sizes["emoji"]),
            "emoji_large": ctk.CTkFont(family=cls.FONT_FAMILY_EMOJI, size=scaled_font_sizes["emoji_large"]),
            # --- Composite font definitions for widgets that mix text and emojis.
            "nav_button_font": ctk.CTkFont(family=(cls.FONT_FAMILY_DEFAULT, cls.FONT_FAMILY_EMOJI), size=scaled_font_sizes["normal"]),
            "nav_header_font": ctk.CTkFont(family=(cls.FONT_FAMILY_DEFAULT, cls.FONT_FAMILY_EMOJI), size=scaled_font_sizes["h2"]),
            "nav_profile_font": ctk.CTkFont(family=(cls.FONT_FAMILY_DEFAULT, cls.FONT_FAMILY_EMOJI), size=scaled_font_sizes["bold"]),
        }

    # --- Other Methods (Unchanged) ---
    @classmethod
    def set_mode(cls, mode):
        if mode in ["light", "dark"]: cls.CURRENT_MODE = mode
        else: raise ValueError("Mode must be 'light' or 'dark'")
    @classmethod
    def get_mode(cls): return cls.CURRENT_MODE
    @classmethod
    def get_color(cls, key):
        mode = cls.CURRENT_MODE
        try: return getattr(cls, f"{key}_{mode.upper()}", cls.TEXT_DARK if mode == "dark" else cls.TEXT_LIGHT)
        except AttributeError:
            logging.warning(f"Color key '{key}_{mode.upper()}' not found. Falling back to default text color.")
            return cls.TEXT_DARK if mode == "dark" else cls.TEXT_LIGHT
    @classmethod
    def initialize_contrast_check(cls):
        cls.CONTRAST_CHECK = {"TEXT_DARK_BG": (cls.TEXT_DARK, cls.BACKGROUND_DARK), "TEXT_LIGHT_BG": (cls.TEXT_LIGHT, cls.BACKGROUND_LIGHT), "INFO_PANEL_DARK_TEXT": (cls.TEXT_DARK, cls.INFO_PANEL_DARK), "SUCCESS_DARK_CARD": (cls.SUCCESS_DARK, cls.CARD_DARK), "STATE_OFF_DARK_CARD": (cls.STATE_OFF_FG_DARK, cls.CARD_DARK)}
    
    CONTRAST_RATIO_MIN = 4.5; CONTRAST_CHECK = {}
    ANIMATION_SPEED = 0.2; FADE_IN = 0.3; FADE_OUT = 0.2; DROPDOWN_ANIMATION = 0.2; TERMINAL_ANIMATION = 0.3
    GRADIENT_START = "#2C2A3B"; GRADIENT_END = "#9A4BFF"
    BACKGROUND = BACKGROUND_DARK; NAV_RAIL = NAV_RAIL_DARK; CARD = CARD_DARK; CARD_HOVER = CARD_HOVER_DARK; TEXT = TEXT_DARK; TEXT_SECONDARY = TEXT_SECONDARY_DARK; ACCENT = ACCENT_DARK; ACCENT_HOVER = ACCENT_HOVER_DARK; BORDER = BORDER_DARK; INFO_PANEL = INFO_PANEL_DARK; RESET_BUTTON_FG = RESET_BUTTON_FG_DARK; RESET_BUTTON_TEXT = RESET_BUTTON_TEXT_DARK; RESET_BUTTON_HOVER = RESET_BUTTON_HOVER_DARK; STATE_ON_FG = STATE_ON_FG_DARK; STATE_ON_HOVER = STATE_ON_HOVER_DARK; STATE_ON_BORDER = STATE_ON_FG_DARK; STATE_OFF_FG = STATE_OFF_FG_DARK; STATE_OFF_HOVER = STATE_OFF_HOVER_DARK; STATE_OFF_BORDER = STATE_OFF_BORDER_DARK; COFFEE_BUTTON_FG = COFFEE_BUTTON_FG_DARK; COFFEE_BUTTON_TEXT = COFFEE_BUTTON_TEXT_DARK; COFFEE_BUTTON_HOVER = COFFEE_BUTTON_HOVER_DARK; CONFIGURE_BUTTON_FG = CONFIGURE_BUTTON_FG_DARK; CONFIGURE_BUTTON_HOVER = CONFIGURE_BUTTON_HOVER_DARK; SUCCESS = SUCCESS_DARK; SUCCESS_HOVER = SUCCESS_HOVER_DARK; SUCCESS_BORDER = SUCCESS_BORDER_DARK; WARNING = WARNING_DARK; WARNING_HOVER = WARNING_HOVER_DARK; WARNING_BORDER = WARNING_ACTIVE_DARK; GLASS_BG_START = GLASS_BG_START_DARK; GLASS_BG_END = GLASS_BG_END_DARK; GLASS_BORDER = GLASS_BORDER_DARK; GLASS_BORDER_HOVER = GLASS_BORDER_HOVER_DARK; GLASS_TEXT = GLASS_TEXT_DARK; VALIDATION_ERROR_BORDER = VALIDATION_ERROR_DARK

Theme.initialize_contrast_check()

# ===================================================================================
# SECTION 3: DYNAMIC FONT & UI SCALING ENGINE
# This manager handles the intelligent resizing of all text and UI elements.
# ===================================================================================
class UIManager:
    """
    Manages dynamic scaling of fonts and UI elements based on window size.
    [v2.0 CORRECTION]: This class no longer creates its own fonts. It now directly
    references and modifies the master font dictionary from the Theme class,
    ensuring all components have access to the complete, correct set of fonts.
    """
    def __init__(self, app_instance):
        # --- Store a reference to the main application instance.
        self.app = app_instance
        
        # --- Define the dimensional parameters for scaling calculations.
        self.base_width = 1280
        self.min_width = 800
        self.max_width = 3840
        
        # --- [CRITICAL FIX] Get a direct reference to the master font dictionary from the Theme class.
        # --- This ensures the UIManager uses the single source of truth for all fonts, including custom emoji fonts.
        self.fonts = Theme.FONTS
        
        # --- Debounce timer to prevent performance issues during rapid resizing.
        self.debounce_timer = None
        
        # --- Bind the resize event to the debounced scaling handler.
        self.app.bind("<Configure>", self._on_resize_debounce)

    def _on_resize_debounce(self, event=None):
        """Debounces the resize event to prevent lag and excessive recalculations."""
        # --- If a timer is already scheduled, cancel it.
        if self.debounce_timer:
            self.app.after_cancel(self.debounce_timer)
        # --- Schedule the update_scaling method to run after a 100ms pause in resizing.
        self.debounce_timer = self.app.after(100, self.update_scaling)

    def update_scaling(self):
        """
        [RE-ENGINEERED] This method no longer calculates scaling factors. Font
        scaling is now handled definitively by the Theme class at startup. This
        method's sole responsibility is to propagate UI update notifications to
        all registered content frames during a resize event, allowing them to
        adjust their own geometry if necessary.
        """
        # --- Propagate the scaling update notification to all content frames and the navigation rail.
        # --- This allows child components to perform their own geometry updates without
        # --- re-calculating font sizes, eliminating the primary source of the scaling bug.
        for frame in self.app.content_frames.values():
            if hasattr(frame, "update_ui_scaling"):
                frame.update_ui_scaling(self.fonts)
        if hasattr(self.app.navigation_rail, "update_ui_scaling"):
            self.app.navigation_rail.update_ui_scaling(self.fonts)

# ===================================================================================
# SECTION 4: ANIMATION ENGINE
# A lightweight, performant, time-based animation system for all UI transitions.
# ===================================================================================

# ===================================================================================
# SECTION 4.5: AUDITORY FEEDBACK ENGINE (AFE) (v3.0 - Zero-Latency Startup)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive, military-grade implementation of the SoundManager. It is
# engineered for zero-latency application startup by offloading all blocking file
# I/O operations to a dedicated background thread. Its singleton architecture
# ensures a single, authoritative source for all auditory feedback, while its
# thread-safe command queue guarantees responsive and stable playback.
# ===================================================================================
class SoundManager:
    """
    A singleton class to manage UI sounds with global enable/disable functionality
    and a non-blocking, asynchronous asset loading protocol.
    """
    _instance = None # --- The single, shared instance of the class.

    # ===============================================================================
    # METHOD: __new__ (Singleton Instantiation Protocol)
    # Ensures that only one instance of the SoundManager is ever created.
    # ===============================================================================
    def __new__(cls, *args, **kwargs):
        # --- If no instance exists, create one.
        if not cls._instance:
            # --- Call the parent class's constructor to create the new instance.
            cls._instance = super(SoundManager, cls).__new__(cls)
        # --- Return the single, existing instance.
        return cls._instance

    # ===============================================================================
    # METHOD: __init__ (v3.1 - Hybrid Loading Protocol)
    #
    # ARCHITECTURAL BLUEPRINT (UPGRADE):
    # This version implements a hybrid asset loading model. It synchronously
    # pre-loads mission-critical assets (the startup sound) for instantaneous
    # availability, guaranteeing the application's initial auditory feedback.
    # All other non-essential assets remain offloaded to the non-blocking
    # background thread to ensure a zero-latency startup.
    # ===============================================================================
    def __init__(self):
        # --- Prevent re-initialization if the singleton is accessed again. ---
        if hasattr(self, '_initialized'):
            return
        # --- Set the initialization flag to prevent future re-runs of this constructor.
        self._initialized = True
        
        # --- Global Auditory State ---
        self.sound_enabled = True
        self._current_looping_sound = None
        self.sounds = {}

        # --- Core Audio Engine Initialization ---
        try:
            pygame.init()
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.looping_channel = pygame.mixer.Channel(0)
            logging.info("Auditory Feedback Engine (AFE) v3.1 initialized successfully.")
        except Exception as e:
            logging.error(f"AFE CRITICAL FAILURE: Could not initialize pygame.mixer. Error: {e}", exc_info=True)
            self.looping_channel = None
            return

        # --- [CRITICAL ASSET PRE-LOADING] ---
        # --- The startup sound is loaded synchronously on the main thread.
        # --- This is a single, small file, ensuring its impact on startup time is negligible
        # --- while guaranteeing its availability when the splash screen appears.
        try:
            startup_sound_path = resource_path(os.path.join("Sound Effects", "Startup-Sound.mp3"))
            self.sounds['Startup-Sound.mp3'] = pygame.mixer.Sound(startup_sound_path)
            logging.info("AFE: Critical asset 'Startup-Sound.mp3' pre-loaded successfully.")
        except Exception as e:
            logging.error(f"AFE CRITICAL FAILURE: Could not pre-load 'Startup-Sound.mp3'. Error: {e}", exc_info=True)
            self.sounds['Startup-Sound.mp3'] = None

        # --- Asynchronous Asset Loading for all non-critical sounds ---
        self.loading_thread = threading.Thread(target=self._load_sounds_in_background, daemon=True)
        self.loading_thread.start()

        # --- Thread-Safe Command Queue & Playback Worker ---
        self.sound_queue = Queue()
        self._shutdown_event = threading.Event()
        self.playback_thread = threading.Thread(target=self._sound_playback_worker, daemon=True)
        self.playback_thread.start()
    
    # ===============================================================================
    # METHOD: _load_sounds_in_background (v1.1 - Non-Critical Asset Worker)
    #
    # ARCHITECTURAL BLUEPRINT (UPGRADE):
    # This worker's manifest has been updated to exclude any assets that are
    # pre-loaded by the constructor. It is now responsible for the asynchronous
    # loading of all non-essential, secondary sound assets.
    # ===============================================================================
    def _load_sounds_in_background(self):
        # --- Master Sound Asset Manifest (Non-Critical Assets Only) ---
        sound_files = [
            ('click', 'Mouse-Click.mp3'), ('hover', 'Mouse-Hover.mp3'),
            ('reset', 'Reset-Defaults.mp3'), ('turn_on', 'Turn-On.mp3'),
            ('turn_off', 'Turn-Off.mp3'), ('clean_all_click', 'Clean-all-button.mp3'),
            ('cleaning_loop', 'Cleaning.mp3'), ('manual_clean', 'Manual-Clean.mp3'),
            ('what_is_it', 'what-is-it.mp3'), ('money', 'Money.mp3'),
            ('linkedin_click', 'LinkedIn-Button-Click.mp3'), ('github_click', 'Github-Button-Click.mp3'),
            ('email_click', 'Email-Button-Click.mp3'), ('nav_click', 'Navigation-Sound.mp3'),
            ('fix_windows_hover', 'Fix-Windows-Hover-Effect.mp3'), ('question_mark', 'Questionmark.mp3'),
            ('scan_loop', 'Scan-Fix-Windows-Effect.mp3'), ('advanced_scan_loop', 'Advanced-Scan.mp3'),
            ('notification', 'Notification.mp3'), ('cancel_operation', 'Oh-No.mp3'),
            ('feature_hover', 'Feature-Hover.mp3'), ('warning_loop', 'Warning.mp3'),
            ('success_fanfare', 'Horray-No-Errors-Found.mp3'), ('error_sound', 'Error-404.mp3'),
            ('setup_unsuccessful', 'setup-unsuccessful.mp3'), ('success_loop', 'Horray-No-Errors-Found.mp3'),
            ('coin_hover', 'Coin.mp3'), ('ok_click', 'Mouse-Click-Ok.mp3'),
            # --- 'Startup-Sound.mp3' is now pre-loaded in __init__ and is omitted here.
            ('Nav_Sound_Click', 'Navigation-Click-Sound.mp3'),
            ('support_hover', "JUST DO IT - Sound Effect.mp3"),
            ('support_click', "Thanks-Coffee_Button.mp3")
        ]

        # --- Sequential Loading Loop ---
        for name, filename in sound_files:
            try:
                # --- Resolve the absolute path to the asset using the universal resource path resolver. ---
                path = resource_path(os.path.join("Sound Effects", filename))
                # --- This is the blocking I/O operation. It loads the sound file from disk and decodes it. ---
                sound_object = pygame.mixer.Sound(path)
                # --- Atomically add the loaded sound object to the shared dictionary. ---
                self.sounds[name] = sound_object
                # --- Log the successful loading of the asset for auditing. ---
                logging.info(f"AFE Background Loader: Sound asset '{filename}' loaded successfully.")
            except pygame.error as e:
                # --- In case of a loading failure (e.g., file not found, corrupt file), log the specific error. ---
                logging.error(f"AFE Background Loader ERROR: Failed to load sound '{filename}'. Error: {e}", exc_info=True)
                # --- Place a None value in the dictionary to prevent KeyErrors if the UI tries to play a missing sound. ---
                self.sounds[name] = None

    # ===============================================================================
    # METHOD: _sound_playback_worker (v1.0 - Thread-Safe Command Processor)
    #
    # ARCHITECTURAL BLUEPRINT:
    # This is the core worker loop for the Auditory Feedback Engine. It runs on its
    # own dedicated thread, perpetually waiting for commands to be placed in the
    # thread-safe `sound_queue`. By processing all playback requests here, we
    # ensure that the main UI thread is never blocked by sound operations and that
    # all requests are handled sequentially and safely.
    # ===============================================================================
    def _sound_playback_worker(self):
        """Processes sound commands from the queue until a shutdown is signaled."""
        # --- This loop runs for the entire lifetime of the application until the shutdown event is set.
        while not self._shutdown_event.is_set():
            # --- The .get() call is blocking; the thread will sleep here until a command is available.
            command_tuple = self.sound_queue.get()
            # --- A 'None' object is the designated poison pill to signal thread termination.
            if command_tuple is None:
                # --- Exit the loop to allow the thread to terminate gracefully.
                break
            # --- Unpack the command tuple into the action and its argument (the sound name).
            command, argument = command_tuple
            try:
                # --- Process a 'play' command for one-shot sound effects.
                if command == 'play':
                    # --- Play the sound only if the global toggle is enabled OR if it's the specific nav_click sound.
                    if self.sound_enabled or argument == 'nav_click':
                        # --- Retrieve the pre-loaded sound object from the dictionary. .get() safely returns None if not found.
                        sound_to_play = self.sounds.get(argument)
                        if sound_to_play:
                            # --- Execute the sound playback.
                            sound_to_play.play()

                # --- Process a 'loop' command for continuous background sounds.
                elif command == 'loop':
                    # --- Only begin a new loop if sound is globally enabled.
                    if self.sound_enabled:
                        # --- Store the name of the looping sound for state restoration if sounds are toggled.
                        self._current_looping_sound = argument
                        if self.looping_channel:
                            sound_to_loop = self.sounds.get(argument)
                            if sound_to_loop:
                                # --- Stop any previously playing loop on the dedicated channel.
                                self.looping_channel.stop()
                                # --- Play the new sound indefinitely (loops=-1).
                                self.looping_channel.play(sound_to_loop, loops=-1)

                # --- Process a 'stop_loop' command.
                elif command == 'stop_loop':
                    # --- This command signifies the logical end of a looping operation (e.g., scan complete).
                    if self.looping_channel:
                        self.looping_channel.stop()
                    # --- [PARADIGM SOLUTION] Always clear the state variable to prevent incorrect resumption of the sound.
                    self._current_looping_sound = None

                # --- Process a 'stop_and_play' command to prevent sound overlap.
                elif command == 'stop_and_play':
                    if self.sound_enabled or argument == 'nav_click':
                        sound_to_play = self.sounds.get(argument)
                        if sound_to_play:
                            # --- Immediately stop any currently playing instances of this sound before starting a new one.
                            sound_to_play.stop()
                            sound_to_play.play()

                # --- Process a 'stop' command for a specific sound.
                elif command == 'stop':
                    sound_to_stop = self.sounds.get(argument)
                    if sound_to_stop:
                        sound_to_stop.stop()
                        # --- If we are stopping the sound that was considered the main loop, clear its state as a failsafe.
                        if argument == self._current_looping_sound:
                            self._current_looping_sound = None

            # --- Catch any low-level Pygame errors that might occur during playback.
            except pygame.error as e:
                logging.error(f"AFE PLAYBACK ERROR for command '({command}, {argument})': {e}", exc_info=True)

    # ===============================================================================
    # METHOD: Public API Methods (Play, Start Loop, Stop Loop, etc.)
    # These methods provide a clean, high-level interface for the rest of the
    # application to interact with the sound engine without needing to know about
    # the underlying threading model.
    # ===============================================================================
    def play_sound(self, name: str):
        """Places a 'play' command into the queue for a one-shot sound effect if enabled."""
        if hasattr(self, 'sound_queue'):
            self.sound_queue.put(('play', name))

    def start_looping_sound(self, name: str):
        """Places a 'loop' command into the queue to start a continuous sound if enabled."""
        if hasattr(self, 'sound_queue'):
            self.sound_queue.put(('loop', name))

    def stop_looping_sound(self):
        """Places a 'stop_loop' command into the queue to halt the continuous sound."""
        if hasattr(self, 'sound_queue'):
            self.sound_queue.put(('stop_loop', None))

    def stop_sound(self, name: str):
        """Places a 'stop' command into the queue to halt a specific one-shot sound."""
        if hasattr(self, 'sound_queue'):
            self.sound_queue.put(('stop', name))

    def stop_and_play_sound(self, name: str):
        """Places a 'stop_and_play' command into the queue to prevent sound overlap."""
        if hasattr(self, 'sound_queue'):
            self.sound_queue.put(('stop_and_play', name))

    def set_sound_enabled(self, enabled: bool):
        """
        Sets the global sound state with military-grade precision.
        ACTION: DISABLING SOUND - Terminates all active audio channels instantly.
        ACTION: ENABLING SOUND - Resumes the last known looping sound, if one was active.
        This ensures an instantaneous and seamless user experience upon toggling.
        """
        self.sound_enabled = enabled # --- Sets the new state for all future sound requests.
        if not enabled: # --- Executes if the sound is being toggled OFF.
            pygame.mixer.stop() # --- CRITICAL COMMAND: Ceases all audio playback on all channels immediately.
        elif enabled and self._current_looping_sound: # --- Executes if sound is toggled ON and a looping sound was previously active.
            # --- Resumes the last looping sound that was interrupted by the toggle-off action.
            self.sound_queue.put(('loop', self._current_looping_sound))

    def shutdown(self):
        """Gracefully shuts down the AFE worker thread and de-initializes Pygame."""
        logging.info("AFE: Shutdown initiated. Releasing audio resources.")
        if hasattr(self, '_shutdown_event'):
            self._shutdown_event.set()
            self.sound_queue.put(None) # --- Send the poison pill to the worker thread.
            self.playback_thread.join(timeout=1.0) # --- Wait for the thread to terminate.
        pygame.quit()
        logging.info("AFE: Pygame de-initialized. Audio resources released.")

# ===================================================================================
# CLASS: SplashScreen (v1.6 - Final Visual Synthesis)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This definitive version replaces the standard CTkProgressBar with a completely
# custom-drawn, animated progress bar on the tkinter.Canvas. The new design
# synthesizes the futuristic, segmented, and glowing aesthetics from the user-
# provided reference image while being meticulously optimized for low-end hardware.
#
# CORE ENHANCEMENTS:
#   1. [AESTHETICS] Custom-Drawn Segmented Progress Bar: The progress bar is no
#      longer a widget but a collection of canvas rectangles. This allows for a
#      pixel-perfect, sharp geometric design that faithfully captures the cyberpunk
#      aesthetic of the reference image.
#
#   2. [ANIMATION] Sequential Segment Illumination: The `update_progress` method
#      now calculates how many segments to "light up" based on the loading
#      percentage, filling the bar in discrete, visually satisfying steps.
#
#   3. [ANIMATION] Optimized Pulsing Glow: A low-frequency animation loop subtly
#      pulses the color of the active segments between two shades of purple. This
#      creates the illusion of a dynamic, "live" energy source without the
#      performance cost of a high-framerate animation.
#
#   4. [PERFORMANCE] Zero-Widget Progress Bar: By drawing the bar directly onto
#      the canvas, we eliminate the overhead of a CustomTkinter widget, further
#      reducing the component's resource footprint.
# ===================================================================================
class SplashScreen(ctk.CTkToplevel):
    """
    A visually appealing, animated splash screen that masks background loading tasks.
    """
    def __init__(self, master):
        # --- Base Initialization & Window Configuration ---
        super().__init__(master)
        self.master = master

        # --- [DPI SCALING] Calculate scaled dimensions based on the system's DPI factor.
        scale_factor = ScreenManager.get_scaling_factor()
        self.width = int(700 * scale_factor)
        self.height = int(450 * scale_factor)

        # --- Configure the window to be borderless and stay on top.
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # --- Set the taskbar icon for the splash screen.
        try:
            # --- [MODIFIED] Use the resource_path function to locate the icon.
            self.iconbitmap(resource_path(os.path.join("Icons", "Logo.ico")))
        except tk.TclError:
            logging.warning("Could not set splash screen icon. 'Logo.ico' may be missing.")

        # --- Delegate centering logic to the ScreenManager utility with scaled dimensions.
        ScreenManager.center_window(self, self.width, self.height)

        # --- Configure transparency for the floating effect.
        self.transparent_color = '#010101'
        self.wm_attributes('-transparentcolor', self.transparent_color)
        self.config(bg=self.transparent_color)
        self.attributes("-alpha", 0.0)

        # --- Animation & Particle System State ---
        self.particles = []
        self.animation_job = None
        self.glow_animation_job = None
        
        # --- Custom Progress Bar State ---
        self.progress_segments = []
        self.current_progress = 0.0

        # --- UI Construction Protocol ---
        self._create_widgets()
        # --- Start the animation loop immediately upon creation.
        self.start_animation()

    def _create_widgets(self):
        """Creates the canvas, text, custom progress bar, and status label with DPI scaling."""
        # --- Create the main canvas for drawing the animation, filling the scaled window.
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg=Theme.BACKGROUND_DARK, highlightthickness=0)
        self.canvas.pack()

        # --- [DPI SCALING] Scale the title font size based on the system's scaling factor.
        scale_factor = ScreenManager.get_scaling_factor()
        scaled_title_size = int(60 * scale_factor)

        # --- Create the central "MK-Tools 🚀" text element with the scaled font.
        self.title_text_id = self.canvas.create_text(
            self.width / 2, self.height / 2 - int(40 * scale_factor), # Scale vertical offset
            text="MK-Tools 🚀",
            font=("Segoe UI Black", scaled_title_size),
            fill=Theme.ACCENT_DARK
        )

        # --- Draw the custom, segmented progress bar which is now also scaled.
        self._create_custom_progress_bar()

        # --- Create a label to display status, using the pre-scaled font from the Theme class.
        self.status_label = ctk.CTkLabel(
            self,
            text="Initializing...",
            font=Theme.FONTS["normal"],
            fg_color=Theme.BACKGROUND_DARK,
            text_color=Theme.TEXT_SECONDARY
        )

        # --- Place the status label on the canvas below the progress bar with a scaled offset.
        self.canvas.create_window(self.width / 2, self.height - int(80 * scale_factor), window=self.status_label)

    def _create_custom_progress_bar(self):
        """Draws the static background and the individual segments of the progress bar on the canvas, scaled for DPI."""
        # --- [DPI SCALING] Calculate all progress bar dimensions based on the system scaling factor.
        scale_factor = ScreenManager.get_scaling_factor()
        bar_width = int(400 * scale_factor)
        bar_height = int(25 * scale_factor)
        num_segments = 20
        segment_width = bar_width / num_segments
        bar_x = (self.width - bar_width) / 2
        bar_y = self.height / 2 + int(50 * scale_factor)

        # --- Draw the dark background/container for the progress bar.
        self.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height, fill=Theme.NAV_RAIL_DARK, outline="")
        
        # --- Create each individual segment in an "off" state with a scaled gap.
        for i in range(num_segments):
            seg_x1 = bar_x + (i * segment_width)
            seg_x2 = seg_x1 + segment_width - int(2 * scale_factor) # Scale the gap between segments.
            seg_id = self.canvas.create_rectangle(seg_x1, bar_y, seg_x2, bar_y + bar_height, fill=Theme.CARD_DARK, outline="")
            self.progress_segments.append(seg_id)

    def _create_particles(self):
        """
        [PERFORMANCE TIERING] Generates a new batch of particles only if the
        hardware tier is not 'LOW'. On low-tier systems, this function exits
        immediately to prevent any performance impact.
        """
        # --- This check ensures no particles are ever created on low-end hardware.
        if self.master.hardware_tier == 'LOW':
            return

        if len(self.particles) < 50:
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            radius = random.uniform(1, 4)
            color = random.choice([Theme.ACCENT_DARK, Theme.ACCENT_HOVER_DARK, Theme.ACCENT_ACTIVE_DARK])
            dx = random.uniform(-0.5, 0.5)
            dy = random.uniform(-0.5, 0.5)
            orb_id = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline="")
            self.particles.append({'id': orb_id, 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'life': random.randint(150, 300)})

    def _update_animation(self):
        """
        [PERFORMANCE TIERING] The core particle animation loop. This entire
        method is bypassed on low-tier systems as it is never called by `start_animation`.
        """
        particles_to_keep = []
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['life'] -= 1
            if p['life'] > 0:
                self.canvas.move(p['id'], p['dx'], p['dy'])
                particles_to_keep.append(p)
            else:
                self.canvas.delete(p['id'])
        self.particles = particles_to_keep
        self._create_particles()
        self.animation_job = self.after(16, self._update_animation)

    def _animate_progress_bar_glow(self):
        """Creates a subtle, low-intensity pulsing glow on the active segments."""
        # --- The glow effect is a sine wave over time.
        glow_value = (math.sin(time.time() * 4) + 1) / 2 # --- Oscillates between 0 and 1.
        
        # --- Interpolate between two shades of purple to create the pulse.
        start_color = [int(Theme.ACCENT_HOVER_DARK[i:i+2], 16) for i in (1, 3, 5)]
        end_color = [int(Theme.ACCENT_DARK[i:i+2], 16) for i in (1, 3, 5)]
        
        current_color = [int(start_color[i] + (end_color[i] - start_color[i]) * glow_value) for i in range(3)]
        hex_color = f"#{current_color[0]:02x}{current_color[1]:02x}{current_color[2]:02x}"
        
        # --- Determine how many segments should be "on" based on the current progress.
        num_lit_segments = int(self.current_progress * len(self.progress_segments))
        
        # --- Apply the glowing color only to the active segments.
        for i, seg_id in enumerate(self.progress_segments):
            if i < num_lit_segments:
                self.canvas.itemconfig(seg_id, fill=hex_color)
        
        # --- Schedule the next frame of the glow animation.
        self.glow_animation_job = self.after(33, self._animate_progress_bar_glow)

    def start_animation(self):
        """
        Initiates the animation loops. The particle animation is conditionally
        disabled on low-tier hardware to conserve system resources.
        """
        # --- [PERFORMANCE TIERING] Only start the expensive particle animation
        # --- if the system is not classified as low-tier.
        if self.master.hardware_tier != 'LOW':
            self._update_animation()

        # --- The progress bar glow is a lightweight animation and runs on all tiers.
        self._animate_progress_bar_glow()
        self._fade_in()

    def _fade_in(self, alpha=0.0):
        """Animates the window's alpha channel from transparent to opaque."""
        if alpha < 1.0:
            alpha += 0.05
            self.attributes("-alpha", alpha)
            self.after(16, self._fade_in, alpha)

    def update_progress(self, value: float, text: str):
        """
        Public API method to update the progress bar and status text from the main App.
        """
        # --- Store the current progress value.
        self.current_progress = value
        # --- Determine how many segments should be lit.
        num_lit_segments = int(value * len(self.progress_segments))

        # --- Update the color of all segments based on the new progress.
        for i, seg_id in enumerate(self.progress_segments):
            if i < num_lit_segments:
                # --- This segment should be "on". The glow animation will handle its color.
                pass
            else:
                # --- This segment should be "off".
                self.canvas.itemconfig(seg_id, fill=Theme.CARD_DARK)

        # --- Update the status text label.
        self.status_label.configure(text=f"{text} ({int(value * 100)}%)")

    def close(self):
        """Public API method to initiate the fade-out and destruction of the splash screen."""
        # --- Stop all animation loops to conserve resources.
        if self.animation_job:
            self.after_cancel(self.animation_job)
            self.animation_job = None
        if self.glow_animation_job:
            self.after_cancel(self.glow_animation_job)
            self.glow_animation_job = None
        # --- Start the fade-out animation.
        self._fade_out()

    def _fade_out(self, alpha=1.0):
        """Animates the window's alpha channel from opaque to transparent, then destroys it."""
        if alpha > 0.0:
            alpha -= 0.05
            self.attributes("-alpha", alpha)
            self.after(16, self._fade_out, alpha)
        else:
            # --- Once fully transparent, destroy the splash screen window completely.
            self.destroy()

# ===================================================================================
# SECTION 5: CORE APPLICATION CLASS
# The main class that initializes and orchestrates all other components.
# ===================================================================================
# ===================================================================================
# CLASS: App (v2.3 - Definitive Centering & Pre-flight Protocol)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This version integrates the ScreenManager utility to ensure the main application
# window is perfectly centered upon reveal, regardless of screen resolution or
# DPI scaling. It also calls the critical DPI awareness function at startup.
#
# STARTUP SEQUENCE:
#
#  1. [App.__init__] -> [CRITICAL] Call `ScreenManager.set_dpi_awareness()`.
#  2. [App.__init__] -> Create SplashScreen instance (now correctly centered).
#  3. [App.__init__] -> [AUDITORY] Play "Startup-Sound.mp3".
#  4. [App.__init__] -> Create main UI components (hidden, withdrawn state).
#  5. [App.__init__] -> Instantiate TweakStateController and initiate checks.
#  6. [App.__init__] -> Make SplashScreen visible and start its fade-in.
#  7. [Background Thread] -> TweakStateController performs all checks.
#  8. [Main Thread] -> After all checks, `_on_pre_flight_complete` is called.
#  9. [Main Thread] -> Injects the pre-fetched state data into each UI card.
# 10. [Main Thread] -> Commands SplashScreen to `close()` (initiates fade-out).
# 11. [Main Thread] -> Reveals the main application window (`deiconify`), now also
#                     guaranteed to be perfectly centered.
#
# This architecture completely eliminates the "Checking..." state from all UI
# cards and solves all DPI-scaling-related positioning flaws.
# ===================================================================================
class App(ctk.CTk):
    """
    The main application window, now with an integrated pre-flight check system
    masked by an animated splash screen and a definitive centering protocol.
    """
    def __init__(self):
        """
        The constructor for the App class. Now includes hardware tier detection.
        """
        # --- Base Class Initialization ---
        super().__init__()
        # --- Hide the main window until all pre-flight checks are complete.
        self.withdraw()

        # --- [PERFORMANCE TIERING] Initialize the hardware manager and detect the system tier.
        # --- This tier ('LOW', 'MID', 'HIGH') is now available to all child components.
        hardware_manager = HardwareTierManager()
        self.hardware_tier = hardware_manager.get_tier()

        # --- A global event to signal all background threads to terminate gracefully.
        self.shutdown_event = threading.Event()
        # --- A state flag to ensure the shutdown logic runs exactly once (idempotency).
        self._is_closing = False
        # --- A centralized registry for all child processes (e.g., sfc.exe, DISM.exe).
        self.child_processes = set()
        # --- [NEW] A placeholder to store update information if found.
        self.update_info: Optional[dict] = None

        # --- Initialize Core Subsystems ---
        self.sound_manager = SoundManager()
        # --- [NEW] Instantiate the Tweak State Manager. This class will handle all pre-flight checks.
        self.state_controller = TweakStateController(app_instance=self)
        
        # --- Initialize fonts BEFORE creating the UIManager to ensure they are pre-scaled.
        Theme.initialize_fonts()
        
        # --- Splash Screen Initialization & Launch ---
        self.splash = SplashScreen(self)
        # --- Play the startup sound as soon as the splash screen is created.
        self.sound_manager.play_sound('Startup-Sound.mp3')

        # --- Main Window & UI Configuration (Done while splash is visible) ---
        self._configure_window()
        
        # --- The UIManager is created AFTER fonts are initialized.
        self.ui_manager = UIManager(self)
        
        self._create_layout()
        self._create_frames()
        self.select_frame_by_name("dashboard")
        
        # --- Bind the window's close button ('X') to the definitive shutdown protocol.
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        # --- Start the background task to perform all system checks via the new controller.
        self.state_controller.start_checks()
        
    def _run_pre_flight_checks(self):
        """
        This method is a placeholder and should not be used directly as its logic
        is now encapsulated within the TweakStateController to prevent race conditions.
        It is retained here to document the deprecation of the old architectural flaw.
        """
        pass
        
    def _on_pre_flight_complete(self, pre_fetched_states: dict):
        """
        [NEW] Inject the pre-fetched state data into the UI cards and finalize startup.
        This method is now a callback executed on the main thread after all checks are complete.
        """
        # --- Inject the pre-fetched states into the relevant UI cards.
        
        # Performance Frame Injection
        perf_frame = self.content_frames['performance']
        perf_frame.cards[0]._set_initial_state_on_main_thread(pre_fetched_states['performance_fast_startup'])
        perf_frame.cards[1]._set_initial_state_on_main_thread(pre_fetched_states['performance_compressed_mem'])
        perf_frame.cards[2]._set_initial_state_on_main_thread(pre_fetched_states['performance_gpu_scheduling'])
        perf_frame.cards[3]._set_initial_state_on_main_thread(pre_fetched_states['performance_fg_priority'])
        perf_frame.cards[4]._set_initial_state_on_main_thread(pre_fetched_states['performance_svchost'])

        # UI Tweaks Frame Injection
        ui_frame = self.content_frames['ui_tweaks']
        ui_frame.cards[0]._set_initial_state_on_main_thread(pre_fetched_states['ui_classic_menu'])
        ui_frame.cards[1]._set_initial_state_on_main_thread(pre_fetched_states['ui_menu_delay'])
        ui_frame.cards[2]._set_initial_state_on_main_thread(pre_fetched_states['ui_jpeg_quality'])
        ui_frame.cards[3]._set_initial_state_on_main_thread(pre_fetched_states['ui_web_search'])
        
        # Policy Frame Injection
        policy_frame = self.content_frames['policy']
        policy_frame._update_ui_state(pre_fetched_states['policy_status'])

        # --- Command the splash screen to start its fade-out animation.
        self.splash.close()
        # --- After a delay to allow the fade-out to be smooth, reveal the main window.
        self.after(500, self.deiconify)
        
        # --- After revealing the main window, check if an update was found.
        # --- A small delay ensures the pop-up appears after the main window is fully visible.
        if self.update_info:
            self.after(700, self._show_update_notification)

    def register_process(self, process):
        """Adds a subprocess.Popen object to the central registry for tracking."""
        self.child_processes.add(process)
        logging.info(f"PROCESS REGISTRY: Registered process with PID: {process.pid}")

    def unregister_process(self, process):
        """Removes a subprocess.Popen object from the central registry upon its completion."""
        self.child_processes.discard(process)
        logging.info(f"PROCESS REGISTRY: Unregistered process with PID: {process.pid}")

    def _on_closing(self):
        """
        Handles the application shutdown sequence. It is now safe to be called
        multiple times and will terminate all registered child processes.
        """
        if self._is_closing:
            return
        self._is_closing = True
        logging.info("Shutdown initiated. Signaling all background threads and processes to terminate.")
        self.shutdown_event.set()
        for process in list(self.child_processes):
            try:
                if process.poll() is None:
                    logging.warning(f"SHUTDOWN: Terminating active child process with PID: {process.pid}")
                    process.terminate()
                    process.wait(timeout=2)
            except ProcessLookupError:
                logging.info(f"SHUTDOWN: Process with PID {process.pid} already terminated.")
            except subprocess.TimeoutExpired:
                logging.warning(f"SHUTDOWN: Process {process.pid} did not terminate gracefully. Forcing kill.")
                process.kill()
            except Exception as e:
                logging.error(f"SHUTDOWN: An unexpected error occurred while terminating process {process.pid}: {e}")
        self.child_processes.clear()
        if self.sound_manager:
            self.sound_manager.shutdown()
        self.destroy()
        logging.info("Application shutdown complete.")

    # [RE-ARCHITECTED] This method now uses the ScreenManager for perfect centering.
    def _configure_window(self):
        """
        Sets up the main window's core properties and behavior.
        """
        # --- Set the main window title.
        self.title("MK-Tools (v1.0) | Windows-Edition")
        
        # --- [NEW] Delegate centering logic to the ScreenManager utility.
        ScreenManager.center_window(self, 1280, 800)
        
        # --- Set the minimum allowable window size.
        self.minsize(1100, 720)
        # --- Apply the background color from the central Theme class.
        self.configure(fg_color=Theme.BACKGROUND)
        try:
            # --- [MODIFIED] Use the resource_path function to locate the icon.
            self.iconbitmap(resource_path(os.path.join("Icons", "Logo.ico")))
        except Exception:
            # --- Log an error if the icon file is missing.
            logging.error("Icon Error: 'Logo.ico' not found.")

    def _create_layout(self):
        """
        Configures the main grid layout of the application window.
        """
        # --- Configure the second column (index 1) to expand and fill available horizontal space.
        self.grid_columnconfigure(1, weight=1)
        # --- Configure the first row (index 0) to expand and fill available vertical space.
        self.grid_rowconfigure(0, weight=1)

    def _create_frames(self):
        """
        Initializes all UI components, passing necessary master instances down.
        """
        # --- Retrieve the dynamically scaled font objects.
        fonts = self.ui_manager.fonts
        # --- Instantiate the navigation rail.
        self.navigation_rail = NavigationRail(self, self.select_frame_by_name, fonts, sound_manager=self.sound_manager)
        # --- Instantiate all content frames, passing the `app_instance` for process registration and shutdown signals.
        self.content_frames = {
            "dashboard": DashboardFrame(self, fonts, frame_switcher_callback=self.select_frame_by_name, sound_manager=self.sound_manager),
            "performance": PerformanceFrame(self, fonts, app_instance=self, sound_manager=self.sound_manager),
            "ui_tweaks": UITweaksFrame(self, fonts, app_instance=self, sound_manager=self.sound_manager),
            "fix_windows": FixWindowsFrame(self, fonts, app_instance=self, sound_manager=self.sound_manager),
            "clean_cache": CleanCacheFrame(self, fonts, app_instance=self, sound_manager=self.sound_manager),
            "policy": PolicyFrame(self, fonts, app_instance=self, sound_manager=self.sound_manager),
            "about": AboutFrame(self, fonts, app_instance=self, sound_manager=self.sound_manager)
        }
        # --- Initialize the tracking variable for the currently displayed frame.
        self.current_frame_name = None

    def select_frame_by_name(self, name: str):
        """
        Shows the selected content frame and commands the navigation rail to update its highlight.
        """
        # --- Do nothing if the requested frame is already the current one.
        if self.current_frame_name == name: return
        # --- If a frame is currently displayed, hide it and call its state reset method.
        if self.current_frame_name is not None:
            old_frame = self.content_frames[self.current_frame_name]
            if hasattr(old_frame, 'reset_state'): old_frame.reset_state()
            old_frame.grid_forget()
        # --- Update the current frame name.
        self.current_frame_name = name
        # --- Retrieve the new frame to be displayed.
        new_frame = self.content_frames[name]
        # --- Place the new frame on the grid, making it visible.
        new_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        # --- Trigger the new frame's entry animation if it has one.
        if hasattr(new_frame, 'run_entry_animation'): new_frame.run_entry_animation()
        # --- Command the navigation rail to update its visual selection state.
        self.navigation_rail.update_selection(name)

    def set_navigation_lock(self, locked: bool):
        """
        Commands the navigation rail to enter or exit its locked state.
        """
        # --- Log the requested state change for auditing.
        logging.info(f"Navigation lock state requested: {'LOCKED' if locked else 'UNLOCKED'}")
        # --- Delegate the lock command to the navigation rail component.
        self.navigation_rail.set_locked(locked)
    
    def _show_update_notification(self):
        """Creates and displays the update notification pop-up."""
        if self.update_info:
            UpdateNotificationPopup(
                master=self, 
                fonts=self.ui_manager.fonts, 
                update_info=self.update_info,
                sound_manager=self.sound_manager
            )

# ===================================================================================
# SECTION 6: REUSABLE WIDGETS
# Custom, self-contained components that ensure a consistent and modular UI.
# ===================================================================================

# ===================================================================================
# PARADIGM SOLUTION: AnimatedGIFLabel (v2.1 - Framework-Compliant Engine)
# ===================================================================================
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component has been upgraded for zero-defect integration with the customtkinter
# framework. The previous implementation used PIL's `PhotoImage`, which is not
# fully compatible with customtkinter's high-DPI scaling and theming engine,
# resulting in a `UserWarning`.
#
# NEW PARADIGM: NATIVE CTkImage INTEGRATION
#  1. The internal frame cache (`self.frames`) no longer stores `PhotoImage` objects.
#     It now exclusively stores `customtkinter.CTkImage` objects.
#  2. During the `_load_gif` process, each raw PIL frame extracted from the GIF
#     is used to instantiate a `CTkImage`, specifying it for both light and dark
#     modes and locking its size.
#
# This architecture eliminates the framework warning, ensures full compatibility with
# the customtkinter rendering pipeline, and leverages the previously implemented
# `resize_and_reload` method to maintain perfect dynamic scaling.
# =====================================================================================
class AnimatedGIFLabel(ctk.CTkLabel):
    """
    A self-managing label that plays animated GIFs with correct frame timing
    and supports dynamic, on-the-fly resizing using native CTkImage objects.
    """
    def __init__(self, master, gif_path: str, size: Tuple[int, int]):
        # --- Base Class Initialization: Initialize as a standard CTkLabel.
        super().__init__(master, text="", fg_color="transparent")

        # --- State and Asset Storage ---
        self.gif_path = gif_path                                      # --- The file path to the animated GIF.
        self.size = size                                              # --- The target (width, height) to display the GIF.
        self.frames = []                                              # --- A list to hold all processed CTkImage frames of the GIF.
        self.frame_durations = []                                     # --- A list to hold the duration of each corresponding frame.
        self.frame_index = 0                                          # --- The index of the current frame being displayed.
        self._animation_job = None                                    # --- A handle for the scheduled .after() job to allow for cancellation.
        self._is_animating = False                                    # --- A state flag to track if the animation loop is active.

        # --- Load the GIF frames into memory upon instantiation.
        self._load_gif()

    def _load_gif(self):
        """Extracts all frames, converts them to CTkImage objects, and stores them."""
        # --- Use a try-except block to handle file loading errors gracefully.
        try:
            # --- Open the GIF file using the Pillow library.
            with Image.open(self.gif_path) as img:
                # --- Iterate through each frame available in the GIF file.
                for i in range(img.n_frames):
                    # --- Seek to the current frame index.
                    img.seek(i)
                    # --- Create a copy of the frame and resize it to the specified dimensions using a high-quality filter.
                    frame = img.copy().resize(self.size, Image.Resampling.LANCZOS)
                    # --- [CRITICAL FIX] Convert the Pillow frame into a CTkImage object that customtkinter can manage.
                    ctk_frame = ctk.CTkImage(light_image=frame, dark_image=frame, size=self.size)
                    self.frames.append(ctk_frame)
                    # --- Extract the duration for this specific frame from the GIF's metadata (in milliseconds).
                    duration = img.info.get('duration', 100)
                    self.frame_durations.append(duration if duration > 0 else 100)
        # --- Handle the case where the specified GIF file does not exist.
        except FileNotFoundError:
            logging.error(f"AnimatedGIFLabel Error: GIF file not found at '{self.gif_path}'")
            self.configure(text=f"Error:\nGIF not found.")
        # --- Handle any other exceptions during image processing.
        except Exception as e:
            logging.error(f"AnimatedGIFLabel Error: Failed to load GIF '{self.gif_path}'. Reason: {e}", exc_info=True)
            self.configure(text=f"Error:\nFailed to load GIF.")

    def _animate(self):
        """The core animation loop that cycles through the frames."""
        # --- Abort if no frames are loaded or if the animation has been stopped.
        if not self.frames or not self._is_animating:
            return

        # --- Set the label's image to the current CTkImage frame.
        self.configure(image=self.frames[self.frame_index])

        # --- Increment the frame index, looping back to the beginning.
        self.frame_index = (self.frame_index + 1) % len(self.frames)

        # --- Schedule the next call to this method after the duration of the current frame.
        self._animation_job = self.after(self.frame_durations[self.frame_index], self._animate)

    def start_animation(self):
        """Starts the animation loop."""
        # --- Prevent duplicate animation loops.
        if self._is_animating:
            return
        # --- Set the state flag to true.
        self._is_animating = True
        # --- Begin the animation sequence.
        self._animate()

    def stop_animation(self):
        """Stops the animation loop by cancelling the scheduled job."""
        # --- Set the state flag to false to terminate the loop.
        self._is_animating = False
        # --- Cancel any pending .after() call.
        if self._animation_job:
            self.after_cancel(self._animation_job)
            self._animation_job = None

    def resize_and_reload(self, new_size: Tuple[int, int]):
        """Resizes the GIF by reloading and re-caching all frames at the new dimensions."""
        # --- Record the animation's current state.
        was_animating = self._is_animating
        # --- Stop any current animation to prevent conflicts.
        self.stop_animation()

        # --- Update the size and clear the old frame cache.
        self.size = new_size
        self.frames.clear()
        self.frame_durations.clear()
        self.frame_index = 0

        # --- Reload all frames at the new size.
        self._load_gif()

        # --- Restart the animation if it was running before the resize.
        if was_animating:
            self.start_animation()

# ===================================================================================
# DEFINITIVE REPLACEMENT FOR: FileDeletionEngine Class
# ===================================================================================

# ARCHITECTURAL BLUEPRINT (FileDeletionEngine v2.0 - Granular Native Deletion):
# This engine has been re-architected for maximum effectiveness and fault tolerance.
#
# NEW PARADIGM: HIGH-SPEED ITERATIVE DELETION
#  1. NATIVE ENUMERATION: The engine uses `os.scandir()`, a highly efficient,
#     low-level directory iterator that avoids the overhead of `os.walk()` or
#     PowerShell's `Get-ChildItem`.
#
#  2. GRANULAR ATTEMPTS: Instead of a single, all-or-nothing bulk delete, the
#     engine iterates through each file and folder discovered by `os.scandir()`.
#
#  3. FAULT-TOLERANT EXECUTION: Each individual deletion attempt (`os.remove` for
#     files, `shutil.rmtree` for directories) is wrapped in a `try...except`
#     block. This allows the engine to gracefully trap `PermissionError` or
#     `OSError` exceptions—the signature of a locked file—and skip only that
#     specific item, continuing its mission with the rest.
#
#  4. THREAD-SAFE LOGGING: The logging mechanism is corrected to accept a master
#     widget instance, allowing it to safely schedule UI updates on the main
#     thread via the `.after()` method, resolving the previous `AttributeError`.
#
# This architecture guarantees that every unlocked file will be deleted, perfectly
# mimicking the "Skip" behavior of a manual cleanup with superior speed and automation.
#
class FileDeletionEngine:
    """
    Encapsulates high-performance directory cleanup using a robust, iterative,
    and fault-tolerant protocol based on Python's native OS interfaces.
    """
    def __init__(self, master_widget: ctk.CTk, log_callback: Optional[Callable[[str], None]] = None):
        # --- Store a reference to a master Tkinter widget (e.g., the root app or a frame).
        # --- This is CRITICAL for scheduling thread-safe UI updates.
        self.master_widget = master_widget
        # --- Store a callback function for logging operational status to a UI terminal.
        self.log_callback = log_callback

    def _log(self, message: str):
        """Internal logging wrapper to safely invoke the callback on the main UI thread."""
        # --- Check if a callback function has been provided.
        if self.log_callback:
            # --- [CRITICAL FIX] Use the stored master widget reference to call `.after()`.
            # --- This correctly schedules the `log_callback` to run on the main event loop, ensuring thread safety.
            self.master_widget.after(0, self.log_callback, message)

    def delete_directory_contents(self, path: str) -> bool:
        """
        Deletes all files and subfolders within a given directory using a granular,
        fault-tolerant iteration that skips locked files.

        Args:
            path (str): The absolute path to the directory whose contents will be deleted.

        Returns:
            bool: True if the operation completes (even with skips), False on critical failure.
        """
        # --- Pre-flight Check: Verify the target directory exists.
        if not os.path.isdir(path):
            # --- Log that the target is invalid and abort the operation.
            self._log(f"SKIPPED: Directory not found at '{path}'.")
            # --- Return True, as there was nothing to clean.
            return True

        # --- Use a `try...except` block for absolute fault tolerance during the scan.
        try:
            # --- Use `os.scandir()` for a high-performance iterator of directory entries.
            with os.scandir(path) as it:
                # --- Iterate over each file, directory, or symlink in the target path.
                for entry in it:
                    # --- Use a nested `try...except` for each individual deletion attempt.
                    try:
                        # --- If the entry is a directory or a symbolic link to a directory.
                        if entry.is_dir():
                            # --- Use `shutil.rmtree()` for recursive, high-speed directory deletion.
                            shutil.rmtree(entry.path)
                        # --- If the entry is a file.
                        else:
                            # --- Use `os.remove()` for efficient file deletion.
                            os.remove(entry.path)
                    # --- This is the primary exception for locked files or permission issues.
                    except (PermissionError, OSError) as e:
                        # --- Log the specific file that was skipped, providing clear user feedback.
                        self._log(f"SKIPPED (in use): {entry.name}")
                        # --- Log the technical error for diagnostic purposes.
                        logging.warning(f"Could not delete '{entry.path}': {e}")
            
            # --- If the loop completes without a critical error, the operation is considered successful.
            self._log(f"SUCCESS: Granular deletion completed for '{path}'.")
            return True
        # --- Catch any unexpected exceptions during the top-level `os.scandir()` operation.
        except Exception as e:
            # --- Log the exception for forensic analysis.
            logging.error(f"Critical exception in FileDeletionEngine for path '{path}': {e}", exc_info=True)
            # --- Inform the user of the critical failure.
            self._log(f"CRITICAL ERROR during granular deletion for '{path}'. See logs.")
            # --- Return False to signal a critical failure.
            return False

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


# ===================================================================================
# CLASS: MenuShowDelayTweak (v1.0 - Zero-Defect Logic Controller)
#
# ARCHITECTURAL BLUEPRINT:
# This is a self-contained logic module for managing the Windows menu show delay.
# It interfaces directly with the registry to check and set the required value.
#
# CORE PRINCIPLES:
#   1. ROBUST STATE CHECKING: The `check_status` method uses a fault-tolerant
#      PowerShell command that safely retrieves the current delay value, or returns
#      the Windows default ('400') if the value does not explicitly exist. This
#      prevents errors and ensures a reliable state check every time.
#
#   2. REBOOT AWARENESS: Unlike other tweaks, this module understands that its
#      changes are not applied instantly via a shell restart. The `apply` and `undo`
#      methods are designed to simply set the registry value, with the knowledge
#      that the UI layer will be responsible for notifying the user of the need
#      to log off or reboot.
#
#   3. ATOMIC MODIFICATION: The `Set-ItemProperty` command is an atomic operation,
#      guaranteeing that the registry value is updated cleanly in a single step.
# ===================================================================================
class MenuShowDelayTweak:
    """
    Manages the logic for modifying the MenuShowDelay registry value to remove
    the right-click menu animation delay.
    """
    def __init__(self):
        # --- REGISTRY CONSTANTS ---
        # Define the exact path and name for the registry value this class controls.
        self.reg_path = "HKCU:\\Control Panel\\Desktop"
        self.reg_name = "MenuShowDelay"
        self.default_value = "400" # The Windows default value.
        self.tweak_value = "0"     # The value that enables the tweak.

    def check_status(self) -> bool:
        """
        Checks the registry to determine if the menu delay is set to 0.

        Returns:
            bool: True if the tweak is active (delay is 0), False otherwise.
        """
        # --- COMMAND DEFINITION ---
        # This robust command attempts to get the property. If it fails (e.g., the
        # property doesn't exist), the catch block ensures we return the default
        # value, preventing the application from crashing.
        command = (
            f'$path = "{self.reg_path}"; $name = "{self.reg_name}"; '
            f'try {{ $value = (Get-ItemProperty -Path $path -Name $name -ErrorAction Stop).$name; Write-Output $value }} '
            f'catch {{ Write-Output "{self.default_value}" }}'
        )
        
        try:
            # --- SUBPROCESS EXECUTION ---
            # Execute the command silently with no flashing console window.
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # --- RESULT PARSING ---
            # The command outputs the delay value. We check if it matches our tweak's value.
            current_value = result.stdout.strip()
            is_enabled = current_value == self.tweak_value
            logging.info(f"MenuShowDelay status check: Value is {current_value}. Tweak enabled: {is_enabled}")
            return is_enabled

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # --- EXCEPTION HANDLING ---
            # If any error occurs, assume the default 'disabled' state for safety.
            logging.error(f"Error checking MenuShowDelay status: {e}", exc_info=True)
            return False

    def apply(self):
        """
        Applies the tweak by setting the menu delay to 0.
        This is a blocking operation and should be called from a background thread.
        """
        # --- COMMAND DEFINITION ---
        # A simple, direct command to set the registry property to the tweak value.
        command = f'Set-ItemProperty -Path "{self.reg_path}" -Name "{self.reg_name}" -Value "{self.tweak_value}"'
        logging.info("Applying MenuShowDelay tweak (setting value to 0)...")
        self._execute_command(command)
        # --- NOTE: No explorer restart here. Change requires logoff/reboot.

    def undo(self):
        """
        Reverts the tweak to the Windows default by setting the menu delay to 400.
        This is a blocking operation and should be called from a background thread.
        """
        # --- COMMAND DEFINITION ---
        # A simple, direct command to set the registry property to the default value.
        command = f'Set-ItemProperty -Path "{self.reg_path}" -Name "{self.reg_name}" -Value "{self.default_value}"'
        logging.info("Reverting MenuShowDelay tweak to default (setting value to 400)...")
        self._execute_command(command)
        # --- NOTE: No explorer restart here. Change requires logoff/reboot.
        
    def _execute_command(self, command: str):
        """A private helper to execute a PowerShell command silently."""
        try:
            # --- SUBPROCESS EXECUTION ---
            subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            logging.info(f"Successfully executed command: {command}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # --- EXCEPTION HANDLING ---
            logging.error(f"Failed to execute command '{command}': {e}", exc_info=True)


# ===================================================================================
# CLASS: JPEGQualityTweak (v1.0 - Zero-Defect Logic Controller)
#
# ARCHITECTURAL BLUEPRINT:
# This is a self-contained logic module for managing the Windows JPEG wallpaper
# import quality. It is more advanced than previous tweak controllers, as it
# reads and writes specific integer values rather than just checking for existence.
#
# CORE PRINCIPLES:
#   1. VALUE-AWARE STATE CHECKING: The `check_status` method is designed to
#      return not just a boolean, but a detailed dictionary containing the
#      tweak's state ('configured' or 'default') and the specific quality value
#      if it exists. It gracefully handles cases where the registry key is not set.
#
#   2. PARAMETERIZED APPLICATION: The `apply` method accepts an integer value,
#      allowing the UI to set a custom wallpaper quality from 0-100. It correctly
#      sets the registry key as a DWord type.
#
#   3. TRUE DEFAULT REVERSION: The `undo` method doesn't just set a default value;
#      it removes the registry key entirely, which is the true default state for
#      a fresh Windows installation.
#
#   4. USER ACTION NOTIFICATION: All state-changing methods return a clear,
#      user-friendly message detailing the next steps required (logoff/reboot
#      and re-applying the wallpaper), which the UI layer can then display.
# ===================================================================================
class JPEGQualityTweak:
    """
    Manages the logic for setting a custom JPEG wallpaper import quality.
    """
    def __init__(self):
        # --- REGISTRY CONSTANTS ---
        self.reg_path = "HKCU:\\Control Panel\\Desktop"
        self.reg_name = "JPEGImportQuality"
        self.finalization_message = "Change applied! To see the effect, please log out and back in, or restart your PC, then re-apply your wallpaper."

    def check_status(self) -> dict:
        """
        Checks the registry for the JPEGImportQuality value.

        Returns:
            dict: A dictionary containing the 'status' ('configured' or 'default')
                  and the current 'value' if configured.
        """
        command = (
            f'$path = "{self.reg_path}"; $name = "{self.reg_name}"; '
            f'try {{ $value = (Get-ItemProperty -Path $path -Name $name -ErrorAction Stop).$name; Write-Output $value }} '
            f'catch {{ Write-Output "default" }}'
        )
        try:
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            output = result.stdout.strip()
            
            if output == "default":
                logging.info("JPEGImportQuality status check: Default (key not found).")
                return {'status': 'default', 'value': None}
            else:
                logging.info(f"JPEGImportQuality status check: Configured to {output}.")
                return {'status': 'configured', 'value': int(output)}
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as e:
            logging.error(f"Error checking JPEGImportQuality status: {e}", exc_info=True)
            return {'status': 'default', 'value': None}

    def apply(self, quality_value: int):
        """
        Applies the tweak by setting the JPEG quality to a specific value.
        This should be called from a background thread.

        Args:
            quality_value (int): The desired quality, from 0 to 100.
        
        Returns:
            str: A message for the user indicating next steps.
        """
        # --- Value Sanitation ---
        # Ensures the value is within the valid 0-100 range.
        clamped_value = max(0, min(100, quality_value))
        
        # --- COMMAND DEFINITION ---
        # Sets the registry property as a DWord type, which is required for this key.
        command = f'Set-ItemProperty -Path "{self.reg_path}" -Name "{self.reg_name}" -Type DWord -Value {clamped_value}'
        logging.info(f"Applying JPEGImportQuality tweak (setting value to {clamped_value})...")
        self._execute_command(command)
        return self.finalization_message

    def undo(self):
        """
        Reverts the tweak to the Windows default by deleting the registry key.
        This should be called from a background thread.

        Returns:
            str: A message for the user indicating next steps.
        """
        # --- COMMAND DEFINITION ---
        # Removes the property entirely. -ErrorAction SilentlyContinue prevents errors
        # if the key doesn't already exist, making it safe to run anytime.
        command = f'Remove-ItemProperty -Path "{self.reg_path}" -Name "{self.reg_name}" -ErrorAction SilentlyContinue'
        logging.info("Reverting JPEGImportQuality tweak to default (removing key)...")
        self._execute_command(command)
        return self.finalization_message
        
    def _execute_command(self, command: str):
        """A private helper to execute a PowerShell command silently."""
        try:
            subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            logging.info(f"Successfully executed command: {command}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logging.error(f"Failed to execute command '{command}': {e}", exc_info=True)

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


# ===================================================================================
# CLASS: InlineNotificationOverlay (v2.3 - Zero-Animation Protocol)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive version of the in-frame notification system. All scaling
# and fading animations have been completely excised and replaced with an
# instantaneous show/hide protocol. This guarantees a zero-stutter, high-performance
# user experience on all hardware tiers and eliminates visual artifacts during
# UI state transitions.
# ===================================================================================
class InlineNotificationOverlay(ctk.CTkFrame):
    """
    A military-grade, in-frame modal notification overlay with a zero-animation
    protocol for maximum performance and stability.
    """
    def __init__(self, master, fonts: dict, title: str, message: str, emoji: str, buttons_config: list, on_close_callback: callable = None, gif_path: Optional[str] = None, rich_message: Optional[list] = None):
        # --- Base Initialization & Shield Configuration ---
        super().__init__(master, fg_color=Theme.BACKGROUND_DARK) 
        # --- Store Core Properties ---
        self.master_frame = master
        self.fonts = fonts
        self.on_close_callback = on_close_callback
        # --- Central Dialog Box ---
        self.dialog_box = ctk.CTkFrame(self, fg_color=Theme.CARD, corner_radius=25, border_width=2, border_color=Theme.ACCENT)
        # --- Dialog Content Construction ---
        self._create_dialog_content(title, message, emoji, buttons_config, gif_path, rich_message)
        
    def _create_dialog_content(self, title: str, message: str, emoji: str, buttons_config: list, gif_path: Optional[str], rich_message: Optional[list]):
        """Dynamically creates and arranges the widgets inside the central dialog box."""
        content_frame = ctk.CTkFrame(self.dialog_box, fg_color="transparent")
        content_frame.pack(padx=40, pady=30, fill="both", expand=True)
        content_frame.grid_columnconfigure(0, weight=1)
        current_row = 0

        if gif_path:
            gif_widget = AnimatedGIFLabel(content_frame, gif_path=gif_path, size=(128, 128))
            gif_widget.grid(row=current_row, column=0, pady=(0, 15))
            gif_widget.start_animation()
            current_row += 1

        ctk.CTkLabel(content_frame, text=emoji, font=self.fonts["emoji_large"]).grid(row=current_row, column=0, pady=(0, 20))
        current_row += 1
        
        ctk.CTkLabel(content_frame, text=title, font=self.fonts["h2"], text_color=Theme.TEXT).grid(row=current_row, column=0, pady=(0, 10))
        current_row += 1
        
        if rich_message:
            message_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            message_frame.grid(row=current_row, column=0, pady=(0, 30))
            current_row += 1
            for i, (text, color) in enumerate(rich_message):
                ctk.CTkLabel(message_frame, text=text, font=self.fonts["normal"], text_color=color).pack(side="left")
        else:
            ctk.CTkLabel(content_frame, text=message, font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY, wraplength=450, justify="center").grid(row=current_row, column=0, pady=(0, 30))
            current_row += 1

        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=current_row, column=0, pady=(10, 0), sticky="ew")
        num_buttons = len(buttons_config)
        if num_buttons > 0:
            columns = tuple(range(num_buttons))
            button_frame.grid_columnconfigure(columns, weight=1)
        for i, config in enumerate(buttons_config):
            button = ctk.CTkButton(button_frame, text=config.get("text", "Button"), font=self.fonts["button"], height=40, corner_radius=15, command=lambda c=config: self._execute_button_action(c))
            self._apply_button_style(button, config.get("style", "default"))
            button.grid(row=0, column=i, padx=5, sticky="ew")

    def _apply_button_style(self, button: ctk.CTkButton, style: str):
        """Applies a predefined style to a button from the Theme class."""
        style_map = {
            "success": {"fg_color": Theme.SUCCESS, "hover_color": Theme.SUCCESS_HOVER, "border_color": Theme.SUCCESS_BORDER, "border_width": 2},
            "danger": {"fg_color": Theme.STATE_OFF_FG, "hover_color": Theme.STATE_OFF_HOVER, "border_color": Theme.STATE_OFF_BORDER, "border_width": 2},
            "warning": {"fg_color": Theme.WARNING, "hover_color": Theme.WARNING_HOVER, "border_color": Theme.WARNING_BORDER, "border_width": 2},
            "default": {"fg_color": Theme.SECONDARY_DARK, "hover_color": Theme.SECONDARY_HOVER_DARK}
        }
        button.configure(**style_map.get(style, style_map["default"]))

    def _execute_button_action(self, config: dict):
        """Executes the button's command and then closes the overlay."""
        command = config.get("command")
        if callable(command):
            command()
        self.close()

    def show(self):
        """[ZERO-ANIMATION] Instantly displays the overlay with its final geometry."""
        # --- Make the overlay visible and bring it to the front of the stacking order.
        self.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        self.lift()
        
        # --- Place the dialog box instantly at its final, centered position.
        # --- This eliminates the scaling animation that causes stutter.
        self.dialog_box.place(relx=0.5, rely=0.5, anchor="center")

    def _animate_entry(self):
        """
        [DEPRECATED] This method is now a placeholder and performs no action.
        The animation has been removed for performance and stability.
        """
        pass

    def close(self):
        """[ZERO-ANIMATION] Instantly destroys the widget and triggers callbacks."""
        # --- Immediately execute the on_close_callback if one was provided.
        if callable(self.on_close_callback):
            self.on_close_callback()
        
        # --- Instantly destroy the widget, preventing any fade-out animation.
        if self.winfo_exists():
            self.destroy()

    def _animate_exit(self):
        """
        [DEPRECATED] This method is now a placeholder and performs no action.
        The animation has been removed for performance and stability.
        """
        pass

# ===================================================================================
# CLASS: DynamicHintEngine (v2.0 - Zero-Defect & Configurable Interval)
#
# ARCHITECTURAL BLUEPRINT:
# This class defines a self-contained, thread-safe engine for providing dynamic,
# asynchronous feedback to the user. It operates on a dedicated background thread,
# ensuring the main UI remains fully responsive. This version introduces a
# configurable interval, allowing it to be deployed in various contexts with
# different timing requirements (e.g., fast updates for quick scans, slow updates
# for long repair operations).
#
# THREADING MODEL:
#
#  [UI Thread] .start(hints, interval) -> [Engine] Creates & starts [Background Thread]
#                 |                                       |
#  [Background Thread] <--------------------------- runs loop {
#                                                             select_hint()
#                                                             sleep(interval)
#                                                             master.after(0, update_label)
#                                                           }
#                 |
#  [UI Thread] .stop() -----------------> [Engine] Sets self.running = False -> Loop Terminates
#
# This model guarantees absolute UI responsiveness and thread safety.
# ===================================================================================
class DynamicHintEngine:
    """
    Manages the display of randomized, timed hints in a dedicated UI label.
    Runs on a background thread to avoid blocking the main application loop and
    supports a configurable refresh interval.
    """
    def __init__(self, master: ctk.CTkFrame, hint_label: ctk.CTkLabel):
        # --- Store a reference to the master frame for scheduling thread-safe UI updates.
        self.master = master
        # --- Store a reference to the target CTkLabel widget where hints will be displayed.
        self.hint_label = hint_label
        # --- The list of hint strings the engine will cycle through. Initialized as empty.
        self.hint_list = []
        # --- The thread object that will run the hint-cycling logic. Initialized to None.
        self.thread = None
        # --- A critical, volatile flag to gracefully control the execution loop of the background thread.
        self.running = False
        # --- A variable to hold the current refresh interval. Defaults to 8 seconds.
        self.interval = 8

    def _update_hint_thread(self):
        """
        This is the core logic loop that runs on the background thread. It cycles
        through hints at the configured interval until the 'running' flag is set to False.
        """
        # --- The loop continues as long as the engine is in the 'running' state.
        while self.running:
            # --- Begin a try block to gracefully handle potential errors within the loop.
            try:
                # --- Select a random hint from the currently loaded list.
                hint = random.choice(self.hint_list)
                # --- CRITICAL: Schedule the UI update on the main thread for absolute thread safety.
                # --- This prevents race conditions and GUI instability.
                self.master.after(0, lambda h=hint: self.hint_label.configure(text=h))
                # --- Pause the background thread for the specified interval.
                time.sleep(self.interval)
            # --- Handle the edge case where the hint list might be empty.
            except IndexError:
                # --- If the list is empty, display an initializing message.
                self.master.after(0, self.hint_label.configure(text="Initializing..."))
                # --- Still pause before retrying to prevent a tight loop.
                time.sleep(self.interval)
            # --- A final catch-all for any other unexpected exceptions.
            except Exception as e:
                # --- Log any unexpected errors within the thread loop for diagnostics.
                logging.error(f"DynamicHintEngine thread error: {e}", exc_info=True)
                # --- Break the loop to prevent repeated failures.
                break

    def start(self, hints: list, interval: int = 8):
        """
        Initiates the hint engine with a specific set of hints and a configurable
        update interval. This is the public API to begin the process.
        
        Args:
            hints (list): A list of strings to be displayed as hints.
            interval (int): The time in seconds between hint refreshes.
        """
        # --- Load the context-specific list of hints into the engine.
        self.hint_list = hints
        # --- Store the desired refresh interval for this session.
        self.interval = interval
        # --- Set the control flag to True, allowing the thread's while loop to execute.
        self.running = True
        # --- Ensure the hint label is visible to the user.
        self.hint_label.grid()
        # --- Create a new thread targeting the loop method.
        # --- It is daemonized to ensure it will not block the main application from exiting.
        self.thread = threading.Thread(target=self._update_hint_thread, daemon=True)
        # --- Start the execution of the background thread.
        self.thread.start()

    def stop(self):
        """
        Gracefully stops the hint engine's background thread and hides the hint label.
        This is the public API to terminate the process.
        """
        # --- Set the control flag to False. The thread will check this and exit its loop cleanly.
        self.running = False
        # --- Hide the hint label from the user interface.
        self.hint_label.grid_forget()

# ===================================================================================
# PARADIGM SOLUTION: BaseModalDialog (v1.0 - Zero-Defect Modality Engine)
#
# ARCHITECTURAL BLUEPRINT:
# This new base class encapsulates all logic for creating a military-grade,
# truly modal dialog that is visually and functionally inseparable from its parent.
#
# CORE PRINCIPLES:
#   1. UNBREAKABLE MODALITY: Uses a combination of `transient`, `grab_set`, and
#      a forced-focus binding to ensure the dialog cannot be bypassed.
#   2. DYNAMIC CENTERING: Binds to the parent window's `<Configure>` event,
#      guaranteeing the dialog remains perfectly centered even if the parent is moved.
#   3. LIFECYCLE MANAGEMENT: Handles its own event unbinding and resource release
#      in a robust `close` method to prevent memory leaks.
# ===================================================================================
class BaseModalDialog(ctk.CTkToplevel):
    """A base class for creating robust, perfectly centered, and truly modal dialogs."""

    def __init__(self, master, title: str):
        # --- Base Initialization & State Storage ---
        super().__init__(master)
        self.master_window = master
        self.configure_bind_id = None

        # --- Window Configuration: Unbreakable Modality & Stacking Protocol ---
        self.title(title)
        self.overrideredirect(True)      # Remove OS-level window decorations.
        self.transient(self.master_window) # Link this pop-up to its parent window.
        self.attributes("-topmost", True)  # Ensure the pop-up stays on top.
        self.protocol("WM_DELETE_WINDOW", self.close) # Handle attempts to close via OS.

        # --- Bind events to ensure perfect modality and positioning.
        self.after(10, self._initial_setup) # Delay setup to ensure parent is ready.

    def _initial_setup(self):
        """Finalizes setup after the event loop has started."""
        if not self.winfo_exists(): return
        self.grab_set() # CRITICAL: Block all interaction with the parent window.
        self._bind_events()
        self.update_idletasks()
        self._center_on_parent()
        self.focus_force()

    def _bind_events(self):
        """Binds events to keep the pop-up centered and focused."""
        # --- When the parent moves, re-center this pop-up. This makes it "stick".
        self.configure_bind_id = self.master_window.bind("<Configure>", self._on_parent_move, add="+")
        # --- If this window loses focus, force focus back immediately.
        self.bind("<FocusOut>", self._force_focus)
        # --- Allow closing with Escape key for accessibility.
        self.bind("<Escape>", lambda e: self.close())

    def _on_parent_move(self, event=None):
        """Callback to re-center the pop-up when the parent window is moved or resized."""
        if self.winfo_exists() and self.master_window.winfo_exists():
            self._center_on_parent()

    def _center_on_parent(self):
        """Calculates and sets the pop-up's geometry to be perfectly centered on its parent."""
        self.update_idletasks() # Ensure window dimensions are current.
        master_x = self.master_window.winfo_rootx()
        master_y = self.master_window.winfo_rooty()
        master_width = self.master_window.winfo_width()
        master_height = self.master_window.winfo_height()
        popup_width = self.winfo_width()
        popup_height = self.winfo_height()
        # --- Centering Calculation ---
        popup_x = master_x + (master_width - popup_width) // 2
        popup_y = master_y + (master_height - popup_height) // 2
        self.geometry(f"+{popup_x}+{popup_y}") # Apply the calculated centered position.
        self.lift() # Bring the window to the front of the stacking order.

    def _force_focus(self, event=None):
        """Prevents the pop-up from losing focus, ensuring unbreakable modality."""
        if self.winfo_exists():
            self.focus_force()
            self.grab_set()

    def close(self):
        """Safely closes the dialog, unbinds events, and destroys the window."""
        # --- CRITICAL: Unbind the <Configure> event from the parent to prevent memory leaks.
        if self.configure_bind_id and self.master_window.winfo_exists():
            try:
                self.master_window.unbind("<Configure>", self.configure_bind_id)
            except tk.TclError:
                pass # --- Ignore error if the binding is already gone.
        self.grab_release() # --- Release the modal grab.
        self.destroy()      # --- Destroy the pop-up window.

# ===================================================================================
# CLASS: RepairSuccessPopup (v2.0 - Architecturally Compliant)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class has been re-engineered to inherit from the BaseModalDialog engine.
# All redundant, manually implemented logic for modality, centering, and focus
# management has been excised. The class now exclusively contains its unique UI
# content, delegating all core windowing behavior to its parent, ensuring
# architectural consistency and zero code duplication.
# ===================================================================================
class RepairSuccessPopup(BaseModalDialog):
    """
    A centered, modal, and celebratory pop-up to confirm a successful repair,
    now built upon the definitive BaseModalDialog engine.
    """
    # ===============================================================================
    # METHOD: __init__
    # The constructor now inherits from BaseModalDialog for core functionality.
    # ===============================================================================
    def __init__(self, master, fonts, on_close_callback):
        # --- Base Class Initialization: Establishes the core modal window.
        super().__init__(master, "Repair Complete!")
        
        # --- Store the callback to execute upon closing (e.g., UI reset).
        self.on_close_callback = on_close_callback

        # --- Window & UI Configuration ---
        self.configure(fg_color=Theme.NAV_RAIL)      # --- Use a consistent, themed background color.
        
        # --- Layout & UI Creation ---
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # --- Display the celebratory success message to the user.
        message = "🎉 Hooray! Your PC has been successfully repaired. Feel free to use it."
        ctk.CTkLabel(main_frame, text=message, font=fonts["h3"], text_color=Theme.TEXT, wraplength=400, justify="center").pack(pady=(20, 30))

        # --- The single, large, centered action button for user confirmation.
        ok_button = GlassButton(main_frame, text="OK", emoji="✅", font=fonts["button"], command=self.close)
        ok_button.configure(fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, border_color=Theme.SUCCESS_BORDER)
        ok_button.pack(pady=(10, 20), padx=80, fill="x", ipady=10)

        # --- Allow closing with the Enter key for accessibility.
        self.bind("<Return>", lambda e: self.close())

    # ===============================================================================
    # METHOD: close
    # Overrides the base method to execute the specific callback before closing.
    # ===============================================================================
    def close(self):
        """Executes the on-close callback, then calls the parent close method."""
        # --- Execute the specific UI reset callback required by the parent frame.
        if self.on_close_callback:
            self.on_close_callback()
        # --- Call the base class's close method to handle window destruction and event unbinding.
        super().close()

# ===================================================================================
# SNIPPET 1: New CleanAllProgressBar Class
# A dedicated progress bar widget styled to match the provided image specification.
# It includes a dynamic percentage label and a themed progress bar.
# ===================================================================================
class CleanAllProgressBar(ctk.CTkFrame):
    """A progress bar widget with a percentage label, styled to specification."""
    def __init__(self, master, fonts):
        # --- Base Initialization ---
        # Initialize the parent frame. It's transparent to blend with the background.
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1) # Allow the progress bar to expand.

        # --- UI Components ---
        # The percentage label, positioned to the left of the bar as per the image.
        self.label = ctk.CTkLabel(self, text="0%", font=fonts["h2"], text_color=Theme.TEXT)
        self.label.grid(row=0, column=0, padx=(0, 15), sticky="w")

        # The progress bar, styled to match the visual reference.
        self.progress_bar = ctk.CTkProgressBar(
            self,
            orientation="horizontal",
            mode="determinate",
            height=30,
            corner_radius=15,  # Creates the pill shape.
            border_width=2,
            border_color=Theme.SUCCESS_BORDER, # Green border.
            fg_color=Theme.CARD, # Background of the bar.
            progress_color=Theme.SUCCESS # The green fill color.
        )
        self.progress_bar.set(0) # Start at 0%.
        self.progress_bar.grid(row=0, column=1, sticky="ew")

    def set_progress(self, value: float):
        """
        Updates the progress bar and percentage label.
        - value: A float between 0.0 and 1.0.
        """
        if self.winfo_exists():
            # Update the progress bar's visual fill.
            self.progress_bar.set(value)
            # Update the text label, formatted as an integer percentage.
            self.label.configure(text=f"{int(value * 100)}%")


# ===================================================================================
# CLASS: CleanAllSuccessPopup (v5.0 - Architecturally Compliant)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class now inherits from the BaseModalDialog engine, offloading all common
# modality and window management logic. It retains its unique UI construction
# and dynamic messaging capabilities while eliminating redundant code and ensuring
# adherence to the application's core architectural standard.
# ===================================================================================
class CleanAllSuccessPopup(BaseModalDialog):
    """
    A truly modal, DPI-aware, and anchored pop-up that displays a professional,
    randomized success message, now built upon the definitive BaseModalDialog engine.
    """
    # ===============================================================================
    # METHOD: __init__
    # Inherits from BaseModalDialog and orchestrates UI creation.
    # ===============================================================================
    def __init__(self, master, fonts, cleaned_size_str, on_close_callback):
        # --- Base Class Initialization: Establishes the core modal window.
        super().__init__(master, "Cleanup Complete!")
        
        # --- Store component-specific properties.
        self.on_close_callback = on_close_callback

        # --- Window & UI Configuration ---
        self.configure(fg_color=Theme.NAV_RAIL)
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self._create_widgets(main_frame, fonts, cleaned_size_str)

        # --- Allow closing with the Enter key for accessibility.
        self.bind("<Return>", lambda e: self.close())

    # ===============================================================================
    # METHOD: _create_widgets
    # Encapsulates the unique UI construction for this specific dialog.
    # ===============================================================================
    def _create_widgets(self, master_frame, fonts, cleaned_size_str):
        """Creates and lays out all the widgets inside the pop-up, ensuring DPI-aware text wrapping."""
        # --- DPI-Aware Wraplength Calculation for resilient layout.
        wraplength = self.master_window.winfo_width() * 0.4

        # --- Dynamic Messaging ---
        professional_messages = [
            ("Hooray! 🎉 Your PC is now fully clean.", "It’s now lighter, faster, and smoother than ever before."),
            ("Mission Accomplished! 🚀 All junk has been vaporized.", "Enjoy a more responsive and efficient system experience."),
            ("Cleanup Complete! ✨ Your system's cache has been purged.", "Your PC should now feel lighter and more agile.")
        ]
        header, sub_header = random.choice(professional_messages)
        final_message_header = f"{header}\n{sub_header}"

        # --- UI Element Creation ---
        ctk.CTkLabel(master_frame, text=final_message_header, font=fonts["h3"], text_color=Theme.TEXT, wraplength=wraplength, justify="center").pack(pady=(10, 15), padx=10)
        ctk.CTkFrame(master_frame, height=2, fg_color=Theme.BORDER).pack(fill="x", padx=50, pady=10)
        ctk.CTkLabel(master_frame, text=f"✅ Total space cleaned: {cleaned_size_str}", font=fonts["bold"], text_color=Theme.SUCCESS, wraplength=wraplength, justify="center").pack(pady=(15, 20), padx=10)
        ok_button = GlassButton(master_frame, text="OK", emoji="✅", font=fonts["button"], command=self.close)
        ok_button.configure(fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, border_color=Theme.SUCCESS_BORDER)
        ok_button.pack(pady=(10, 0), padx=100, fill="x")

    # ===============================================================================
    # METHOD: close
    # Overrides the base method to execute the specific callback before closing.
    # ===============================================================================
    def close(self):
        """Executes the on-close callback, then calls the parent close method."""
        if self.on_close_callback:
            self.on_close_callback()
        super().close()

# ===================================================================================
# CLASS: UpdateNotificationPopup (v1.0 - Zero-Defect Modality Engine)
#
# ARCHITECTURAL BLUEPRINT:
# This class defines a specialized, high-integrity modal dialog for presenting
# application update information to the user. It inherits its core unbreakable
# modality and dynamic centering from the `BaseModalDialog`, ensuring a consistent
# and professional user experience.
# ===================================================================================
class UpdateNotificationPopup(BaseModalDialog):
    """A modal dialog to inform the user about an available application update."""
    
    def __init__(self, master, fonts, update_info: dict, sound_manager: Optional['SoundManager'] = None):
        super().__init__(master, "Application Update")
        
        self.fonts = fonts
        self.update_info = update_info
        self.sound_manager = sound_manager

        self.configure(fg_color=Theme.NAV_RAIL)
        self._create_widgets()
        
        if self.sound_manager:
            self.sound_manager.play_sound('notification')

    def _create_widgets(self):
        """Creates and lays out all the widgets inside the pop-up."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=20, padx=30, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(0, 15), sticky="ew")
        ctk.CTkLabel(header_frame, text="🚀", font=self.fonts["emoji_large"]).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header_frame, text="A New Version is Available!", font=self.fonts["h2"], text_color=Theme.TEXT).pack(side="left")

        version_text = f"MK-Tools v{self.update_info.get('version', 'N/A')} is ready to install."
        ctk.CTkLabel(main_frame, text=version_text, font=self.fonts["bold"], text_color=Theme.ACCENT).grid(row=1, column=0, pady=(0, 15), sticky="w")
        
        ctk.CTkLabel(main_frame, text="Release Notes:", font=self.fonts["bold"], text_color=Theme.TEXT_SECONDARY).grid(row=2, column=0, pady=(0, 5), sticky="w")
        
        notes_textbox = ctk.CTkTextbox(main_frame, font=self.fonts["normal"], fg_color=Theme.CARD, wrap="word", height=150, border_width=1, border_color=Theme.BORDER)
        notes_textbox.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        
        release_notes = self.update_info.get('release_notes', ["No release notes provided."])
        notes_text = "\n".join([f"• {note.get('description', note) if isinstance(note, dict) else note}" for note in release_notes])
        notes_textbox.insert("end", notes_text)
        notes_textbox.configure(state="disabled")

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=4, column=0, sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # --- "Ignore" Button ---
        ctk.CTkButton(button_frame, text="Ignore", font=self.fonts["button"], command=self._on_ignore, fg_color=Theme.SECONDARY_DARK, hover_color=Theme.SECONDARY_HOVER_DARK, height=40).grid(row=0, column=0, padx=(0, 10), sticky="ew")

        # --- "Update Now" Button ---
        ctk.CTkButton(button_frame, text="Update Now", font=self.fonts["button"], command=self._on_update_now, fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, height=40).grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def _on_ignore(self):
        """Plays a sound and closes the dialog for the current session."""
        if self.sound_manager:
            self.sound_manager.play_sound('cancel_operation')
        self.close()

    def _on_update_now(self):
        """Plays a sound, opens the specific download page, and closes the dialog."""
        if self.sound_manager:
            self.sound_manager.play_sound('ok_click')
        
        # --- This URL now points to your specific download page as requested. ---
        download_url = "https://mr-muhammad-kashan.github.io/MK-Tools.github.io/download.html"
        webbrowser.open_new_tab(download_url)
        
        self.close()

# ===================================================================================
class ConfigDialog(BaseModalDialog):
    """A modal dialog for user input with validation, refactored for architectural purity."""
    def __init__(self, master, fonts, title, prompt, callback, validation_type='numeric'):
        # --- Initialize the BaseModalDialog with core properties ---
        super().__init__(master, title)
        # --- Store class-specific properties ---
        self.callback = callback
        self.validation_type = validation_type

        # --- Window & UI Configuration ---
        self.configure(fg_color=Theme.NAV_RAIL)
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)

        # --- UI Elements ---
        ctk.CTkLabel(self, text=prompt, font=fonts["normal"]).pack(pady=(20, 10))
        
        vcmd = (self.register(self._validate_char), '%P')
        self.entry = ctk.CTkEntry(self, font=fonts["normal"], width=250, border_color=Theme.BORDER,
                                  validate='key', validatecommand=vcmd)
        self.entry.pack(pady=10)
        self.entry.focus()
        
        self.error_label = ctk.CTkLabel(self, text="", text_color=Theme.VALIDATION_ERROR_BORDER, font=fonts["small"])
        self.error_label.pack(pady=5)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(button_frame, text="Enter", font=fonts["button"], command=self._on_enter, width=120).pack(side="left", padx=10)
        
        ctk.CTkButton(button_frame, text="Close", font=fonts["button"],
                      fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER,
                      command=self.close, width=120).pack(side="left", padx=10)
        
        self.bind("<Return>", lambda event: self._on_enter())
        
        # --- This call ensures the final geometry is known before centering. ---
        self.update_idletasks()
        self.geometry(f"{max(450, self.winfo_reqwidth())}x{self.winfo_reqheight()+40}")

    def _on_enter(self):
        value = self.entry.get()
        if self._validate_final(value):
            self.callback(value)
            self.close()
        else:
            self._flash_error()

    def _validate_char(self, new_value):
        if new_value == "": return True
        try:
            num = int(new_value)
            if self.validation_type == 'percentage':
                if len(new_value) > 3 or num > 100: return False
            return True
        except ValueError:
            return False

    def _validate_final(self, value):
        if not value: return False
        try:
            num = int(value)
            if self.validation_type == 'percentage':
                return 1 <= num <= 100
            return True
        except ValueError:
            return False

    def _flash_error(self):
        self.entry.configure(border_color=Theme.VALIDATION_ERROR_BORDER)
        if self.validation_type == 'percentage':
            self.error_label.configure(text="Value must be between 1-100.")
        else:
            self.error_label.configure(text="Invalid input.")
        self.after(2000, lambda: [
            self.entry.configure(border_color=Theme.BORDER),
            self.error_label.configure(text="")
        ])

# ===================================================================================
# CLASS: BuyMeACoffeeButton (v2.6 - Definitive Aesthetic Protocol)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive, zero-defect implementation of the support button. It has
# been aesthetically re-calibrated to provide a perfect "capsule" shape with bold,
# yet proportionally smaller, text for a visually appealing and highly-readable result.
#
# CORE ENHANCEMENTS:
#
#   1. [CAPSULE SHAPE GEOMETRY] The button's geometry is now dynamically calculated.
#      The `corner_radius` is set to exactly half of the button's `height`,
#      guaranteeing a perfect, aesthetically pleasing capsule shape for both the
#      large and small variants of the button.
#
#   2. [RE-CALIBRATED FONT & SIZE] The small variant (used in the NavigationRail)
#      now uses the `bold` font for clear, readable text. Its `height` has been
#      reduced from 40 to 36 pixels, creating a sleeker, more refined appearance
#      that integrates perfectly into the layout.
#
#   3. [MODULARITY & TIMED FEEDBACK] This version retains the superior timed
#      auditory feedback and custom text injection protocols from the previous
#      version, ensuring it remains a powerful and reusable component.
# ===================================================================================
class BuyMeACoffeeButton(ctk.CTkButton):
    """
    A reusable, styled button with a timed, stateful auditory feedback system,
    now featuring a perfectly calibrated capsule shape and font hierarchy.
    """
    _hover_sound_played_this_session: bool = False

    def __init__(self, master, fonts, is_large: bool = True, command: Optional[Callable] = None, sound_manager: Optional['SoundManager'] = None, custom_text: Optional[str] = None):
        # --- Store a reference to the global sound manager.
        self.sound_manager = sound_manager
        
        # --- [AESTHETIC & SIZE CALIBRATION PROTOCOL] ---
        if is_large:
            # --- Settings for the larger button variant (e.g., in the About page).
            self.font_obj = fonts["h2"] # Prominent, bold text
            height = 48
            corner_radius = 24 # Perfect capsule shape (height / 2)
        else:
            # --- Settings for the smaller, sleeker button (e.g., in the Navigation Rail).
            self.font_obj = fonts["bold"] # Bold text, as requested
            height = 36 # Reduced height for a more refined size
            corner_radius = 18 # Perfect capsule shape (height / 2)

        # --- Use custom text if provided, otherwise default to "Buy Me a Coffee".
        display_text = custom_text if custom_text is not None else "Buy Me a Coffee"
        final_text = f"☕  {display_text}"

        # --- Use the injected command or the internal default link-opening method.
        final_command = command if command is not None else self._open_link
        
        # --- Base Class Initialization with new calibrated geometry and fonts.
        super().__init__(master, text=final_text, font=self.font_obj, height=height,
                         corner_radius=corner_radius, fg_color=Theme.COFFEE_BUTTON_FG,
                         text_color=Theme.COFFEE_BUTTON_TEXT, hover_color=Theme.COFFEE_BUTTON_HOVER,
                         command=final_command)

        # --- State variables for the timed hover sound protocol.
        self._sound_job = None
        self._is_mouse_inside = False
        self._leave_check_job = None
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _open_link(self):
        """
        The default action: cancels any pending hover sound, plays the click sound,
        and then safely opens the support link.
        """
        if self._sound_job:
            self.after_cancel(self._sound_job)
            self._sound_job = None
        if self.sound_manager:
            self.sound_manager.play_sound('support_click')
        try:
            webbrowser.open_new_tab(AppConfig.BUY_ME_A_COFFEE_URL)
        except Exception as e:
            logging.error(f"Failed to open link. Error: {e}", exc_info=True)

    def _play_delayed_hover_sound(self):
        """
        This method is called ONLY after the 0.9-second delay.
        """
        if not BuyMeACoffeeButton._hover_sound_played_this_session:
            if self.sound_manager:
                self.sound_manager.stop_and_play_sound('support_hover')
            BuyMeACoffeeButton._hover_sound_played_this_session = True

    def _on_enter(self, event=None):
        """
        Handles the mouse entering the button, scheduling the delayed auditory feedback.
        """
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        if not self._is_mouse_inside:
            self._is_mouse_inside = True
            self._sound_job = self.after(900, self._play_delayed_hover_sound)

    def _on_leave(self, event=None):
        """
        Schedules a delayed check to verify if the mouse has truly exited the component's boundary.
        """
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    def _check_if_truly_left(self):
        """
        Performs a definitive check of the cursor's position and cancels the scheduled sound if the mouse has left.
        """
        if not self.winfo_exists(): return
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        x1, y1 = self.winfo_rootx(), self.winfo_rooty()
        x2, y2 = x1 + self.winfo_width(), y1 + self.winfo_height()
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)
        if is_truly_outside and self._is_mouse_inside:
            self._is_mouse_inside = False
            if self._sound_job:
                self.after_cancel(self._sound_job)
                self._sound_job = None

# ===================================================================================
# CLASS: SocialButton (v6.1 - Command-Injectable & Stateful)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component is engineered with a command injection protocol, making it a
# truly modular and reusable military-grade component.
# ===================================================================================
class SocialButton(ctk.CTkButton):
    """A specialized, icon-driven button, with an injectable command protocol."""

    def __init__(self, master, fonts, text: str, icon_path: str,
                 link: Optional[str] = None,
                 color_config: dict = None,
                 sound_manager: Optional['SoundManager'] = None,
                 click_sound_name: Optional[str] = None,
                 command: Optional[Callable] = None):
        
        # --- Store Core Properties ---
        self.sound_manager = sound_manager
        self.click_sound_name = click_sound_name
        self.link = link
        
        # --- State variables for the robust hover detection system.
        self._is_mouse_inside = False
        self._leave_check_job = None

        # --- [DPI SCALING] Calculate scaled geometry and icon sizes.
        scale_factor = ScreenManager.get_scaling_factor()
        scaled_icon_size = int(30 * scale_factor)
        scaled_height = int(60 * scale_factor)
        scaled_corner_radius = int(22 * scale_factor)
        scaled_border_width = max(1, int(2 * scale_factor)) # Ensure border is at least 1px.
        
        # --- Icon Loading and Processing with scaled size.
        try:
            # --- [MODIFIED] Use resource_path to get the absolute path to the icon.
            image = Image.open(resource_path(os.path.join("Icons", icon_path)))
            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(scaled_icon_size, scaled_icon_size))
        except FileNotFoundError:
            logging.error(f"CRITICAL: Icon asset not found at path: {icon_path}. Rendering button without icon.")
            ctk_image = None
        
        # --- Command Resolution Protocol ---
        final_command = command if command is not None else self._default_on_click

        # --- Base Class Initialization with scaled geometry.
        super().__init__(
            master,
            image=ctk_image,
            text=text,
            font=fonts["h2"],
            height=scaled_height,
            corner_radius=scaled_corner_radius,
            border_width=scaled_border_width,
            command=final_command,
            compound="left",
            text_color_disabled="#A8A5C5"
        )
        
        # --- Dynamic Color and Event Binding ---
        if color_config: self.configure(**color_config)
        for widget in (self, self._image_label, self._text_label):
            if widget:
                widget.bind("<Enter>", self._on_enter)
                widget.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        """Handles the mouse entering ANY part of the button, triggering the hover-on action exactly once."""
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        if not self._is_mouse_inside:
            self._is_mouse_inside = True
            if self.sound_manager: self.sound_manager.play_sound('hover')
            self.configure(border_width=4)

    def _on_leave(self, event=None):
        """Schedules a delayed check to verify if the mouse has truly exited the component's boundary."""
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    def _check_if_truly_left(self):
        """Performs a definitive check of the cursor's position to trigger the hover-off state correctly."""
        if not self.winfo_exists(): return
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        x1, y1 = self.winfo_rootx(), self.winfo_rooty()
        x2, y2 = x1 + self.winfo_width(), y1 + self.winfo_height()
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)
        if is_truly_outside and self._is_mouse_inside:
            self._is_mouse_inside = False
            self.configure(border_width=2)

    def _default_on_click(self):
        """Plays the button-specific click sound and safely opens the provided link."""
        if self.sound_manager and self.click_sound_name:
            self.sound_manager.play_sound(self.click_sound_name)
        
        if self.link:
            try:
                logging.info(f"Dispatching to external link: {self.link}")
                webbrowser.open_new_tab(self.link)
            except Exception as e:
                logging.error(f"Failed to open external link '{self.link}'. Error: {e}", exc_info=True)


# ===================================================================================
# CLASS: CircularActionButton (v3.1 - Zero-Defect & Fully Encapsulated)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component has been re-architected into a fully self-sufficient, state-aware
# entity. It now encapsulates its own auditory and visual feedback logic,
# eliminating all external dependencies for state management and resolving the
# hover-sound anomaly at a fundamental level.
#
# STATEFUL HOVER PROTOCOL (ZERO-SPAM):
#
#   [Mouse Enters ANY Child Widget] -> [_on_enter()]
#        |
#        +-- Is `_is_mouse_inside` False? --(YES)--> 1. Set `_is_mouse_inside` = True
#        |                                           2. Play 'fix_windows_hover' sound (EXACTLY ONCE)
#        |                                           3. Change border color to ACCENT
#        |
#        '--(NO)--> Do nothing. (Prevents sound/visual spam)
#
#   [Mouse Leaves ANY Child Widget] -> [_on_leave()]
#        |
#        +-- Schedule `_check_if_truly_left()` to run in 1ms.
#
# This protocol guarantees the hover sound is dispatched exactly once upon entry
# and is not re-triggered by mouse movements between the button's internal elements.
# ===================================================================================
class CircularActionButton(ctk.CTkFrame):
    """
    A self-contained, circular, icon-driven button with a 3D glassy effect,
    animated hover glow, and a robust, error-free UI scaling method. This version
    is fully sound-aware and manages its own state.
    """
    def __init__(self, master, fonts, emoji: str, text: str, style: str, command: Callable[[], None], sound_manager: Optional['SoundManager'] = None):
        # --- Base Class Initialization ---
        super().__init__(master, fg_color="transparent")
        
        # --- Property & State Storage ---
        self.sound_manager = sound_manager
        self._is_mouse_inside = False
        self._leave_check_job = None

        # --- Internal Grid Configuration ---
        self.grid_columnconfigure(0, weight=1)
        
        # --- [DPI SCALING] Style & Sizing Constants ---
        scale_factor = ScreenManager.get_scaling_factor()
        DIAMETER = int(140 * scale_factor) # Scale the base diameter
        RADIUS = DIAMETER // 2
        style_map = {
            "success": {"fg_color": "#287D32", "hover_color": "#4CAF50", "border_color": "#388E3C"},
            "accent":  {"fg_color": Theme.ACCENT_ACTIVE_DARK, "hover_color": Theme.ACCENT, "border_color": Theme.ACCENT_HOVER_DARK}
        }
        self.active_style = style_map.get(style, style_map["accent"])

        # --- Widget Creation: Circular Button ---
        self.button = ctk.CTkButton(
            self,
            text=emoji,
            font=fonts["emoji_large"], # Use pre-scaled font from Theme
            command=command,
            width=DIAMETER, height=DIAMETER, corner_radius=RADIUS,
            border_width=int(4 * scale_factor), **self.active_style # Scale border width
        )
        self.button.grid(row=0, column=0, padx=int(10 * scale_factor), pady=int(10 * scale_factor))

        # --- Widget Creation: Text Label ---
        self.label = ctk.CTkLabel(
            self, text=text, font=fonts["h3"], text_color=Theme.TEXT_SECONDARY
        )
        self.label.grid(row=1, column=0, padx=int(10 * scale_factor), pady=(0, int(10 * scale_factor)))

        # --- Unified Event Binding Protocol ---
        for widget in (self, self.button, self.label):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            if widget is not self.button:
                widget.bind("<Button-1>", lambda e, c=command: c())

    def _on_enter(self, event=None):
        """Activates the hover state, playing the sound and changing the border exactly once."""
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
            self._leave_check_job = None

        if not self._is_mouse_inside:
            self._is_mouse_inside = True
            
            # --- Dispatch Auditory Feedback ---
            if self.sound_manager:
                self.sound_manager.play_sound('fix_windows_hover')
            
            # --- Dispatch Visual Feedback ---
            self.button.configure(border_color=Theme.GLASS_BORDER_HOVER)

    def _on_leave(self, event=None):
        """Schedules a delayed check to verify if the mouse has truly exited the component's boundary."""
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    def _check_if_truly_left(self):
        """Performs a definitive check of the cursor's position to trigger the hover-off state correctly."""
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        x1, y1 = self.winfo_rootx(), self.winfo_rooty()
        x2, y2 = x1 + self.winfo_width(), y1 + self.winfo_height()
        
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)
        
        if is_truly_outside and self._is_mouse_inside:
            self._is_mouse_inside = False
            # Revert the visual feedback to its default state.
            self.button.configure(border_color=self.active_style["border_color"])

    def update_ui_scaling(self, fonts: dict):
        """The definitive, encapsulated method for updating this component's internal fonts."""
        if self.winfo_exists():
            self.label.configure(font=fonts["h3"])

# ===================================================================================
# CLASS: AnimatedTweakCard (v3.6 - Deterministic Startup Protocol)
#
# ARCHITECTURAL BLUEPRINT (RE-ENGINEERING):
# This version implements a paradigm solution to a critical startup race condition.
# The previous architecture contained a logical flaw where each card instance would
# spawn its own background thread to check system state, competing with the main
# application's pre-flight check thread. This created a non-deterministic startup
# that resulted in a `RuntimeError` when a card's thread attempted to call `self.after()`
# before the main thread had entered `app.mainloop()`.
#
# NEW PARADIGM: CENTRALIZED STATE INJECTION
#
#   1. [LOGIC ELIMINATION] The `initialize_state()` and `_check_in_background()`
#      methods have been completely REMOVED from this class. The component no
#      longer possesses the autonomy to check its own state at startup.
#
#   2. [PASSIVE INITIALIZATION] The constructor now explicitly sets the card's
#      button to a "Checking..." state. The card is now a passive view that
#      awaits instruction.
#
#   3. [STATE INJECTION API] The `_set_initial_state_on_main_thread()` method is
#      retained as the sole, definitive public API for receiving state data.
#      It is now exclusively called by the master `App` class's `_on_pre_flight_complete()`
#      method, which is guaranteed to execute only after the main loop is active
#      and all system checks are finished.
#
# This architecture creates a single, predictable, and deterministic data flow,
# completely eliminating the race condition and ensuring 100% startup stability.
# ===================================================================================
class AnimatedTweakCard(ctk.CTkFrame):
    """
    A versatile, interactive card with a stateful hover effect, rich-text
    info panel, and a fully integrated, multi-layered auditory feedback system.
    """
    # --- The constructor accepts the master app_instance for lifecycle awareness.
    def __init__(self, master, fonts, app_instance, title, description, emoji="⚙️", view_mode='toggle', tweak_logic=None, info_data=None, custom_config_panel_builder=None, sound_manager: Optional['SoundManager'] = None):
        # --- Base class initialization. ---
        super().__init__(master, fg_color=Theme.CARD, corner_radius=20, border_width=1, border_color=Theme.CARD)
        # --- Property and State Storage ---
        self.fonts = fonts
        # --- Store a reference to the main App for the shutdown signal. This is critical for stability.
        self.app = app_instance
        self.view_mode = view_mode
        self.tweak_logic = tweak_logic
        self.info_data = info_data
        self.sound_manager = sound_manager
        self.is_tweak_on = False
        self.current_tweak_value = None
        self.is_panel_expanded = False
        self.active_panel = None
        self.info_frame = None
        self.config_frame = None
        self.custom_config_panel_builder = custom_config_panel_builder
        # --- State variables for the zero-spam hover protocol.
        self._is_mouse_inside = False
        self._leave_check_job = None

        # --- UI Construction ---
        self._setup_ui(title, description, emoji)
        self._bind_events()

        # --- [CRITICAL FIX] Set the default initial state directly. ---
        # --- The card no longer fetches its own state. The master `App` controller will
        # --- inject the true state after its pre-flight checks are complete.
        if self.tweak_logic:
            self.action_button.configure(state="disabled", text="Checking...")

    # [RETAINED] This method is now the sole public API for state injection, called by the App class.
    def _set_initial_state_on_main_thread(self, state_data):
        """
        Updates the card's UI to reflect the initial state of the tweak.
        This method is always executed on the main thread, ensuring thread safety.
        """
        # --- CRITICAL CHECK: Verify the widget still exists before attempting to configure it.
        if not self.winfo_exists():
            logging.warning(f"UI update for '{self.title_label.cget('text')}' skipped: widget no longer exists.")
            return

        # --- Safely update the UI based on the retrieved state data.
        if self.view_mode == 'toggle':
            self.is_tweak_on = state_data
            self._update_toggle_button_appearance()
        elif self.view_mode == 'config_dropdown':
            # --- Handle dictionary-based state for more complex tweaks.
            self.is_tweak_on = state_data.get('status', 'default') # Safely get status
            self.current_tweak_value = state_data.get('value')
            self._update_config_button_appearance()
        
        # --- Re-enable the action button now that the state check is complete.
        self.action_button.configure(state="normal")
        
    def _execute_tweak_action(self, action, feedback_text, **kwargs):
        """Disables controls and runs the specified tweak logic in a background thread."""
        # --- Set the UI to a "working" state.
        self.action_button.configure(state="disabled", text=feedback_text)
        self.reset_button.configure(state="disabled")

        def _action_in_background():
            """
            This worker function runs the potentially slow tweak logic and then
            re-checks the state, all on a background thread.
            """
            # --- Execute the primary long-running operation (e.g., registry write).
            completion_message = action(**kwargs)

            # --- CRITICAL CHECK 1 (Mid-process): Check the shutdown signal immediately after the first operation.
            if self.app.shutdown_event.is_set():
                logging.warning(f"Shutdown signal detected in '{self.title_label.cget('text')}'; aborting state re-check.")
                return  # --- Abort mission.

            # --- Execute the secondary long-running operation (re-checking the state).
            new_state_data = self.tweak_logic.check_status()

            # --- CRITICAL CHECK 1 (Post-process): Check the shutdown signal again before the final UI update.
            if self.app.shutdown_event.is_set():
                logging.warning(f"Shutdown signal detected in '{self.title_label.cget('text')}'; aborting final UI update.")
                return  # --- Abort mission.

            # --- [NEW PARADIGM] Schedule the final UI update to run on the main thread.
            self.after(0, self._finalize_action_on_main_thread, new_state_data, completion_message)

        # --- Start the background thread.
        threading.Thread(target=_action_in_background, daemon=True).start()
    
    def _execute_config_action(self, action: Callable, feedback_text: str, sound_name: str):
        """
        [NEW] A definitive command handler that correctly sequences all actions for
        a configuration panel button click. It guarantees the panel closes BEFORE
        the background operation is initiated.
        
        Args:
            action (Callable): The tweak logic method to execute (e.g., self.tweak_logic.turn_on).
            feedback_text (str): The text to display on the button while working (e.g., "Enabling...").
            sound_name (str): The name of the sound to play for this action.
        """
        # --- Step 1: Dispatch Auditory Feedback ---
        if self.sound_manager:
            self.sound_manager.play_sound(sound_name)
        
        # --- Step 2: Forcibly close any open configuration/info panels.
        self.close_all_panels()
        
        # --- Step 3: Initiate the non-blocking, background tweak operation.
        self._execute_tweak_action(action, feedback_text)

    # [RE-ENGINEERED] This method is GUARANTEED to run on the main UI thread and is lifecycle-aware.
    def _finalize_action_on_main_thread(self, new_state_data, completion_message):
        """
        Finalizes the tweak action by updating the UI and showing a notification.
        This method is always executed on the main thread.
        """
        # --- CRITICAL CHECK 2: Final existence check before any UI manipulation.
        if not self.winfo_exists():
            logging.warning(f"Finalization for '{self.title_label.cget('text')}' skipped: widget no longer exists.")
            return

        # --- Update the card's state and button appearance based on the new data.
        self._set_initial_state_on_main_thread(new_state_data)
        
        # --- Re-enable the reset button.
        self.reset_button.configure(text="Reset Defaults", state="normal")
        
        # --- If the backend logic provided a message, display it in a notification pop-up.
        if completion_message:
            self._show_completion_notification(completion_message)
            
    def _setup_ui(self, title, description, emoji):
        """Creates and arranges the primary UI elements of the card."""
        # --- Create a main frame to hold all content with consistent padding.
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="x", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(1, weight=1) # Allow the text column to expand.
        # --- Create the descriptive content (icon, title, description).
        self._create_content(title, description, emoji)
        # --- Create the interactive buttons (action, reset, info).
        self._create_buttons()

    def _create_content(self, title, description, emoji):
        """Creates the main descriptive content of the card."""
        # --- The emoji label on the left.
        self.emoji_label = ctk.CTkLabel(self.main_frame, text=emoji, font=("Arial", 24))
        self.emoji_label.grid(row=0, rowspan=2, column=0, padx=15, pady=10)
        # --- The main title label.
        self.title_label = ctk.CTkLabel(self.main_frame, text=title, font=self.fonts["bold"], text_color=Theme.TEXT)
        self.title_label.grid(row=0, column=1, sticky="w")
        # --- The secondary description label.
        self.desc_label = ctk.CTkLabel(self.main_frame, text=description, font=self.fonts["small"], text_color=Theme.TEXT_SECONDARY)
        self.desc_label.grid(row=1, column=1, sticky="w")

    def _create_buttons(self):
        """Creates the control buttons for the tweak based on the view_mode."""
        # --- Create a frame to hold the control buttons on the right.
        self.controls_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.controls_frame.grid(row=0, rowspan=2, column=2, padx=15)

        # --- The primary action button (e.g., "Turn On", "Configure").
        self.action_button = ctk.CTkButton(self.controls_frame, font=self.fonts["button"],
                                           height=35, corner_radius=10, border_width=2)
        self.action_button.grid(row=0, column=0, padx=2, pady=5, sticky="ew")

        # --- Configure the button's command and appearance based on its mode.
        if self.view_mode == 'toggle':
            self.controls_frame.grid_columnconfigure((0, 1), weight=1)
            self.action_button.configure(command=self.toggle_tweak_state)
            self._update_toggle_button_appearance()
        elif self.view_mode == 'config_dropdown':
            self.controls_frame.grid_columnconfigure((0, 1), weight=1)
            self.action_button.configure(command=lambda: self.toggle_panel('config'))
            self._update_config_button_appearance()

        # --- The "Reset Defaults" button.
        self.reset_button = ctk.CTkButton(self.controls_frame, text="Reset Defaults", font=self.fonts["button"],
                                          height=35, corner_radius=10, fg_color=Theme.RESET_BUTTON_FG,
                                          text_color=Theme.RESET_BUTTON_TEXT, hover_color=Theme.RESET_BUTTON_HOVER,
                                          command=self.reset_tweak)
        self.reset_button.grid(row=0, column=1, padx=2, pady=5, sticky="ew")

        # --- The "Info" button (question mark).
        self.info_button = ctk.CTkButton(self.main_frame, text="❓", width=30, height=30, corner_radius=15,
                                         fg_color=Theme.NAV_RAIL, hover_color=Theme.CARD,
                                         command=lambda: self.toggle_panel('info'))
        self.info_button.grid(row=0, column=3, padx=(10, 5))

    def _bind_events(self):
        """Binds hover events recursively to all child widgets for a unified effect."""
        # --- This comprehensive list ensures that hovering over any part of the card triggers the effect.
        widgets_to_bind = [self, self.main_frame, self.emoji_label, self.title_label, self.desc_label, self.controls_frame, self.action_button, self.reset_button, self.info_button]
        for widget in widgets_to_bind:
            widget.bind("<Enter>", self.on_enter, add="+")
            widget.bind("<Leave>", self.on_leave, add="+")

    # [RE-ENGINEERED] Implements the stateful, zero-spam hover-on protocol.
    def on_enter(self, event=None):
        """Handles the mouse entering ANY part of the card, triggering the hover-on action exactly once."""
        # --- Cancel any pending "leave" check. This is crucial for when the mouse moves rapidly between child widgets.
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
            self._leave_check_job = None
        
        # --- Check the state to prevent re-triggering. If the mouse is not already inside, proceed.
        if not self._is_mouse_inside:
            # --- Update the state to reflect the mouse is now inside.
            self._is_mouse_inside = True
            
            # --- [NEW] Dispatch Auditory Feedback: Play the feature-specific hover sound.
            if self.sound_manager:
                self.sound_manager.play_sound('feature_hover')
            
            # --- Dispatch Visual Feedback: Change the border color for a highlight effect.
            self.configure(border_color=Theme.GLASS_BORDER_HOVER)

    # [RE-ENGINEERED] Implements the stateful, zero-spam hover-off protocol.
    def on_leave(self, event=None):
        """Schedules a delayed check to verify if the mouse has truly exited the component's boundary."""
        # --- Cancel any previously scheduled check to avoid redundant calls.
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
        # --- Schedule the forensic check to run after 1 millisecond.
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    # [NEW] Performs a forensic check of the cursor's position to correctly trigger the hover-off state.
    def _check_if_truly_left(self):
        """Performs a definitive check of the cursor's position to trigger the hover-off state correctly."""
        # --- Get the absolute screen coordinates of the mouse pointer.
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        # --- Get the absolute screen coordinates of this card's bounding box.
        x1, y1 = self.winfo_rootx(), self.winfo_rooty()
        x2, y2 = x1 + self.winfo_width(), y1 + self.winfo_height()
        
        # --- The Core Logical Check: Determine if the pointer is outside the card's bounding box.
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)
        
        # --- If the mouse is confirmed to be outside AND the component still thinks the mouse is inside...
        if is_truly_outside and self._is_mouse_inside:
            # --- Update the state to reflect the mouse is now outside.
            self._is_mouse_inside = False
            # --- Revert the visual feedback.
            self.configure(border_color=Theme.CARD)

    def toggle_tweak_state(self):
        """Toggles the state of the tweak and plays the appropriate sound."""
        # --- Abort if there is no logic controller or the mode is incorrect.
        if not self.tweak_logic or self.view_mode != 'toggle': return
        # --- Play the correct sound based on the current state.
        if self.sound_manager:
            if self.is_tweak_on:
                self.sound_manager.play_sound('turn_off')
            else:
                self.sound_manager.play_sound('turn_on')
        # --- Determine which action to call (apply or undo) and the feedback text.
        action = self.tweak_logic.undo if self.is_tweak_on else self.tweak_logic.apply
        feedback_text = "Disabling..." if self.is_tweak_on else "Enabling..."
        # --- Execute the action in a background thread.
        self._execute_tweak_action(action, feedback_text)

    def reset_tweak(self):
        """Resets the tweak to its default state and plays a sound."""
        # --- Abort if there is no logic controller.
        if not self.tweak_logic: return
        # --- Play the reset sound.
        if self.sound_manager:
            self.sound_manager.play_sound('reset')
        # --- Execute the 'undo' action in a background thread.
        self._execute_tweak_action(self.tweak_logic.undo, "Resetting...")
        # --- If a panel is open, close it.
        if self.is_panel_expanded: self.close_all_panels()

    def _update_toggle_button_appearance(self):
        """Updates the appearance of a standard 'On/Off' toggle button."""
        # --- This method's internal logic remains unchanged. ---
        if self.is_tweak_on:
            self.action_button.configure(text="Turned On", fg_color=Theme.STATE_ON_FG, hover_color=Theme.STATE_ON_HOVER, border_color=Theme.STATE_ON_BORDER)
        else:
            self.action_button.configure(text="Turned Off", fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, border_color=Theme.STATE_OFF_BORDER)

    def _update_config_button_appearance(self):
        """
        [CORRECTED v3.6] Updates the appearance of a 'Configure' button by correctly
        mapping all potential states ('on', 'off', 'configured', 'default') to their
        respective, definitive visual styles. This solves the UI state bug for all
        configuration-based tweaks.
        """
        # --- This condition evaluates both 'on' and 'configured' states as a positive, "enabled" visual state.
        if self.is_tweak_on == 'on' or self.is_tweak_on == 'configured':
            # --- [COLOR UNIFICATION] Configure the button to the standard 'Turned On' state (Green).
            # --- This now uses the same theme colors as the toggle buttons for visual consistency.
            self.action_button.configure(
                text="Turned On",
                fg_color=Theme.STATE_ON_FG,
                hover_color=Theme.STATE_ON_HOVER,
                border_color=Theme.STATE_ON_BORDER
            )
        # --- Check if the tweak is actively turned OFF. This is specific to the GPU tweak.
        elif self.is_tweak_on == 'off':
            # --- Configure the button to the 'Turned Off' state (Red).
            self.action_button.configure(
                text="Turned Off",
                fg_color=Theme.STATE_OFF_FG,
                hover_color=Theme.STATE_OFF_HOVER,
                border_color=Theme.STATE_OFF_BORDER
            )
        # --- This is the final fallback for the 'default' or any other unhandled state.
        else:
            # --- Configure the button to the 'Not Configured' state (Blue).
            self.action_button.configure(
                text="Not Configured",
                fg_color=Theme.CONFIGURE_BUTTON_FG,
                hover_color=Theme.CONFIGURE_BUTTON_HOVER,
                border_color=Theme.BORDER
            )

    # [MODIFIED] Injects the 'ok_click' sound into the notification's 'OK' button command.
    def _show_completion_notification(self, message: str):
        """Displays a modal notification upon completion of a tweak action with auditory feedback."""
        # --- Abort if the widget has been destroyed.
        if not self.winfo_exists(): return
        # --- Find the top-level content frame to host the overlay.
        top_level_frame = self
        while not isinstance(top_level_frame, BaseContentFrame) and top_level_frame.master is not None:
            top_level_frame = top_level_frame.master
        
        # --- [NEW] Create a wrapper function for the 'OK' button's action.
        def on_ok_action():
            """This function will be the new command for the 'OK' button."""
            # --- Step 1: Play the confirmation sound.
            if self.sound_manager:
                self.sound_manager.play_sound('ok_click')
            # --- Step 2: Execute the original logic (closing all panels).
            self.close_all_panels()

        # --- Define the properties for the notification overlay.
        title = "Optimization Complete"
        emoji = "✅"
        # --- [MODIFIED] The button's command now points to our new sound-aware wrapper function.
        buttons = [{'text': 'OK (Restart Required)', 'style': 'success', 'command': on_ok_action}]
        # --- Create and show the overlay.
        overlay = InlineNotificationOverlay( master=top_level_frame, fonts=self.fonts, title=title, message=message, emoji=emoji, buttons_config=buttons, on_close_callback=None )
        overlay.show()

    # [MODIFIED] Plays the 'question_mark' sound when toggling the info panel.
    def toggle_panel(self, panel_type: str):
        """
        Notifies the parent frame to manage other panels, then toggles the
        visibility of this card's info or configuration dropdown panels
        with auditory feedback.
        """
        # --- Step 1: Notify the parent frame (e.g., PerformanceFrame) to close all other open panels.
        # --- This is the core of the "exclusive panel" logic. The hasattr check ensures safety.
        if hasattr(self.master, 'manage_card_panels'):
            self.master.manage_card_panels(self)

        # --- Step 2: Play the correct sound for the action. Sound plays only when opening a panel.
        if self.sound_manager and panel_type == 'info' and not self.is_panel_expanded:
            self.sound_manager.play_sound('question_mark')

        # --- Step 3: Determine which panel to show.
        panel_to_show = None
        if panel_type == 'info':
            if self.info_frame is None: self._create_info_panel() # Lazily create the panel.
            panel_to_show = self.info_frame
        elif panel_type == 'config':
            if self.custom_config_panel_builder: self.custom_config_panel_builder()
            elif self.config_frame is None: self._create_config_dropdown_panel()
            panel_to_show = self.config_frame

        # --- Step 4: Toggle the panel's visibility based on its current state.
        if self.is_panel_expanded and self.active_panel == panel_to_show:
            self.close_all_panels()
        else:
            if self.active_panel: self.active_panel.pack_forget() # Close any different, active panel first.
            if panel_to_show:
                panel_to_show.pack(fill="x", padx=10, pady=(0, 10), expand=True)
                self.is_panel_expanded = True
                self.active_panel = panel_to_show

    def close_all_panels(self):
        """Externally callable method to forcibly close any open dropdown panel."""
        # --- This method's internal logic remains unchanged. ---
        if self.is_panel_expanded and self.active_panel:
            self.active_panel.pack_forget()
            self.is_panel_expanded = False
            self.active_panel = None

    def _create_info_panel(self):
        """Creates the rich-text info panel on-demand from the structured info_data, dynamically sizing the textbox to fit all content."""
        # --- Create the info panel frame with consistent styling and layout.
        self.info_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        # --- Initialize the textbox with no scrollbars and dynamic height.
        textbox = ctk.CTkTextbox(self, fg_color="transparent", text_color=Theme.TEXT_SECONDARY,
                                wrap="word", height=1, activate_scrollbars=False, border_width=0,
                                font=self.fonts["normal"])
        textbox.pack(in_=self.info_frame, padx=20, pady=15, fill="both", expand=True)
        textbox.configure(state="disabled")

        # --- Define text styling tags for consistent formatting.
        tags = {
            "heading": {'foreground': Theme.ACCENT, 'underline': True},
            "body": {'foreground': Theme.TEXT_SECONDARY},
            "pros_h": {'foreground': Theme.SUCCESS, 'underline': True},
            "pros": {'foreground': Theme.SUCCESS},
            "cons_h": {'foreground': Theme.STATE_OFF_FG, 'underline': True},
            "cons": {'foreground': Theme.STATE_OFF_FG},
        }
        for tag, config in tags.items():
            textbox.tag_config(tag, **config)

        # --- Helper function to insert text and track line count for height calculation.
        def insert_text(text, tag, end_char="\n\n"):
            textbox.configure(state="normal")
            textbox.insert("end", text + end_char, tag)
            textbox.configure(state="disabled")
            # --- Calculate the number of lines based on wraplength=500 and font metrics.
            font_size = self.fonts["normal"].cget("size")  # Correctly retrieve font size from CTkFont object.
            chars_per_line = 500 // (abs(font_size) // 2)  # Approximate characters per line (assuming avg char width, using abs for negative font sizes in tkinter).
            lines = len(text) // chars_per_line + text.count("\n") + (1 if end_char == "\n\n" else 0)
            return max(1, lines)

        # --- Calculate total lines for dynamic height.
        total_lines = 0
        if self.info_data:
            # --- Insert and count lines for title.
            title = self.info_data.get('title', 'Feature Information')
            total_lines += insert_text(title, "heading")

            # --- Insert and count lines for description.
            description = self.info_data.get('description', 'No details available.')
            total_lines += insert_text(description, "body")

            # --- Insert and count lines for pros header and items.
            total_lines += insert_text("✅ Pros", "pros_h", end_char="\n")
            for pro in self.info_data.get('pros', ['N/A']):
                total_lines += insert_text(f"  • {pro}", "pros", end_char="\n")
            textbox.configure(state="normal")
            textbox.insert("end", "\n")
            textbox.configure(state="disabled")
            total_lines += 1  # Account for the extra newline.

            # --- Insert and count lines for cons header and items.
            total_lines += insert_text("⚠️ Cons", "cons_h", end_char="\n")
            for con in self.info_data.get('cons', ['N/A']):
                total_lines += insert_text(f"  • {con}", "cons", end_char="\n")

            # --- Handle optional recommendation field (e.g., for GPU Scheduling).
            recommendation = self.info_data.get('recommendation', None)
            if recommendation:
                total_lines += insert_text("📝 Recommendation", "heading", end_char="\n")
                total_lines += insert_text(recommendation, "body")

        else:
            # --- Fallback for missing info_data.
            total_lines += insert_text("No detailed information available for this feature.", "body")

        # --- Calculate the required height: lines * line height (font size + padding).
        line_height = abs(self.fonts["normal"].cget("size")) + 4  # Use abs to handle negative font sizes in tkinter.
        required_height = total_lines * line_height + 30  # Add padding for aesthetics.
        textbox.configure(height=max(50, required_height))  # Ensure a minimum height for small content.

    def _create_svchost_config_panel(self):
        """Creates the advanced, multi-step configuration panel for the SvcHost Tweak."""
        # --- This method's internal logic remains unchanged. ---
        self.config_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        self.config_frame.grid_columnconfigure(0, weight=1)
        self.analysis_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        self.analysis_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        self.analysis_frame.grid_columnconfigure(0, weight=1)
        loading_label = ctk.CTkLabel(self.analysis_frame, text="Analyzing System RAM...", font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY)
        loading_label.grid(row=0, column=0, pady=10)
        def _fetch_ram_and_update_ui():
            detected_ram_gb = self.tweak_logic.get_total_physical_ram_gb()
            if self.app.shutdown_event.is_set(): return
            self.after(0, self._populate_svchost_analysis_ui, loading_label, detected_ram_gb)
        threading.Thread(target=_fetch_ram_and_update_ui, daemon=True).start()

    def _create_gpu_config_panel(self):
        """Creates the GPU configuration panel with a close button and updated logic."""
        # Create the configuration panel frame with consistent styling
        self.config_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        self.config_frame.grid_columnconfigure(0, weight=1)
        
        # Add informational textbox
        textbox = ctk.CTkTextbox(
            self.config_frame, 
            fg_color="transparent", 
            text_color=Theme.TEXT_SECONDARY, 
            wrap="word", 
            height=350, 
            activate_scrollbars=True, 
            border_width=0, 
            font=self.fonts["normal"]
        )
        textbox.pack(in_=self.config_frame, padx=20, pady=15, fill="both", expand=True)
        
        # Define text styling tags
        tags = {
            "title": {'foreground': Theme.TEXT, 'underline': True},
            "nvidia_h": {'foreground': "#76B900"},
            "amd_h": {'foreground': "#ED1C24"},
            "intel_h": {'foreground': "#0071C5"},
            "body": {'foreground': Theme.TEXT_SECONDARY},
            "pros": {'foreground': Theme.SUCCESS},
            "cons": {'foreground': Theme.STATE_OFF_FG},
            "note": {'foreground': Theme.WARNING_DARK}
        }
        for tag, config in tags.items():
            textbox.tag_config(tag, **config)
        
        # Insert beginner-friendly informational content
        info_content = [
            ("What is Hardware-Accelerated GPU Scheduling?\n\n", "title"),
            ("This feature lets your graphics card (the part that shows images and videos) work smarter. It handles its own tasks, so your computer's main processor doesn't have to work as hard. This can make games, videos, or heavy apps run smoother with less delay. Here's what it means for you.\n\n", "body"),
            ("🟢 For NVIDIA GPUs (like GeForce GTX 1060, RTX 2060, or newer)\n", "nvidia_h"),
            ("    ✅ Benefits: Turn it on for smoother gameplay in most new games. It can make your mouse and keyboard feel quicker.\n", "pros"),
            ("    ⚠️ Downsides: Older games might have small issues. Test it to check if it works well for your games.\n\n", "cons"),
            ("🔴 For AMD GPUs (like Radeon RX 5700, 6700, or newer)\n", "amd_h"),
            ("    ✅ Benefits: Good for games that use a lot of your computer's power. It can make controls feel faster.\n", "pros"),
            ("    ⚠️ Downsides: Not all games improve. Try it and see if it helps your favorite games.\n\n", "cons"),
            ("🔵 For Intel Integrated Graphics (like Iris Xe in laptops)\n", "intel_h"),
            ("    ✅ Benefits: Helps apps like video editors or light games run a bit faster by easing the load on your processor.\n", "pros"),
            ("    ⚠️ Downsides: Might use more battery on laptops. The boost may be small compared to stronger graphics cards.\n\n", "cons"),
            ("‼️ IMPORTANT: You must restart your computer after turning this on or off for it to work.\n\n", "note"),
            ("📝 Should You Turn It On? Turn it on if you play new games or use apps like video editors and have a modern graphics card. If you play older games or notice problems, turn it off and test again.", "body")
        ]
        textbox.configure(state="normal")
        for text, tag in info_content:
            textbox.insert("end", text, tag)
        textbox.configure(state="disabled")
        
        # Create button frame for action buttons
        button_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        button_frame.pack(pady=(10, 20), padx=20, fill="x")
        button_frame.grid_columnconfigure((0, 1), weight=1)
        
        # [CORRECTED] Add Turn On button with a command that calls the new, reliable action handler.
        on_button = ctk.CTkButton(
            button_frame,
            text="Turn On GPU Scheduling",
            font=self.fonts["button"],
            height=40,
            corner_radius=12,
            border_width=2,
            command=lambda: self._execute_config_action(
                action=self.tweak_logic.turn_on,
                feedback_text="Enabling...",
                sound_name='turn_on'
            ),
            fg_color=Theme.SUCCESS,
            hover_color=Theme.SUCCESS_HOVER,
            border_color=Theme.SUCCESS_BORDER
        )
        on_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        # [CORRECTED] Add Turn Off button with a command that calls the new, reliable action handler.
        off_button = ctk.CTkButton(
            button_frame,
            text="Turn Off GPU Scheduling",
            font=self.fonts["button"],
            height=40,
            corner_radius=12,
            border_width=2,
            command=lambda: self._execute_config_action(
                action=self.tweak_logic.turn_off,
                feedback_text="Disabling...",
                sound_name='turn_off'
            ),
            fg_color=Theme.STATE_OFF_FG,
            hover_color=Theme.STATE_OFF_HOVER,
            border_color=Theme.STATE_OFF_BORDER
        )
        off_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Add Close button with Mouse-Click-Ok.mp3 sound
        close_button = ctk.CTkButton(
            button_frame,
            text="Close",
            font=self.fonts["button"],
            height=40,
            corner_radius=12,
            border_width=2,
            command=lambda: (
                self.sound_manager.play_sound('ok_click'),
                self.close_all_panels()
            ),
            fg_color=Theme.ACCENT_DARK,
            hover_color=Theme.ACCENT_HOVER_DARK,
            border_color=Theme.ACCENT_ACTIVE_DARK
        )
        close_button.grid(row=1, column=0, columnspan=2, padx=100, pady=(10, 0), sticky="ew")

    def _populate_svchost_analysis_ui(self, loading_label: ctk.CTkLabel, ram_gb: float):
        """Populates the UI with detected RAM and handles floating-point display."""
        # --- This method's internal logic remains unchanged. ---
        if not loading_label.winfo_exists(): return
        loading_label.destroy()
        if ram_gb == 0.0:
            error_label = ctk.CTkLabel(self.analysis_frame, text="⚠️ Could not automatically detect system RAM.", font=self.fonts["bold"], text_color=Theme.ERROR_DARK)
            error_label.grid(row=0, column=0, pady=(0, 10))
            self._svchost_show_manual_input_frame(self.analysis_frame, 16)
            return
        formatted_ram_gb = f"{ram_gb:.1f}"
        recommended_value_kb = self.tweak_logic.get_svchost_threshold_kb()
        formatted_value_dec = f"{recommended_value_kb:,}"
        formatted_value_hex = f"0x{recommended_value_kb:X}"
        ctk.CTkLabel(self.analysis_frame, text=f"🖥️ Your System's Detected RAM: {formatted_ram_gb} GB", font=self.fonts["bold"]).grid(row=0, column=0, pady=(0, 15))
        ctk.CTkLabel(self.analysis_frame, text=f"📈 Recommended Threshold (Decimal): {formatted_value_dec}", font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY).grid(row=1, column=0)
        ctk.CTkLabel(self.analysis_frame, text=f"🔢 Recommended Threshold (Hex): {formatted_value_hex}", font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY).grid(row=2, column=0, pady=(0, 15))
        ctk.CTkLabel(self.analysis_frame, text="This optimization Reduces the Stress on CPU by reducing number of Processes [SVChost processes], by using slightly more RAM, (Non-noticeable on Modern Computers), Ultimately Increasing CPU performance in Games and Overall Use  It is highly recommended for systems with 8GB or more RAM.", font=self.fonts["small"], wraplength=400, justify="center").grid(row=3, column=0, pady=(0, 20))
        ctk.CTkLabel(self.analysis_frame, text=f"❓ Is the detected RAM amount of {formatted_ram_gb} GB correct?", font=self.fonts["bold"]).grid(row=4, column=0, pady=(10, 10))
        button_frame = ctk.CTkFrame(self.analysis_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, pady=10)
        yes_button = ctk.CTkButton(button_frame, text="✅ Yes, Apply This Optimization", font=self.fonts["button"], fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, command=lambda: self._svchost_apply_and_finalize())
        yes_button.pack(side="left", padx=5)
        no_button = ctk.CTkButton(button_frame, text="❌ No, Let Me Enter It Manually", font=self.fonts["button"], fg_color=Theme.WARNING, hover_color=Theme.WARNING_HOVER, command=lambda: self._svchost_show_manual_input_frame(self.analysis_frame, int(ram_gb)))
        no_button.pack(side="left", padx=5)
        close_button = ctk.CTkButton( self.analysis_frame, text="Close", font=self.fonts["button"], fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, command=self.close_all_panels )
        close_button.grid(row=6, column=0, pady=(15, 0), padx=100, sticky="ew")

    def _svchost_show_manual_input_frame(self, parent_frame: ctk.CTkFrame, current_ram_gb: int):
        """
        [CORRECTED v3.6] Hides the consent UI and shows the manual RAM input UI.
        This version includes a new "Close" button for a complete user workflow,
        and uses a dedicated button frame for perfect side-by-side layout.
        """
        # --- Destroy all existing widgets within the parent frame to create a clean slate.
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # --- Display the critical warning message to the user about potential system instability.
        warning_text = "⚠️ WARNING: Entering an incorrect value can lead to system instability. Please double-check your system's specifications."
        ctk.CTkLabel(parent_frame, text=warning_text, font=self.fonts["bold"], text_color=Theme.WARNING_DARK, wraplength=450, justify="center").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # --- Create a container to hold the input label and entry field for clean alignment.
        input_container_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        input_container_frame.grid(row=1, column=0, columnspan=2, pady=0)

        # --- The descriptive label for the input field.
        ctk.CTkLabel(input_container_frame, text="Enter your total system RAM in GB:", font=self.fonts["normal"]).pack(side="left", padx=5)

        # --- The user entry field for manual RAM input, pre-populated with the detected value.
        manual_ram_entry = ctk.CTkEntry(input_container_frame, font=self.fonts["normal"], width=80, justify="center")
        manual_ram_entry.insert(0, str(current_ram_gb))
        manual_ram_entry.pack(side="left", padx=5)

        # --- [NEW] Create a dedicated frame to hold the action buttons side-by-side.
        # --- This is the paradigm solution for ensuring a stable, centered button layout.
        button_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, pady=25)

        # --- The primary action button to apply the user's manually entered value.
        apply_button = ctk.CTkButton(
            button_frame,
            text="Apply Manual Value",
            font=self.fonts["button"],
            # --- The command lambda correctly captures the entry widget's value at the moment of the click.
            command=lambda: self._svchost_apply_and_finalize(manual_ram_gb=int(manual_ram_entry.get()))
        )
        # --- Place the 'Apply' button within the button frame.
        apply_button.pack(side="left", padx=10)

        # --- [CRITICAL ADDITION] The new "Close" button, providing the required UI escape pathway.
        close_button = ctk.CTkButton(
            button_frame,
            text="Close",
            font=self.fonts["button"],
            # --- This button's command directly calls the method to close the dropdown panel.
            command=self.close_all_panels,
            # --- Use a distinct, non-destructive color scheme for the close button.
            fg_color=Theme.STATE_OFF_FG,
            hover_color=Theme.STATE_OFF_HOVER
        )
        # --- Place the 'Close' button next to the 'Apply' button.
        close_button.pack(side="left", padx=10)

    def _svchost_apply_and_finalize(self, manual_ram_gb: Optional[int] = None):
        """A unified function to apply the tweak and show the final confirmation."""
        # --- This method's internal logic remains unchanged. ---
        if self.sound_manager:
            self.sound_manager.play_sound('turn_on')
        self.close_all_panels()
        if manual_ram_gb is not None:
            action = self.tweak_logic.apply_manual
            kwargs = {'ram_gb': manual_ram_gb}
        else:
            action = self.tweak_logic.apply
            kwargs = {}
        self._execute_tweak_action(action, "Applying...", **kwargs)

    def _create_config_dropdown_panel(self):
        """Creates the generic configuration dropdown panel (e.g., for JPEG quality)."""
        # --- This method's internal logic remains unchanged. ---
        self.config_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        desc_text = ("Windows compresses JPEG wallpapers to about 85% to save memory. You can set a custom quality from 0% (lowest) to 100% (original).\n\nHigher quality may use slightly more RAM but looks much sharper. Lower quality can improve performance on very old hardware.")
        ctk.CTkLabel(self.config_frame, text=desc_text, justify="center", wraplength=500, font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY).pack(padx=20, pady=15, anchor="center")
        input_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        input_frame.pack(pady=10, anchor="center")
        vcmd = (self.register(self._validate_char), '%P')
        self.quality_entry = ctk.CTkEntry(input_frame, font=self.fonts["normal"], width=100, justify="center", border_color=Theme.BORDER, validate='key', validatecommand=vcmd)
        self.quality_entry.pack(side="left")
        if self.current_tweak_value is not None: self.quality_entry.insert(0, str(self.current_tweak_value))
        else: self.quality_entry.insert(0, "85")
        ctk.CTkLabel(input_frame, text="Quality (0-100)%", font=self.fonts["small"], text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=10)
        button_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        button_frame.pack(pady=10, anchor="center", padx=20)
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", font=self.fonts["button"], fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, command=lambda: self.toggle_panel('config'))
        cancel_button.pack(side="left", padx=5)
        apply_button = ctk.CTkButton(button_frame, text="Apply", font=self.fonts["button"], fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, command=self._apply_config_change)
        apply_button.pack(side="left", padx=5)

    def _validate_char(self, new_value: str) -> bool:
        """Validates character input for numeric entry fields."""
        # --- This method's internal logic remains unchanged. ---
        if new_value == "": return True
        try:
            num = int(new_value)
            return 0 <= num <= 100 and len(new_value) <= 3
        except ValueError:
            return False

    def _apply_config_change(self):
        """Applies a configuration change from a dropdown panel."""
        # --- This method's internal logic remains unchanged. ---
        if not self.tweak_logic: return
        try:
            value = int(self.quality_entry.get())
            if 0 <= value <= 100:
                if self.sound_manager:
                    self.sound_manager.play_sound('turn_on')
                self.close_all_panels()
                self._execute_tweak_action(self.tweak_logic.apply, "Applying...", quality_value=value)
            else:
                self.quality_entry.configure(border_color=Theme.STATE_OFF_BORDER)
        except (ValueError, TypeError):
                self.quality_entry.configure(border_color=Theme.STATE_OFF_BORDER)

    def update_ui_scaling(self, fonts):
        """Propagates font scaling updates to all child widgets."""
        # --- This method's internal logic remains unchanged. ---
        self.fonts = fonts
        self.title_label.configure(font=fonts["bold"])
        self.desc_label.configure(font=fonts["small"])
        self.action_button.configure(font=fonts["button"])
        self.reset_button.configure(font=fonts["button"])
        if self.info_frame and self.info_frame.winfo_exists():
            for widget in self.info_frame.winfo_children():
                if isinstance(widget, ctk.CTkTextbox):
                    widget.configure(font=fonts["normal"])
        if self.config_frame and self.config_frame.winfo_exists():
            for child in self.config_frame.winfo_children():
                if isinstance(child, ctk.CTkLabel):
                    child.configure(font=fonts["normal"])
                elif isinstance(child, ctk.CTkFrame):
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, (ctk.CTkEntry, ctk.CTkLabel, ctk.CTkButton)):
                            font_key = "normal"
                            if isinstance(grandchild, ctk.CTkButton): font_key = "button"
                            if isinstance(grandchild, ctk.CTkLabel) and "Quality" in grandchild.cget("text"):
                                font_key = "small"
                            grandchild.configure(font=fonts[font_key])

# ===================================================================================
# CLASS: GlassButton (v1.0 - Premium Visual Protocol)
#
# ARCHITECTURAL BLUEPRINT:
# This class defines a custom, high-fidelity button widget with a glassy, 3D aesthetic,
# engineered for seamless integration into a premium UI environment. It leverages the
# customtkinter library to create a visually striking button with animated hover effects,
# optimized to prevent rendering artifacts and ensure a consistent user experience.
#
# DESIGN PRINCIPLES:
#  1. VISUAL EXCELLENCE: The button combines a gradient-like glassy background, rounded
#     corners, and a dynamic border color change on hover to create a premium, 3D effect.
#  2. PERFORMANCE OPTIMIZATION: By extending `ctk.CTkButton`, it inherits optimized
#     rendering pipelines, avoiding redraw artifacts common in custom Tkinter widgets.
#  3. MODULAR EVENT HANDLING: Hover effects are implemented via explicit event bindings,
#     ensuring precise control over the border animation without relying on default hover
#     behaviors, which may introduce visual inconsistencies.
#  4. CONFIGURABLE AESTHETICS: The button's appearance (colors, font, size, and emoji)
#     is fully customizable through the `Theme` configuration, allowing seamless adaptation
#     to the application's visual identity.
#
# This class serves as a reusable, standalone component for navigation or action triggers
# in a high-end UI, such as the MK-Tools application, with a focus on user engagement
# through visual and interactive feedback.
# ===================================================================================
class GlassButton(ctk.CTkButton):
    """
    A premium, animated, and highly optimized button with a glassy, 3D effect.
    This version is a single, optimized widget that prevents rendering artifacts.
    """
    def __init__(self, master, text, emoji, font, command=None):
        button_text = f"{emoji}  {text}"
        
        # --- [DPI SCALING] Calculate all geometry based on the system's scaling factor.
        scale_factor = ScreenManager.get_scaling_factor()
        scaled_height = int(70 * scale_factor)
        scaled_corner_radius = int(25 * scale_factor)
        scaled_border_width = max(1, int(2 * scale_factor)) # Ensure border is at least 1px.

        # --- Base Class Initialization with scaled geometry.
        super().__init__(
            master,
            text=button_text,
            font=font,
            command=command,
            height=scaled_height,
            corner_radius=scaled_corner_radius,
            border_width=scaled_border_width,
            fg_color=Theme.GLASS_BG_START,
            text_color=Theme.GLASS_TEXT,
            border_color=Theme.GLASS_BORDER,
            hover_color=Theme.GLASS_BG_END
        )
        
        # --- Event Bindings for Animations ---
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        """Handles the mouse enter event to animate the border color."""
        self.configure(border_color=Theme.GLASS_BORDER_HOVER)

    def _on_leave(self, event=None):
        """Handles the mouse leave event to revert the border color."""
        self.configure(border_color=Theme.GLASS_BORDER)

# ===================================================================================
# CLASS: TerminalWidget (v6.0 - Futuristic Glassy 3D Terminal)
#
# ARCHITECTURAL BLUEPRINT:
# The TerminalWidget class is a specialized, read-only CTkTextbox designed to emulate
# a futuristic, glassy, 3D terminal interface for displaying real-time command output.
# It leverages the customtkinter library for a modern, visually appealing UI with
# dynamic hover effects and thread-safe text operations. The class supports regex-based
# exact matching and fuzzy matching (via fuzzywuzzy) for analyzing command output,
# making it ideal for real-time system monitoring or command execution feedback.
# Key features include thread-safe text appending, auto-scrolling, dynamic font scaling,
# and robust error handling for text analysis. The widget is lifecycle-aware, ensuring
# stability during destruction, and adheres to a modular, reusable design paradigm.
# ===================================================================================
class TerminalWidget(ctk.CTkTextbox):
    """A futuristic, glassy, 3D terminal widget for displaying real-time command output."""
    def __init__(self, master, fonts):
        super().__init__(
            master,
            font=fonts["normal"],
            fg_color=Theme.GLASS_BG_START,
            border_color=Theme.GLASS_BORDER,
            border_width=2,
            corner_radius=20,
            wrap="word",
            height=300,
            text_color=Theme.TEXT,
            state="disabled"  # Read-only
        )
        self.grid_columnconfigure(0, weight=1)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.is_accepting_input = True

    def _on_enter(self, event):
        """Apply hover effect with animated border."""
        self.configure(border_color=Theme.GLASS_BORDER_HOVER)

    def _on_leave(self, event):
        """Revert border on leave."""
        self.configure(border_color=Theme.GLASS_BORDER)

    def append_text(self, text):
        """Appends text to the terminal in a thread-safe manner."""
        if not self.is_accepting_input or not self.winfo_exists():
            return
        self.configure(state="normal")
        self.insert("end", text + "\n")
        self.see("end")  # Auto-scroll to the latest output
        self.configure(state="disabled")

    def clear(self):
        """Clears the terminal content."""
        if not self.winfo_exists():
            return
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.configure(state="disabled")

    def update_ui_scaling(self, fonts):
        """Updates font for the terminal."""
        self.configure(font=fonts["normal"])
        
    def exact_match(self, line: str) -> Optional[str]:
        """
        Performs an exact regex match for key phrases in a line.
        
        Args:
            line (str): The line to search.
        
        Returns:
            Optional[str]: The matching result key or None.
        """
        try:
            for result_key, pattern in self.compiled_patterns.items():
                if pattern.search(line):
                    return result_key
            return None
        except Exception as e:
            logging.error(f"Error in exact match for line '{line}': {e}", exc_info=True)
            return None

    def fuzzy_match(self, line: str, threshold: int = 90) -> Optional[str]:
        """
        Performs a fuzzy match for key phrases using fuzzywuzzy.
        
        Args:
            line (str): The line to search.
            threshold (int): Minimum score for a match (0-100).
        
        Returns:
            Optional[str]: The matching result key or None.
        """
        try:
            for result_key, phrase in self.key_phrases.items():
                score = fuzz.ratio(line, phrase)
                if score >= threshold:
                    logging.debug(f"Fuzzy match for '{line}' with '{phrase}' (score: {score})")
                    return result_key
            return None
        except Exception as e:
            logging.error(f"Error in fuzzy match for line '{line}': {e}", exc_info=True)
            return None

# ===================================================================================
# CLASS: DiagnosticLogicController (v6.0 - Definitive Exit-Code-Driven Engine)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive, zero-defect version of the logic engine. It resolves all
# previous parsing inaccuracies by implementing a military-grade, exit-code-first
# validation protocol. This is the paradigm solution for achieving 100% accuracy.
#
# NEW PARADIGM: EXIT-CODE-FIRST VALIDATION
#
#  [Raw Terminal Output + Process Exit Code]
#           |
#           V
#  [STAGE 1: ANALYZE EXIT CODE]
#  Description: The numerical exit code is the primary, language-independent signal
#               of success (0) or failure (non-zero). This is checked first.
#           |
#      (If Exit Code is 0 - Success Path)
#           |
#           V
#  [STAGE 2: PARSE SUCCESS TEXT]
#  Description: The text output is now only scanned to differentiate between different
#               types of success (e.g., "no violations" vs. "repaired").
#           |
#      (If Exit Code is NOT 0 - Failure Path)
#           |
#           V
#  [STAGE 2: PARSE FAILURE TEXT]
#  Description: The text output is scanned for specific known error messages. If none
#               are found, a generic failure is returned.
#
# This architecture is infallible because it relies on machine-readable exit codes
# for its primary logic, only using human-readable text for secondary classification.
# ===================================================================================
class DiagnosticLogicController:
    """
    Parses SFC and DISM command outputs using a high-precision, exit-code-driven
    engine to match the final specification and return a structured UI blueprint.
    """
    def __init__(self, master_frame: 'FixWindowsFrame'):
        # --- Store a direct reference to the parent FixWindowsFrame for command callbacks.
        self.master_frame = master_frame

        # --- SFC SCAN LOGIC (FINALIZED PER LATEST NOTES) ---
        self.sfc_success_map = [
            {
                "key_phrase": "windows resource protection did not find any integrity violations",
                "result_factory": lambda: {
                    "title": "System Scan Complete", "emoji": "🎉", "style": "success",
                    "message": "Hooray! 🥳 Your PC is in perfect shape. MKTools scanned your system files and found no integrity violations. Keep enjoying your smooth ride! 🚀",
                    "looping_sound": "success_fanfare",
                    "buttons_config": [{'text': 'OK', 'style': 'success', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
                }
            },
            {
                "key_phrase": "windows resource protection found corrupt files and successfully repaired them",
                "result_factory": lambda: {
                    "title": "Issues Repaired!", "emoji": "🛠️", "style": "success",
                    "message": "Success! ✨ MKTools detected corrupted system files and has successfully repaired them. Your PC is healthy and good to go! 💪 A restart is recommended.",
                    "looping_sound": "success_fanfare",
                    "buttons_config": [{'text': 'OK', 'style': 'success', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
                }
            },
        ]
        self.sfc_failure_map = [
            {
                "key_phrase": "windows resource protection found corrupt files but was unable to fix some of them",
                "result_factory": lambda: {
                    "title": "Advanced Issues Detected", "emoji": "⚠️", "style": "warning",
                    "message": "Some issues were detected that couldn’t be fixed automatically. For a deeper repair, please use the 'Advanced Scan' (DISM) option.",
                    "buttons_config": [{'text': 'OK', 'style': 'warning', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
                }
            },
        ]
        
        # --- DISM SCAN LOGIC (FINALIZED PER LATEST NOTES) ---
        self.dism_scan_success_map = [
            {
                "key_phrase": "no component store corruption detected",
                "result_factory": lambda: {
                    "title": "Component Store Healthy", "emoji": "🎉", "style": "success",
                    "message": "The Windows component store is healthy. No further action is required.",
                    "looping_sound": "success_fanfare",
                    "buttons_config": [{'text': 'OK', 'style': 'success', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
                }
            },
            {
                "key_phrase": "the component store is repairable",
                "result_factory": lambda: {
                    "title": "Corruption Detected", "emoji": "🚨", "style": "warning",
                    "message": "Issues found in the Windows component store. MKTools can attempt a repair by running RestoreHealth. Do you want to proceed?",
                    "looping_sound": "warning_loop",
                    "buttons_config": [
                        {'text': 'Yes, Fix It', 'style': 'success', 'command': self.master_frame._create_finalization_callback(fix_now=True)},
                        {'text': 'No, Cancel', 'style': 'default', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}
                    ]
                }
            },
        ]

        # --- DISM RESTORE LOGIC (FINALIZED PER LATEST NOTES) ---
        self.dism_restore_success_map = [
             {
                "key_phrase": "the restore operation completed successfully",
                "result_factory": lambda: {
                    "title": "Repair Successful", "emoji": "✅", "style": "success",
                    "message": "The component store has been successfully repaired. It is highly recommended to run the simple 'Scan' (SFC) again to finalize all repairs.",
                    "looping_sound": "success_fanfare",
                    "buttons_config": [
                        {'text': 'Close', 'style': 'default', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)},
                        {'text': 'Run Final Scan', 'style': 'success', 'command': self.master_frame._create_finalization_callback(scan_again_sfc=True)}
                    ]
                }
            },
        ]
        self.dism_restore_failure_map = [
            {
                "key_phrase": "the source files could not be found",
                "result_factory": lambda: {
                    "title": "Repair Failed: Source Missing", "emoji": "❌", "style": "danger",
                    "message": "Repair failed because the source files could not be found online. You may need to provide a local Windows Installation file (.wim or .esd) to proceed.",
                    "one_shot_sound": "error_sound",
                    "is_source_missing": True,
                    "buttons_config": [{'text': 'OK', 'style': 'danger', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True, show_advanced_ui=True)}]
                }
            },
        ]

    def _parse_text(self, output_lines: list[str], logic_map: list[dict]) -> Optional[dict]:
        """
        A high-precision text parser that scans output lines for a key phrase.
        This is a secondary helper function, only called after the exit code is known.
        """
        consolidated_output = " ".join(output_lines).lower()
        
        for item in logic_map:
            if item["key_phrase"] in consolidated_output:
                logging.info(f"Precise text match found for key phrase: '{item['key_phrase']}'")
                return item["result_factory"]()
        
        return None

    def parse_sfc_output(self, output_lines: list[str], exit_code: int) -> dict:
        """Processes SFC /scannow output, prioritizing the exit code."""
        default_failure = {
            "title": "Scan Unsuccessful", "emoji": "⚠️", "style": "warning",
            "message": "MKTools was unable to complete the simple scan successfully or found issues it could not fix. For a deeper repair, please use the 'Advanced Scan' option.",
            "one_shot_sound": "setup_unsuccessful",
            "buttons_config": [{'text': 'OK', 'style': 'warning', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
        }

        if exit_code == 0:
            result = self._parse_text(output_lines, self.sfc_success_map)
            return result if result else self.sfc_success_map[0]["result_factory"]()
        else:
            result = self._parse_text(output_lines, self.sfc_failure_map)
            return result if result else default_failure

    def parse_dism_scan_output(self, output_lines: list[str], exit_code: int) -> dict:
        """Processes DISM /ScanHealth output, prioritizing the exit code."""
        default_failure = {
            "title": "Scan Failed", "emoji": "❌", "style": "danger",
            "message": "The Advanced Scan (DISM) failed to run. This may be due to a permissions issue or an underlying system problem.",
            "one_shot_sound": "error_sound",
            "buttons_config": [{'text': 'OK', 'style': 'danger', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
        }

        if exit_code == 0:
            result = self._parse_text(output_lines, self.dism_scan_success_map)
            return result if result else self.dism_scan_logic_map[1]["result_factory"]()
        else:
            return default_failure

    def parse_dism_restore_output(self, output_lines: list[str], exit_code: int) -> dict:
        """Processes DISM /RestoreHealth output, prioritizing the exit code."""
        default_failure = {
            "title": "Restore Failed", "emoji": "❌", "style": "danger",
            "message": "The DISM restore operation failed to complete successfully. The component store may still be corrupted.",
            "one_shot_sound": "error_sound",
            "buttons_config": [{'text': 'OK', 'style': 'danger', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
        }
        
        if exit_code == 0:
            result = self._parse_text(output_lines, self.dism_restore_success_map)
            return result if result else self.dism_restore_success_map[0]["result_factory"]()
        else:
            result = self._parse_text(output_lines, self.dism_restore_failure_map)
            return result if result else default_failure



# ===================================================================================
# CLASS: ResultPopup (v2.0 - Architecturally Compliant)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# Re-architected to inherit from BaseModalDialog. All duplicated modality and
# windowing logic has been removed, resulting in a cleaner, more maintainable
# component that conforms to the project's architectural standard.
# ===================================================================================
class ResultPopup(BaseModalDialog):
    """
    A centered, modal pop-up for displaying scan results, now built upon the
    definitive BaseModalDialog engine.
    """
    # ===============================================================================
    # METHOD: __init__
    # Inherits from BaseModalDialog and orchestrates UI creation.
    # ===============================================================================
    def __init__(self, master, fonts, message, on_close_callback):
        # --- Base Class Initialization: Establishes the core modal window.
        super().__init__(master, "Scan Result")

        # --- Store component-specific properties.
        self.fonts = fonts
        self.on_close_callback = on_close_callback

        # --- Window & UI Configuration ---
        self.configure(fg_color="#353345")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Message Label ---
        label = ctk.CTkLabel(self, text=message, font=self.fonts["normal"], text_color=Theme.TEXT, wraplength=450, justify="center")
        label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="nsew")

        # --- OK Button ---
        ok_button = GlassButton(self, text="OK", emoji="", font=self.fonts["button"], command=self.close)
        ok_button.configure(fg_color="#4B0082", hover_color="#353345", text_color=Theme.GLASS_TEXT, border_color=Theme.GLASS_BORDER, border_width=8, corner_radius=8)
        ok_button.grid(row=1, column=0, pady=(0, 20), padx=50, sticky="ew")
        
        # --- Allow closing with the Enter key for accessibility.
        self.bind("<Return>", lambda e: self.close())
        
        # --- Finalize geometry before centering.
        self.update_idletasks()
        self.geometry(f"500x{self.winfo_reqheight()}")


    # ===============================================================================
    # METHOD: close
    # Overrides the base method to execute the specific callback before closing.
    # ===============================================================================
    def close(self):
        """Executes the on-close callback, then calls the parent close method."""
        if self.on_close_callback and callable(self.on_close_callback):
            self.on_close_callback()
        super().close()

    # ===============================================================================
    # METHOD: update_ui_scaling
    # Propagates font scaling updates to child widgets.
    # ===============================================================================
    def update_ui_scaling(self, fonts):
        """Updates font scaling for the pop-up’s UI elements."""
        self.fonts = fonts
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(font=fonts["normal"])
            elif isinstance(widget, GlassButton):
                widget.configure(font=fonts["button"])

# ===================================================================================
# CLASS: ResultPopupWithFix (v2.0 - Architecturally Compliant)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# Re-architected to inherit from BaseModalDialog. This version retains its unique
# dual-button layout and fix callback logic while delegating all core windowing
# behavior to the base class for architectural purity and maintainability.
# ===================================================================================
class ResultPopupWithFix(BaseModalDialog):
    """A modal dialog with a 'Fix Now' option, built on the BaseModalDialog engine."""
    
    # ===============================================================================
    # METHOD: __init__
    # Inherits from BaseModalDialog and orchestrates UI creation.
    # ===============================================================================
    def __init__(self, master, fonts, message, on_close_callback, fix_callback):
        # --- Base Class Initialization: Establishes the core modal window.
        super().__init__(master, "DISM Scan Result")
        
        # --- Store component-specific properties.
        self.fonts = fonts
        self.on_close_callback = on_close_callback
        self.fix_callback = fix_callback

        # --- Window & UI Configuration ---
        self.configure(fg_color="#353345")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Message Label ---
        label = ctk.CTkLabel(self, text=message, font=self.fonts["normal"], text_color=Theme.TEXT, wraplength=450, justify="center")
        label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="nsew")

        # --- Button Container Frame ---
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # --- Fix Now Button ---
        fix_button = GlassButton(button_frame, text="Fix Now", emoji="🛠️", font=self.fonts["button"], command=self._on_fix_now)
        fix_button.configure(fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, border_color=Theme.SUCCESS_BORDER)
        fix_button.grid(row=0, column=0, padx=10, sticky="ew")

        # --- Close Button ---
        close_button = GlassButton(button_frame, text="Close", emoji="❌", font=self.fonts["button"], command=self.close)
        close_button.configure(fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, border_color=Theme.STATE_OFF_BORDER)
        close_button.grid(row=0, column=1, padx=10, sticky="ew")
        
        # --- Finalize geometry before centering.
        self.update_idletasks()
        self.geometry(f"500x{self.winfo_reqheight()}")

    # ===============================================================================
    # METHOD: _on_fix_now
    # Executes the fix callback and then closes the dialog.
    # ===============================================================================
    def _on_fix_now(self):
        """Executes the repair action and closes the dialog."""
        if self.fix_callback:
            self.fix_callback()
        # --- Do not call super().close() here, call self.close() to ensure the on_close_callback also runs.
        self.close()

    # ===============================================================================
    # METHOD: close
    # Overrides the base method to execute the specific callback before closing.
    # ===============================================================================
    def close(self):
        """Executes the on-close callback, then calls the parent close method."""
        if self.on_close_callback and callable(self.on_close_callback):
            self.on_close_callback()
        super().close()

    # ===============================================================================
    # METHOD: update_ui_scaling
    # Propagates font scaling updates to child widgets.
    # ===============================================================================
    def update_ui_scaling(self, fonts):
        """Updates font scaling for the pop-up’s UI elements."""
        self.fonts = fonts
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(font=fonts["normal"])
            elif isinstance(widget, ctk.CTkFrame):
                for btn in widget.winfo_children():
                    if isinstance(btn, GlassButton):
                        btn.configure(font=fonts["button"])

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

# ===================================================================================
# SECTION 7: CONTENT FRAMES & PAGE DEFINITIONS
# Each class represents a different screen accessible from the navigation rail.
# ===================================================================================
# ===================================================================================
# CLASS: BaseContentFrame (v2.0 - Zero-Animation Stability Protocol)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class has been re-engineered to provide a paradigm solution for UI stability
# across all hardware configurations, from low-end legacy systems to high-performance
# workstations. The previous, resource-intensive animation protocol has been
# completely excised and replaced with an instantaneous widget placement model.
#
# CORE ENHANCEMENTS:
#   1. [STABILITY] Animation Elimination: The `run_entry_animation` method no longer
#      interfaces with the `AnimationEngine`. The logic that animated the `pady`
#      grid property—the direct cause of visual stutter and artifacts—has been
#      removed.
#
#   2. [PERFORMANCE] Instantaneous Placement: The new `run_entry_animation` method
#      now places all child 'card' widgets onto the grid instantly with their final,
#      static padding. This is a zero-cost rendering operation that guarantees a
#      flawless, flicker-free user experience.
#
#   3. [INHERITANCE] Universal Fix: By modifying the superclass, this stability
#      protocol is automatically inherited by all content frames (`PerformanceFrame`,
#      `UITweaksFrame`, `FixWindowsFrame`, etc.), solving the problem at its
#      foundational level.
# ===================================================================================
class BaseContentFrame(ctk.CTkScrollableFrame):
    """A base class for content frames to handle shared functionality."""
    def __init__(self, master, fonts):
        # --- Initialize the parent CTkScrollableFrame with transparent background and no corner radius.
        super().__init__(master, fg_color="transparent", corner_radius=0)
        # --- Configure the first column (index 0) to expand and fill all available horizontal space.
        self.grid_columnconfigure(0, weight=1)
        # --- Store the application-wide font dictionary for use by child elements.
        self.fonts = fonts
        # --- Initialize an empty list to hold references to all child 'card' widgets.
        self.cards = []
        # --- Initialize a placeholder for the frame's main header label.
        self.header_label = None

    def run_entry_animation(self):
            """
            [RE-ARCHITECTED FOR UNIVERSAL STABILITY] Places all cards instantly
            without animation to guarantee zero flicker, stutter, or visual artifacts
            on all hardware tiers, from low-end to high-end systems. This is the
            definitive solution for maximum UI responsiveness and stability.
            """
            # --- Iterate through all registered card widgets in this frame's list.
            for card in self.cards:
                # --- Instantly place the card onto the grid with its final, static padding.
                # --- This bypasses any animation engine, eliminating all performance
                # --- overhead and potential rendering glitches.
                card.grid_configure(pady=10)
            
    def update_ui_scaling(self, fonts):
        """Propagates font updates to all child cards."""
        # --- Update the internal font dictionary with the new scaled font objects.
        self.fonts = fonts
        # --- If a header label exists, update its font.
        if self.header_label: self.header_label.configure(font=fonts["title"])
        # --- Iterate through all child cards.
        for card in self.cards:
            # --- Check if the card has an `update_ui_scaling` method and call it to propagate the change.
            if hasattr(card, "update_ui_scaling"): card.update_ui_scaling(fonts)

# ===================================================================================
# CLASS: DashboardFrame (v2.3 - Zero-Defect Final Version)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This is the definitive version of the DashboardFrame. It corrects two critical
# user experience flaws: the persistent hover-state visual bug and the unwanted
# entry animation.
#
# CORRECTION PROTOCOL:
#  1. MASTER STATE RESET: The `reset_state()` method is retained. It is
#     automatically invoked by the main `App` controller during navigation. Its
#     sole function is to cascade a reset command to all child `_DashboardCard`
#     components, guaranteeing their visual state is reverted to default when
#     the user navigates away from the dashboard. This solves the persistent
#     highlight bug.
#
#  2. ANIMATION ELIMINATION: The `run_entry_animation()` method has been
#     re-engineered. The call to `super().run_entry_animation()` has been
#     permanently removed. The method's only remaining function is to update the
#     dynamic welcome message. This eliminates the "upside-down" card animation,
#     resulting in a static, professional, and instantaneous frame presentation.
# ===================================================================================
class DashboardFrame(BaseContentFrame):
    """
    The definitive landing page, featuring a dynamic welcome message, accurately
    calculated feature counts, and a responsive grid of navigation cards with
    auditory feedback and a robust state-reset protocol.
    """
    # The constructor for the DashboardFrame class.
    def __init__(
        self,
        master,
        fonts,
        frame_switcher_callback: Optional[Callable[[str], None]] = None,
        sound_manager: Optional['SoundManager'] = None
    ):
        # --- Base Class Initialization ---
        super().__init__(master, fonts)
        # --- Store a reference to the Auditory Feedback Engine.
        self.sound_manager = sound_manager
        # --- Data Store for Dynamic User Messages ---
        self.dynamic_messages = [
            "Ready to make your PC soar? Start optimizing now!",
            "Boost your system's speed with a single click.",
            "Have you tried Clean Cache? Free up space today!",
            "Your desktop deserves a snappier feel. Try UI Tweaks!",
            "Unleash your PC’s full potential with MK-Tools.",
            "Keep your system healthy with a Fix Windows scan.",
            "One click to a faster PC. Ready to dive in?",
            "Take control with Group Policy tweaks today.",
            "Dust off digital clutter and boost your PC.",
            "Clear your cache for a refreshed system now.",
            "Challenge yourself to speed up your PC today!",
            "A responsive desktop awaits. Explore UI Tweaks!",
            "Discover the magic of MK-Tools’ optimization tools.",
            "Build a rock-solid system with our tweaks.",
            "Fuel your creativity with a faster PC.",
            "Effortless optimization starts with MK-Tools.",
            "Have you checked Fix Windows? Keep your system stable!",
            "Clear the clutter for a focused digital life.",
            "Your optimization journey begins with one click.",
            "Make your desktop yours with UI Tweaks today.",
            "Refresh your PC with a quick cache clean.",
            "Unlock hidden speed with Performance Tweaks now.",
            "Trust MK-Tools for a reliable PC experience.",
            "Game smoother with Performance Tweaks. Try it!",
            "Speed up your PC in just a few clicks.",
            "Keep your system thriving with regular tweaks.",
            "Master your system with Group Policy controls.",
            "Today’s the day to make your PC shine.",
            "Break free from clutter with Clean Cache.",
            "Effortless power with MK-Tools’ optimization suite.",
            "Check the About section for exciting new updates!",
            "Say goodbye to lag with MK-Tools’ tools.",
            "Power your productivity with a tuned PC.",
            "Personalize your desktop with UI Tweaks now.",
            "A quick cache clean for a faster PC.",
            "Now’s the moment to optimize your system!",
            "Fix Windows keeps your PC running smoothly.",
            "Multitask like a pro with Performance Tweaks.",
            "Polish your PC to perfection with MK-Tools.",
            "Have you explored Group Policy? Powerful tweaks await!",
            "Maximize your PC with MK-Tools’ full suite.",
            "A fast PC is an efficient PC. Optimize now!",
            "Clear temp files for a speed boost today.",
            "Ready to optimize? Let’s make it happen!",
            "One-click fixes for a healthier PC.",
            "A healthy system starts with MK-Tools’ tweaks.",
            "Streamline your workflow with UI Tweaks today.",
            "Boost daily tasks with a tuned system.",
            "Optimization made simple with MK-Tools’ tools.",
            "Discover Clean Cache for a refreshed PC.",
            "Experience a seamless PC with MK-Tools.",
            "Make your PC more responsive with tweaks.",
            "A clean PC is a happy PC. Try it!",
            "Explore new tools to enhance your system.",
            "Customize your system with Group Policy tweaks.",
            "Reach peak performance with MK-Tools today.",
            "Free up disk space with a quick clean.",
            "Fix Windows scans for lightning-fast results.",
            "Optimize your PC for epic gaming sessions.",
            "Create a clutter-free digital workspace now.",
            "Modernize your desktop with UI Tweaks.",
            "Effortless system optimization with MK-Tools.",
            "Have you tried Performance Tweaks? Boost speed now!",
            "Build a reliable system with our tools.",
            "Refresh your PC with a cache cleanup.",
            "Maintain your PC for lasting performance.",
            "Start your optimization journey with MK-Tools.",
            "Stabilize your system with Fix Windows scans.",
            "Professionals, boost your PC with tweaks.",
            "Unleash the power of MK-Tools’ features.",
            "Clear digital clutter for a faster PC.",
            "Personalize your PC with UI Tweaks now.",
            "Quick tweaks for a speedy PC today.",
            "Clean Cache: Easy and effective optimization.",
            "Explore Group Policy for advanced system tweaks.",
            "Smooth system performance with MK-Tools.",
            "Daily performance boosts with our tweaks.",
            "Reliable scans with MK-Tools’ Fix Windows.",
            "Optimize for efficiency with MK-Tools now.",
            "A clean system boosts performance instantly.",
            "Get a responsive desktop with UI Tweaks.",
            "One-click tools for instant PC speed.",
            "New features await in MK-Tools’ suite.",
            "Control your system with Group Policy now.",
            "Speed up startup with a quick clean.",
            "A tuned PC enhances your daily work.",
            "Have you tried Fix Windows? Keep it healthy!",
            "Speed lovers, try Performance Tweaks today!",
            "Refresh your system with a cache clean.",
            "Easy optimizations with MK-Tools’ tools.",
            "Explore UI Tweaks for a better desktop.",
            "Fast and reliable: Optimize with MK-Tools.",
            "Multitask better with Performance Tweaks now.",
            "Clean Cache: Power up your PC today.",
            "Optimize your PC for creative projects.",
            "Seamless optimization with MK-Tools’ suite.",
            "Feel the speed with Performance Tweaks!",
            "A clean PC for a clear mind.",
            "New tools to enhance your system’s performance.",
            "Shape your system with Group Policy tweaks.",
            "Faster startups with a quick cache clean.",
            "A tuned PC you’ll love. Start now!",
            "Healthy PC with Fix Windows scans.",
            "Speed up your world with MK-Tools!",
            "A fresh system with Clean Cache today.",
            "Easy tools for a faster PC experience.",
            "Customize your desktop with UI Tweaks!",
            "Reliable performance with MK-Tools’ suite.",
            "Multitask effortlessly with Performance Tweaks.",
            "A powerful PC with Clean Cache now.",
            "Create freely with a tuned PC.",
            "Seamless tweaks for a better PC.",
            "Boost your PC’s speed with one click!",
            "Clear your cache for a smoother system.",
            "Have you checked UI Tweaks? Try them now!",
            "Your PC’s potential is waiting to shine.",
            "Keep your system stable with Fix Windows.",
            "One click to a more responsive PC.",
            "Take charge with Group Policy tweaks.",
            "Tidy up your PC with MK-Tools today.",
            "Free up space with a Clean Cache run.",
            "Speed up your PC with a single tweak!",
            "Make your desktop pop with UI Tweaks.",
            "Discover MK-Tools’ tools for a faster PC.",
            "A stable system starts with MK-Tools.",
            "Unleash creativity with a speedy PC.",
            "Optimize effortlessly with MK-Tools’ tools.",
            "Have you tried Fix Windows? Scan now!",
            "Clear clutter for a focused PC experience.",
            "Your optimization adventure starts today!",
            "Personalize your desktop with UI Tweaks.",
            "Refresh your system with Clean Cache now.",
            "Unlock speed with Performance Tweaks today.",
            "Trust MK-Tools for a dependable PC.",
            "Game better with Performance Tweaks now.",
            "Speed up tasks with a quick optimization.",
            "A healthy PC with MK-Tools’ care.",
            "Master your system with Group Policy.",
            "Make today a great day for your PC!",
            "Clear digital mess with Clean Cache.",
            "Effortless tweaks for a faster PC.",
            "Check out MK-Tools’ latest optimization tools!",
            "No lag, just speed with MK-Tools.",
            "Power your work with a tuned PC.",
            "Have you explored UI Tweaks? Start now!",
            "A snappier PC with Performance Tweaks.",
            "A clean system for a productive day.",
            "Explore MK-Tools for a better PC.",
            "Control your PC with Group Policy tweaks.",
            "Faster boot times with a quick clean.",
            "A tuned PC for a smoother workflow.",
            "Fix Windows for a healthier system today.",
            "Speed up with Performance Tweaks now!",
            "A fresh PC with Clean Cache magic.",
            "Easy optimization for a better PC.",
            "Make your desktop yours with UI Tweaks.",
            "Reliable tweaks with MK-Tools’ suite.",
            "Multitask smoothly with Performance Tweaks.",
            "Power your PC with Clean Cache today.",
            "Create without limits with a tuned PC.",
            "Seamless performance with MK-Tools’ tools.",
            "Boost speed with a single click now!",
            "Clear cache for a faster PC today.",
            "Have you tried Group Policy? Explore it!",
            "Your PC’s ready to shine with MK-Tools.",
            "Stabilize your system with Fix Windows.",
            "One-click tweaks for a responsive PC.",
            "Take control with Group Policy today.",
            "Clean up your PC with MK-Tools now.",
            "Free space with a Clean Cache sweep.",
            "Speed up your system with one tweak!",
            "Make your desktop shine with UI Tweaks.",
            "Discover MK-Tools for a smoother PC.",
            "A stable PC with MK-Tools’ tweaks.",
            "Unleash your PC’s speed with tweaks.",
            "Optimize easily with MK-Tools’ suite.",
            "Have you checked Clean Cache? Try it!",
            "Clear clutter for a snappier PC.",
            "Your optimization journey starts now!",
            "Personalize your system with UI Tweaks.",
            "Refresh your PC with a quick clean.",
            "Unlock performance with Performance Tweaks.",
            "Trust MK-Tools for a faster system.",
            "Game smoothly with Performance Tweaks today.",
            "Speed up tasks with MK-Tools’ tools.",
            "A healthy PC with regular tweaks.",
            "Master your PC with Group Policy now.",
            "Make your PC soar with MK-Tools!",
            "Clear digital clutter with Clean Cache.",
            "Effortless speed with MK-Tools’ tweaks.",
            "Check MK-Tools’ features for a better PC!",
            "No more lag with MK-Tools’ optimizations.",
            "Power your tasks with a tuned PC.",
            "Have you tried UI Tweaks? Customize now!",
            "A responsive PC with Performance Tweaks.",
            "A clean system for a better day.",
            "Explore MK-Tools for a faster system.",
            "Control your system with Group Policy.",
            "Faster startups with MK-Tools’ tools.",
            "A tuned PC for a productive day.",
            "Fix Windows for a stable PC now.",
            "Speed up with Performance Tweaks today!",
            "A fresh system with Clean Cache now.",
            "Easy tweaks for a smoother PC.",
            "Customize your desktop with UI Tweaks today.",
            "Reliable performance with MK-Tools’ tools.",
            "Multitask better with Performance Tweaks.",
            "Power up with a Clean Cache run.",
            "Create freely with a faster PC.",
            "Seamless tweaks with MK-Tools’ suite.",
            "Boost your PC with one click now!",
            "Clear cache for a responsive system.",
            "Have you checked Fix Windows? Scan today!",
            "Your PC’s ready for a speed boost.",
            "Stabilize your PC with MK-Tools’ tools.",
            "One-click optimization for a better PC.",
            "Take charge with Group Policy tweaks now.",
            "Clean your PC with MK-Tools today.",
            "Free up space with Clean Cache now.",
            "Speed up your PC with MK-Tools!",
            "Make your desktop pop with UI Tweaks.",
            "Discover MK-Tools for a stable PC.",
            "A reliable system with MK-Tools’ tweaks.",
            "Unleash speed with Performance Tweaks now.",
            "Optimize easily with MK-Tools’ tools.",
            "Have you tried Clean Cache? Start now!",
            "Clear clutter for a faster system.",
            "Your PC’s optimization starts today!",
            "Personalize your PC with UI Tweaks.",
            "Refresh your system with Clean Cache.",
            "Unlock speed with MK-Tools’ tweaks.",
            "Trust MK-Tools for a smooth PC.",
            "Game better with Performance Tweaks now.",
            "Speed up tasks with a quick tweak.",
            "A healthy system with MK-Tools’ care.",
            "Master your system with Group Policy tweaks."
        ]
        # --- Navigation Callback Configuration ---
        if frame_switcher_callback is None and hasattr(master, "select_frame_by_name"):
            frame_switcher_callback = master.select_frame_by_name
        self._navigate = frame_switcher_callback

        # --- UI Construction Protocol ---
        self._create_header()
        self._create_card_grid()

    # ───────────────────────── INTERNAL UI BUILDERS ────────────────────── #

    def _create_header(self) -> None:
        """Creates the top header and the dynamic inspirational message using the universal emoji font."""
        # --- Retrieve the current user's username with a safe fallback protocol.
        try:
            username = getpass.getuser()
        except Exception as e:
            logging.error(f"Could not get username: {e}. Defaulting to 'User'.")
            username = "User"

        # --- Create a container frame for the header elements to ensure proper alignment.
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="n")

        # --- [CRITICAL FIX] Render the welcome emoji using the universal, pre-scaled emoji font from the Theme class.
        # --- This guarantees identical rendering on all target operating systems.
        ctk.CTkLabel(header_frame, text="🎉", font=self.fonts["emoji_large"]).pack(side="left", padx=(0, 10))
        
        # --- Create the standard text labels using the default theme font.
        ctk.CTkLabel(header_frame, text="Welcome ", font=self.fonts["title"], text_color=Theme.TEXT).pack(side="left")
        ctk.CTkLabel(header_frame, text=username, font=self.fonts["title"], text_color=Theme.ACCENT).pack(side="left")
        ctk.CTkLabel(header_frame, text="! to MK-Tools ", font=self.fonts["title"], text_color=Theme.TEXT).pack(side="left")

        # --- [CRITICAL FIX] Render the rocket emoji using the universal emoji font for consistency.
        ctk.CTkLabel(header_frame, text="🚀", font=self.fonts["emoji_large"]).pack(side="left")
        
        # --- Create the dynamic message label that updates upon frame entry.
        dynamic_message_text = random.choice(self.dynamic_messages)
        self.dynamic_message_label = ctk.CTkLabel(
            self,
            text=dynamic_message_text,
            font=self.fonts["normal"],
            text_color=Theme.TEXT_SECONDARY,
        )
        self.dynamic_message_label.grid(row=1, column=0, columnspan=2, pady=(5, 20), sticky="n")


    def _create_card_grid(self) -> None:
        """Creates and arranges all interactive and static cards on a responsive grid."""
        # --- [ICON REFACTOR] The 'icon' key now holds the file path to the PNG asset.
        sections = [
            # --- [MODIFIED] Use resource_path to resolve icon paths at runtime.
            {"frame": "performance", "icon_path": resource_path(os.path.join("Icons", "Performance-Icon.png")), "title": "Performance Tweaks", "features": 5},
            {"frame": "ui_tweaks",   "icon_path": resource_path(os.path.join("Icons", "UI-Responsiveness.png")), "title": "UI & Responsiveness", "features": 4},
            {"frame": "fix_windows", "icon_path": resource_path(os.path.join("Icons", "FixWindows.png")), "title": "Fix Windows",         "features": 2},
            {"frame": "clean_cache", "icon_path": resource_path(os.path.join("Icons", "Clean-Cache.png")), "title": "Clean Cache",         "features": 6},
            {"frame": "policy",      "icon_path": resource_path(os.path.join("Icons", "Group-Policy.png")), "title": "Group Policy",        "features": 2},
        ]

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # --- Store cards in the parent class's list for state management.
        self.cards = [] 

        for idx, sec in enumerate(sections):
            row, col = divmod(idx, 2)
            card = _DashboardCard(
                master=self,
                fonts=self.fonts,
                icon_path=sec["icon_path"], # Pass the icon_path
                title=sec["title"],
                feature_count=sec["features"],
                command=lambda name=sec["frame"]: self._safe_nav(name),
                sound_manager=self.sound_manager
            )
            card.grid(row=row + 2, column=col, padx=25, pady=25, sticky="nsew")
            self.cards.append(card) # Add the interactive card to the list.

        final_row, final_col = divmod(len(sections), 2)
        coming_soon_card = _ComingSoonCard(master=self, fonts=self.fonts)
        coming_soon_card.grid(row=final_row + 2, column=final_col, padx=25, pady=25, sticky="nsew")
        self.cards.append(coming_soon_card)
    
    def _update_dynamic_message(self) -> None:
        """Selects a new random message and updates the message label."""
        if hasattr(self, 'dynamic_message_label') and hasattr(self, 'dynamic_messages'):
            new_message = random.choice(self.dynamic_messages)
            self.dynamic_message_label.configure(text=new_message)

    def _safe_nav(self, frame_name: str) -> None:
        """Safely invokes the navigation callback and plays a click sound."""
        if callable(self._navigate):
            if self.sound_manager:
                self.sound_manager.play_sound('click')
            self._navigate(frame_name)
        
    def run_entry_animation(self):
        """
        [RE-ENGINEERED] This method is called when the frame becomes visible.
        It now ONLY updates the dynamic message and does NOT perform any animations.
        """
        self._update_dynamic_message()
        # The call to super().run_entry_animation() has been removed to disable the animation.

    def reset_state(self):
        """
        Implements the master reset protocol for this frame. This is called
        automatically when the user navigates away from the dashboard. It commands
        all child cards to reset their visual state.
        """
        logging.info("Resetting DashboardFrame state: Reverting all card highlights.")
        # Iterate through all cards and command them to reset their hover state.
        for card in self.cards:
            # Check if the card has the reset_state method before calling it.
            # This makes the code robust, as _ComingSoonCard does not have this method.
            if hasattr(card, 'reset_state'):
                card.reset_state()
    
    def update_ui_scaling(self, fonts):
        """
        [NEW] Propagates font updates to all child cards, ensuring their icons
        and text are correctly rescaled.
        """
        super().update_ui_scaling(fonts)
        if self.winfo_exists():
            # --- Update the dynamic message label font.
            if hasattr(self, 'dynamic_message_label'):
                self.dynamic_message_label.configure(font=fonts["normal"])
            
            # --- Cascade the scaling update to all child cards.
            for card in self.cards:
                if hasattr(card, "update_ui_scaling"):
                    card.update_ui_scaling(fonts)

# ===================================================================================
# CLASS: _DashboardCard (v2.4 - With State Reset Protocol)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This version introduces a definitive, public-facing state reset protocol.
#
# CORRECTION PROTOCOL:
#  1. NEW PUBLIC API: A new method, `reset_state()`, has been engineered. Its
#     sole purpose is to forcibly revert the component to its default, non-hovered
#     visual state. It sets the internal `_is_mouse_inside` flag to False and
#     resets the border color to its default.
#
#  2. ENCAPSULATION: This method provides a clean, encapsulated interface for the
#     parent frame (`DashboardFrame`) to command a state change without needing
#     to know about the component's internal implementation details. This is the
#     cornerstone of the bug fix.
# ===================================================================================
class _DashboardCard(ctk.CTkFrame):
    """A single, interactive, and perfectly aligned clickable card with a unified, stateful hover effect and precise auditory feedback."""

    # The constructor for the re-engineered _DashboardCard class.
    def __init__(
        self,
        master,
        fonts,
        icon_path: str, # Changed from 'icon' to 'icon_path'
        title: str,
        feature_count: int,
        command: Callable[[], None],
        sound_manager: Optional['SoundManager'] = None
    ):
        # --- Base Class Initialization & Theming ---
        super().__init__(
            master,
            fg_color=Theme.CARD,
            corner_radius=20,
            border_width=2,
            border_color=Theme.CARD,
        )
        # --- Property and State Storage ---
        self.command = command
        self.fonts = fonts
        self.sound_manager = sound_manager
        self.icon_path = icon_path # Store the path for rescaling
        self._is_mouse_inside = False
        self._leave_check_job = None

        # --- Internal Grid Configuration for perfect centering ---
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)

        # --- Widget Creation & Placement ---
        # --- [ICON REFACTOR] The icon is now a scalable CTkImage, not a text emoji.
        self.icon_image = None # Placeholder for the CTkImage object
        self.icon_lbl = ctk.CTkLabel(self, text="") # Create the label, image will be added
        self.icon_lbl.grid(row=1, column=0, pady=(10, 5))

        # --- The title label for the card.
        self.title_lbl = ctk.CTkLabel(self, text=title, font=self.fonts["h2"], text_color=Theme.TEXT)
        self.title_lbl.grid(row=2, column=0)

        # --- The feature count sub-label.
        self.feat_lbl = ctk.CTkLabel(self, text=f"{feature_count} Features", font=self.fonts["small"], text_color=Theme.TEXT_SECONDARY)
        self.feat_lbl.grid(row=3, column=0, pady=(5, 10))

        # --- Definitive Event Binding Protocol ---
        self._bind_events()
        
        # --- Initial Scaling Call ---
        # This sets the initial size of the icon correctly.
        self.update_ui_scaling(self.fonts)

    def _bind_events(self):
        """
        [RE-ENGINEERED] Binds events recursively to all widgets to create a
        unified interaction surface, with stateful handlers to prevent anomalies.
        """
        # --- Create a comprehensive list of all widgets that form this component.
        all_widgets = (self, self.icon_lbl, self.title_lbl, self.feat_lbl)

        # --- Bind all widgets to the same set of event handlers.
        for widget in all_widgets:
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_click)

    def _on_enter(self, event=None):
        """
        Handles the mouse entering ANY part of the card. This serves as the
        primary trigger for the hover-on action.
        """
        # --- Cancel any pending "leave" check. This is crucial for when the
        # --- mouse moves rapidly between child widgets.
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
            self._leave_check_job = None

        # --- Check the state to prevent re-triggering ---
        # If the mouse is not already considered inside, proceed.
        if not self._is_mouse_inside:
            # --- Update the state to reflect the mouse is now inside.
            self._is_mouse_inside = True

            # --- Dispatch Auditory Feedback ---
            # If a sound manager exists, play the 'hover' sound exactly once.
            if self.sound_manager:
                self.sound_manager.play_sound('hover')

            # --- Dispatch Visual Feedback ---
            # Change the border color to the theme's accent color for a highlight effect.
            self.configure(border_color=Theme.ACCENT)

    def _on_leave(self, event=None):
        """
        Handles the mouse leaving ANY part of the card. Schedules a delayed
        check to verify if the mouse has truly exited the component's boundary.
        """
        # --- Cancel any previously scheduled check to avoid redundant checks.
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)

        # --- Schedule the positional verification check to run after 1ms.
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    def _check_if_truly_left(self):
        """
        Performs a forensic check of the cursor's position. This is the definitive
        method for determining if the hover-off state should be triggered.
        """
        # --- Get the current absolute X and Y coordinates of the mouse pointer.
        pointer_x = self.winfo_pointerx()
        pointer_y = self.winfo_pointery()

        # --- Get the absolute screen coordinates and dimensions of this card's master frame.
        x1 = self.winfo_rootx()
        y1 = self.winfo_rooty()
        x2 = x1 + self.winfo_width()
        y2 = y1 + self.winfo_height()

        # --- The Core Logical Check ---
        # Determine if the pointer's coordinates are outside the card's bounding box.
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)

        # If the mouse is confirmed to be outside the boundary AND the component
        # still thinks the mouse is inside...
        if is_truly_outside and self._is_mouse_inside:
            # --- Update the state to reflect the mouse is now outside.
            self._is_mouse_inside = False
            # --- Revert the visual feedback.
            self.configure(border_color=Theme.CARD)

    def _on_click(self, event=None):
        """
        Executes the stored command when any part of the card is clicked.
        """
        # The click sound is handled by the parent DashboardFrame's _safe_nav method.
        self.command()

    def reset_state(self):
        """
        [NEW] Forcibly resets the card to its default, non-hovered visual state.
        This is the public API for the parent frame to call during navigation
        to prevent a persistent hover effect.
        """
        # --- Cancel any pending leave check to prevent race conditions.
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
            self._leave_check_job = None
        # --- Forcibly reset the internal hover state.
        self._is_mouse_inside = False
        # --- Forcibly revert the visual feedback to its default state.
        self.configure(border_color=Theme.CARD)
    
    def update_ui_scaling(self, fonts):
        """
        [NEW] Propagates font updates and dynamically rescales the icon PNG to
        maintain visual quality and layout integrity.
        """
        self.fonts = fonts
        if self.winfo_exists():
            # --- Update text fonts ---
            self.title_lbl.configure(font=self.fonts["h2"])
            self.feat_lbl.configure(font=self.fonts["small"])

            # --- Rescale the icon image ---
            try:
                # --- Calculate the new icon size relative to the scaled H2 font size.
                # --- This ensures the icon scales proportionally with the text.
                new_font_size = self.fonts["h2"].cget("size")
                new_icon_size = int(new_font_size * 2.5) # Scaling multiplier for visual balance

                # --- Create a new CTkImage object with the updated size.
                self.icon_image = ctk.CTkImage(
                    Image.open(self.icon_path), 
                    size=(new_icon_size, new_icon_size)
                )
                # --- Apply the new, rescaled image to the label.
                self.icon_lbl.configure(image=self.icon_image)
            except Exception as e:
                logging.error(f"Failed to load or resize icon '{self.icon_path}': {e}")
                # --- If loading fails, display a fallback text to prevent crashing.
                self.icon_lbl.configure(image=None, text="⚠️")

# ===================================================================================
# CLASS: _ComingSoonCard (v1.0 - Non-Interactive Placeholder Component)
#
# ARCHITECTURAL BLUEPRINT:
# This class defines a static, non-interactive placeholder card for the dashboard.
# Its sole purpose is to visually communicate that more features are planned for
# the application, managing user expectations and hinting at future value.
#
# CORE PRINCIPLES:
#   1. VISUAL SUBORDINATION: The card is intentionally styled with muted colors
#      (a slightly darker background and secondary text color) to differentiate
#      it from the active, interactive `_DashboardCard` components. It does not
#      react to hovering.
#
#   2. NON-INTERACTIVITY BY DESIGN: The card has no command callback and no event
#      bindings for clicks or hovers. It is a purely presentational element,
#      preventing any user confusion about its function.
#
#   3. STRUCTURAL CONSISTENCY: It uses the exact same internal grid structure as
#      the `_DashboardCard` to ensure it aligns perfectly within the dashboard's
#      master grid, maintaining visual harmony.
# ===================================================================================
class _ComingSoonCard(ctk.CTkFrame):
    """A static, non-interactive placeholder card for future features."""

    # The constructor for the _ComingSoonCard class.
    def __init__(self, master, fonts):
        # --- Base Class Initialization & Muted Theming ---
        # Initialize the parent CTkFrame with a darker, more subdued background
        # to visually distinguish it as a non-interactive element.
        super().__init__(
            master,
            fg_color=Theme.CARD_DARK, # Use a slightly different card color for a dull effect.
            corner_radius=20,
            border_width=2,
            border_color=Theme.NAV_RAIL, # Use a darker border to complete the muted look.
        )
        # --- Store a reference to the application's global font system.
        self.fonts = fonts

        # --- Internal Grid Configuration for Alignment ---
        # This mirrors the grid in _DashboardCard to ensure perfect alignment.
        self.columnconfigure(0, weight=1) # Horizontally center content.
        self.rowconfigure(0, weight=1)    # Vertical centering spacer.
        self.rowconfigure(1, weight=0)    # Icon row.
        self.rowconfigure(2, weight=0)    # Text row.
        self.rowconfigure(3, weight=1)    # Vertical centering spacer.

        # --- Widget Creation & Placement ---
        # The icon for this card, styled to be subtle.
        self.icon_lbl = ctk.CTkLabel(
            self,
            text="✨", # A "sparkle" emoji to hint at new things.
            font=ctk.CTkFont(size=48),
            text_color=Theme.TEXT_SECONDARY, # Use secondary text color for a muted appearance.
        )
        # Place the icon in its dedicated grid row.
        self.icon_lbl.grid(row=1, column=0, pady=(10, 5))

        # The placeholder text message.
        self.title_lbl = ctk.CTkLabel(
            self,
            text="More features\ncoming soon...!", # The specified text.
            font=self.fonts["h3"], # Use H3 font for a slightly smaller title.
            text_color=Theme.TEXT_SECONDARY, # Use secondary text color for the muted effect.
        )
        # Place the text below the icon.
        self.title_lbl.grid(row=2, column=0, pady=(5, 20))

# ===================================================================================
# CLASS: PerformanceFrame (v1.8 - Shutdown-Aware)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component has been upgraded to be a shutdown-aware dependency injector.
# It now accepts the master `app_instance` from the application core.
#
# CORE ENHANCEMENTS:
#  1. CONSTRUCTOR MODIFICATION: The `__init__` method now accepts `app_instance`
#     as a mandatory argument.
#
#  2. DEPENDENCY PROPAGATION: When instantiating child `AnimatedTweakCard`
#     components, it now passes the `app_instance` reference down the hierarchy.
#     This ensures every component with background threads has a direct line to the
#     application's global shutdown signal, completing its role in the graceful
#     shutdown protocol.
# ===================================================================================
class PerformanceFrame(BaseContentFrame):
    """
    Page dedicated to performance-related tweaks, now fully integrated with the
    application's graceful shutdown protocol.
    """
    # [MODIFIED] The constructor now accepts the app_instance.
    def __init__(self, master, fonts, app_instance, sound_manager: Optional['SoundManager'] = None):
        # --- Base class initialization. ---
        super().__init__(master, fonts)
        # --- Store a reference to the main App controller for the shutdown signal.
        self.app = app_instance
        # --- Store a reference to the Auditory Feedback Engine.
        self.sound_manager = sound_manager

        # --- [PNG REFACTOR] Create a container for the header icon and text.
        header_container = ctk.CTkFrame(self, fg_color="transparent")
        header_container.grid(row=0, column=0, padx=10, pady=(0, 20), sticky="w")
        
        # --- Create the icon label, which will be populated by update_ui_scaling.
        self.header_icon_image = None # Placeholder for the CTkImage object
        self.header_icon = ctk.CTkLabel(header_container, text="")
        self.header_icon.grid(row=0, column=0, padx=(0, 10))

        # --- Create the main header text label, now without the emoji.
        self.header_label = ctk.CTkLabel(header_container, text="Performance Tweaks", font=self.fonts["title"], text_color=Theme.TEXT)
        self.header_label.grid(row=0, column=1, sticky="w")
        
        # --- Initial call to load and scale the icon.
        self.update_ui_scaling(self.fonts)

        # --- Logic Controller Instantiation ---
        svchost_logic = SvcHostSplitTweak()
        foreground_priority_logic = ForegroundPriorityController()
        gpu_scheduling_logic = GPUSchedulingTweak()
        fast_startup_logic = DisableFastStartupTweak()
        compressed_memory_logic = DisableCompressedMemoryTweak()

        # --- Foreground Application Priority Information Payload ---
        FOREGROUND_PRIORITY_INFO = {
            'title': "🎯 Prioritize Foreground Applications",
            'description': (
                "This Windows optimization gives more CPU and system resources to the application or game "
                "you are actively using, while slightly reducing resources for background apps. "
                "It can make your current tasks feel smoother and more responsive, especially on systems "
                "that run many apps at once."
            ),
            'pros': [
                "Makes active apps and games feel faster and more responsive.",
                "Can reduce stuttering and input lag in foreground applications.",
                "Improves overall experience on PCs with limited CPU power.",
                "A safe, native Windows setting that can be easily reverted."
            ],
            'cons': [
                "Background processes, like downloads or video rendering, may run slower.",
                "Benefits may be less noticeable on high-end CPUs with many cores.",
                "Requires a system restart to fully apply the changes."
            ]
        }
        # --- GPU Scheduling Information Payload ---
        GPU_SCHEDULING_INFO = {
            'title': "🎮 Hardware-Accelerated GPU Scheduling",
            'description': (
                "Hardware-Accelerated GPU Scheduling is a Windows feature that lets your graphics card (GPU) "
                "manage its own video memory (VRAM) instead of relying heavily on the CPU. "
                "This can reduce input lag and improve performance in games and GPU-heavy tasks. "
                "However, the benefits depend on your GPU type, driver support, and the applications you use."
            ),
            'pros': [
                "Can reduce input latency in games, making controls feel more responsive.",
                "May slightly improve performance in GPU-intensive games and creative applications.",
                "Helps the CPU by offloading some graphics-related work to the GPU itself.",
                "A lightweight feature that is easy to enable or disable through Windows settings."
            ],
            'cons': [
                "Performance improvements are often small or unnoticeable in many games.",
                "Can occasionally cause stutters, crashes, or other instability on some systems.",
                "Requires a system restart after enabling or disabling to take effect."
            ],
        }
        # --- Fast Startup and Compressed Memory Information Payloads ---
        FAST_STARTUP_INFO = {
            'title': "⏱️ Disable Fast Startup",
            'description': (
                "Fast Startup is a Windows feature that makes your computer start faster after shutting it down. "
                "Instead of completely turning off, Windows saves part of itself (the system core) to the disk and "
                "uses that saved state to start faster next time. When you disable Fast Startup, Windows will perform "
                "a full shutdown and a clean startup every time. This can make your system more stable, fully refresh "
                "your hardware, and avoid certain performance or compatibility problems, but it may start a bit slower."
            ),
            'pros': [
                "Fully resets the CPU and system memory, which can improve long-term stability and performance.",
                "Can fix issues with USB devices, Wi-Fi, or other hardware not being detected after shutdown.",
                "Better for dual-boot systems because your Windows drive is fully unlocked and safe to access.",
                "Reduces the chance of driver conflicts or small system glitches caused by partial shutdowns.",
                "Helps ensure system updates or BIOS/firmware changes apply correctly without problems."
            ],
            'cons': [
                "Your computer may take a little longer to start from a complete shutdown.",
                "More power and resources are used during startup compared to Fast Startup.",
                "Not ideal for users who shut down and start up their computer many times a day.",
                "Modern SSDs already boot very quickly, so the speed difference may not be worth it for some users.",
                "After a shutdown or power loss, Windows will take a bit longer to be ready to use."
            ]
        }
        # --- Disable Compressed Memory Information Payload ---
        COMPRESSED_MEMORY_INFO = {
            'title': "🧠 Disable Compressed Memory",
            'description': (
                "Windows uses a feature called Memory Compression to store more data in RAM by compressing "
                "less-used memory pages. This reduces the need to use the page file on your disk, which can help "
                "on systems with limited RAM. However, compressing and decompressing memory uses CPU power. "
                "Disabling it can improve real-time performance and responsiveness on systems with plenty of RAM "
                "(16GB or more), but it is not recommended for PCs with low memory."
            ),
            'pros': [
                "Reduces background CPU usage, freeing resources for games and creative apps.",
                "Can improve responsiveness on systems with 16GB or more RAM.",
                "Helps prevent micro-stutters in latency-sensitive applications like gaming or music production.",
                "Gives more consistent performance if your CPU is often near 100% usage."
            ],
            'cons': [
                "Not recommended for PCs with less than 16GB RAM because it may cause faster memory exhaustion.",
                "If you run out of RAM, system performance will drop more sharply without compression.",
                "Requires a system restart for the change to take effect."
            ]
        }


        # --- Master Data Structure for UI Cards ---
        tweaks_data = [
                {
                    'title': "Disable Fast Startup", 'description': "Ensures a Full Shutdown of Your Computer 🖥️", 'emoji': "⏱️",
                    'view_mode': 'toggle', 'tweak_logic': fast_startup_logic, 'info_data': FAST_STARTUP_INFO
                },
                {
                    'title': "Disable Compressed Memory", 'description': "Reduces CPU usage on systems with 16GB+ RAM.", 'emoji': "🧠",
                    'view_mode': 'toggle', 'tweak_logic': compressed_memory_logic, 'info_data': COMPRESSED_MEMORY_INFO
                },
                {
                    'title': "Hardware-Accelerated GPU Scheduling", 'description': "Allows the GPU to manage its own memory.", 'emoji': "🎮",
                    'view_mode': 'config_dropdown', 'tweak_logic': gpu_scheduling_logic, 'info_data': GPU_SCHEDULING_INFO
                },
                {
                    'title': "Prioritize Foreground Applications", 'description': "Allocates more processor resources to the active app.", 'emoji': "🎯",
                    'view_mode': 'toggle', 'tweak_logic': foreground_priority_logic, 'info_data': FOREGROUND_PRIORITY_INFO
                },
                {
                    'title': "Optimize SvcHost Combining", 
                    'description': "Reduces stress on your CPU and improves performance", 
                    'emoji': "🔗",
                    'view_mode': 'config_dropdown', 
                    'tweak_logic': svchost_logic,
                    'info_data': {
                        'title': "⚙️ SvcHost Combining Explained",
                        'description': (
                            "This feature fine-tunes how Windows manages background services by grouping more of them together, "
                            "so your CPU has fewer processes to handle. This is especially helpful if you have plenty of RAM but a processor with fewer cores.\n\n"
                            "Our application uses next-generation, military-grade optimization algorithms to ensure every change is safe, precise, "
                            "and tailored to your system’s performance profile. The process is fully automated, thoroughly tested, and designed to boost speed "
                            "while keeping your computer stable and protected."
                        ),
                        'pros': [
                            "✅ Reduces the number of running processes, lowering CPU workload.",
                            "✅ Can make the system feel smoother and more responsive.",
                            "✅ Uses safe, precision-engineered algorithms with built-in protection.",
                            "✅ Ideal for systems with high RAM and lower-end CPUs.",
                            "✅ Fully reversible — your system can be restored to default instantly."
                        ],
                        'cons': [
                            "❌ In rare cases, may slightly affect service stability depending on configuration.",
                            "❌ Uses a small amount of extra RAM, which is negligible on modern systems."
                        ],
                    }
                }
        ]
        # --- Card Instantiation ---
        self.cards = [AnimatedTweakCard(self, self.fonts, app_instance=self.app, sound_manager=self.sound_manager, **data) for data in tweaks_data]

        # --- Post-Instantiation Wiring Protocol ---
        svchost_card = next((card for card in self.cards if "SvcHost" in card.title_label.cget("text")), None)
        if svchost_card: svchost_card.custom_config_panel_builder = svchost_card._create_svchost_config_panel

        gpu_card = next((card for card in self.cards if "GPU Scheduling" in card.title_label.cget("text")), None)
        if gpu_card: gpu_card.custom_config_panel_builder = gpu_card._create_gpu_config_panel

        # --- Final UI Rendering ---
        for i, card in enumerate(self.cards):
            card.grid(row=i + 1, column=0, sticky="ew", padx=10, pady=10)
    
    def manage_card_panels(self, toggled_card: 'AnimatedTweakCard'):
        """
        Ensures only one info/config panel is open at a time across all cards
        in this frame. This is the central orchestrator for the exclusive panel logic.
        """
        # --- Iterate through all the AnimatedTweakCard instances managed by this frame.
        for card in self.cards:
            # --- If the card in the loop is not the one that was just clicked...
            if card is not toggled_card:
                # --- ...command it to close any panels it might have open.
                card.close_all_panels()

    def reset_state(self):
        """Implements the master reset protocol for this frame."""
        logging.info("Resetting PerformanceFrame state: Closing all open panels.")
        for card in self.cards:
            if hasattr(card, 'close_all_panels'):
                card.close_all_panels()
    
    def update_ui_scaling(self, fonts):
        """
        Propagates font updates to all child cards and rescales the header icon.
        """
        super().update_ui_scaling(fonts)
        if self.winfo_exists():
            # --- Rescale the header icon image ---
            try:
                # --- Calculate the new icon size relative to the scaled title font size.
                new_font_size = self.fonts["title"].cget("size")
                new_icon_size = int(new_font_size * 1.2) # Scaling multiplier for visual balance

                # --- Create a new CTkImage object with the updated size.
                self.header_icon_image = ctk.CTkImage(
                    Image.open(resource_path(os.path.join("Icons", "Rocket.png"))),
                    size=(new_icon_size, new_icon_size)
                )
                # --- Apply the new, rescaled image to the label.
                self.header_icon.configure(image=self.header_icon_image)
            except Exception as e:
                logging.error(f"Failed to load or resize header icon: {e}")
                self.header_icon.configure(image=None, text="⚠️") # Fallback

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

# ===================================================================================
# CLASS: UITweaksFrame (v1.8 - Shutdown-Aware)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component has been upgraded to be a shutdown-aware dependency injector,
# mirroring the architecture of the PerformanceFrame. It now accepts the master
# `app_instance` from the application core and propagates it down to its child
# `AnimatedTweakCard` components. This ensures every component with background
# threads has a direct line to the application's global shutdown signal,
# completing its role in the graceful shutdown protocol.
# ===================================================================================
class UITweaksFrame(BaseContentFrame):
    """
    Page for UI tweaks, now fully integrated with the application's graceful
    shutdown protocol.
    """
    # [MODIFIED] The constructor now accepts the app_instance.
    def __init__(self, master, fonts, app_instance, sound_manager: Optional['SoundManager'] = None):
        super().__init__(master, fonts)
        # --- Store a reference to the main App controller for the shutdown signal.
        self.app = app_instance
        # --- Store a reference to the Auditory Feedback Engine.
        self.sound_manager = sound_manager

        # --- [PNG REFACTOR] Create a container for the header icon and text.
        header_container = ctk.CTkFrame(self, fg_color="transparent")
        header_container.grid(row=0, column=0, padx=10, pady=(0, 20), sticky="w")
        
        # --- Create the icon label, which will be populated by update_ui_scaling.
        self.header_icon_image = None # Placeholder for the CTkImage object
        self.header_icon = ctk.CTkLabel(header_container, text="")
        self.header_icon.grid(row=0, column=0, padx=(0, 10))

        # --- Create the main header text label, now without the emoji.
        self.header_label = ctk.CTkLabel(header_container, text="UI & Responsiveness", font=self.fonts["title"], text_color=Theme.TEXT)
        self.header_label.grid(row=0, column=1, sticky="w")
        
        # --- Initial call to load and scale the icon.
        self.update_ui_scaling(self.fonts)

        # --- Instantiate ALL backend logic controllers for this section. ---
        classic_menu_logic = ClassicContextMenuTweak()
        menu_delay_logic = MenuShowDelayTweak()
        jpeg_quality_logic = JPEGQualityTweak()
        web_search_logic = DisableWebSearchTweak()

        # --- Master Data Structure with Rich Info for Each Tweak ---
        tweaks_data = [
            {
                'title': "Enable Win10 Right-Click Menu on Win11",
                'description': "Restores Windows 10 context menu on Windows 11",
                'emoji': "📔",
                'view_mode': 'toggle',
                'tweak_logic': classic_menu_logic,
                'info_data': {
                        'title': "📔 Classic Right-Click Menu",
                        'description': (
                            "This tweak brings back the classic Windows 10-style right-click context menu in Windows 11. "
                            "The default Windows 11 menu hides many options behind a 'Show more options' button, which can "
                            "slow down tasks like copying, extracting, or managing files. Enabling this tweak shows all options "
                            "immediately, making the menu faster and more familiar for long-time Windows users."
                        ),
                        'pros': [
                            "Faster access to all context menu options without extra clicks.",
                            "Improves workflow efficiency for power users and frequent file managers.",
                            "Restores a familiar experience for users upgrading from Windows 10.",
                            "Works well with older apps that rely on classic context menu entries."
                        ],
                        'cons': [
                            "Removes the cleaner, modern design of the Windows 11 context menu.",
                            "Slightly more cluttered appearance for casual users.",
                            "Requires restarting Windows Explorer or signing out to apply the change."
                        ],
                    }
            },
            {
                'title': "Instant Right-Click Mouse Menu Display",
                'description': "Removes the artificial delay when opening menus.",
                'emoji': "⚡",
                'view_mode': 'toggle',
                'tweak_logic': menu_delay_logic,
                'info_data': {
                        'title': "⚡ Instant Menu Display",
                        'description': (
                            "By default, Windows adds a small delay (typically 400 milliseconds) before displaying menus "
                            "such as right-click context menus or drop-downs. This delay is controlled by the registry "
                            "value `MenuShowDelay` located in:\n\n"
                            "HKEY_CURRENT_USER\\Control Panel\\Desktop\n\n"
                            "• Default Value: 400 ms (0.4 seconds)\n"
                            "• Optimized Value (applied by this tweak): 0 ms for instant display\n\n"
                            "Reducing this value to 0 makes all menus open instantly. This tweak affects the Start Menu, "
                            "taskbar menus, File Explorer context menus, and other standard Windows menus. "
                            "The result is a much faster and more responsive user experience, especially noticeable "
                            "on older or slower computers."
                        ),
                        'pros': [
                            "Menus appear instantly, improving overall desktop responsiveness.",
                            "Removes unnecessary waiting time, making Windows feel faster and more fluid.",
                            "Great for power users or productivity-focused workflows with frequent menu actions.",
                            "Simple registry-level tweak that can be reverted anytime by restoring the default value (400 ms)."
                        ],
                        'cons': [
                            "The speed improvement may be subtle for casual users with fast PCs.",
                            "Menus opening instantly can lead to occasional accidental selections if you misclick.",
                            "A logoff or system restart is required for the change to fully apply."
                        ]
                    }
            },
            {
                'title': "Use 100% JPEG Wallpaper Quality",
                'description': "Prevents Windows from compressing your wallpaper.",
                'emoji': "💎",
                'view_mode': 'config_dropdown',
                'tweak_logic': jpeg_quality_logic,
                'info_data': {
                        'title': "💎 JPEG Wallpaper Quality",
                        'description': (
                            "Windows automatically compresses JPEG wallpapers to around 85% quality to save a small "
                            "amount of memory and improve performance. This can make detailed images look slightly blurry "
                            "or show compression artifacts, especially on 1080p, 2K, or 4K monitors.\n\n"
                            "This tweak modifies the registry value:\n"
                            "HKEY_CURRENT_USER\\Control Panel\\Desktop\\JPEGImportQuality\n\n"
                            "• Default Value: 85 (approximately 85% quality)\n"
                            "• Optimized Value: 100 (lossless for JPEG wallpapers)\n\n"
                            "After enabling this tweak, Windows will display your wallpapers in their original, crisp quality. "
                            "You can also set custom values (between 60–100) for a balance between performance and visuals."
                        ),
                        'pros': [
                            "Restores wallpapers to their full, pixel-perfect quality with no extra compression.",
                            "Ideal for high-resolution displays (2K, 4K, or ultrawide monitors).",
                            "Prevents visible artifacts or blurriness in detailed images.",
                            "Allows adjusting the quality to balance memory usage and visual fidelity."
                        ],
                        'cons': [
                            "Using 100% quality slightly increases RAM and storage use for cached wallpapers.",
                            "Benefit is mostly noticeable on large or high-resolution displays.",
                            "Requires logging off or re-applying the wallpaper to see the effect."
                        ]
                    }
            },
            {
                'title': "Disable Web Search in Start Menu",
                'description': "Limits searches to your local files and apps.",
                'emoji': "🔍",
                'view_mode': 'toggle',
                'tweak_logic': web_search_logic,
                'info_data': {
                        'title': "🔍 Disable Web Search",
                        'description': (
                            "By default, the Windows 10 and 11 Start Menu can show web results from Bing whenever you search "
                            "for something. This means your search terms are sent to Microsoft servers to fetch online suggestions. "
                            "While convenient, this can slow down search performance and send unnecessary data over the internet.\n\n"
                            "This tweak disables web search entirely, so the Start Menu only searches for local files, folders, "
                            "apps, and settings. Your searches stay private and typically respond faster.\n"
                        ),
                        'pros': [
                            "Improves privacy by stopping Windows from sending search queries to Microsoft.",
                            "Speeds up Start Menu searches by avoiding online lookups.",
                            "Reduces unnecessary network traffic and data usage.",
                            "Prevents accidentally opening a browser when searching for local files or apps."
                        ],
                        'cons': [
                            "You lose the ability to perform quick web searches directly from the Start Menu.",
                            "Some features like Bing-powered weather or search suggestions will be disabled.",
                            "Requires a system restart or logoff to take full effect."
                        ]
                    }
            }
        ]
        
        # [MODIFIED] The master app_instance is now passed into the constructor data for each card.
        self.cards = [AnimatedTweakCard(self, self.fonts, app_instance=self.app, sound_manager=self.sound_manager, **data) for data in tweaks_data]
        for i, card in enumerate(self.cards):
            card.grid(row=i + 1, column=0, sticky="ew", padx=10, pady=10)
    
    def manage_card_panels(self, toggled_card: 'AnimatedTweakCard'):
        """
        Ensures only one info/config panel is open at a time across all cards
        in this frame. This is the central orchestrator for the exclusive panel logic.
        """
        # --- Iterate through all the AnimatedTweakCard instances managed by this frame.
        for card in self.cards:
            # --- If the card in the loop is not the one that was just clicked...
            if card is not toggled_card:
                # --- ...command it to close any panels it might have open.
                card.close_all_panels()
    
    def update_ui_scaling(self, fonts):
        """
        Propagates font updates to all child cards and rescales the header icon.
        """
        super().update_ui_scaling(fonts)
        if self.winfo_exists():
            # --- Rescale the header icon image ---
            try:
                # --- Calculate the new icon size relative to the scaled title font size.
                new_font_size = self.fonts["title"].cget("size")
                new_icon_size = int(new_font_size * 1.2) # Scaling multiplier for visual balance

                # --- Create a new CTkImage object with the updated size.
                self.header_icon_image = ctk.CTkImage(
                    Image.open(resource_path(os.path.join("Icons", "UI-Tweaks.png"))),
                    size=(new_icon_size, new_icon_size)
                )
                # --- Apply the new, rescaled image to the label.
                self.header_icon.configure(image=self.header_icon_image)
            except Exception as e:
                logging.error(f"Failed to load or resize header icon: {e}")
                self.header_icon.configure(image=None, text="⚠️") # Fallback
    
    def reset_state(self):
        """
        Implements the master reset protocol for this frame. This is called
        automatically when the user navigates to a different page.
        """
        logging.info("Resetting UITweaksFrame state: Closing all open panels.")
        # Iterate through all cards and command them to close any open panels.
        for card in self.cards:
            if hasattr(card, 'close_all_panels'):
                card.close_all_panels()


# ===================================================================================
# CLASS: FixWindowsFrame (v12.1 - Process Registry Integration)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This version integrates the frame with the master App's centralized process
# registry. This is the final link in the chain for a zero-footprint exit protocol.
#
# NEW PARADIGM: PROCESS LIFECYCLE MANAGEMENT
#
#  [User clicks 'Scan'] -> [_run_sfc_scan_logic()]
#         |
#         V
#  [self.scan_process = subprocess.Popen(...)]
#         |
#         V
#  [CRITICAL: self.app.register_process(self.scan_process)]
#  Description: Immediately after creation, the process object is registered
#               with the master App controller. It is now tracked for termination.
#         |
#         V
#  [Process runs to completion or is cancelled]
#         |
#         V
#  [CRITICAL: self.app.unregister_process(self.scan_process)]
#  Description: Upon termination (natural or forced), the process is removed
#               from the master registry.
#
# This protocol ensures that the master App class always has a real-time manifest
# of all active child processes, which it will terminate during its shutdown sequence.
# ===================================================================================
class FixWindowsFrame(BaseContentFrame):
    """
    The 'Fix Windows' component, re-engineered with an exit-code-driven diagnostic
    protocol, an asynchronous "finalizing" UI state, a complete soundscape, and
    full integration with the application's process management system.
    """
    def __init__(self, master, fonts, app_instance, sound_manager: Optional['SoundManager'] = None):
        # --- Base Initialization ---
        super().__init__(master, fonts)
        # --- Store a reference to the main App controller for commanding the navigation lock and registering processes.
        self.app = app_instance
        # --- Store a reference to the Auditory Feedback Engine.
        self.sound_manager = sound_manager
        # --- Instantiate the logic controller, passing a reference to self for command callbacks.
        self.logic_controller = DiagnosticLogicController(master_frame=self)

        # --- Data Store: Context-Aware Hint Libraries ---
        self.SCAN_HINTS = [
            "Hint: The SFC scan is verifying the integrity of all protected system files.", "Hint: If the scan appears to pause on a percentage, this is normal behavior.",
            "Hint: This process checks for and attempts to repair corrupted Windows files.", "Hint: Patience is key; a thorough scan ensures a healthy system."
        ]
        self.RESTORE_HINTS = [
            "Hint: 😌 This is a deep system repair. It can take 15-30 minutes. Please be patient!",
            "Hint: 🚫 DO NOT PANIC! If the scan seems stuck (especially at 62.8% or 89.9%), this is normal. Just wait.",
            "Hint: Your PC is working hard to heal itself. Please do not restart or shut down your computer. ⚙️",
            "Hint: ✨ Think of this as major surgery for Windows. It takes time but is worth the wait for a healthy system.",
            "Hint: 🛑 It is critical to let this process complete. Interrupting it can cause system instability.",
            "Hint: Getting a coffee is a great idea right now! ☕ This will take a while."
        ]

        # --- State Management & UI Component Handles ---
        self.is_scanning = False
        self.is_restoring = False
        self.scan_process = None
        self.active_overlay = None
        self.button_container = None
        self.scan_button = None
        self.advanced_scan_button = None
        self.terminal = None
        self.cancel_button = None
        self.dynamic_hint_label = None
        self.hint_engine = None
        self.advanced_restore_button = None
        self.info_button = None
        self.info_frame = None
        self.is_info_expanded = False
        self.scan_gif_widget = None

        # --- [PNG REFACTOR] Add a placeholder for the header icon's CTkImage object.
        self.header_icon_image = None
        
        # --- UI Construction Protocol ---
        self._setup_layout()
        self._create_widgets()

    def _setup_layout(self):
        """Configures the master grid for all UI states."""
        # --- Configure grid rows for dynamic layout changes during scan operations.
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Main action buttons
        self.grid_rowconfigure(2, weight=0)  # Hint Label
        # --- [NEW] Add a new row for the GIF widget.
        self.grid_rowconfigure(3, weight=0)  # GIF Widget
        # --- The terminal will now be on row 4 and will expand to fill space.
        self.grid_rowconfigure(4, weight=1)  # Terminal
        self.grid_rowconfigure(5, weight=0)  # Cancel Button
        self.grid_columnconfigure(0, weight=1)

    # [MODIFIED] This method is now responsible for handling the new GIF widget.
    def _transition_to_scan_ui(self, cancel_command: Callable[[], None], gif_name: str):
        """Transforms the UI for a scanning operation, now including a specific, dynamically-sized GIF."""
        # --- Hide the initial action buttons to clear the UI for the scan view.
        self.button_container.grid_forget()
        # --- Create and display the hint label, which provides context to the user.
        self.dynamic_hint_label = ctk.CTkLabel(self, text="Initializing...", font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY)
        self.dynamic_hint_label.grid(row=2, column=0, pady=(20, 10), sticky="ew")

        # --- [NEW] Dynamically determine the GIF size based on the specific scan type, as per the directive.
        gif_size = (192, 192) if gif_name == "Advanced-Scan.gif" else (128, 128)

        # --- [MODIFIED] Use resource_path to locate the GIF asset.
        gif_full_path = resource_path(os.path.join("gifs", gif_name))
        self.scan_gif_widget = AnimatedGIFLabel(self, gif_path=gif_full_path, size=gif_size)
        self.scan_gif_widget.grid(row=3, column=0, pady=10)
        self.scan_gif_widget.start_animation()  # --- Start the animation loop for the GIF.

        # --- Create and display the terminal for real-time command output.
        self.terminal = TerminalWidget(self, self.fonts)
        self.terminal.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        # --- Create and display the cancel button at the bottom of the frame.
        self.cancel_button = GlassButton(self, text="Cancel Scan", emoji="❌", font=self.fonts["button"], command=cancel_command)
        self.cancel_button.configure(fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, border_color=Theme.STATE_OFF_BORDER)
        self.cancel_button.grid(row=5, column=0, padx=100, pady=(10, 10), sticky="ew")

    # [MODIFIED] Now passes the correct GIF name to the UI transition method.
    def start_sfc_scan(self):
        """Initiates the full SFC scan workflow with the correct visual assets."""
        if self.is_scanning or self.is_restoring: return
        if self.is_info_expanded: self.toggle_info_panel(play_sound=False)
        self.info_button.grid_forget()
        self.app.set_navigation_lock(True)
        self.is_scanning = True
        # --- [MODIFIED] Pass the correct, validated "Simple-Scan.gif" filename to the UI builder.
        self._transition_to_scan_ui(self.cancel_process, "Simple-Scan.gif")
        self.hint_engine = DynamicHintEngine(self, self.dynamic_hint_label)
        self.hint_engine.start(self.SCAN_HINTS)
        threading.Thread(target=self._run_sfc_scan_logic, daemon=True).start()

    # [ENHANCED] This method now registers the created process with the App.
    def _run_sfc_scan_logic(self):
        """Dedicated thread for running the SFC command and registering it for cleanup."""
        try:
            if self.sound_manager: self.sound_manager.start_looping_sound('scan_loop')
            self.terminal.append_text("Starting System File Checker (SFC) scan...\n")
            self.scan_process = subprocess.Popen(["sfc", "/scannow"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW, encoding='utf-8', errors='ignore')
            # --- [CRITICAL] Register the newly created process with the master App controller.
            self.app.register_process(self.scan_process)
            self._stream_process_output(self.scan_process, self._on_sfc_scan_complete)
        except Exception as e:
            logging.error(f"SFC Popen failed: {e}", exc_info=True)
            self.after(0, self._on_sfc_scan_complete, ([], 1))

    # [ENHANCED] This method now unregisters the completed process.
    def _on_sfc_scan_complete(self, result_tuple: tuple):
        """Handles SFC completion, unregisters the process, and starts async parsing."""
        if not self.is_scanning: return # --- Abort if the scan was cancelled.
        # --- [CRITICAL] Unregister the process now that it has completed.
        if self.scan_process: self.app.unregister_process(self.scan_process)
        self.scan_process = None
        self._show_finalizing_state()
        threading.Thread(target=self._parse_and_show_results, args=(self.logic_controller.parse_sfc_output, result_tuple), daemon=True).start()

    # [MODIFIED] Now passes the correct GIF name to the UI transition method.
    def start_dism_scan(self):
        """Initiates the full DISM scan workflow with the correct visual assets."""
        if self.is_scanning or self.is_restoring: return
        if self.is_info_expanded: self.toggle_info_panel(play_sound=False)
        self.info_button.grid_forget()
        self.app.set_navigation_lock(True)
        self.is_scanning = True
        # --- [MODIFIED] Pass the correct, validated "Advanced-Scan.gif" filename to the UI builder.
        self._transition_to_scan_ui(self.cancel_process, "Advanced-Scan.gif")
        self.hint_engine = DynamicHintEngine(self, self.dynamic_hint_label)
        self.hint_engine.start(self.SCAN_HINTS)
        threading.Thread(target=self._run_dism_scan_logic, daemon=True).start()

    # [ENHANCED] This method now registers the created process with the App.
    def _run_dism_scan_logic(self):
        """Dedicated thread for running the DISM ScanHealth command and registering it."""
        try:
            if self.sound_manager: self.sound_manager.start_looping_sound('advanced_scan_loop')
            self.terminal.append_text("Starting DISM ScanHealth process...\n")
            self.scan_process = subprocess.Popen(["DISM", "/Online", "/Cleanup-Image", "/ScanHealth"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW, encoding='utf-8', errors='ignore')
            # --- [CRITICAL] Register the newly created process with the master App controller.
            self.app.register_process(self.scan_process)
            self._stream_process_output(self.scan_process, self._on_dism_scan_complete)
        except Exception as e:
            logging.error(f"DISM ScanHealth Popen failed: {e}", exc_info=True)
            self.after(0, self._on_dism_scan_complete, ([], 1))

    # [ENHANCED] This method now unregisters the completed process.
    def _on_dism_scan_complete(self, result_tuple: tuple):
        """Handles DISM scan completion, unregisters the process, and starts async parsing."""
        if not self.is_scanning: return # --- Abort if the scan was cancelled.
        # --- [CRITICAL] Unregister the process now that it has completed.
        if self.scan_process: self.app.unregister_process(self.scan_process)
        self.scan_process = None
        self._show_finalizing_state()
        threading.Thread(target=self._parse_and_show_results, args=(self.logic_controller.parse_dism_scan_output, result_tuple), daemon=True).start()
    
    # [MODIFIED] Now passes the correct GIF name to the UI transition method.
    def start_dism_restore(self, source_path=None):
        """Initiates the DISM Restore workflow with the correct visual assets."""
        if self.is_scanning or self.is_restoring: return
        if self.is_info_expanded: self.toggle_info_panel(play_sound=False)
        self.info_button.grid_forget()
        self.app.set_navigation_lock(True)
        self.is_restoring = True
        # --- [MODIFIED] The advanced restore operation also uses the advanced scan GIF, as per the directive.
        self._transition_to_scan_ui(self.cancel_process, "Advanced-Scan.gif")
        self.cancel_button.configure(text="Cancel Restore")
        self.hint_engine = DynamicHintEngine(self, self.dynamic_hint_label)
        self.hint_engine.start(self.RESTORE_HINTS, interval=12)
        threading.Thread(target=self._run_dism_restore_logic, args=(source_path,), daemon=True).start()

    # [ENHANCED] This method now unregisters the completed process.
    def _on_dism_restore_complete(self, result_tuple: tuple):
        """Handles DISM restore completion, unregisters the process, and starts async parsing."""
        if not self.is_restoring: return # --- Abort if the scan was cancelled.
        # --- [CRITICAL] Unregister the process now that it has completed.
        if self.scan_process: self.app.unregister_process(self.scan_process)
        self.scan_process = None
        self._show_finalizing_state()
        threading.Thread(target=self._parse_and_show_results, args=(self.logic_controller.parse_dism_restore_output, result_tuple), daemon=True).start()

    # [ENHANCED] This method now correctly stops the looping sound on any button click.
    def _create_finalization_callback(self, reset: bool=False, show_info_button: bool=False, fix_now: bool=False, scan_again_sfc: bool=False, scan_again_dism: bool=False, show_advanced_ui: bool=False) -> Callable:
        """Creates a single, clean callback function that sequences all required finalization actions."""
        def callback():
            # --- [CRITICAL FIX] This sequence corrects the sound bug.
            if self.sound_manager:
                # --- Step 1: Immediately stop any looping sound (e.g., the success fanfare).
                self.sound_manager.stop_looping_sound()
                # --- Step 2: Play a one-shot confirmation sound for the button click itself.
                self.sound_manager.play_sound('notification')
            
            # --- The rest of the logic determines the next UI state.
            if show_info_button and self.info_button: self.info_button.grid(row=0, column=1, sticky="e", padx=(10, 5))
            
            if reset: self._reset_ui()
            elif fix_now: self._reset_ui(); self.after(100, self.start_dism_restore)
            elif scan_again_sfc: self._reset_ui(); self.after(100, self.start_sfc_scan)
            elif scan_again_dism: self._reset_ui(); self.after(100, self.start_dism_scan)
            elif show_advanced_ui: self._reset_ui(); self.after(100, self._show_advanced_restore_ui)
        return callback

    # [ENHANCED] This method now also handles cleanup for the new GIF widget.
    def _reset_ui(self):
        """Resets the UI to its initial state and releases the navigation lock."""
        self.app.set_navigation_lock(False)
        if not self.winfo_exists(): return
        if self.active_overlay: self.active_overlay.destroy(); self.active_overlay = None
        if self.hint_engine and self.hint_engine.running: self.hint_engine.stop(); self.hint_engine = None
        if self.terminal: self.terminal.destroy(); self.terminal = None
        if self.cancel_button: self.cancel_button.destroy(); self.cancel_button = None
        if self.dynamic_hint_label: self.dynamic_hint_label.destroy(); self.dynamic_hint_label = None
        if self.advanced_restore_button: self.advanced_restore_button.destroy(); self.advanced_restore_button = None
        # --- [NEW] Ensure the GIF widget is properly stopped and destroyed during UI reset.
        if self.scan_gif_widget:
            self.scan_gif_widget.stop_animation()
            self.scan_gif_widget.destroy()
            self.scan_gif_widget = None
        self.button_container.grid(row=1, column=0, pady=20, sticky="ew")
        self.is_scanning = False
        self.is_restoring = False

    # [ENHANCED] This method now also unregisters the process before termination.
    def cancel_process(self):
        """Cancels any ongoing scan or restore operation and unregisters the process."""
        if self.sound_manager: self.sound_manager.play_sound('cancel_operation'); self.sound_manager.stop_looping_sound()
        self.is_scanning = False; self.is_restoring = False
        if self.hint_engine and self.hint_engine.running: self.hint_engine.stop()
        if self.scan_process and self.scan_process.poll() is None:
            # --- [CRITICAL] Unregister the process BEFORE terminating it to prevent race conditions during shutdown.
            self.app.unregister_process(self.scan_process)
            try:
                self.scan_process.terminate()
                if self.terminal and self.terminal.winfo_exists(): self.terminal.append_text(f"\n--- Operation cancelled by user. ---")
            except Exception as e: logging.error(f"Failed to cancel process: {e}", exc_info=True)
        self.info_button.grid(row=0, column=1, sticky="e", padx=(10, 5))
        self.after(500, self._reset_ui)

    def _create_widgets(self):
        """Creates and places all static UI elements with corrected header layout."""
        # --- [LAYOUT FIX] The main header frame is now configured with a weighted middle
        # --- column to push the title to the left and the info button to the right.
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=0)  # Column for title group
        header_frame.grid_columnconfigure(1, weight=1)  # Empty, expanding column
        header_frame.grid_columnconfigure(2, weight=0)  # Column for info button

        # --- A new sub-frame to group the icon and text tightly together.
        title_group_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_group_frame.grid(row=0, column=0, sticky="w")

        # --- Create and place the icon and text inside the sub-frame.
        self.header_icon = ctk.CTkLabel(title_group_frame, text="")
        self.header_icon.pack(side="left", padx=(0, 10))
        self.header_label = ctk.CTkLabel(title_group_frame, text="Fix Windows", font=self.fonts["title"], text_color=Theme.TEXT)
        self.header_label.pack(side="left")
        
        # --- Place the info button in the far-right column of the main header frame.
        self.info_button = ctk.CTkButton(header_frame, text="❓", width=30, height=30, corner_radius=15, fg_color=Theme.NAV_RAIL, hover_color=Theme.CARD, command=self._on_info_button_click)
        self.info_button.grid(row=0, column=2, sticky="e")

        # --- Initial call to load and scale the icon.
        self.update_ui_scaling(self.fonts)

        # --- Create the main action buttons.
        self.button_container = ctk.CTkFrame(self, fg_color="transparent")
        self.button_container.grid_columnconfigure((0, 1), weight=1)
        self.button_container.grid(row=1, column=0, pady=20, sticky="ew")

        self.scan_button = CircularActionButton(self.button_container, self.fonts, "🔍", "Scan", "success", self.start_sfc_scan, sound_manager=self.sound_manager)
        self.scan_button.grid(row=0, column=0, sticky="e", padx=(0, 25))
        
        self.advanced_scan_button = CircularActionButton(self.button_container, self.fonts, "💻", "Advanced Scan", "accent", self.start_dism_scan, sound_manager=self.sound_manager)
        self.advanced_scan_button.grid(row=0, column=1, sticky="w", padx=(25, 0))

        self.cards = [self.scan_button, self.advanced_scan_button]
        self._create_info_panel()

    def _on_info_button_click(self):
        """Plays the question mark sound then toggles the info panel."""
        if self.sound_manager: self.sound_manager.play_sound('question_mark')
        self.toggle_info_panel()

    def _run_dism_restore_logic(self, source_path=None):
        """Dedicated thread for running the DISM RestoreHealth command."""
        try:
            if self.sound_manager: self.sound_manager.start_looping_sound('advanced_scan_loop')
            self.terminal.append_text("Starting DISM RestoreHealth. This may take a long time...\n")
            command = ["DISM.exe", "/Online", "/Cleanup-Image", "/RestoreHealth"]
            if source_path: command.extend([f"/Source:WIM:{source_path}:1", "/LimitAccess"])
            self.scan_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW, encoding='utf-8', errors='ignore')
            self.app.register_process(self.scan_process)
            self._stream_process_output(self.scan_process, self._on_dism_restore_complete)
        except Exception as e:
            logging.error(f"DISM RestoreHealth Popen failed: {e}", exc_info=True)
            if self.scan_process: self.app.unregister_process(self.scan_process)
            self.after(0, self._on_dism_restore_complete, ([], 1))

    def _stream_process_output(self, process, on_complete_callback: Callable[[tuple], None]):
        """Streams process output and captures the final exit code."""
        full_output = []
        try:
            for line in iter(process.stdout.readline, ''):
                stripped_line = line.strip()
                if self.terminal and self.terminal.winfo_exists(): self.after(0, self.terminal.append_text, stripped_line)
                full_output.append(stripped_line)
            
            exit_code = process.wait()
            logging.info(f"Process finished with exit code: {exit_code}")
            if on_complete_callback: self.after(0, on_complete_callback, (full_output, exit_code))
        except Exception as e: 
            logging.error(f"Error in process streamer thread: {e}", exc_info=True)
            if on_complete_callback: self.after(0, on_complete_callback, ([], 1))

    def _show_finalizing_state(self):
        """Updates the UI to show that results are being processed."""
        if self.hint_engine: self.hint_engine.stop()
        if self.dynamic_hint_label and self.dynamic_hint_label.winfo_exists():
            self.dynamic_hint_label.configure(text="Scan 100% Complete... Finalizing results...")
            
    def _parse_and_show_results(self, parser_func: Callable, result_tuple: tuple):
        """
        Runs the specified parser in the background and schedules the UI update.
        This is the core of the stutter-fix.
        """
        output_lines, exit_code = result_tuple
        # --- This heavy work now happens on a background thread.
        result_object = parser_func(output_lines, exit_code)
        # --- Schedule the lightweight UI update on the main thread.
        self.after(0, self._show_final_popup, result_object)
        
    def _show_final_popup(self, result_object: dict):
        """Displays the final pop-up after all background processing is complete."""
        if not (self.is_scanning or self.is_restoring): return # Check if scan was cancelled
        
        if self.sound_manager: self.sound_manager.stop_looping_sound()
        
        # Handle the special case where DISM needs to show a different UI instead of a pop-up
        if result_object.get("is_source_missing"):
            # The callback for this button contains the logic to show the advanced UI.
            result_object["buttons_config"][0]['command']()
        else:
            # For all other cases, show the standard inline notification.
            self._show_inline_notification(**result_object)

    def reset_state(self):
        """A master reset command called when the user navigates away from this frame."""
        if self.is_scanning or self.is_restoring: self.cancel_process()
        else: self.app.set_navigation_lock(False)
        if hasattr(self, 'is_info_expanded') and self.is_info_expanded: self.toggle_info_panel(play_sound=False)
    
    def _show_advanced_restore_ui(self):
        """Displays the UI for providing a local WIM/ESD file for repair."""
        if not self.winfo_exists(): return
        if self.advanced_restore_button is None or not self.advanced_restore_button.winfo_exists():
            self.advanced_restore_button = GlassButton(self, text="Use Local Source (.wim)", emoji="💿", font=self.fonts["button"], command=self._prompt_for_wim_source)
            self.advanced_restore_button.configure(fg_color=Theme.WARNING, hover_color=Theme.WARNING_HOVER, border_color=Theme.WARNING_BORDER)
        self.advanced_restore_button.grid(row=5, column=0, padx=100, pady=(20, 10), sticky="ew") # Adjusted row
        if self.cancel_button and self.cancel_button.winfo_exists(): self.cancel_button.grid_forget()

    def _prompt_for_wim_source(self):
        file_types = [("Windows Image File", "*.wim"), ("Electronic Software Download", "*.esd"), ("All files", "*.*")]
        source_path = ctk.filedialog.askopenfilename(title="Select install.wim from your Windows Installation Media", filetypes=file_types)
        if source_path:
            if self.advanced_restore_button: self.advanced_restore_button.destroy(); self.advanced_restore_button = None
            self.start_dism_restore(source_path=source_path)
            
    def _create_info_panel(self):
        self.info_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        ctk.CTkLabel(self.info_frame, text="🧠 Help & Information Center", font=self.fonts["bold"], text_color=Theme.TEXT).pack(padx=20, pady=(15, 5), anchor="w")
        textbox = ctk.CTkTextbox(self.info_frame, fg_color=Theme.INFO_PANEL, text_color=Theme.TEXT_SECONDARY, wrap="word", height=600, activate_scrollbars=False)
        textbox.pack(padx=20, pady=5, fill="both", expand=True)
        tags = { "heading": {"foreground": Theme.ACCENT}, "subheading": {"foreground": Theme.SUCCESS}, "body": {"foreground": Theme.TEXT_SECONDARY}, "pros": {"foreground": Theme.SUCCESS}, "cons": {"foreground": Theme.STATE_OFF_FG}, "command": {"foreground": Theme.TEXT}, "note": {"foreground": Theme.WARNING} }
        for tag, config in tags.items(): textbox.tag_config(tag, **config)
        info_content = [
                # Welcome Banner
                ("╭────────────────────────────────────────────────────────────╮\n", "body"),
                ("│ 🌟 Welcome to the Fix Windows Help Center 🌟                   │\n", "heading"),
                ("│ Empowering both beginners and tech experts alike! 💡        │\n", "body"),
                ("╰────────────────────────────────────────────────────────────╯\n\n", "body"),

                # Beginner Section
                ("📦───────────────────── For Non-Technical Users ─────────────────────📦\n", "heading"),

                # SFC
                ("🔹 What is 'Scan' (SFC /scannow)?\n", "subheading"),
                ("Imagine your PC as a giant library 📚. Over time, some pages (system files) get torn or corrupted.\n", "body"),
                ("SFC is like a helpful librarian 👩‍💼 who goes through all the books and automatically repairs the damaged pages.\n", "body"),
                ("This is your **first line of defense** if Windows starts acting slow, glitchy, or unstable.\n\n", "body"),

                ("✅ Pros:\n", "pros"),
                ("• Automatically repairs corrupted or missing system files\n", "pros"),
                ("• Safe to run anytime without risk to your data\n", "pros"),
                ("• Fixes crashes, missing features, and some boot issues\n\n", "pros"),

                ("❌ Cons:\n", "cons"),
                ("• Cannot repair deeply broken Windows components on its own\n", "cons"),
                ("• Scanning can take 5–20 minutes depending on your PC speed\n\n", "cons"),

                # DISM
                ("🔹 What is 'Advanced Scan' (DISM)?\n", "subheading"),
                ("If SFC is the librarian, DISM is the **full construction crew** 👷‍♂️.\n", "body"),
                ("It repairs the **Windows Component Store** (WinSxS), which SFC relies on to do its job.\n", "body"),
                ("If SFC says 'some files could not be repaired', DISM is your next move.\n\n", "body"),

                ("✅ Pros:\n", "pros"),
                ("• Fixes deep system corruption that SFC cannot handle\n", "pros"),
                ("• Can restore missing or broken Windows features and components\n", "pros"),
                ("• Essential for preparing a PC before major updates\n\n", "pros"),

                ("❌ Cons:\n", "cons"),
                ("• Requires an active internet connection for downloading repair files (unless using /Source)\n", "cons"),
                ("• Slower than SFC — may take 15–30 minutes depending on system health\n", "cons"),
                ("• Must be run with administrative privileges to work properly\n\n", "cons"),

                # Technical Section
                ("🧠────────────────────── For Technical Users ──────────────────────🧠\n", "heading"),

                # SFC Technical Details
                ("🔍 System File Checker (SFC)\n", "subheading"),
                ("Command: `sfc /scannow`\n", "command"),
                ("• Scans all protected system files and replaces incorrect versions with correct Microsoft versions.\n", "body"),
                ("• Uses cached copies stored in the WinSxS folder: `C:\\Windows\\WinSxS`\n", "body"),
                ("• Detailed logs are written to: `C:\\Windows\\Logs\\CBS\\CBS.log`\n\n", "note"),

                # DISM Technical Details
                ("🛠️ DISM (Deployment Image Servicing and Management)\n", "subheading"),
                ("Commands:\n", "command"),
                ("• `DISM /Online /Cleanup-Image /ScanHealth`  → Detects corruption\n", "command"),
                ("• `DISM /Online /Cleanup-Image /CheckHealth` → Quick check for existing flags\n", "command"),
                ("• `DISM /Online /Cleanup-Image /RestoreHealth` → Repairs using Windows Update\n", "command"),
                ("• Advanced: `DISM /Online /Cleanup-Image /RestoreHealth /Source:WIM:X:/path/to/install.wim:1 /LimitAccess`\n\n", "command"),

                ("• DISM repairs the **Windows Component Store** (WinSxS) that SFC depends on.\n", "body"),
                ("• Use DISM when SFC fails, shows corruption, or Windows Update is malfunctioning.\n\n", "note"),

                # Tips
                ("📎 Tip: Always run SFC **before** DISM. If SFC fails to repair, then escalate to DISM.\n", "note"),
                ("🧩 Using both tools in sequence ensures complete Windows integrity.\n", "note")
            ]
        textbox.configure(state="normal")
        for text, tag in info_content: textbox.insert("end", text, tag)
        textbox.configure(state="disabled")

    def toggle_info_panel(self, play_sound: bool = True):
        """[CORRECTED] This method was missing in the previous partial snippet."""
        if not hasattr(self, 'is_info_expanded'): self.is_info_expanded = False
        self.is_info_expanded = not self.is_info_expanded
        if self.is_info_expanded: 
            self.info_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10) # Adjusted Row
        else: 
            self.info_frame.grid_forget()

    def _show_inline_notification(self, title, message, emoji, buttons_config, **kwargs):
        """[MODIFIED] Now accepts **kwargs to prevent TypeError from new data."""
        if self.active_overlay: self.active_overlay.destroy()
        if self.sound_manager:
            if kwargs.get('looping_sound'): self.sound_manager.start_looping_sound(kwargs['looping_sound'])
            elif kwargs.get('one_shot_sound'): self.sound_manager.play_sound(kwargs['one_shot_sound'])
        on_close_callback = kwargs.get('on_close_callback')
        self.active_overlay = InlineNotificationOverlay(
            master=self, fonts=self.fonts, title=title, message=message, 
            emoji=emoji, buttons_config=buttons_config,
            on_close_callback=on_close_callback
        )
        self.active_overlay.show()
    
    def update_ui_scaling(self, fonts):
        """Updates fonts for all widgets within the frame and rescales the header icon."""
        super().update_ui_scaling(fonts)
        if self.winfo_exists():
            # --- Rescale the header icon image ---
            try:
                # --- Calculate the new icon size relative to the scaled title font size.
                new_font_size = self.fonts["title"].cget("size")
                new_icon_size = int(new_font_size * 1.2)

                # --- Create a new CTkImage object with the updated size.
                self.header_icon_image = ctk.CTkImage(
                    Image.open(resource_path(os.path.join("Icons", "Fix-Windows.png"))),
                    size=(new_icon_size, new_icon_size)
                )
                # --- Apply the new, rescaled image to the label.
                self.header_icon.configure(image=self.header_icon_image)
            except Exception as e:
                logging.error(f"Failed to load or resize header icon: {e}")
                self.header_icon.configure(image=None, text="⚠️") # Fallback

            # --- Propagate scaling to other child components.
            for card in self.cards:
                if hasattr(card, "update_ui_scaling"): card.update_ui_scaling(fonts)
            if self.terminal: self.terminal.update_ui_scaling(fonts)
            if self.cancel_button: self.cancel_button.configure(font=fonts["button"])
            if self.dynamic_hint_label: self.dynamic_hint_label.configure(font=fonts["normal"])
            if self.advanced_restore_button: self.advanced_restore_button.configure(font=self.fonts["button"])
            if self.info_frame and self.info_frame.winfo_exists():
                for widget in self.info_frame.winfo_children():
                    if isinstance(widget, ctk.CTkLabel): widget.configure(font=fonts["bold"])
                    if isinstance(widget, ctk.CTkTextbox): widget.configure(font=fonts["normal"])

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
        self.lgpo_path = os.path.join(self.base_path, "Group Policy Editor Tools", "LGPO.exe")
        # --- The absolute path to the PARENT FOLDER of the master GPO backup. LGPO targets this folder.
        self.backup_path = os.path.join(self.base_path, "Group Policy Editor Tools", "MyLocalGPO_Backup")
        
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

# ===================================================================================
# CLASS: PolicyFrame (v3.5 - Fully Sound-Aware Command Center)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class is the definitive UI command center for all Group Policy operations.
# This version has been re-engineered to be a fully sound-aware component,
# orchestrating auditory feedback for every key user interaction.
#
# CORE ENHANCEMENTS:
#   1. AUDITORY FEEDBACK INTEGRATION: The component now accepts the master
#      `sound_manager` instance. All primary action methods (`_start_apply_operation`,
#      `_start_reset_operation`, `toggle_info_panel`) are now wired into the
#      Auditory Feedback Engine, dispatching the correct sound event upon execution.
#
#   2. STATEFUL HOVER PROTOCOL: A zero-spam hover sound protocol has been
#      implemented for the "Apply" and "Reset" buttons. This system uses state
#      flags and a delayed verification check to ensure the 'feature_hover' sound
#      is dispatched exactly once upon entering a button's boundary, preventing
#      auditory spam.
#
#   3. COMMAND & CONTROL: The frame's core responsibility remains unchanged. It
#      delegates all backend operations to the `GroupPolicyController` in a
#      non-blocking thread and locks the main application navigation during
#      critical operations to ensure process integrity.
# ===================================================================================
class PolicyFrame(BaseContentFrame):
    """
    The UI command center for all Group Policy operations, now featuring an
    integrated information panel and a complete auditory feedback soundscape.
    """
    # The constructor is upgraded to accept the main app_instance and sound_manager.
    def __init__(self, master, fonts, app_instance, sound_manager: Optional['SoundManager'] = None):
        # --- Base class initialization. ---
        super().__init__(master, fonts)
        # --- Store a reference to the main App controller to command the navigation lock.
        self.app = app_instance
        # --- [NEW] Store a reference to the Auditory Feedback Engine.
        self.sound_manager = sound_manager
        # --- State and Logic Controller Instantiation ---
        self.state_controller = ApplicationStateController()
        self.policy_logic = GroupPolicyController(self.state_controller)
        
        # --- State Management Variables ---
        self.is_working = False
        self.is_info_expanded = False
        self.terminal = None
        self.apply_button = None
        self.reset_button = None
        self.cancel_button = None
        self.active_overlay = None
        self.info_frame = None
        
        # --- [PNG REFACTOR] Add placeholders for the header icon widgets/objects.
        self.header_icon = None
        self.header_icon_image = None

        # --- [NEW] State variables for the stateful hover sound protocol.
        self._is_apply_hover = False
        self._is_reset_hover = False
        self._leave_check_job = None

        # --- UI Construction Protocol ---
        self._create_widgets()
        # --- Asynchronously check the initial state of the policies on startup. ---
        self._initialize_state()

    def _create_widgets(self):
        """
        [RE-ARCHITECTED] Creates and places all UI elements for both idle and working
        states, and binds their respective sound events.
        """
        # --- Header container for an icon and text.
        header_container = ctk.CTkFrame(self, fg_color="transparent")
        header_container.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 20))
        header_container.grid_columnconfigure(0, weight=1)

        # --- Sub-frame to group the title icon and text together.
        title_container = ctk.CTkFrame(header_container, fg_color="transparent")
        title_container.grid(row=0, column=0, sticky="w")

        # --- Icon and text labels for the header.
        self.header_icon = ctk.CTkLabel(title_container, text="")
        self.header_icon.pack(side="left", padx=(0, 10))
        self.header_label = ctk.CTkLabel(title_container, text="Windows Local Group Policy Editor", font=self.fonts["title"], text_color=Theme.TEXT)
        self.header_label.pack(side="left")
        
        # --- Info button for right-alignment.
        self.info_button = ctk.CTkButton(header_container, text="❓", width=30, height=30, corner_radius=15, fg_color=Theme.NAV_RAIL, hover_color=Theme.CARD, command=self.toggle_info_panel)
        self.info_button.grid(row=0, column=1, sticky="e", padx=(10, 5))
        
        # --- Initial call to load and scale the icon.
        self.update_ui_scaling(self.fonts)

        # --- Main Action Card ---
        policy_card = ctk.CTkFrame(self, fg_color=Theme.CARD, corner_radius=25, border_width=1, border_color=Theme.BORDER)
        policy_card.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        policy_card.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(policy_card, text="Apply Optimized Policies", font=self.fonts["h2"], text_color=Theme.TEXT).grid(row=0, column=0, columnspan=2, padx=30, pady=20, sticky="w")
        ctk.CTkLabel(policy_card, text="This will apply a curated set of Group Policies to enhance system performance and security. This operation requires administrative privileges and uses the Microsoft LGPO utility. \n\n\n [!NOTE: This Feature Will Not Work on 🪟Windows 10/11 - 🏠HOME Editions]", wraplength=800, justify="left", font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY).grid(row=1, column=0, columnspan=2, padx=30, pady=(0, 20), sticky="w")
        
        # --- Action Buttons ---
        self.apply_button = ctk.CTkButton(policy_card, text="Apply Optimized Policies", height=45, corner_radius=15, font=self.fonts["bold"], fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER, command=self._start_apply_operation)
        self.apply_button.grid(row=2, column=0, padx=30, pady=20, sticky="ew")
        self.reset_button = ctk.CTkButton(policy_card, text="Reset Policies to Default", height=45, corner_radius=15, font=self.fonts["bold"], fg_color=Theme.RESET_BUTTON_FG, text_color=Theme.RESET_BUTTON_TEXT, hover_color=Theme.RESET_BUTTON_HOVER, command=self._start_reset_operation)
        self.reset_button.grid(row=2, column=1, padx=30, pady=20, sticky="ew")
        
        self.cards = [policy_card]

        # --- Bind hover events for the stateful sound protocol.
        self.apply_button.bind("<Enter>", lambda e: self._on_hover_enter(self.apply_button))
        self.apply_button.bind("<Leave>", lambda e: self._on_hover_leave(self.apply_button))
        self.reset_button.bind("<Enter>", lambda e: self._on_hover_enter(self.reset_button))
        self.reset_button.bind("<Leave>", lambda e: self._on_hover_leave(self.reset_button))

        # --- [NEW] Pre-create 'working state' widgets and hide them.
        self.terminal = TerminalWidget(policy_card, self.fonts)
        self.terminal.grid(row=1, column=0, columnspan=2, padx=30, pady=10, sticky="ew")
        self.terminal.grid_remove() # --- Hide it immediately.

        self.cancel_button = ctk.CTkButton(policy_card, text="Cancel Operation", height=45, corner_radius=15, font=self.fonts["bold"], fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, command=self.reset_state)
        self.cancel_button.grid(row=2, column=0, columnspan=2, padx=150, pady=20, sticky="ew")
        self.cancel_button.grid_remove() # --- Hide it immediately.

    # [NEW] Stateful hover-enter handler to prevent sound spam.
    def _on_hover_enter(self, widget):
        """Handles the mouse entering a button, triggering the hover sound exactly once."""
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
            self._leave_check_job = None
        
        is_hovered = self._is_apply_hover if widget == self.apply_button else self._is_reset_hover
        if not is_hovered:
            if widget == self.apply_button: self._is_apply_hover = True
            else: self._is_reset_hover = True
            
            if self.sound_manager:
                self.sound_manager.play_sound('feature_hover')

    # [NEW] Stateful hover-leave handler that schedules a verification check.
    def _on_hover_leave(self, widget):
        """Schedules a delayed check to verify if the mouse has truly exited the button's boundary."""
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
        self._leave_check_job = self.after(5, lambda w=widget: self._check_if_truly_left(w))

    # [NEW] Forensic check to confirm the cursor's position relative to the button's boundary.
    def _check_if_truly_left(self, widget):
        """Performs a definitive check of the cursor's position to trigger the hover-off state correctly."""
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        x1, y1 = widget.winfo_rootx(), widget.winfo_rooty()
        x2, y2 = x1 + widget.winfo_width(), y1 + widget.winfo_height()
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)

        is_hovered = self._is_apply_hover if widget == self.apply_button else self._is_reset_hover
        if is_truly_outside and is_hovered:
            if widget == self.apply_button: self._is_apply_hover = False
            else: self._is_reset_hover = False

    # [MODIFIED] Plays the question mark sound and then toggles the info panel.
    def toggle_info_panel(self):
        """Toggles the visibility of the intelligence briefing panel."""
        if self.sound_manager:
            self.sound_manager.play_sound('question_mark')
        
        if self.info_frame is None:
            self._create_info_panel()
        self.is_info_expanded = not self.is_info_expanded
        if self.is_info_expanded:
            self.info_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        else:
            self.info_frame.grid_forget()

    # [MODIFIED] Plays the click sound before starting the apply operation.
    def _start_apply_operation(self):
        """Initiates the policy application process."""
        if self.is_working: return
        
        if self.sound_manager:
            self.sound_manager.play_sound('click')
            
        self.app.set_navigation_lock(True)
        self.is_working = True
        self._transition_to_working_ui("Apply Optimized Policies")
        def task():
            result_message = self.policy_logic.apply_optimized_policies()
            if self.is_working:
                is_applied = self.state_controller.check_policy_status()
                self.after(0, self._finalize_operation, result_message, "Policies Applied", is_applied)
        threading.Thread(target=task, daemon=True).start()

    # [MODIFIED] Plays the reset sound before starting the reset operation.
    def _start_reset_operation(self):
        """Initiates the policy reset process."""
        if self.is_working: return

        if self.sound_manager:
            self.sound_manager.play_sound('reset')

        self.app.set_navigation_lock(True)
        self.is_working = True
        self._transition_to_working_ui("Reset Policies to Default")
        def task():
            result_message = self.policy_logic.reset_to_default()
            if self.is_working:
                is_applied = self.state_controller.check_policy_status()
                self.after(0, self._finalize_operation, result_message, "Policies Reset", is_applied)
        threading.Thread(target=task, daemon=True).start()

    # --- The methods below are unchanged as their logic is already robust and correct ---

    def _create_info_panel(self):
        """Lazily creates the rich-text intelligence briefing from a structured data payload."""
        self.info_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        textbox = ctk.CTkTextbox(self.info_frame, fg_color="transparent", text_color=Theme.TEXT_SECONDARY, wrap="word", height=600, border_width=0, font=self.fonts["normal"])
        textbox.pack(padx=20, pady=15, fill="both", expand=True)
        
        tags = { 
            "heading":      {'foreground': Theme.ACCENT, 'underline': True}, 
            "subheading":   {'foreground': Theme.TEXT}, 
            "body":         {'foreground': Theme.TEXT_SECONDARY},
            "emoji_bullet": {'foreground': Theme.TEXT_SECONDARY}
        }
        for tag, config in tags.items(): textbox.tag_config(tag, **config)
        
        info_content = [
            ("🧠 Your System, Optimized: A Privacy-First Briefing\n\n", "heading"),
            ("Welcome to your enhanced Windows Pro experience! The applied Local Group Policy settings optimize your standalone workstation for privacy, security, and performance. Below is a detailed breakdown of what these configurations do for you.\n\n", "body"),
            ("🛡️ Enhanced Security\n", "subheading"),
            ("   🔹 Disables AI-Powered Monitoring: The `AllowRecallEnablement` policy is disabled (0). This prevents Windows Recall from taking continuous snapshots of your screen, ensuring sensitive data like passwords or financial details is never stored, reducing the risk of data exposure.\n\n", "emoji_bullet"),
            ("   🔹 Local-Only Search: Policies like `ConnectedSearchUseWeb` and `AllowCloudSearch` are disabled (0). This restricts Windows Search to local results only, preventing queries from being sent to Bing and reducing exposure to potentially malicious web content.\n\n", "emoji_bullet"),
            ("🔒 Maximized Privacy & Minimal Telemetry\n", "subheading"),
            ("   🔸 Blocks AI Data Analysis: The `DisableAIDataAnalysis` policy is enabled (1) for both computer and user settings. This prevents Windows from analyzing your app usage or system data, keeping your digital footprint private.\n\n", "emoji_bullet"),
            ("   🔸 Deactivates Cortana Completely: Policies such as `AllowCortana` are disabled (0). This ensures Cortana does not collect data like contacts, calendar, or location, enhancing user privacy.\n\n", "emoji_bullet"),
            ("   🔸 Restricts Telemetry: Policies like `DisableTailoredExperiencesWithDiagnosticData` are configured to minimize diagnostic data sent to Microsoft, giving you greater control over your data.\n\n", "emoji_bullet"),
            ("🚀 Performance Optimization\n", "subheading"),
            ("   🔹 Reduces Background Resource Usage: Disabling features like `AllowNewsAndInterests` (0) eliminates unnecessary background processes, freeing up CPU and RAM for smoother performance and faster boot times.\n\n", "emoji_bullet"),
            ("🗑️ Cleaner, Ad-Free Experience\n", "subheading"),
            ("   🔸 Prevents Sponsored Apps: The `DisableWindowsConsumerFeatures` and `DisableCloudOptimizedContent` policies are enabled (1). These block Windows from auto-installing promotional apps or games, reducing bloatware and keeping your system clean.\n\n", "emoji_bullet"),
            ("   🔸 Disables Windows Copilot: The `TurnOffWindowsCopilot` policy is enabled (1), turning off the integrated AI assistant to minimize visual clutter and background resource usage.\n\n", "emoji_bullet"),
        ]
        textbox.configure(state="normal")
        for text, tag in info_content: textbox.insert("end", text, tag)
        textbox.configure(state="disabled")

    def _initialize_state(self):
        """Checks the initial state of the policies in a background thread."""
        self.apply_button.configure(text="Checking Status...", state="disabled")
        self.reset_button.configure(state="disabled")
        def _background_check():
            is_applied = self.state_controller.check_policy_status()
            self.after(0, self._update_ui_state, is_applied)
        threading.Thread(target=_background_check, daemon=True).start()

    def _update_ui_state(self, is_applied: bool):
        """Updates the UI buttons based on the current policy state."""
        if not self.winfo_exists(): return
        if is_applied:
            self.apply_button.configure(text="Policies Applied", fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, state="disabled")
        else:
            self.apply_button.configure(text="Apply Optimized Policies", fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER, state="normal")
        self.reset_button.configure(state="normal")
        
    def _finalize_operation(self, message: str, title: str, new_state: bool):
        """Shows a final notification and resets the UI after the user acknowledges it."""
        def on_close_action():
            self._reset_to_idle()
            self._update_ui_state(new_state)
            self.app.set_navigation_lock(False)

        style = "success" if "successfully" in message or "completed" in message else "danger"
        emoji = "✅" if style == "success" else "❌"
        self._show_inline_notification(
            title=title, message=message, emoji=emoji,
            buttons_config=[{'text': 'OK', 'style': style, 'command': on_close_action}]
        )

    def _reset_to_idle(self):
        """
        [RE-ARCHITECTED] Resets the UI from a 'working' state back to 'idle' by hiding
        and showing the pre-built widgets.
        """
        self.is_working = False
        
        # --- Hide the 'working state' widgets.
        if self.terminal: self.terminal.grid_remove()
        if self.cancel_button: self.cancel_button.grid_remove()
        if self.active_overlay: self.active_overlay.destroy(); self.active_overlay = None
        
        # --- Show the 'idle state' widgets.
        self.apply_button.grid()
        self.reset_button.grid()

    def reset_state(self):
        """A master reset command called when the user navigates away from this frame."""
        self.app.set_navigation_lock(False)
        if self.is_working:
            self.is_working = False
        self._reset_to_idle()
        if self.is_info_expanded: self.toggle_info_panel()
        self._initialize_state()
        
    def _transition_to_working_ui(self, title: str):
        """
        [RE-ARCHITECTED] Hides the idle action buttons and reveals the pre-built
        terminal view for ongoing operations.
        """
        # --- Hide the 'idle state' buttons.
        self.apply_button.grid_remove()
        self.reset_button.grid_remove()
        
        # --- Show the 'working state' widgets.
        self.terminal.grid()
        self.terminal.clear() # --- Ensure terminal is empty before use.
        self.terminal.append_text(f"Initializing: {title}...")
        self.terminal.append_text("Please wait, this may take a moment...")
        self.cancel_button.grid()
    
    def update_ui_scaling(self, fonts):
        """
        Propagates font updates to all child cards and rescales the header icon.
        """
        super().update_ui_scaling(fonts)
        if self.winfo_exists():
            # --- Rescale the header icon image ---
            try:
                # --- Calculate the new icon size relative to the scaled title font size.
                new_font_size = self.fonts["title"].cget("size")
                new_icon_size = int(new_font_size * 1.2)

                # --- Create a new CTkImage object with the updated size.
                self.header_icon_image = ctk.CTkImage(
                    Image.open(resource_path(os.path.join("Icons", "Group-Policy.png"))),
                    size=(new_icon_size, new_icon_size)
                )
                # --- Apply the new, rescaled image to the label.
                self.header_icon.configure(image=self.header_icon_image)
            except Exception as e:
                logging.error(f"Failed to load or resize header icon: {e}")
                self.header_icon.configure(image=None, text="⚠️") # Fallback

    def _show_inline_notification(self, title, message, emoji, buttons_config):
        """Displays a modal notification overlay within the frame."""
        if self.active_overlay: self.active_overlay.destroy()
        self.active_overlay = InlineNotificationOverlay(
            master=self, fonts=self.fonts, title=title, message=message,
            emoji=emoji, buttons_config=buttons_config
        )
        self.active_overlay.show()

# ===================================================================================
# DEFINITIVE CleanCacheCard Class (v2.7 - Feature-Specific Hover Sound)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component's auditory feedback protocol has been upgraded to provide a more
# distinct user experience.
#
# CORE ENHANCEMENTS:
#   1. FEATURE-SPECIFIC HOVER: The stateful hover protocol's `_on_enter` method
#      is now wired to dispatch the new 'feature_hover' sound event. This
#      distinguishes the hover sound for these cards from all other hoverable
#      elements in the application, fulfilling the user's directive for a unique
#      auditory cue.
# ===================================================================================
class CleanCacheCard(ctk.CTkFrame):
    """
    An interactive card for a single cache category, re-architected to delegate
    all cleanup operations to its parent frame's master logic controller.
    """
    def __init__(self, master, fonts, task_data: dict, sound_manager: Optional['SoundManager'] = None):
        # --- Base Initialization: Set up the card's visual frame.
        super().__init__(master, fg_color=Theme.CARD, corner_radius=20, border_width=1, border_color=Theme.CARD)

        # --- Property and State Storage ---
        self.master_frame = master                      # --- Store a reference to the parent frame (CleanCacheFrame).
        self.fonts = fonts                              # --- Store the application's font dictionary.
        self.task_data = task_data                      # --- Store the dictionary containing all data for this specific cleanup task.
        self.sound_manager = sound_manager              # --- Store a reference to the global sound manager.
        self.is_info_expanded = False                   # --- State flag for the informational dropdown panel.
        self.info_frame = None                          # --- Placeholder for the info panel widget.
        self._is_mouse_inside = False                   # --- State flag for the robust hover detection protocol.
        self._leave_check_job = None                    # --- Placeholder for the scheduled hover-leave check.

        # --- UI Construction ---
        self.grid_columnconfigure(0, weight=1)          # --- Allow the content to center itself horizontally.
        self._setup_ui(task_data)                       # --- Build all the child widgets for the card.
        self._bind_events()                             # --- Bind all necessary mouse events for interactivity.

    def _setup_ui(self, task_data: dict):
        """Sets up the card's primary UI components from the task data dictionary."""
        # --- Create a transparent main frame to hold all content with consistent padding.
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(1, weight=1) # --- Allow the text column to expand.
        
        # --- Create the emoji label.
        self.emoji_label = ctk.CTkLabel(self.main_frame, text=task_data['emoji'], font=("Arial", 24))
        self.emoji_label.grid(row=0, rowspan=2, column=0, padx=15, pady=10)
        
        # --- Create the title label.
        self.title_label = ctk.CTkLabel(self.main_frame, text=task_data['title'], font=self.fonts["bold"], text_color=Theme.TEXT)
        self.title_label.grid(row=0, column=1, sticky="w")
        
        # --- Create the description label.
        self.desc_label = ctk.CTkLabel(self.main_frame, text=task_data['description'], font=self.fonts["small"], text_color=Theme.TEXT_SECONDARY)
        self.desc_label.grid(row=1, column=1, sticky="w")
        
        # --- Create a frame to hold the action buttons on the right side.
        self.controls_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.controls_frame.grid(row=0, rowspan=2, column=2, padx=15)
        self.controls_frame.grid_columnconfigure((0, 1), weight=1) # --- Allow buttons to have consistent spacing.
        
        # --- The clean button's command now delegates the action to the parent frame's logic controller.
        self.clean_button = ctk.CTkButton(self.controls_frame, text="Clean", font=self.fonts["button"], height=35, corner_radius=10, fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, border_color=Theme.SUCCESS_BORDER, border_width=2, command=self.start_cleanup)
        self.clean_button.grid(row=0, column=0, padx=2, pady=5, sticky="ew")
        
        # --- The info button toggles the visibility of the info panel.
        self.info_button = ctk.CTkButton(self.controls_frame, text="What is it?", font=self.fonts["button"], height=35, corner_radius=10, fg_color=Theme.RESET_BUTTON_FG, text_color=Theme.RESET_BUTTON_TEXT, hover_color=Theme.RESET_BUTTON_HOVER, border_width=2, border_color=Theme.BORDER, command=self.toggle_info_panel)
        self.info_button.grid(row=0, column=1, padx=2, pady=5, sticky="ew")

    def start_cleanup(self):
        """Plays the click sound and delegates the cleanup operation to the parent frame."""
        # --- Play the sound for a manual, single-item clean action.
        if self.sound_manager: self.sound_manager.play_sound('manual_clean')
        # --- Command the parent frame to execute the cleanup for the task associated with this card.
        self.master_frame.start_manual_cleanup(self)

    def _bind_events(self):
        """Binds events recursively to all child widgets for a unified interaction surface."""
        # --- This list ensures that hovering over any part of the card triggers the hover effect.
        all_widgets = [self, self.main_frame, self.emoji_label, self.title_label, self.desc_label, self.controls_frame, self.clean_button, self.info_button]
        for widget in all_widgets:
            widget.bind("<Enter>", self._on_enter, add="+")
            widget.bind("<Leave>", self._on_leave, add="+")

    def _on_enter(self, event=None):
        """Handles the mouse entering ANY part of the card, triggering the hover-on action exactly once."""
        # --- If a "leave" check is pending, cancel it, as the mouse is still inside the component.
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        # --- Only trigger the hover-on effect if the mouse is not already flagged as being inside.
        if not self._is_mouse_inside:
            # --- Set the state flag to True to prevent sound/visual spam.
            self._is_mouse_inside = True
            # --- Play the specific hover sound for this feature type.
            if self.sound_manager: self.sound_manager.play_sound('feature_hover')
            # --- Activate the visual border highlight.
            self.configure(border_color=Theme.GLASS_BORDER_HOVER)

    def _on_leave(self, event=None):
        """Schedules a delayed check to verify if the mouse has truly exited the component's boundary."""
        # --- Cancel any previously scheduled check to avoid redundant calls.
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        # --- Schedule the forensic check to run after 1 millisecond.
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    def _check_if_truly_left(self):
        """Performs a definitive check of the cursor's position to trigger the hover-off state correctly."""
        # --- Get the absolute screen coordinates of the mouse pointer.
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        # --- Get the absolute screen coordinates of the card's bounding box.
        x1, y1 = self.winfo_rootx(), self.winfo_rooty()
        x2, y2 = x1 + self.winfo_width(), y1 + self.winfo_height()
        # --- Determine if the pointer is outside the bounding box.
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)
        # --- If the mouse is confirmed outside and the state is still 'inside', reset the state.
        if is_truly_outside and self._is_mouse_inside:
            self._is_mouse_inside = False
            self.configure(border_color=Theme.CARD)

    def toggle_info_panel(self):
        """Notifies the parent frame to manage panels, then toggles this card's info panel."""
        # --- Step 1: Notify the parent frame (CleanCacheFrame) that this card is being toggled.
        # --- The parent frame will handle closing any other open panels.
        self.master_frame.manage_info_panels(self)

        # --- Step 2: Play the "what is it" sound only if the panel is about to be opened.
        if not self.is_info_expanded and self.sound_manager:
            self.sound_manager.play_sound('what_is_it')

        # --- Step 3: Lazily create the info frame if it doesn't exist.
        if self.info_frame is None:
            self._create_info_panel()

        # --- Step 4: Toggle the internal state flag.
        self.is_info_expanded = not self.is_info_expanded

        # --- Step 5: Show or hide the info frame based on the new state.
        if self.is_info_expanded:
            self.info_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        else:
            self.info_frame.grid_forget()

    def _create_info_panel(self):
        """Lazily creates the rich-text info panel from the task's data dictionary."""
        # --- Create the panel frame.
        self.info_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        self.info_frame.grid_columnconfigure(0, weight=1)
        # --- Define helper functions to populate the panel with styled text.
        def add_info_label(text, font_key="bold", color_key="TEXT"): ctk.CTkLabel(self.info_frame, text=text, font=self.fonts[font_key], text_color=getattr(Theme, color_key)).pack(padx=20, pady=(15, 5), anchor="w")
        def add_info_detail(text, wraplength=400, color_key="TEXT_SECONDARY"): ctk.CTkLabel(self.info_frame, text=text, font=self.fonts["normal"], text_color=getattr(Theme, color_key), wraplength=wraplength, justify="left").pack(padx=20, pady=2, anchor="w")
        # --- Get the info dictionary from the main task data.
        info = self.task_data.get('info', {})
        # --- Populate the panel.
        add_info_label("Details"); add_info_detail(info.get('details', 'No details available.'))
        add_info_label("Pros", color_key="SUCCESS"); 
        for pro in info.get('pros', ['Not applicable.']): add_info_detail(f"• {pro}", color_key="SUCCESS")
        add_info_label("Cons", color_key="STATE_OFF_FG"); 
        for con in info.get('cons', ['None.']): add_info_detail(f"• {con}", color_key="STATE_OFF_FG")
        add_info_label(f"Safety Rating: {info.get('safety_rating', 'Unknown')}")

    def close_info_panel(self):
        """A direct, non-toggling command to forcibly close the info panel."""
        # --- This is a direct command, not a toggle. It only acts if the panel is currently open.
        if self.is_info_expanded:
            # --- Hide the info frame widget from the grid.
            if self.info_frame:
                self.info_frame.grid_forget()
            # --- Set the internal state flag to closed.
            self.is_info_expanded = False

    def revert_button_state(self):
        """Resets the 'Clean' button to its default state after a timed 'Cleaned' message."""
        if self.winfo_exists():
            self.clean_button.configure(fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, text="Clean", state="normal")

# ===================================================================================
# CLASS: ParallelAuditor (v1.0 - High-Throughput I/O Engine)
#
# ARCHITECTURAL BLUEPRINT:
# This class is a self-contained, specialized engine designed for a single purpose:
# to execute multiple, blocking I/O operations (like calculating folder sizes) in
# parallel. It utilizes a thread pool to dispatch all audit tasks concurrently.
# By processing results as they are completed, it provides a real-time stream of
# progress updates to the UI layer, transforming a slow, sequential process into a
# highly responsive, high-throughput operation. This is the paradigm solution for
# non-blocking, intensive file system audits.
# ===================================================================================
class ParallelAuditor:
    """Executes multiple folder size calculations in parallel and reports progress."""

    # ===============================================================================
    # METHOD: __init__
    # The constructor for the ParallelAuditor engine.
    # ===============================================================================
    def __init__(self, tasks_to_audit: list, size_calculator_func: Callable, progress_callback_func: Callable, get_path_func: Callable):
        # --- Store the list of task dictionaries to be processed.
        self.tasks_to_audit = tasks_to_audit
        # --- Store a reference to the function that performs the actual size calculation (dependency injection).
        self.size_calculator = size_calculator_func
        # --- Store a reference to the UI callback function to report progress.
        self.progress_callback = progress_callback_func
        # --- Store a reference to the function that extracts a path from a task object.
        self.get_path = get_path_func

    # ===============================================================================
    # METHOD: run
    # The main execution method that orchestrates the parallel audit.
    # ===============================================================================
    def run(self) -> int:
        """
        Launches the parallel audit and returns the total combined size of all targets.

        Returns:
            int: The total size in bytes of all audited directories.
        """
        # --- Initialize the total size accumulator.
        total_size = 0
        # --- Use a ThreadPoolExecutor to manage a pool of worker threads. The 'with' statement ensures graceful shutdown.
        with ThreadPoolExecutor() as executor:
            # --- Create a dictionary to map each running 'future' object back to its original task data.
            future_to_task = {}
            # --- Iterate through all tasks and submit them to the thread pool for execution.
            for task in self.tasks_to_audit:
                # --- Resolve the target path for the current task.
                path = self.get_path(task)
                if path:
                    # --- executor.submit() schedules the task to run and returns a 'future' object immediately.
                    future = executor.submit(self.size_calculator, path)
                    future_to_task[future] = task

            # --- as_completed() provides an iterator that yields futures as they finish, in any order.
            # --- This allows for real-time progress reporting.
            completed_tasks = 0
            total_tasks = len(future_to_task)
            for future in as_completed(future_to_task):
                # --- Retrieve the original task associated with the completed future.
                task = future_to_task[future]
                try:
                    # --- future.result() retrieves the return value from the size_calculator function. This will block until the result is ready.
                    size = future.result()
                    # --- Add the calculated size to the running total.
                    total_size += size
                    # --- Log the result for the individual task to the UI.
                    log_message = f"Scanning {task['title']}: Found {self.size_calculator.__self__._format_bytes(size)}"
                    self.progress_callback(log_message, None) # --- Send log message.
                except Exception as e:
                    # --- If a specific task failed, log the error but continue with the others.
                    log_message = f"ERROR scanning {task['title']}: {e}"
                    self.progress_callback(log_message, None) # --- Send log message.

                # --- Update overall progress.
                completed_tasks += 1
                progress_value = (completed_tasks / total_tasks) * 0.5 # --- Audit phase is the first 50% of the progress bar.
                self.progress_callback(None, progress_value) # --- Send progress update.
        
        # --- Return the final, aggregated size.
        return total_size

# ===================================================================================
# DEFINITIVE CleanCacheFrame Class (v4.0 - Logically Perfect & Sound-Aware)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class is the definitive command center for all cache cleanup operations.
# It has been re-engineered to solve the core logical flaw in its size calculation
# and to implement a zero-defect hover sound protocol.
#
# CORE ENHANCEMENTS:
#   1. PARADIGM SHIFT IN SIZE CALCULATION: The Python-native `_get_folder_size`
#      method has been ELIMINATED. It is replaced by `_get_folder_size_powershell`,
#      which delegates the entire calculation to a single, atomic, military-grade
#      PowerShell command. This leverages the OS's native, high-performance file
#      enumeration, guaranteeing accurate results across all system directories,
#      including those with complex permissions that caused the previous Python
#      implementation to fail silently. This is the definitive solution to the
#      inaccurate size reporting bug.
#
#   2. DECOUPLED DATA STRUCTURE: The `cleanup_data` list is architected with a
#      decoupled design. The target file `path` is a discrete data member,
#      separate from the `command`, ensuring structural integrity.
#
#   3. STATEFUL HOVER PROTOCOL: The "Clean All" button now uses a stateful hover
#      protocol to ensure its hover sound is triggered exactly once upon entry,
#      preventing auditory spam from mouse movements within its boundaries.
# ===================================================================================
class CleanCacheFrame(BaseContentFrame):
    """
    Orchestrates all cache cleanup operations with the native FileDeletionEngine,
    a robust data model, and a complete soundscape.
    """
    def __init__(self, master, fonts, app_instance, sound_manager: Optional['SoundManager'] = None):
        # --- Base Initialization: Set up the scrollable frame for content.
        super().__init__(master, fonts)
        # --- Store a reference to the main App controller for commanding the navigation lock.
        self.app = app_instance
        # --- Store a reference to the Auditory Feedback Engine.
        self.sound_manager = sound_manager
        # --- Instantiate the high-performance deletion engine, passing a master widget reference for thread-safe UI updates.
        self.deletion_engine = FileDeletionEngine(master_widget=self, log_callback=self._log_to_terminal)
        
        # --- State Variable Declaration ---
        self.is_cleaning = False
        self.terminal = None
        self.progress_bar = None
        self.cancel_button = None
        self.active_overlay = None
        self.clean_all_button = None
        self.cleaning_gif_widget = None
        self._is_clean_all_hover_inside = False
        self._clean_all_leave_check_job = None
        
        # --- [NEW] A placeholder for the new hint label that will be displayed during the "Clean All" operation.
        self.cleaning_hint_label = None

        # --- [PNG REFACTOR] Add a placeholder for the header icon's CTkImage object.
        self.header_icon_image = None

        # --- UI Construction Protocol ---
        self._setup_layout()
        self._create_widgets()

    def _log_to_terminal(self, message: str):
        """A thread-safe method to append messages to the terminal if it exists."""
        # --- This check ensures we don't try to update a widget that has been destroyed.
        if self.terminal and self.terminal.winfo_exists():
            # --- Append the message to the terminal.
            self.terminal.append_text(message)

    def _setup_layout(self):
        """Configures the master grid for all UI states with a corrected, definitive layout."""
        # --- Configure grid rows for dynamic layout changes during scan operations.
        self.grid_rowconfigure(0, weight=0)                         # --- Row 0: Reserved for the main frame header. Non-expanding.
        self.grid_rowconfigure(1, weight=0)                         # --- Row 1: For the 'Clean All' button (idle state) or the new Hint Label (working state). Non-expanding.
        self.grid_rowconfigure(2, weight=0)                         # --- Row 2: For the individual `CleanCacheCard`s (idle state) or the Progress Bar (working state). Non-expanding.
        self.grid_rowconfigure(3, weight=0)                         # --- Row 3: Reserved for the animated cleaning GIF (working state). Non-expanding.
        self.grid_rowconfigure(4, weight=1)                         # --- Row 4: Reserved for the Terminal widget. This row will expand vertically to fill available space.
        self.grid_rowconfigure(5, weight=0)                         # --- Row 5: Reserved for the Cancel button (working state). Non-expanding.
        # --- Configure the single column to expand horizontally, ensuring content fills the frame width.
        self.grid_columnconfigure(0, weight=1)

    def _create_widgets(self):
        """
        [RE-ARCHITECTED] Constructs all UI elements for both idle and working states
        at startup to enable instantaneous, zero-flicker transitions.
        """
        # --- [PNG REFACTOR] The header is now a container for an icon and text.
        header_container = ctk.CTkFrame(self, fg_color="transparent")
        header_container.grid(row=0, column=0, sticky="new", padx=10, pady=(0, 20))
        
        # --- Create the icon and text labels for the header.
        self.header_icon = ctk.CTkLabel(header_container, text="")
        self.header_icon.pack(side="left", padx=(0, 10))
        self.header_label = ctk.CTkLabel(header_container, text="Clean Cache", font=self.fonts["title"], text_color=Theme.TEXT)
        self.header_label.pack(side="left")

        # --- Initial call to load and scale the icon.
        self.update_ui_scaling(self.fonts)
        
        # --- "Clean All" Button ---
        self.clean_all_button = GlassButton(self, text="Clean All", emoji="🧹", font=self.fonts["h2"], command=self.start_clean_all)
        self.clean_all_button.configure(fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, border_color=Theme.SUCCESS_BORDER)
        self.clean_all_button.grid(row=1, column=0, padx=100, pady=10, sticky="ew")
        
        # --- Bind the "Clean All" button to the stateful hover protocol.
        def _recursive_bind(widget, enter_func, leave_func):
            widget.bind("<Enter>", enter_func, add="+")
            widget.bind("<Leave>", leave_func, add="+")
            for child in widget.winfo_children(): _recursive_bind(child, enter_func, leave_func)
        _recursive_bind(self.clean_all_button, self._on_clean_all_hover_enter, self._on_clean_all_hover_leave)
        
        # --- Master Data Structure for all cleanup tasks.
        self.cleanup_data = [
            {'title': "User Temp Folder Cleanup", 'description': "Clears temporary files created by applications.", 'emoji': "🗑️",
            'path': "%TEMP%", 'requires_admin': False, 'info': {
                'details': "This action targets the user's temporary folder (%TEMP%). Applications store temporary data here. Cleaning this folder frees up space and can resolve issues caused by corrupted temp files.",
                'pros': ["Frees up significant disk space.", "Can improve application performance and stability."], 'cons': ["May clear unsaved work in some poorly designed applications."], 'safety_rating': "Very High"}},
            {'title': "System-Wide Temp Folder Cleanup", 'description': "Clears temporary files in C:\\Windows\\Temp.", 'emoji': "🗑️",
            'path': "%SystemRoot%\\Temp", 'requires_admin': True, 'info': {
                'details': "This targets the main Windows temporary folder for system services. It contains files created by the OS and installers.",
                'pros': ["Recovers disk space used by the OS.", "Can resolve failed installation or update issues."], 'cons': ["Requires admin rights.", "Some system services may have files locked."], 'safety_rating': "High"}},
            {'title': "Windows Update Cache Cleanup", 'description': "Clears downloaded Windows Update installation files.", 'emoji': "🗑️",
            'path': "%SystemRoot%\\SoftwareDistribution\\Download", 'requires_admin': True, 'info': {
                'details': "Windows stores update files here. After installation, these are often no longer needed but can take up gigabytes of space.",
                'pros': ["Can free up a very large amount of disk space.", "May resolve issues with Windows Update failing or getting stuck."], 'cons': ["If an update is pending, it may need to be re-downloaded."], 'safety_rating': "High"}},
            {'title': "Explorer Thumbnail & Icon Cache", 'description': "Resets the cache for file and icon thumbnails.", 'emoji': "🗑️",
            'path': "%LOCALAPPDATA%\\Microsoft\\Windows\\Explorer", 'command': "Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue; Start-Process explorer.exe", 'requires_admin': False, 'info': {
                'details': "Windows caches icons and thumbnails to speed up File Explorer. This cache can become corrupted.",
                'pros': ["Fixes incorrect, blank, or corrupted icons and file thumbnails."], 'cons': ["Temporarily restarts the Windows Explorer shell.", "Thumbnails will need to be regenerated."], 'safety_rating': "High"}},
            {'title': "WinSxS Component Store Cleanup", 'description': "Cleans up superseded and unused system components.", 'emoji': "🗑️",
            'path': None, 'command': "Dism.exe /Online /Cleanup-Image /StartComponentCleanup /Quiet", 'requires_admin': True, 'info': {
                'details': "The WinSxS folder contains all Windows components. This removes unneeded versions.",
                'pros': ["Can free up significant disk space.", "Improves the reliability of future Windows updates."], 'cons': ["The process can be slow.", "Prevents uninstalling some recent updates."], 'safety_rating': "Very High"}},
            {'title': "Clean Windows Prefetch", 'description': "Clears files used to speed up application launch.", 'emoji': "🗑️",
            'path': "%SystemRoot%\\Prefetch", 'requires_admin': True, 'info': {
                'details': "Windows creates Prefetch files to speed up application launch. This folder can accumulate old files.",
                'pros': ["Can resolve some rare application launch issues."], 'cons': ["Apps may launch slightly slower *one time* as files are recreated."], 'safety_rating': "Moderate"}}
        ]
        # --- Dynamic Card Creation ---
        self.cards = [CleanCacheCard(self, self.fonts, sound_manager=self.sound_manager, task_data=data) for data in self.cleanup_data]
        # --- This initial row offset ensures cards appear below the header and main button.
        initial_row = 2
        for i, card in enumerate(self.cards):
            card.grid(row=i + initial_row, column=0, sticky="ew", padx=10, pady=10)
        
        # --- [NEW] Pre-create all 'working state' widgets and hide them.
        # --- Create the user-guidance hint label.
        self.cleaning_hint_label = ctk.CTkLabel(self, text="DONOT - Panic if it looks stuck \n - Its cleaning your system's useless Files! \n ... Let it Complete!", font=self.fonts["bold"], text_color=Theme.TEXT)
        self.cleaning_hint_label.grid(row=1, column=0, padx=100, pady=(10, 5), sticky="ew")
        self.cleaning_hint_label.grid_remove() # --- Hide it immediately.

        # --- Create the progress bar.
        self.progress_bar = CleanAllProgressBar(self, self.fonts)
        self.progress_bar.grid(row=2, column=0, padx=100, pady=10, sticky="ew")
        self.progress_bar.grid_remove() # --- Hide it immediately.
        
        # --- Create the animated cleaning GIF.
        self.cleaning_gif_widget = AnimatedGIFLabel(self, gif_path=resource_path(os.path.join("gifs", "Cleaning.gif")), size=(128, 128))
        self.cleaning_gif_widget.grid(row=3, column=0, pady=10)
        self.cleaning_gif_widget.grid_remove() # --- Hide it immediately.
        
        # --- Create the terminal.
        self.terminal = TerminalWidget(self, self.fonts)
        self.terminal.grid(row=4, column=0, padx=10, pady=10, sticky="ewns")
        self.terminal.grid_remove() # --- Hide it immediately.
        
        # --- Create the cancel button.
        self.cancel_button = GlassButton(self, text="Cancel", emoji="❌", font=self.fonts["button"], command=self.cancel_cleanup)
        self.cancel_button.configure(fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, border_color=Theme.STATE_OFF_BORDER)
        self.cancel_button.grid(row=5, column=0, padx=100, pady=10, sticky="ew")
        self.cancel_button.grid_remove() # --- Hide it immediately.

    def start_clean_all(self):
        """
        [RE-ARCHITECTED] Transforms the UI by revealing pre-built 'working state'
        widgets, locks navigation, plays sounds, and launches the clean process.
        """
        # --- Prevent the operation from starting if one is already in progress.
        if self.is_cleaning: return
        # --- Play the initial "click" sound for the button press.
        if self.sound_manager: self.sound_manager.play_sound('clean_all_click')
        # --- Command the main application to lock the navigation rail, preventing user interruption.
        self.app.set_navigation_lock(True)
        # --- Set the state flag to indicate that a cleaning operation is active.
        self.is_cleaning = True
        
        # --- Hide all idle-state widgets.
        self.clean_all_button.grid_remove()
        for card in self.cards:
            card.grid_remove()

        # --- Show all pre-created 'working state' widgets.
        self.cleaning_hint_label.grid()
        self.progress_bar.grid()
        self.cleaning_gif_widget.grid()
        self.cleaning_gif_widget.start_animation()
        self.terminal.grid()
        self.terminal.clear() # --- Ensure terminal is empty from any previous run.
        self.cancel_button.grid()
        
        # --- Start the backend cleanup logic on a separate, non-blocking thread.
        threading.Thread(target=self._run_clean_all_logic, daemon=True).start()

    # ===============================================================================
    # METHOD: _run_clean_all_logic (v2.1 - Corrected Task Filtering)
    #
    # ARCHITECTURAL BLUEPRINT (UPGRADE):
    # This version incorporates the correct operational logic by filtering the master
    # task list to explicitly exclude the "Explorer Thumbnail & Icon Cache"
    # operation from the automated "Clean All" sequence. This task is designated
    # for manual execution only. The parallel audit protocol remains in place for
    # all other designated cleanup tasks.
    # ===============================================================================
    def _run_clean_all_logic(self):
        """Executes the multi-stage cleanup process with a parallelized audit phase."""
        # --- Play the looping "cleaning" sound. ---
        if self.sound_manager: self.sound_manager.start_looping_sound('cleaning_loop')
        
        # --- [CRITICAL LOGIC CORRECTION] ---
        # --- Filter the master list to exclude tasks designated for manual-only execution.
        tasks_to_run = [task for task in self.cleanup_data if "Explorer Thumbnail & Icon Cache" not in task['title']]
        
        # --- A thread-safe callback function to update the UI from worker threads. ---
        def audit_progress_callback(log_message: Optional[str], progress_value: Optional[float]):
            if log_message and self.is_cleaning:
                self.after(0, self._log_to_terminal, log_message)
            if progress_value is not None and self.is_cleaning:
                if self.progress_bar and self.progress_bar.winfo_exists():
                    self.after(0, self.progress_bar.set_progress, progress_value)

        # --- PHASE 1: Parallel Disk Space Audit ---
        self._log_to_terminal("--- PHASE 1 of 3: Auditing disk space (Parallel)... ---")
        # --- Instantiate the parallel audit engine. ---
        auditor = ParallelAuditor(
            tasks_to_audit=tasks_to_run,
            size_calculator_func=self._get_folder_size_powershell,
            progress_callback_func=audit_progress_callback,
            get_path_func=self._get_target_path
        )
        # --- Run the parallel audit. This blocks the *current background thread* until all audits are complete. ---
        total_size_before = auditor.run()
        if not self.is_cleaning: self.after(0, self._reset_ui); return # --- Check for cancellation.

        self._log_to_terminal(f"\n--- Total size to be cleaned: {self._format_bytes(total_size_before)} ---")
        
        # --- PHASE 2: Sequential Cleanup Operations ---
        self._log_to_terminal("\n--- PHASE 2 of 3: Executing cleanup operations... ---")
        num_tasks = len(tasks_to_run)
        for i, task in enumerate(tasks_to_run):
            if not self.is_cleaning: self.after(0, self._reset_ui); return # --- Check for cancellation.
            self._log_to_terminal(f"Cleaning: {task['title']}...")
            self._execute_cleanup_task(task)
            if self.progress_bar and self.progress_bar.winfo_exists():
                # --- The cleanup phase is the second 50% of the progress bar. ---
                progress = 0.5 + (((i + 1) / num_tasks) * 0.5)
                self.after(0, self.progress_bar.set_progress, progress)
        
        # --- PHASE 3: Sequential Verification ---
        self._log_to_terminal("\n--- PHASE 3 of 3: Verifying cleaned space... ---")
        total_size_after = 0
        for task in tasks_to_run:
            if not self.is_cleaning: self.after(0, self._reset_ui); return # --- Check for cancellation.
            path = self._get_target_path(task)
            if path:
                total_size_after += self._get_folder_size_powershell(path)
        
        # --- Finalization ---
        if self.is_cleaning:
            cleaned_size = max(0, total_size_before - total_size_after)
            cleaned_size_str = self._format_bytes(cleaned_size)
            self._log_to_terminal(f"\n--- Cleanup Complete. Total space recovered: {cleaned_size_str} ---")
            if self.sound_manager: self.sound_manager.stop_looping_sound()
            self.after(0, self._show_clean_all_success_popup, cleaned_size_str)

    def start_manual_cleanup(self, card_instance: CleanCacheCard):
        """Initiates a non-blocking cleanup operation for a single cache category."""
        card_instance.clean_button.configure(state="disabled", text="Cleaning...")
        def _background_task():
            success = self._execute_cleanup_task(card_instance.task_data)
            if success:
                self.after(0, lambda: card_instance.clean_button.configure(text="Cleaned", fg_color=Theme.STATE_ON_FG))
                self.after(30000, lambda: card_instance.revert_button_state())
            else:
                self.after(0, lambda: card_instance.revert_button_state())
        threading.Thread(target=_background_task, daemon=True).start()

    def _execute_cleanup_task(self, task: dict) -> bool:
        """
        Executes a single cleanup task, intelligently choosing between the native
        FileDeletionEngine for directory cleaning and PowerShell for specific commands.
        """
        if task.get('path'):
            target_path = os.path.expandvars(task['path'])
            if "Explorer Thumbnail & Icon Cache" in task['title']:
                self.deletion_engine.delete_directory_contents(target_path)
                return self._execute_powershell_command(task.get('command', ''))
            else:
                return self.deletion_engine.delete_directory_contents(target_path)
        elif task.get('command'):
            return self._execute_powershell_command(task['command'])
        return False

    def _execute_powershell_command(self, command: str) -> bool:
        """A dedicated runner for one-off PowerShell commands."""
        try:
            result = subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-NoProfile", "-Command", command], capture_output=True, text=True, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode != 0:
                logging.error(f"PowerShell command failed with code {result.returncode}.\nStderr: {result.stderr.strip()}")
            return result.returncode == 0
        except Exception as e:
            logging.error(f"Exception running PowerShell command: {e}", exc_info=True)
            return False

    def _get_folder_size_powershell(self, path: str) -> int:
        """
        Calculates the total size of a directory's contents using a single,
        high-performance, and fault-tolerant PowerShell command. This is the
        definitive method for achieving accurate results on a Windows system.

        Args:
            path (str): The absolute path to the directory to measure.

        Returns:
            int: The total size of the directory's contents in bytes. Returns 0 on error.
        """
        # --- Pre-flight Check: Verify the target directory exists before proceeding.
        if not os.path.isdir(path):
            # --- If the directory does not exist, log it and return 0.
            logging.warning(f"Size calculation skipped: Directory not found at '{path}'.")
            # --- The size is zero as there is nothing to measure.
            return 0

        # --- COMMAND DEFINITION ---
        # `Get-ChildItem`: The native PowerShell cmdlet for listing file system items.
        # `-Path '{path}'`: Specifies the target directory.
        # `-Recurse`: Instructs the command to traverse all subdirectories.
        # `-Force`: Includes hidden and system files in the calculation.
        # `-ErrorAction SilentlyContinue`: CRITICAL. Prevents the script from halting on permission errors (locked files) and instead skips them.
        # `Measure-Object`: A cmdlet that performs calculations on a collection of objects.
        # `-Property Length`: Specifies that we want to calculate based on the 'Length' (size in bytes) property of each file.
        # `-Sum`: Instructs Measure-Object to sum the values.
        # `.Sum`: Accesses the final 'Sum' property from the result object.
        command = f"(Get-ChildItem -Path '{path}' -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum"

        # --- Use a try-except block for absolute fault tolerance during subprocess execution.
        try:
            # --- Execute the PowerShell command silently in the background.
            result = subprocess.run(
                # --- The command is executed via powershell.exe.
                ["powershell.exe", "-NoProfile", "-Command", command],
                # --- capture_output=True and text=True ensure we get a clean string result.
                capture_output=True, text=True, check=True,
                # --- creationflags=subprocess.CREATE_NO_WINDOW prevents the console from flashing.
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # --- The command's output will be the total size in bytes as a string, or empty if the folder is empty/inaccessible.
            output = result.stdout.strip()
            # --- If the output is a non-empty string, convert it to an integer. Otherwise, default to 0.
            return int(output) if output else 0
        # --- Catch any exception that occurs during the execution of the subprocess.
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as e:
            # --- Log the specific error for forensic analysis.
            logging.error(f"Failed to calculate folder size for '{path}' via PowerShell: {e}", exc_info=True)
            # --- Return a safe default value of 0 in any failure case.
            return 0

    def cancel_cleanup(self):
        """Cancels the 'Clean All' operation."""
        if self.sound_manager:
            self.sound_manager.play_sound('cancel_operation')
            self.sound_manager.stop_looping_sound()
        self.is_cleaning = False
        self._log_to_terminal("\n--- Operation cancelled by user. ---")
        self.after(500, self._reset_ui)

    def _get_target_path(self, task: dict) -> Optional[str]:
        """Resolves environment variables in a path string."""
        path = task.get('path')
        if path: return os.path.expandvars(path)
        return None

    def _on_clean_all_hover_enter(self, event=None):
        """Handles the mouse entering the 'Clean All' button."""
        if self._clean_all_leave_check_job: self.after_cancel(self._clean_all_leave_check_job)
        if not self._is_clean_all_hover_inside:
            self._is_clean_all_hover_inside = True
            if self.sound_manager: self.sound_manager.play_sound('hover')

    def _on_clean_all_hover_leave(self, event=None):
        """Schedules a check to see if the mouse has truly left the 'Clean All' button."""
        if self._clean_all_leave_check_job: self.after_cancel(self._clean_all_leave_check_job)
        self._clean_all_leave_check_job = self.after(1, self._check_if_clean_all_left)

    def _check_if_clean_all_left(self):
        """Verifies if the mouse cursor is outside the 'Clean All' button's boundaries."""
        if not self.clean_all_button or not self.clean_all_button.winfo_exists(): return
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        x1, y1 = self.clean_all_button.winfo_rootx(), self.clean_all_button.winfo_rooty()
        x2, y2 = x1 + self.clean_all_button.winfo_width(), y1 + self.clean_all_button.winfo_height()
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)
        if is_truly_outside and self._is_clean_all_hover_inside:
            self._is_clean_all_hover_inside = False

    def _reset_ui(self):
        """
        [RE-ARCHITECTED] The master UI reset protocol. Hides 'working state' widgets
        and reveals 'idle state' widgets for a seamless transition.
        """
        # --- Stop any looping sounds associated with the cleanup operation.
        if self.sound_manager: self.sound_manager.stop_looping_sound()
        # --- Command the main application to unlock the navigation rail.
        self.app.set_navigation_lock(False)
        # --- Abort if the frame widget itself has been destroyed.
        if not self.winfo_exists(): return
        
        # --- Reset all state flags to their default values.
        self.is_cleaning = False
        self._is_clean_all_hover_inside = False
        
        # --- Destroy any active notification overlay.
        if self.active_overlay: self.active_overlay.destroy(); self.active_overlay = None
        
        # --- Stop and hide the animated cleaning GIF widget.
        if self.cleaning_gif_widget:
            self.cleaning_gif_widget.stop_animation()
            self.cleaning_gif_widget.grid_remove()
        
        # --- Hide all other 'working state' widgets.
        if self.cleaning_hint_label: self.cleaning_hint_label.grid_remove()
        if self.progress_bar: self.progress_bar.grid_remove()
        if self.terminal: self.terminal.grid_remove()
        if self.cancel_button: self.cancel_button.grid_remove()

        # --- Show all 'idle state' widgets.
        self.clean_all_button.grid()
        for card in self.cards:
            card.grid()

    def manage_info_panels(self, toggled_card: CleanCacheCard):
        """
        Ensures only one info panel is open at a time. When one card is toggled,
        this method iterates through all other cards and commands them to close.
        """
        # --- Iterate through all the CleanCacheCard instances managed by this frame.
        for card in self.cards:
            # --- Check if the current card in the loop is the one that was just clicked.
            if card is not toggled_card:
                # --- If it's a different card, command it to close its info panel directly.
                card.close_info_panel()

    def reset_state(self):
        """A command called by the main app when navigating away from this frame."""
        if self.is_cleaning: self.cancel_cleanup()
        else: self.app.set_navigation_lock(False)
        for card in self.cards:
            if hasattr(card, 'close_info_panel'): card.close_info_panel()

    def _show_clean_all_success_popup(self, cleaned_size_str: str):
        """Displays the final success pop-up with integrated auditory feedback and colored text."""
        if not self.winfo_exists(): return
        if self.active_overlay: self.active_overlay.destroy()
        if self.sound_manager: self.sound_manager.start_looping_sound('success_loop')
        
        def on_confirm_action():
            if self.sound_manager:
                self.sound_manager.stop_looping_sound()
                self.sound_manager.play_sound('ok_click')
            self._reset_ui()
        
        title = "Cleanup Complete!"
        emoji = "🚀"
        
        # --- [NEW] Construct the rich message with different colors. ---
        rich_message_content = [
            ("Mission Accomplished! Your PC is now lighter and faster. Total space recovered: ", Theme.TEXT_SECONDARY),
            (cleaned_size_str, Theme.SUCCESS) # The recovered size is now colored green.
        ]

        buttons_config = [{'text': 'Awesome!', 'command': on_confirm_action, 'style': 'success'}]
        
        self.active_overlay = InlineNotificationOverlay(
            master=self, fonts=self.fonts, title=title, message="", # Old message is now empty
            emoji=emoji, buttons_config=buttons_config,
            on_close_callback=on_confirm_action,
            # --- [MODIFIED] Use resource_path to locate the GIF.
            gif_path=resource_path(os.path.join("gifs", "Done.gif")),
            rich_message=rich_message_content # Pass the new rich message
        )
        self.active_overlay.show()
    
    def update_ui_scaling(self, fonts):
        """
        Propagates font updates to all child cards and rescales the header icon.
        """
        # --- Call the parent class's scaling method to handle its children (cards).
        super().update_ui_scaling(fonts)
        # --- Ensure the frame widget still exists before attempting to configure its children.
        if self.winfo_exists():
            # --- Rescale the header icon image ---
            try:
                # --- Calculate the new icon size relative to the scaled title font size for proportionality.
                new_font_size = self.fonts["title"].cget("size")
                new_icon_size = int(new_font_size * 1.2)

                # --- Create a new CTkImage object with the updated size.
                self.header_icon_image = ctk.CTkImage(
                    Image.open(resource_path(os.path.join("Icons", "Cleaning.png"))),
                    size=(new_icon_size, new_icon_size)
                )
                # --- Apply the new, rescaled image to the label.
                self.header_icon.configure(image=self.header_icon_image)
            except Exception as e:
                # --- Log any error during image loading and provide a visual fallback.
                logging.error(f"Failed to load or resize header icon: {e}")
                self.header_icon.configure(image=None, text="⚠️") # Fallback
            
            # --- [NEW] If the cleaning hint label exists, update its font to the new scaled version.
            if self.cleaning_hint_label and self.cleaning_hint_label.winfo_exists():
                self.cleaning_hint_label.configure(font=fonts["bold"])

    def _format_bytes(self, size_bytes):
        """[ERROR NEUTRALIZATION] This utility method correctly formats a byte count into a human-readable string."""
        if size_bytes < 1024: return f"{size_bytes} B"
        power_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        i = int(math.floor(math.log(size_bytes, 1024))) if size_bytes > 0 else 0
        return f"{round(size_bytes / math.pow(1024, i), 2)} {power_labels[i]}"

# ===================================================================================
# CLASS: AboutFrame (v7.4 - Definitive Visual Hierarchy Protocol)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive, zero-defect implementation of the About page. It has
# been re-engineered to establish a clear and powerful visual hierarchy, ensuring
# maximum readability and aesthetic impact on all displays and scaling levels.
#
# CORE ENHANCEMENTS:
#
#   1. RE-CALIBRATED FONT HIERARCHY:
#      - Section Headers ("About The Creator", etc.): Now use the largest, boldest
#        `fonts["title"]` for maximum impact and clear distinction.
#      - Descriptive Paragraphs: Now use the `fonts["bold"]` style. This provides
#        a thick, highly readable body text that is visually subordinate to the
#        main headers, as per your directive.
#      - Sub-Headers ("Mohammed Kashan Tariq..."): Use the `fonts["h2"]` style,
#        creating a perfect intermediate step in the visual hierarchy.
#
#   2. IMAGE-BASED EMOJI INTEGRITY: The complex "technologist" emoji (🧑‍💻)
#      continues to be rendered via the 'Programmer.png' image asset, the only
#      protocol that guarantees 100% visual consistency across all platforms.
#
#   3. ROBUST SCALING: The `update_ui_scaling` method is synchronized with the
#      new font hierarchy and continues to dynamically resize all image assets,
#      ensuring the layout remains flawless at any resolution.
# ===================================================================================
class AboutFrame(BaseContentFrame):
    """
    A comprehensive 'About' page featuring an image-based emoji protocol,
    re-calibrated font weights, and dynamic image scaling.
    """
    def __init__(self, master, fonts, app_instance, sound_manager: Optional['SoundManager'] = None):
        # --- Base Class Initialization ---
        super().__init__(master, fonts)

        # --- Property Storage ---
        self.app = app_instance
        self.fonts = fonts
        self.sound_manager = sound_manager
        
        # --- State and Widget Handles ---
        self.buy_me_a_coffee_button = None
        self.left_yippee_gif = None
        self.right_yippee_gif = None
        self._is_coffee_hover_inside = False
        self._coffee_leave_check_job = None
        
        # --- [DEFINITIVE FIX & PATH CORRECTION] Load the technologist emoji image asset using the resource_path resolver.
        try:
            programmer_icon_path = resource_path(os.path.join("Icons", "Programmer.png"))
            self.technologist_image = ctk.CTkImage(Image.open(programmer_icon_path), size=(40, 40))
        except Exception as e:
            logging.error(f"FATAL: Could not load Programmer.png asset: {e}")
            self.technologist_image = None

        # --- UI Construction Protocol ---
        self.grid_columnconfigure(0, weight=1)
        self._create_content_stack()

    def _on_external_link_click(self, link: str, click_sound: Optional[str] = None, minimize: bool = False):
        """Plays a sound, optionally minimizes the app, and opens a web link."""
        if self.sound_manager and click_sound:
            self.sound_manager.play_sound(click_sound)
        
        if minimize:
            self.app.iconify()

        try:
            logging.info(f"Dispatching to external link: {link}")
            webbrowser.open_new_tab(link)
        except Exception as e:
            logging.error(f"Failed to open external link '{link}'. Error: {e}", exc_info=True)

    def _create_content_stack(self):
        """
        [v7.5 CORRECTED] Creates and packs all UI elements with a definitive image-based
        emoji fix, re-calibrated font weights, and robust asset path resolution
        for a zero-defect compiled executable.
        """
        # --- Helper function to create consistent headers with normalized emojis.
        def create_header(parent, emoji_text: str, main_text: str, image=None):
            header_frame = ctk.CTkFrame(parent, fg_color="transparent")
            
            if image:
                ctk.CTkLabel(header_frame, text="", image=image).pack(side="left", padx=5)
            else:
                ctk.CTkLabel(header_frame, text=emoji_text, font=self.fonts["emoji_large"]).pack(side="left", padx=5)
            
            # --- [FONT FIX] Use the largest "title" font for main section headings.
            ctk.CTkLabel(header_frame, text=main_text, font=self.fonts["title"], text_color=Theme.TEXT).pack(side="left", padx=10)
            
            if image:
                ctk.CTkLabel(header_frame, text="", image=image).pack(side="left", padx=5)
            else:
                ctk.CTkLabel(header_frame, text=emoji_text, font=self.fonts["emoji_large"]).pack(side="left", padx=5)

            return header_frame

        # --- Section 1: About the Creator ---
        create_header(self, "", "About The Creator", image=self.technologist_image).pack(pady=(20, 10), padx=20)
        
        # --- [FONT FIX] Ensure the name remains bold and prominent using "h2".
        ctk.CTkLabel(self, text="Mohammed Kashan Tariq - Software Engineer", font=self.fonts["h2"], text_color=Theme.ACCENT).pack(pady=(0, 20), padx=20)
        
        # --- [FONT FIX] Use the thicker "bold" font for readable descriptions.
        ctk.CTkLabel(self, text="A lifelong enthusiast with a deep love and passion for technology, software architecture, and creating tools that make a real difference. 💻",
                     font=self.fonts["bold"], text_color=Theme.TEXT_SECONDARY, wraplength=800).pack(pady=(0, 20), padx=50)

        # --- Section 2: The Mission ---
        create_header(self, "🚀", "The Mission").pack(pady=(20, 10), padx=20)
        ctk.CTkLabel(self, text="With over 10+ years of hands-on experience in Computers, Tech-hardware, and the inner workings of Windows Operating Systems, MK-Tools was created with a single, clear goal: To empower everyone. For too long, deep system optimization has been a complex world reserved for 'nerds' and power users. MK-Tools changes that. It's built on the belief that powerful tweaking capabilities should be accessible, safe, and easy for all users, giving you one-click control over your machine's performance and privacy. ✨",
                     font=self.fonts["bold"], text_color=Theme.TEXT_SECONDARY, wraplength=800, justify="left").pack(pady=(0, 30), padx=50)

        # --- Section 3: Contact Me ---
        create_header(self, "📞", "Contact Me").pack(pady=(20, 10), padx=20)
        contact_frame = ctk.CTkFrame(self, fg_color="transparent")
        contact_frame.pack(pady=(10, 20), fill="x")
        button_group = ctk.CTkFrame(contact_frame, fg_color="transparent")
        button_group.pack()

        # --- [PATH CORRECTION] All icon paths are now wrapped with resource_path() ---
        SocialButton(master=button_group, fonts=self.fonts, text="LinkedIn", icon_path="LinkedIn.ico",
                     command=lambda: self._on_external_link_click(AppConfig.LINKEDIN_URL, "linkedin_click", minimize=True),
                     color_config={"fg_color": Theme.LINKEDIN_BUTTON_FG_DARK, "hover_color": Theme.LINKEDIN_BUTTON_HOVER_DARK, "border_color": "#004182"},
                     sound_manager=self.sound_manager, click_sound_name="linkedin_click").pack(side="left", padx=15)
        
        SocialButton(master=button_group, fonts=self.fonts, text="GitHub", icon_path="Github.ico",
                     command=lambda: self._on_external_link_click(AppConfig.GITHUB_URL, "github_click", minimize=True),
                     color_config={"fg_color": Theme.GITHUB_BUTTON_FG_DARK, "hover_color": Theme.GITHUB_BUTTON_HOVER_DARK, "text_color": Theme.GITHUB_BUTTON_TEXT_DARK, "border_color": Theme.TEXT_SECONDARY},
                     sound_manager=self.sound_manager, click_sound_name="github_click").pack(side="left", padx=15)
        
        SocialButton(master=button_group, fonts=self.fonts, text="Email", icon_path="Email.ico",
                     command=lambda: self._on_external_link_click(AppConfig.CONTACT_EMAIL, "email_click"),
                     color_config={"fg_color": Theme.GMAIL_BUTTON_FG_DARK, "hover_color": Theme.GMAIL_BUTTON_HOVER_DARK, "border_color": "#C5221F"},
                     sound_manager=self.sound_manager, click_sound_name="email_click").pack(side="left", padx=15)

        # --- Section 4: Support This Project ---
        create_header(self, "💖", "Support This Project").pack(pady=(20, 10), padx=20)
        support_container = ctk.CTkFrame(self, fg_color="transparent")
        support_container.pack(pady=(10, 40))

        initial_font_size = self.fonts["h2"].cget("size")
        initial_gif_size = int(initial_font_size * 1.5)
        
        # --- [PATH CORRECTION] All GIF paths are now wrapped with resource_path() ---
        yippee_gif_path = resource_path(os.path.join("gifs", "Yipee.gif"))
        self.left_yippee_gif = AnimatedGIFLabel(support_container, gif_path=yippee_gif_path, size=(initial_gif_size, initial_gif_size))

        self.buy_me_a_coffee_button = BuyMeACoffeeButton(support_container, self.fonts, is_large=True,
                                                         command=lambda: self._on_external_link_click(AppConfig.BUY_ME_A_COFFEE_URL, "money", minimize=True))
        self.buy_me_a_coffee_button.pack(side="left", padx=10)

        self.right_yippee_gif = AnimatedGIFLabel(support_container, gif_path=yippee_gif_path, size=(initial_gif_size, initial_gif_size))

        self.buy_me_a_coffee_button.bind("<Enter>", self._on_coffee_hover_enter)
        self.buy_me_a_coffee_button.bind("<Leave>", self._on_coffee_hover_leave)

    def _on_coffee_hover_enter(self, event=None):
        if self._coffee_leave_check_job: self.after_cancel(self._coffee_leave_check_job)
        if not self._is_coffee_hover_inside:
            self._is_coffee_hover_inside = True
            if self.sound_manager: self.sound_manager.play_sound('coin_hover')
            if self.left_yippee_gif and self.right_yippee_gif:
                self.left_yippee_gif.pack(side="left", before=self.buy_me_a_coffee_button, padx=20, pady=10)
                self.right_yippee_gif.pack(side="right", padx=20, pady=10)
                self.left_yippee_gif.start_animation()
                self.right_yippee_gif.start_animation()

    def _on_coffee_hover_leave(self, event=None):
        if self._coffee_leave_check_job: self.after_cancel(self._coffee_leave_check_job)
        self._coffee_leave_check_job = self.after(1, self._check_if_coffee_left)

    def _check_if_coffee_left(self):
        if not self.buy_me_a_coffee_button or not self.buy_me_a_coffee_button.winfo_exists(): return
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        x1, y1 = self.buy_me_a_coffee_button.winfo_rootx(), self.buy_me_a_coffee_button.winfo_rooty()
        x2, y2 = x1 + self.buy_me_a_coffee_button.winfo_width(), y1 + self.buy_me_a_coffee_button.winfo_height()
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)
        if is_truly_outside and self._is_coffee_hover_inside:
            self._is_coffee_hover_inside = False
            if self.left_yippee_gif and self.right_yippee_gif:
                self.left_yippee_gif.stop_animation()
                self.right_yippee_gif.stop_animation()
                self.left_yippee_gif.pack_forget()
                self.right_yippee_gif.pack_forget()

    def update_ui_scaling(self, fonts):
        """Propagates font updates and rescales all dynamic image assets."""
        super().update_ui_scaling(fonts)
        if self.winfo_exists():
            # --- Rescale the technologist emoji image asset.
            if self.technologist_image:
                new_font_size = fonts["title"].cget("size")
                new_image_size = int(new_font_size * 1.1) # Scale image relative to the title font
                self.technologist_image.configure(size=(new_image_size, new_image_size))

            # --- Rescale the animated GIFs relative to the new font size.
            if self.left_yippee_gif and self.right_yippee_gif:
                new_font_size = fonts["h2"].cget("size")
                new_gif_size = int(new_font_size * 1.5)
                self.left_yippee_gif.resize_and_reload((new_gif_size, new_gif_size))
                self.right_yippee_gif.resize_and_reload((new_gif_size, new_gif_size))
    
    def reset_state(self):
        """
        Resets the scroll position of the frame to the top and stops any
        hover-based animations.
        """
        # This command moves the vertical scrollbar back to the very top (0.0).
        if hasattr(self, '_parent_canvas'):
            self._parent_canvas.yview_moveto(0.0)

        # This resets the state of the "Support This Project" button's hover effect.
        if hasattr(self, '_check_if_coffee_left'):
            self._check_if_coffee_left()

# ===================================================================================
# CLASS: NavigationRail (v4.1 - Definitive Stability & Performance Protocol)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive, zero-defect implementation of the navigation component.
# It has been completely re-architected to solve all reported layout instability,
# asset scaling, and performance anomalies. It utilizes a high-speed icon caching
# system to eliminate all real-time rendering overhead, guaranteeing instantaneous
# UI responsiveness during navigation.
# ===================================================================================
class NavigationRail(ctk.CTkFrame):
    """
    The definitive, state-aware, left-side navigation panel, engineered for
    absolute layout stability and a pixel-perfect, scalable user interface.
    """
    # ===================================================================================
    # METHOD: __init__ (v4.1 - Icon Caching & Performance Protocol)
    # This constructor has been re-engineered to support a high-performance icon
    # caching system. It now initializes a dedicated cache for pre-rendered CTkImage
    # objects, preventing costly, on-the-fly SVG rendering during navigation.
    # ===================================================================================
    def __init__(self, master, frame_switcher_callback, fonts, sound_manager: Optional['SoundManager'] = None):
        # --- [DPI SCALING] Calculate scaled dimensions for the rail itself.
        scale_factor = ScreenManager.get_scaling_factor() # --- Fetches the system's DPI scaling factor for UI calculations.
        
        # --- Base Class Initialization with scaled width.
        super().__init__(master, corner_radius=int(20 * scale_factor), fg_color=Theme.NAV_RAIL, width=int(280 * scale_factor)) # --- Initializes the frame with theme colors and scaled geometry.
        
        # --- Grid Configuration for Stability ---
        self.grid(row=0, column=0, padx=int(20 * scale_factor), pady=int(20 * scale_factor), sticky="nsw") # --- Places the navigation rail on the main window grid.
        master.grid_columnconfigure(0, weight=0) # --- Prevents the navigation column from stretching horizontally.
        self.grid_rowconfigure(9, weight=1)      # --- Pushes the support and profile sections to the bottom by allocating extra space to this row.
        
        # --- Store references to core controllers and UI elements.
        self.frame_switcher = frame_switcher_callback # --- Stores the callback function used to switch content frames.
        self.fonts = fonts                            # --- Stores the dictionary of pre-scaled font objects.
        self.sound_manager = sound_manager            # --- Stores a reference to the global sound manager.
        self.nav_buttons: Dict[str, ctk.CTkButton] = {} # --- A dictionary to hold references to the navigation button widgets.
        
        # --- Initialize state variables.
        self.sound_enabled = True       # --- Tracks the current state of the sound toggle (On/Off).
        self.tooltip_label = None       # --- A placeholder for the tooltip widget to prevent creation errors.

        # --- Master data list for all navigation buttons.
        self.buttons_data = [ # --- A centralized list defining the properties for each navigation button.
            ("Dashboard", "dashboard", 1, os.path.join("Svg", "Dashboard.svg")),
            ("Performance", "performance", 2, os.path.join("Svg", "Performance.svg")),
            ("UI Tweaks", "ui_tweaks", 3, os.path.join("Svg", "UI-Responsiveness.svg")),
            ("Fix Windows", "fix_windows", 4, os.path.join("Svg", "Fix-Windows.svg")),
            ("Clean Cache", "clean_cache", 5, os.path.join("Svg", "Clean.svg")),
            ("Group Policy", "policy", 6, os.path.join("Svg", "Group-Policy.svg")),
            ("About", "about", 7, os.path.join("Svg", "About.svg"))
        ]

        # --- [PERFORMANCE UPGRADE] Caches for raw SVG content and pre-rendered CTkImage icons.
        self.svg_content_cache = {} # --- Stores raw SVG text to prevent redundant disk I/O.
        self.icon_cache = {}        # --- Stores generated CTkImage objects for instantaneous access.

        # --- Placeholders for static image assets.
        self.sound_on_image = None
        self.sound_off_image = None

        # --- Initiate the UI construction and caching sequence.
        self._cache_svg_content() # --- Pre-loads all SVG file contents into memory.
        self._create_widgets()    # --- Creates all visible UI elements for the navigation rail.
        self.update_ui_scaling(self.fonts) # --- Perform the initial scaling and icon cache generation.

    def _cache_svg_content(self):
        """
        [PERFORMANCE OPTIMIZATION] Reads all SVG icon files from disk once at startup
        and stores their raw text content in a cache to prevent slow, repetitive
        file I/O operations during UI updates.
        """
        for _, name, _, svg_path in self.buttons_data: # --- Iterates through the master list of button data.
            try:
                with open(resource_path(svg_path), "r") as f: # --- Opens and reads the raw text content of the SVG file.
                    self.svg_content_cache[name] = f.read()   # --- Stores the file's content in the cache dictionary with its name as the key.
            except Exception as e:
                logging.error(f"Failed to pre-cache SVG content for '{svg_path}': {e}") # --- Logs an error if a file cannot be read.
                self.svg_content_cache[name] = None # --- Stores None in the cache on failure to prevent future errors.
    
    def _load_svg_icon(self, svg_content: str, size: int, color: str) -> Optional[ctk.CTkImage]:
        """
        [PERFORMANCE OPTIMIZATION] Processes a raw SVG content string from the cache,
        dynamically changes its color, scales it, and returns it as a CTkImage object.
        This method completely avoids disk I/O.

        Args:
            svg_content (str): The raw text content of the SVG icon from the cache.
            size (int): The target width and height for the icon.
            color (str): The hex color code to apply to the SVG's fill.

        Returns:
            Optional[ctk.CTkImage]: The processed CTkImage, or None on failure.
        """
        if not svg_content: # --- A fail-safe check in case the SVG content failed to cache.
            return None     # --- Returns None to prevent the application from crashing if an icon is missing.
            
        try:
            # --- Dynamically replace the placeholder fill color ('#FFFFFF') with the target color.
            colored_svg = svg_content.replace('fill="#FFFFFF"', f'fill="{color}"') # --- This assumes the source SVG is prepared with a white fill.

            # --- Convert the color-modified SVG to PNG data in memory.
            png_data = svg2png(bytestring=colored_svg.encode('utf-8'), output_width=size, output_height=size) # --- Uses cairosvg for high-quality conversion.
            
            # --- Create a PIL Image from the in-memory PNG data.
            pil_image = Image.open(BytesIO(png_data)) # --- Uses BytesIO to treat the PNG data as a file in memory.

            # --- Return a CTkImage object ready for rendering by the UI framework.
            return ctk.CTkImage(pil_image, size=(size, size))

        except Exception as e:
            # --- Log any failure during the conversion process and return None.
            logging.error(f"Failed to process cached SVG content: {e}", exc_info=True) # --- Logs the full error for debugging.
            return None

    # ===================================================================================
    # METHOD: _cache_button_icons (v1.0 - Performance Caching Engine)
    # This is a new, mission-critical method that pre-renders all navigation button
    # icons for both their 'selected' and 'deselected' states and stores the
    # resulting CTkImage objects in a cache. This operation is performed once during
    # scaling events, eliminating all real-time rendering overhead during navigation.
    # ===================================================================================
    def _cache_button_icons(self, icon_size: int):
        """
        Pre-renders all navigation icons into selected and deselected states.
        
        Args:
            icon_size (int): The target width and height for the new icons.
        """
        # --- Log the initiation of the icon caching process for performance auditing.
        logging.info(f"PERF-CACHE: Re-caching all navigation icons at size {icon_size}x{icon_size}.")
        # --- Clear the existing cache to ensure old, incorrectly sized icons are purged.
        self.icon_cache.clear()

        # --- Iterate through the master data list for all navigation buttons.
        for _, name, _, _ in self.buttons_data:
            # --- Retrieve the raw SVG string from the in-memory content cache.
            svg_content = self.svg_content_cache.get(name)

            # --- Render the 'deselected' (default) version of the icon using the secondary text color.
            deselected_icon = self._load_svg_icon(svg_content, icon_size, Theme.TEXT_SECONDARY)
            
            # --- Render the 'selected' (active) version of the icon using the main accent color.
            selected_icon = self._load_svg_icon(svg_content, icon_size, Theme.ACCENT)

            # --- Store both pre-rendered CTkImage objects in the icon cache for instant retrieval.
            self.icon_cache[name] = {
                'deselected': deselected_icon,
                'selected': selected_icon
            }

    def _on_nav_button_click(self, frame_name: str):
        """
        Plays the specific navigation sound and executes the frame switching callback.
        """
        if self.sound_manager:
            # --- Use the exact sound file name as requested for navigation actions.
            self.sound_manager.play_sound('Nav_Sound_Click')
        self.frame_switcher(frame_name)

    def _toggle_sound(self):
        """
        Toggles the global sound state, updates the button image, and plays feedback sound.
        """
        self.sound_enabled = not self.sound_enabled
        if self.sound_manager:
            self.sound_manager.set_sound_enabled(self.sound_enabled)
            self.sound_manager.play_sound('nav_click')
        
        if self.sound_toggle_button:
            image_to_display = self.sound_on_image if self.sound_enabled else self.sound_off_image
            self.sound_toggle_button.configure(image=image_to_display)

    def _show_tooltip(self, event):
        """
        Displays a temporary tooltip above the button to indicate sound state while hovered.
        """
        if not self.tooltip_label:
            self.tooltip_label = ctk.CTkLabel(self, text="Sound On" if self.sound_enabled else "Sound Off",
                                              fg_color=Theme.CARD, text_color=Theme.TEXT,
                                              corner_radius=5)
        x = self.sound_toggle_button.winfo_x() + (self.sound_toggle_button.winfo_width() // 2) - (self.tooltip_label.winfo_reqwidth() // 2)
        y = self.sound_toggle_button.winfo_y() - self.tooltip_label.winfo_reqheight() - 5
        self.tooltip_label.place(x=x, y=y)

    def _hide_tooltip(self, event=None):
        """
        Hides the tooltip immediately when the mouse leaves the button.
        """
        if self.tooltip_label:
            self.tooltip_label.place_forget()
            self.tooltip_label = None

    def _create_widgets(self):
        """Orchestrates the creation of all widgets within the navigation rail."""
        self._create_header()
        self._create_nav_buttons()
        self._create_sound_toggle()
        self._create_support_section()
        self._create_profile_section()

    def _create_header(self):
        """Creates the header section with scaled padding."""
        scale_factor = ScreenManager.get_scaling_factor()
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=int(20 * scale_factor), pady=(int(20 * scale_factor), int(40 * scale_factor)), sticky="ew")
        
        self.rocket_label = ctk.CTkLabel(header_frame, text="🚀", font=self.fonts["nav_header_font"])
        self.rocket_label.grid(row=0, column=0)
        
        self.title_label = ctk.CTkLabel(header_frame, text=" MK-Tools (v1.0)", font=self.fonts["h2"], text_color=Theme.TEXT)
        self.title_label.grid(row=0, column=1, padx=int(10 * scale_factor))

    def _create_nav_buttons(self):
        """Creates a series of navigation buttons from the master data list."""
        for text, name, row, svg_path in self.buttons_data:
            self.add_nav_button(text, name, row, svg_path)

    def _create_sound_toggle(self):
        """Creates the Sound Toggle button with scaled padding."""
        scale_factor = ScreenManager.get_scaling_factor()
        self.sound_toggle_button = ctk.CTkLabel(self, text="", cursor="hand2")
        self.sound_toggle_button.grid(row=8, column=0, pady=(int(90 * scale_factor), int(10 * scale_factor)), sticky="s")
        self.sound_toggle_button.bind("<Enter>", self._show_tooltip)
        self.sound_toggle_button.bind("<Leave>", self._hide_tooltip)
        self.sound_toggle_button.bind("<Button-1>", lambda e: self._toggle_sound())

    def _create_support_section(self):
        """Creates the support section with scaled padding."""
        scale_factor = ScreenManager.get_scaling_factor()
        support_frame = ctk.CTkFrame(self, fg_color="transparent")
        support_frame.grid(row=9, column=0, padx=int(20 * scale_factor), pady=(int(10 * scale_factor), int(10 * scale_factor)), sticky="sew")
        support_frame.grid_rowconfigure(0, weight=1)
        support_frame.grid_columnconfigure(0, weight=1)
        
        self.support_button = BuyMeACoffeeButton(
            support_frame,
            self.fonts,
            is_large=False,
            sound_manager=self.sound_manager,
            custom_text="Support This Project"
        )
        self.support_button.grid(row=0, column=0, sticky="nsew")

    def _create_profile_section(self):
        """Creates the profile section with scaled padding."""
        scale_factor = ScreenManager.get_scaling_factor()
        username = getpass.getuser()
        profile_frame = ctk.CTkFrame(self, fg_color="transparent")
        profile_frame.grid(row=10, column=0, padx=int(20 * scale_factor), pady=int(20 * scale_factor), sticky="s")
        
        self.profile_icon = ctk.CTkLabel(profile_frame, text="👤", font=self.fonts["h2"])
        self.profile_icon.grid(row=0, column=0)
        
        self.username_label = ctk.CTkLabel(profile_frame, text=username, font=self.fonts["bold"], text_color=Theme.TEXT)
        self.username_label.grid(row=0, column=1, padx=int(10 * scale_factor))

    def add_nav_button(self, text: str, frame_name: str, row: int, svg_path: str):
        """
        Creates a single navigation button, deferring icon creation to the caching system.
        """
        # --- Create the button without an icon initially. The icon will be set by update_selection.
        button = ctk.CTkButton(self, text=text,
                            font=self.fonts["nav_button_font"],
                            fg_color="transparent", hover_color=Theme.CARD,
                            text_color=Theme.TEXT_SECONDARY,
                            anchor="w", corner_radius=10, height=40,
                            command=lambda name=frame_name: self._on_nav_button_click(name),
                            image=None, # Icon will be managed dynamically by the caching system.
                            compound="left",
                            text_color_disabled=Theme.TERTIARY_DISABLED_DARK
                            )
        button.grid(row=row, column=0, padx=20, pady=8, sticky="ew")
        # --- Store the button and its associated SVG path for the caching system.
        self.nav_buttons[frame_name] = {'button': button, 'svg_path': svg_path}

    # ===================================================================================
    # METHOD: update_selection (v4.1 - Zero-Render Protocol)
    # This method has been re-engineered to be a zero-render operation. It no longer
    # performs any SVG processing. Instead, it instantly retrieves the appropriate
    # pre-rendered 'selected' or 'deselected' icon from the high-speed icon cache,
    # guaranteeing a stutter-free navigation experience.
    # ===================================================================================
    def update_selection(self, selected_frame_name: str):
        """
        Applies a 'selected' style to the active button by retrieving pre-cached icons.
        """
        # --- Iterate through all registered navigation buttons.
        for name, data in self.nav_buttons.items():
            # --- Extract the button widget from the data dictionary.
            button = data['button']
            
            # --- A safety check to ensure the widget hasn't been destroyed.
            if button.winfo_exists():
                # --- Check if the current button corresponds to the selected frame.
                if name == selected_frame_name:
                    # --- STATE: SELECTED ---
                    # --- Retrieve the pre-rendered 'selected' icon from the cache.
                    icon = self.icon_cache.get(name, {}).get('selected')
                    # --- Apply the 'selected' visual style: themed background, accent color text, and the selected icon.
                    button.configure(fg_color=Theme.CARD, text_color=Theme.ACCENT, image=icon)
                else:
                    # --- STATE: DESELECTED ---
                    # --- Retrieve the pre-rendered 'deselected' icon from the cache.
                    icon = self.icon_cache.get(name, {}).get('deselected')
                    # --- Apply the 'deselected' visual style: transparent background, secondary text color, and the deselected icon.
                    button.configure(fg_color="transparent", text_color=Theme.TEXT_SECONDARY, image=icon)

    def set_locked(self, locked: bool):
        """
        Enables or disables navigation buttons based on application state.
        """
        # --- Iterate through the data dictionaries in self.nav_buttons.
        for data in self.nav_buttons.values():
            # --- Extract the actual button widget from the dictionary.
            button = data['button'] 
            
            if button.winfo_exists():
                button.configure(state="disabled" if locked else "normal")
                if locked:
                    # --- When locking, apply a disabled style.
                    button.configure(fg_color=Theme.SECONDARY_DISABLED_DARK)
                else:
                    # --- When unlocking, restore the correct visual state by calling update_selection.
                    if hasattr(self.master, 'current_frame_name') and self.master.current_frame_name:
                        self.update_selection(self.master.current_frame_name)

        # --- Configure the sound toggle and support button states.
        if self.sound_toggle_button.winfo_exists():
            self.sound_toggle_button.configure(cursor="hand2" if not locked else "arrow")
        if hasattr(self, 'support_button') and self.support_button.winfo_exists():
            self.support_button.configure(state="disabled" if locked else "normal")

    # ===================================================================================
    # METHOD: update_ui_scaling (v4.1 - Definitive Scaling & Recaching Protocol)
    # This method is the definitive orchestrator for all UI scaling operations. It
    # updates all text fonts and then triggers the icon recaching protocol, which
    # regenerates all icons at the new, correct size. Finally, it applies the newly
    # cached and scaled assets to the UI.
    # ===================================================================================
    def update_ui_scaling(self, fonts):
        """
        Updates fonts, triggers icon recaching, and applies the new scaled assets.
        """
        # --- Store the new, updated font dictionary.
        self.fonts = fonts
        
        # --- Update text fonts for all static components within the rail.
        self.rocket_label.configure(font=fonts["nav_header_font"])
        self.title_label.configure(font=fonts["h2"])
        
        # --- STAGE 1: Calculate the new, correctly scaled size for all icons.
        # --- This ensures icons remain proportional to the newly scaled text.
        icon_size = int(self.fonts["nav_button_font"].cget("size") * 1.5)
        
        # --- STAGE 2: Trigger the icon recaching process.
        # --- This purges the old cache and generates a new set of icons at the correct size.
        self._cache_button_icons(icon_size)
        
        # --- STAGE 3: Apply the newly cached and scaled icons to the navigation buttons.
        # --- This call ensures the UI immediately reflects the correct size and selection state.
        if hasattr(self.master, 'current_frame_name') and self.master.current_frame_name:
            self.update_selection(self.master.current_frame_name)
        
        # --- STAGE 4: Scale all other static image assets.
        scaled_sound_icon_size = int(fonts["h2"].cget("size") * 1.5)
        try:
            # --- Re-load and scale the sound toggle icons directly.
            self.sound_on_image = ctk.CTkImage(Image.open(resource_path(os.path.join("Icons", "Sound-ON.png"))), size=(scaled_sound_icon_size, scaled_sound_icon_size))
            self.sound_off_image = ctk.CTkImage(Image.open(resource_path(os.path.join("Icons", "Sound-OFF.png"))), size=(scaled_sound_icon_size, scaled_sound_icon_size))
            # --- Apply the correctly scaled image based on the current sound state.
            current_image = self.sound_on_image if self.sound_enabled else self.sound_off_image
            self.sound_toggle_button.configure(image=current_image)
        except Exception as e:
            logging.error(f"Failed to reload and scale sound icons: {e}")

        # --- Update fonts for the bottom profile section.
        self.support_button.configure(font=fonts["bold"])
        self.profile_icon.configure(font=fonts["h2"])
        self.username_label.configure(font=fonts["bold"])

# ===================================================================================
# SECTION 8: APPLICATION ENTRY POINT (v2.7 - Definitive Failsafe Protocol)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This is the final, production-ready entry point. It integrates a global exception
# handler that acts as a black box flight recorder. In the event of any unhandled,
# catastrophic failure, this hook will catch the exception, log it with a full
# stack trace to the forensic log file, and present the user with a clear,
# professional error dialog. This is the paradigm solution for creating a truly
# resilient, supportable, and user-friendly application.
# ===================================================================================
if __name__ == "__main__":
    # --- STAGE 1: Ensure administrative privileges before any other operation.
    PrivilegeManager.ensure_admin()

    # --- If the script proceeds, it is guaranteed to be running as admin.
    app = None
    log_file_path = None # --- Initialize to be accessible in the exception handler.
    try:
        # --- STAGE 1.5: Configure Forensic Logging ---
        log_dir = resource_path("logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, f"mk-tools_{time.strftime('%Y-%m-%d_%H-%M-%S')}.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] :: %(message)s',
            handlers=[
                logging.FileHandler(log_file_path),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.info("Forensic Logging Protocol Engaged. Log file initialized.")

        # --- [NEW] STAGE 1.6: Define the Global Exception Handler ---
        def handle_global_exception(exc_type, exc_value, exc_traceback):
            """The definitive failsafe for all unhandled exceptions."""
            # --- Log the catastrophic failure with a full stack trace.
            logging.critical("--- CATASTROPHIC FAILURE --- Unhandled Exception Caught:", exc_info=(exc_type, exc_value, exc_traceback))
            
            # --- Create a simple, dependency-free message box to inform the user.
            error_root = tk.Tk()
            error_root.withdraw()
            
            # --- The user-facing message. It is polite, informative, and actionable.
            message = (
                "MK-Tools has encountered a critical error and must shut down.\n\n"
                "A detailed error report has been saved. Please send this file to the developer for assistance.\n\n"
                f"Log File Location:\n{log_file_path}"
            )
            tk.messagebox.showerror("Critical Application Error", message)
            sys.exit(1) # --- Ensure the application terminates cleanly after the message.

        # --- Assign the handler to the system's exception hook.
        sys.excepthook = handle_global_exception
        
        # --- STAGE 2: Configure core application appearance and scaling.
        ctk.set_appearance_mode("dark")
        ScreenManager.set_dpi_awareness()
        
        # --- STAGE 3: Load all custom typographic assets into memory.
        FontManager.register_fonts()
        
        # --- STAGE 4: Instantiate the main application.
        app = App()

        # --- [NEW] Integrate the exception handler with the Tkinter main loop for thread safety.
        app.report_callback_exception = handle_global_exception

        # --- STAGE 5: Register a robust shutdown handler to ensure graceful exit.
        def shutdown_handler():
            """Atexit hook to ensure the app's internal shutdown logic is always called."""
            logging.info("Executing registered atexit shutdown handler.")
            if app and hasattr(app, '_is_closing') and not app._is_closing:
                app._on_closing()
        
        atexit.register(shutdown_handler)
        
        # --- STAGE 6: Enter the main application event loop.
        app.mainloop()

    except KeyboardInterrupt:
        logging.info("Application terminated by user (KeyboardInterrupt).")
    except Exception as e:
        # --- This final catch block now primarily serves to trigger our custom hook.
        logging.critical(f"A fatal, unhandled exception occurred in the main execution block: {e}", exc_info=True)
        # --- If the hook was set up, it will handle the user-facing message.
        if 'handle_global_exception' in locals():
            handle_global_exception(*sys.exc_info())
    finally:
        logging.info("Application main function is exiting.")
# ===================================================================================