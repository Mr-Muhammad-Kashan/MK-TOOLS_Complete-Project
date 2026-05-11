# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================


import os
import psutil
import logging
from utils.logger import logger
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
