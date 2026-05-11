import subprocess
from .logger import logger


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


def run_powershell(command, elevate=False):
    try:
        if elevate:
            ps_command = f"Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -Command {command}' -Verb RunAs -Wait"
        else:
            ps_command = command
        result = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_command], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        logger.error(f"Failed to execute PowerShell command: {e}")
        return False, "", str(e)
