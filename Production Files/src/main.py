import sys
import ctypes
import traceback
import tkinter as tk
import customtkinter as ctk

from utils import logger, resource_path
from core.privilege_manager import PrivilegeManager
from ui.app_window import App
from ui.splash_screen import SplashScreen

def custom_excepthook(exc_type, exc_value, exc_traceback):
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = custom_excepthook

def setup_dpi():
    if sys.platform == 'win32':
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            logger.warning(f"Failed to set DPI awareness: {e}")

def main():
    setup_dpi()
    # PrivilegeManager.ensure_admin() # Disable for linux tests

    ctk.set_appearance_mode("Dark")

    app = App()
    splash = SplashScreen(app, on_complete=app.deiconify)

    try:
        app.mainloop()
    except Exception as e:
        logger.critical(f"Fatal error in mainloop: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
