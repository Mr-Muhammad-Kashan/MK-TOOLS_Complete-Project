# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================


import json
from packaging.version import parse as parse_version
from utils.paths import resource_path
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
