# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

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
            self.iconbitmap(resource_path(os.path.join("assets", "icons", "Logo.ico")))
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
