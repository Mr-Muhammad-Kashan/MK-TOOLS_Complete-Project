# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# -----------------------------------------------------------------------------------
# SECTION 1.5: CENTRALIZED CONFIGURATION
# -----------------------------------------------------------------------------------
# ===================================================================================
# File: main.py
# Location: SECTION 1.5: CENTRALIZED CONFIGURATION
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


class AppConfig:
    """A centralized store for all external links and configurable constants."""
    BUY_ME_A_COFFEE_URL = "https://mr-muhammad-kashan.github.io/Buy-Me-A-Coffee-Website/"
    LINKEDIN_URL = "https://www.linkedin.com/in/muhammad-kashan-tariq"
    GITHUB_URL = "https://github.com/Mr-Muhammad-Kashan"
    CONTACT_EMAIL = "mailto:m.kashan.exe@gmail.com"
    # --- [MODIFIED] This is the corrected, direct link to the raw JSON file for the update check.
    LATEST_VERSION_URL = "https://raw.githubusercontent.com/Mr-Muhammad-Kashan/MK-Tools/main/Version/Version.json"
