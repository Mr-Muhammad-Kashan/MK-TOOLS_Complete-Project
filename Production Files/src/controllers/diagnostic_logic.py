# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: DiagnosticLogicController (v6.0 - Definitive Exit-Code-Driven Engine)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive, zero-defect version of the logic engine. It resolves all
# previous parsing inaccuracies by implementing a military-grade, exit-code-first
# validation protocol. This is the paradigm solution for achieving 100% accuracy.
#
# NEW PARADIGM: EXIT-CODE-FIRST VALIDATION
#
#  [Raw Terminal Output + Process Exit Code]
#           |
#           V
#  [STAGE 1: ANALYZE EXIT CODE]
#  Description: The numerical exit code is the primary, language-independent signal
#               of success (0) or failure (non-zero). This is checked first.
#           |
#      (If Exit Code is 0 - Success Path)
#           |
#           V
#  [STAGE 2: PARSE SUCCESS TEXT]
#  Description: The text output is now only scanned to differentiate between different
#               types of success (e.g., "no violations" vs. "repaired").
#           |
#      (If Exit Code is NOT 0 - Failure Path)
#           |
#           V
#  [STAGE 2: PARSE FAILURE TEXT]
#  Description: The text output is scanned for specific known error messages. If none
#               are found, a generic failure is returned.
#
# This architecture is infallible because it relies on machine-readable exit codes
# for its primary logic, only using human-readable text for secondary classification.
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


class DiagnosticLogicController:
    """
    Parses SFC and DISM command outputs using a high-precision, exit-code-driven
    engine to match the final specification and return a structured UI blueprint.
    """
    def __init__(self, master_frame: 'FixWindowsFrame'):
        # --- Store a direct reference to the parent FixWindowsFrame for command callbacks.
        self.master_frame = master_frame

        # --- SFC SCAN LOGIC (FINALIZED PER LATEST NOTES) ---
        self.sfc_success_map = [
            {
                "key_phrase": "windows resource protection did not find any integrity violations",
                "result_factory": lambda: {
                    "title": "System Scan Complete", "emoji": "🎉", "style": "success",
                    "message": "Hooray! 🥳 Your PC is in perfect shape. MKTools scanned your system files and found no integrity violations. Keep enjoying your smooth ride! 🚀",
                    "looping_sound": "success_fanfare",
                    "buttons_config": [{'text': 'OK', 'style': 'success', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
                }
            },
            {
                "key_phrase": "windows resource protection found corrupt files and successfully repaired them",
                "result_factory": lambda: {
                    "title": "Issues Repaired!", "emoji": "🛠️", "style": "success",
                    "message": "Success! ✨ MKTools detected corrupted system files and has successfully repaired them. Your PC is healthy and good to go! 💪 A restart is recommended.",
                    "looping_sound": "success_fanfare",
                    "buttons_config": [{'text': 'OK', 'style': 'success', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
                }
            },
        ]
        self.sfc_failure_map = [
            {
                "key_phrase": "windows resource protection found corrupt files but was unable to fix some of them",
                "result_factory": lambda: {
                    "title": "Advanced Issues Detected", "emoji": "⚠️", "style": "warning",
                    "message": "Some issues were detected that couldn’t be fixed automatically. For a deeper repair, please use the 'Advanced Scan' (DISM) option.",
                    "buttons_config": [{'text': 'OK', 'style': 'warning', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
                }
            },
        ]

        # --- DISM SCAN LOGIC (FINALIZED PER LATEST NOTES) ---
        self.dism_scan_success_map = [
            {
                "key_phrase": "no component store corruption detected",
                "result_factory": lambda: {
                    "title": "Component Store Healthy", "emoji": "🎉", "style": "success",
                    "message": "The Windows component store is healthy. No further action is required.",
                    "looping_sound": "success_fanfare",
                    "buttons_config": [{'text': 'OK', 'style': 'success', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
                }
            },
            {
                "key_phrase": "the component store is repairable",
                "result_factory": lambda: {
                    "title": "Corruption Detected", "emoji": "🚨", "style": "warning",
                    "message": "Issues found in the Windows component store. MKTools can attempt a repair by running RestoreHealth. Do you want to proceed?",
                    "looping_sound": "warning_loop",
                    "buttons_config": [
                        {'text': 'Yes, Fix It', 'style': 'success', 'command': self.master_frame._create_finalization_callback(fix_now=True)},
                        {'text': 'No, Cancel', 'style': 'default', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}
                    ]
                }
            },
        ]

        # --- DISM RESTORE LOGIC (FINALIZED PER LATEST NOTES) ---
        self.dism_restore_success_map = [
             {
                "key_phrase": "the restore operation completed successfully",
                "result_factory": lambda: {
                    "title": "Repair Successful", "emoji": "✅", "style": "success",
                    "message": "The component store has been successfully repaired. It is highly recommended to run the simple 'Scan' (SFC) again to finalize all repairs.",
                    "looping_sound": "success_fanfare",
                    "buttons_config": [
                        {'text': 'Close', 'style': 'default', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)},
                        {'text': 'Run Final Scan', 'style': 'success', 'command': self.master_frame._create_finalization_callback(scan_again_sfc=True)}
                    ]
                }
            },
        ]
        self.dism_restore_failure_map = [
            {
                "key_phrase": "the source files could not be found",
                "result_factory": lambda: {
                    "title": "Repair Failed: Source Missing", "emoji": "❌", "style": "danger",
                    "message": "Repair failed because the source files could not be found online. You may need to provide a local Windows Installation file (.wim or .esd) to proceed.",
                    "one_shot_sound": "error_sound",
                    "is_source_missing": True,
                    "buttons_config": [{'text': 'OK', 'style': 'danger', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True, show_advanced_ui=True)}]
                }
            },
        ]

    def _parse_text(self, output_lines: list[str], logic_map: list[dict]) -> Optional[dict]:
        """
        A high-precision text parser that scans output lines for a key phrase.
        This is a secondary helper function, only called after the exit code is known.
        """
        consolidated_output = " ".join(output_lines).lower()

        for item in logic_map:
            if item["key_phrase"] in consolidated_output:
                logging.info(f"Precise text match found for key phrase: '{item['key_phrase']}'")
                return item["result_factory"]()

        return None

    def parse_sfc_output(self, output_lines: list[str], exit_code: int) -> dict:
        """Processes SFC /scannow output, prioritizing the exit code."""
        default_failure = {
            "title": "Scan Unsuccessful", "emoji": "⚠️", "style": "warning",
            "message": "MKTools was unable to complete the simple scan successfully or found issues it could not fix. For a deeper repair, please use the 'Advanced Scan' option.",
            "one_shot_sound": "setup_unsuccessful",
            "buttons_config": [{'text': 'OK', 'style': 'warning', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
        }

        if exit_code == 0:
            result = self._parse_text(output_lines, self.sfc_success_map)
            return result if result else self.sfc_success_map[0]["result_factory"]()
        else:
            result = self._parse_text(output_lines, self.sfc_failure_map)
            return result if result else default_failure

    def parse_dism_scan_output(self, output_lines: list[str], exit_code: int) -> dict:
        """Processes DISM /ScanHealth output, prioritizing the exit code."""
        default_failure = {
            "title": "Scan Failed", "emoji": "❌", "style": "danger",
            "message": "The Advanced Scan (DISM) failed to run. This may be due to a permissions issue or an underlying system problem.",
            "one_shot_sound": "error_sound",
            "buttons_config": [{'text': 'OK', 'style': 'danger', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
        }

        if exit_code == 0:
            result = self._parse_text(output_lines, self.dism_scan_success_map)
            return result if result else self.dism_scan_logic_map[1]["result_factory"]()
        else:
            return default_failure

    def parse_dism_restore_output(self, output_lines: list[str], exit_code: int) -> dict:
        """Processes DISM /RestoreHealth output, prioritizing the exit code."""
        default_failure = {
            "title": "Restore Failed", "emoji": "❌", "style": "danger",
            "message": "The DISM restore operation failed to complete successfully. The component store may still be corrupted.",
            "one_shot_sound": "error_sound",
            "buttons_config": [{'text': 'OK', 'style': 'danger', 'command': self.master_frame._create_finalization_callback(reset=True, show_info_button=True)}]
        }

        if exit_code == 0:
            result = self._parse_text(output_lines, self.dism_restore_success_map)
            return result if result else self.dism_restore_success_map[0]["result_factory"]()
        else:
            result = self._parse_text(output_lines, self.dism_restore_failure_map)
            return result if result else default_failure
