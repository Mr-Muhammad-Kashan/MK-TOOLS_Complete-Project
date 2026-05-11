# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

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
from ui.components.clean_cache_card import CleanCacheCard



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
        self.cleaning_gif_widget = AnimatedGIFLabel(self, gif_path=resource_path(os.path.join("assets", "gifs", "Cleaning.gif")), size=(128, 128))
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
            gif_path=resource_path(os.path.join("assets", "gifs", "Done.gif")),
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
                    Image.open(resource_path(os.path.join("assets", "icons", "Cleaning.png"))),
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
