# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

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

from ui.frames.base_frame import BaseContentFrame
from utils.paths import resource_path
from utils.logger import logger
from core.theme import Theme
from core.font_manager import FontManager



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
        gif_full_path = resource_path(os.path.join("assets", "gifs", gif_name))
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
                    Image.open(resource_path(os.path.join("assets", "icons", "Fix-Windows.png"))),
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
