import os
from .logger import logger

try:
    import winreg
except ImportError:
    pass

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


def registry_key_exists(hive, subkey):
    try:
        key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
        winreg.CloseKey(key)
        return True
    except WindowsError:
        return False

def get_registry_value(hive, subkey, value_name):
    try:
        key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return value
    except WindowsError:
        return None

def set_registry_value(hive, subkey, value_name, value, regtype):
    try:
        key = winreg.CreateKey(hive, subkey)
        winreg.SetValueEx(key, value_name, 0, regtype, value)
        winreg.CloseKey(key)
        return True
    except WindowsError as e:
        logger.error(f"Failed to set registry value: {e}")
        return False

def delete_registry_value(hive, subkey, value_name):
    try:
        key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, value_name)
        winreg.CloseKey(key)
        return True
    except WindowsError as e:
        logger.error(f"Failed to delete registry value: {e}")
        return False

def delete_registry_key(hive, subkey):
    try:
        winreg.DeleteKey(hive, subkey)
        return True
    except WindowsError as e:
        logger.error(f"Failed to delete registry key: {e}")
        return False
