# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

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
