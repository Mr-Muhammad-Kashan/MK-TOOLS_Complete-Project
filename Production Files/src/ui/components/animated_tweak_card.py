# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: AnimatedTweakCard (v3.6 - Deterministic Startup Protocol)
#
# ARCHITECTURAL BLUEPRINT (RE-ENGINEERING):
# This version implements a paradigm solution to a critical startup race condition.
# The previous architecture contained a logical flaw where each card instance would
# spawn its own background thread to check system state, competing with the main
# application's pre-flight check thread. This created a non-deterministic startup
# that resulted in a `RuntimeError` when a card's thread attempted to call `self.after()`
# before the main thread had entered `app.mainloop()`.
#
# NEW PARADIGM: CENTRALIZED STATE INJECTION
#
#   1. [LOGIC ELIMINATION] The `initialize_state()` and `_check_in_background()`
#      methods have been completely REMOVED from this class. The component no
#      longer possesses the autonomy to check its own state at startup.
#
#   2. [PASSIVE INITIALIZATION] The constructor now explicitly sets the card's
#      button to a "Checking..." state. The card is now a passive view that
#      awaits instruction.
#
#   3. [STATE INJECTION API] The `_set_initial_state_on_main_thread()` method is
#      retained as the sole, definitive public API for receiving state data.
#      It is now exclusively called by the master `App` class's `_on_pre_flight_complete()`
#      method, which is guaranteed to execute only after the main loop is active
#      and all system checks are finished.
#
# This architecture creates a single, predictable, and deterministic data flow,
# completely eliminating the race condition and ensuring 100% startup stability.
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


class AnimatedTweakCard(ctk.CTkFrame):
    """
    A versatile, interactive card with a stateful hover effect, rich-text
    info panel, and a fully integrated, multi-layered auditory feedback system.
    """
    # --- The constructor accepts the master app_instance for lifecycle awareness.
    def __init__(self, master, fonts, app_instance, title, description, emoji="⚙️", view_mode='toggle', tweak_logic=None, info_data=None, custom_config_panel_builder=None, sound_manager: Optional['SoundManager'] = None):
        # --- Base class initialization. ---
        super().__init__(master, fg_color=Theme.CARD, corner_radius=20, border_width=1, border_color=Theme.CARD)
        # --- Property and State Storage ---
        self.fonts = fonts
        # --- Store a reference to the main App for the shutdown signal. This is critical for stability.
        self.app = app_instance
        self.view_mode = view_mode
        self.tweak_logic = tweak_logic
        self.info_data = info_data
        self.sound_manager = sound_manager
        self.is_tweak_on = False
        self.current_tweak_value = None
        self.is_panel_expanded = False
        self.active_panel = None
        self.info_frame = None
        self.config_frame = None
        self.custom_config_panel_builder = custom_config_panel_builder
        # --- State variables for the zero-spam hover protocol.
        self._is_mouse_inside = False
        self._leave_check_job = None

        # --- UI Construction ---
        self._setup_ui(title, description, emoji)
        self._bind_events()

        # --- [CRITICAL FIX] Set the default initial state directly. ---
        # --- The card no longer fetches its own state. The master `App` controller will
        # --- inject the true state after its pre-flight checks are complete.
        if self.tweak_logic:
            self.action_button.configure(state="disabled", text="Checking...")

    # [RETAINED] This method is now the sole public API for state injection, called by the App class.
    def _set_initial_state_on_main_thread(self, state_data):
        """
        Updates the card's UI to reflect the initial state of the tweak.
        This method is always executed on the main thread, ensuring thread safety.
        """
        # --- CRITICAL CHECK: Verify the widget still exists before attempting to configure it.
        if not self.winfo_exists():
            logging.warning(f"UI update for '{self.title_label.cget('text')}' skipped: widget no longer exists.")
            return

        # --- Safely update the UI based on the retrieved state data.
        if self.view_mode == 'toggle':
            self.is_tweak_on = state_data
            self._update_toggle_button_appearance()
        elif self.view_mode == 'config_dropdown':
            # --- Handle dictionary-based state for more complex tweaks.
            self.is_tweak_on = state_data.get('status', 'default') # Safely get status
            self.current_tweak_value = state_data.get('value')
            self._update_config_button_appearance()

        # --- Re-enable the action button now that the state check is complete.
        self.action_button.configure(state="normal")

    def _execute_tweak_action(self, action, feedback_text, **kwargs):
        """Disables controls and runs the specified tweak logic in a background thread."""
        # --- Set the UI to a "working" state.
        self.action_button.configure(state="disabled", text=feedback_text)
        self.reset_button.configure(state="disabled")

        def _action_in_background():
            """
            This worker function runs the potentially slow tweak logic and then
            re-checks the state, all on a background thread.
            """
            # --- Execute the primary long-running operation (e.g., registry write).
            completion_message = action(**kwargs)

            # --- CRITICAL CHECK 1 (Mid-process): Check the shutdown signal immediately after the first operation.
            if self.app.shutdown_event.is_set():
                logging.warning(f"Shutdown signal detected in '{self.title_label.cget('text')}'; aborting state re-check.")
                return  # --- Abort mission.

            # --- Execute the secondary long-running operation (re-checking the state).
            new_state_data = self.tweak_logic.check_status()

            # --- CRITICAL CHECK 1 (Post-process): Check the shutdown signal again before the final UI update.
            if self.app.shutdown_event.is_set():
                logging.warning(f"Shutdown signal detected in '{self.title_label.cget('text')}'; aborting final UI update.")
                return  # --- Abort mission.

            # --- [NEW PARADIGM] Schedule the final UI update to run on the main thread.
            self.after(0, self._finalize_action_on_main_thread, new_state_data, completion_message)

        # --- Start the background thread.
        threading.Thread(target=_action_in_background, daemon=True).start()

    def _execute_config_action(self, action: Callable, feedback_text: str, sound_name: str):
        """
        [NEW] A definitive command handler that correctly sequences all actions for
        a configuration panel button click. It guarantees the panel closes BEFORE
        the background operation is initiated.

        Args:
            action (Callable): The tweak logic method to execute (e.g., self.tweak_logic.turn_on).
            feedback_text (str): The text to display on the button while working (e.g., "Enabling...").
            sound_name (str): The name of the sound to play for this action.
        """
        # --- Step 1: Dispatch Auditory Feedback ---
        if self.sound_manager:
            self.sound_manager.play_sound(sound_name)

        # --- Step 2: Forcibly close any open configuration/info panels.
        self.close_all_panels()

        # --- Step 3: Initiate the non-blocking, background tweak operation.
        self._execute_tweak_action(action, feedback_text)

    # [RE-ENGINEERED] This method is GUARANTEED to run on the main UI thread and is lifecycle-aware.
    def _finalize_action_on_main_thread(self, new_state_data, completion_message):
        """
        Finalizes the tweak action by updating the UI and showing a notification.
        This method is always executed on the main thread.
        """
        # --- CRITICAL CHECK 2: Final existence check before any UI manipulation.
        if not self.winfo_exists():
            logging.warning(f"Finalization for '{self.title_label.cget('text')}' skipped: widget no longer exists.")
            return

        # --- Update the card's state and button appearance based on the new data.
        self._set_initial_state_on_main_thread(new_state_data)

        # --- Re-enable the reset button.
        self.reset_button.configure(text="Reset Defaults", state="normal")

        # --- If the backend logic provided a message, display it in a notification pop-up.
        if completion_message:
            self._show_completion_notification(completion_message)

    def _setup_ui(self, title, description, emoji):
        """Creates and arranges the primary UI elements of the card."""
        # --- Create a main frame to hold all content with consistent padding.
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="x", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(1, weight=1) # Allow the text column to expand.
        # --- Create the descriptive content (icon, title, description).
        self._create_content(title, description, emoji)
        # --- Create the interactive buttons (action, reset, info).
        self._create_buttons()

    def _create_content(self, title, description, emoji):
        """Creates the main descriptive content of the card."""
        # --- The emoji label on the left.
        self.emoji_label = ctk.CTkLabel(self.main_frame, text=emoji, font=("Arial", 24))
        self.emoji_label.grid(row=0, rowspan=2, column=0, padx=15, pady=10)
        # --- The main title label.
        self.title_label = ctk.CTkLabel(self.main_frame, text=title, font=self.fonts["bold"], text_color=Theme.TEXT)
        self.title_label.grid(row=0, column=1, sticky="w")
        # --- The secondary description label.
        self.desc_label = ctk.CTkLabel(self.main_frame, text=description, font=self.fonts["small"], text_color=Theme.TEXT_SECONDARY)
        self.desc_label.grid(row=1, column=1, sticky="w")

    def _create_buttons(self):
        """Creates the control buttons for the tweak based on the view_mode."""
        # --- Create a frame to hold the control buttons on the right.
        self.controls_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.controls_frame.grid(row=0, rowspan=2, column=2, padx=15)

        # --- The primary action button (e.g., "Turn On", "Configure").
        self.action_button = ctk.CTkButton(self.controls_frame, font=self.fonts["button"],
                                           height=35, corner_radius=10, border_width=2)
        self.action_button.grid(row=0, column=0, padx=2, pady=5, sticky="ew")

        # --- Configure the button's command and appearance based on its mode.
        if self.view_mode == 'toggle':
            self.controls_frame.grid_columnconfigure((0, 1), weight=1)
            self.action_button.configure(command=self.toggle_tweak_state)
            self._update_toggle_button_appearance()
        elif self.view_mode == 'config_dropdown':
            self.controls_frame.grid_columnconfigure((0, 1), weight=1)
            self.action_button.configure(command=lambda: self.toggle_panel('config'))
            self._update_config_button_appearance()

        # --- The "Reset Defaults" button.
        self.reset_button = ctk.CTkButton(self.controls_frame, text="Reset Defaults", font=self.fonts["button"],
                                          height=35, corner_radius=10, fg_color=Theme.RESET_BUTTON_FG,
                                          text_color=Theme.RESET_BUTTON_TEXT, hover_color=Theme.RESET_BUTTON_HOVER,
                                          command=self.reset_tweak)
        self.reset_button.grid(row=0, column=1, padx=2, pady=5, sticky="ew")

        # --- The "Info" button (question mark).
        self.info_button = ctk.CTkButton(self.main_frame, text="❓", width=30, height=30, corner_radius=15,
                                         fg_color=Theme.NAV_RAIL, hover_color=Theme.CARD,
                                         command=lambda: self.toggle_panel('info'))
        self.info_button.grid(row=0, column=3, padx=(10, 5))

    def _bind_events(self):
        """Binds hover events recursively to all child widgets for a unified effect."""
        # --- This comprehensive list ensures that hovering over any part of the card triggers the effect.
        widgets_to_bind = [self, self.main_frame, self.emoji_label, self.title_label, self.desc_label, self.controls_frame, self.action_button, self.reset_button, self.info_button]
        for widget in widgets_to_bind:
            widget.bind("<Enter>", self.on_enter, add="+")
            widget.bind("<Leave>", self.on_leave, add="+")

    # [RE-ENGINEERED] Implements the stateful, zero-spam hover-on protocol.
    def on_enter(self, event=None):
        """Handles the mouse entering ANY part of the card, triggering the hover-on action exactly once."""
        # --- Cancel any pending "leave" check. This is crucial for when the mouse moves rapidly between child widgets.
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
            self._leave_check_job = None

        # --- Check the state to prevent re-triggering. If the mouse is not already inside, proceed.
        if not self._is_mouse_inside:
            # --- Update the state to reflect the mouse is now inside.
            self._is_mouse_inside = True

            # --- [NEW] Dispatch Auditory Feedback: Play the feature-specific hover sound.
            if self.sound_manager:
                self.sound_manager.play_sound('feature_hover')

            # --- Dispatch Visual Feedback: Change the border color for a highlight effect.
            self.configure(border_color=Theme.GLASS_BORDER_HOVER)

    # [RE-ENGINEERED] Implements the stateful, zero-spam hover-off protocol.
    def on_leave(self, event=None):
        """Schedules a delayed check to verify if the mouse has truly exited the component's boundary."""
        # --- Cancel any previously scheduled check to avoid redundant calls.
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
        # --- Schedule the forensic check to run after 1 millisecond.
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    # [NEW] Performs a forensic check of the cursor's position to correctly trigger the hover-off state.
    def _check_if_truly_left(self):
        """Performs a definitive check of the cursor's position to trigger the hover-off state correctly."""
        # --- Get the absolute screen coordinates of the mouse pointer.
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        # --- Get the absolute screen coordinates of this card's bounding box.
        x1, y1 = self.winfo_rootx(), self.winfo_rooty()
        x2, y2 = x1 + self.winfo_width(), y1 + self.winfo_height()

        # --- The Core Logical Check: Determine if the pointer is outside the card's bounding box.
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)

        # --- If the mouse is confirmed to be outside AND the component still thinks the mouse is inside...
        if is_truly_outside and self._is_mouse_inside:
            # --- Update the state to reflect the mouse is now outside.
            self._is_mouse_inside = False
            # --- Revert the visual feedback.
            self.configure(border_color=Theme.CARD)

    def toggle_tweak_state(self):
        """Toggles the state of the tweak and plays the appropriate sound."""
        # --- Abort if there is no logic controller or the mode is incorrect.
        if not self.tweak_logic or self.view_mode != 'toggle': return
        # --- Play the correct sound based on the current state.
        if self.sound_manager:
            if self.is_tweak_on:
                self.sound_manager.play_sound('turn_off')
            else:
                self.sound_manager.play_sound('turn_on')
        # --- Determine which action to call (apply or undo) and the feedback text.
        action = self.tweak_logic.undo if self.is_tweak_on else self.tweak_logic.apply
        feedback_text = "Disabling..." if self.is_tweak_on else "Enabling..."
        # --- Execute the action in a background thread.
        self._execute_tweak_action(action, feedback_text)

    def reset_tweak(self):
        """Resets the tweak to its default state and plays a sound."""
        # --- Abort if there is no logic controller.
        if not self.tweak_logic: return
        # --- Play the reset sound.
        if self.sound_manager:
            self.sound_manager.play_sound('reset')
        # --- Execute the 'undo' action in a background thread.
        self._execute_tweak_action(self.tweak_logic.undo, "Resetting...")
        # --- If a panel is open, close it.
        if self.is_panel_expanded: self.close_all_panels()

    def _update_toggle_button_appearance(self):
        """Updates the appearance of a standard 'On/Off' toggle button."""
        # --- This method's internal logic remains unchanged. ---
        if self.is_tweak_on:
            self.action_button.configure(text="Turned On", fg_color=Theme.STATE_ON_FG, hover_color=Theme.STATE_ON_HOVER, border_color=Theme.STATE_ON_BORDER)
        else:
            self.action_button.configure(text="Turned Off", fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, border_color=Theme.STATE_OFF_BORDER)

    def _update_config_button_appearance(self):
        """
        [CORRECTED v3.6] Updates the appearance of a 'Configure' button by correctly
        mapping all potential states ('on', 'off', 'configured', 'default') to their
        respective, definitive visual styles. This solves the UI state bug for all
        configuration-based tweaks.
        """
        # --- This condition evaluates both 'on' and 'configured' states as a positive, "enabled" visual state.
        if self.is_tweak_on == 'on' or self.is_tweak_on == 'configured':
            # --- [COLOR UNIFICATION] Configure the button to the standard 'Turned On' state (Green).
            # --- This now uses the same theme colors as the toggle buttons for visual consistency.
            self.action_button.configure(
                text="Turned On",
                fg_color=Theme.STATE_ON_FG,
                hover_color=Theme.STATE_ON_HOVER,
                border_color=Theme.STATE_ON_BORDER
            )
        # --- Check if the tweak is actively turned OFF. This is specific to the GPU tweak.
        elif self.is_tweak_on == 'off':
            # --- Configure the button to the 'Turned Off' state (Red).
            self.action_button.configure(
                text="Turned Off",
                fg_color=Theme.STATE_OFF_FG,
                hover_color=Theme.STATE_OFF_HOVER,
                border_color=Theme.STATE_OFF_BORDER
            )
        # --- This is the final fallback for the 'default' or any other unhandled state.
        else:
            # --- Configure the button to the 'Not Configured' state (Blue).
            self.action_button.configure(
                text="Not Configured",
                fg_color=Theme.CONFIGURE_BUTTON_FG,
                hover_color=Theme.CONFIGURE_BUTTON_HOVER,
                border_color=Theme.BORDER
            )

    # [MODIFIED] Injects the 'ok_click' sound into the notification's 'OK' button command.
    def _show_completion_notification(self, message: str):
        """Displays a modal notification upon completion of a tweak action with auditory feedback."""
        # --- Abort if the widget has been destroyed.
        if not self.winfo_exists(): return
        # --- Find the top-level content frame to host the overlay.
        top_level_frame = self
        while not isinstance(top_level_frame, BaseContentFrame) and top_level_frame.master is not None:
            top_level_frame = top_level_frame.master

        # --- [NEW] Create a wrapper function for the 'OK' button's action.
        def on_ok_action():
            """This function will be the new command for the 'OK' button."""
            # --- Step 1: Play the confirmation sound.
            if self.sound_manager:
                self.sound_manager.play_sound('ok_click')
            # --- Step 2: Execute the original logic (closing all panels).
            self.close_all_panels()

        # --- Define the properties for the notification overlay.
        title = "Optimization Complete"
        emoji = "✅"
        # --- [MODIFIED] The button's command now points to our new sound-aware wrapper function.
        buttons = [{'text': 'OK (Restart Required)', 'style': 'success', 'command': on_ok_action}]
        # --- Create and show the overlay.
        overlay = InlineNotificationOverlay( master=top_level_frame, fonts=self.fonts, title=title, message=message, emoji=emoji, buttons_config=buttons, on_close_callback=None )
        overlay.show()

    # [MODIFIED] Plays the 'question_mark' sound when toggling the info panel.
    def toggle_panel(self, panel_type: str):
        """
        Notifies the parent frame to manage other panels, then toggles the
        visibility of this card's info or configuration dropdown panels
        with auditory feedback.
        """
        # --- Step 1: Notify the parent frame (e.g., PerformanceFrame) to close all other open panels.
        # --- This is the core of the "exclusive panel" logic. The hasattr check ensures safety.
        if hasattr(self.master, 'manage_card_panels'):
            self.master.manage_card_panels(self)

        # --- Step 2: Play the correct sound for the action. Sound plays only when opening a panel.
        if self.sound_manager and panel_type == 'info' and not self.is_panel_expanded:
            self.sound_manager.play_sound('question_mark')

        # --- Step 3: Determine which panel to show.
        panel_to_show = None
        if panel_type == 'info':
            if self.info_frame is None: self._create_info_panel() # Lazily create the panel.
            panel_to_show = self.info_frame
        elif panel_type == 'config':
            if self.custom_config_panel_builder: self.custom_config_panel_builder()
            elif self.config_frame is None: self._create_config_dropdown_panel()
            panel_to_show = self.config_frame

        # --- Step 4: Toggle the panel's visibility based on its current state.
        if self.is_panel_expanded and self.active_panel == panel_to_show:
            self.close_all_panels()
        else:
            if self.active_panel: self.active_panel.pack_forget() # Close any different, active panel first.
            if panel_to_show:
                panel_to_show.pack(fill="x", padx=10, pady=(0, 10), expand=True)
                self.is_panel_expanded = True
                self.active_panel = panel_to_show

    def close_all_panels(self):
        """Externally callable method to forcibly close any open dropdown panel."""
        # --- This method's internal logic remains unchanged. ---
        if self.is_panel_expanded and self.active_panel:
            self.active_panel.pack_forget()
            self.is_panel_expanded = False
            self.active_panel = None

    def _create_info_panel(self):
        """Creates the rich-text info panel on-demand from the structured info_data, dynamically sizing the textbox to fit all content."""
        # --- Create the info panel frame with consistent styling and layout.
        self.info_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        # --- Initialize the textbox with no scrollbars and dynamic height.
        textbox = ctk.CTkTextbox(self, fg_color="transparent", text_color=Theme.TEXT_SECONDARY,
                                wrap="word", height=1, activate_scrollbars=False, border_width=0,
                                font=self.fonts["normal"])
        textbox.pack(in_=self.info_frame, padx=20, pady=15, fill="both", expand=True)
        textbox.configure(state="disabled")

        # --- Define text styling tags for consistent formatting.
        tags = {
            "heading": {'foreground': Theme.ACCENT, 'underline': True},
            "body": {'foreground': Theme.TEXT_SECONDARY},
            "pros_h": {'foreground': Theme.SUCCESS, 'underline': True},
            "pros": {'foreground': Theme.SUCCESS},
            "cons_h": {'foreground': Theme.STATE_OFF_FG, 'underline': True},
            "cons": {'foreground': Theme.STATE_OFF_FG},
        }
        for tag, config in tags.items():
            textbox.tag_config(tag, **config)

        # --- Helper function to insert text and track line count for height calculation.
        def insert_text(text, tag, end_char="\n\n"):
            textbox.configure(state="normal")
            textbox.insert("end", text + end_char, tag)
            textbox.configure(state="disabled")
            # --- Calculate the number of lines based on wraplength=500 and font metrics.
            font_size = self.fonts["normal"].cget("size")  # Correctly retrieve font size from CTkFont object.
            chars_per_line = 500 // (abs(font_size) // 2)  # Approximate characters per line (assuming avg char width, using abs for negative font sizes in tkinter).
            lines = len(text) // chars_per_line + text.count("\n") + (1 if end_char == "\n\n" else 0)
            return max(1, lines)

        # --- Calculate total lines for dynamic height.
        total_lines = 0
        if self.info_data:
            # --- Insert and count lines for title.
            title = self.info_data.get('title', 'Feature Information')
            total_lines += insert_text(title, "heading")

            # --- Insert and count lines for description.
            description = self.info_data.get('description', 'No details available.')
            total_lines += insert_text(description, "body")

            # --- Insert and count lines for pros header and items.
            total_lines += insert_text("✅ Pros", "pros_h", end_char="\n")
            for pro in self.info_data.get('pros', ['N/A']):
                total_lines += insert_text(f"  • {pro}", "pros", end_char="\n")
            textbox.configure(state="normal")
            textbox.insert("end", "\n")
            textbox.configure(state="disabled")
            total_lines += 1  # Account for the extra newline.

            # --- Insert and count lines for cons header and items.
            total_lines += insert_text("⚠️ Cons", "cons_h", end_char="\n")
            for con in self.info_data.get('cons', ['N/A']):
                total_lines += insert_text(f"  • {con}", "cons", end_char="\n")

            # --- Handle optional recommendation field (e.g., for GPU Scheduling).
            recommendation = self.info_data.get('recommendation', None)
            if recommendation:
                total_lines += insert_text("📝 Recommendation", "heading", end_char="\n")
                total_lines += insert_text(recommendation, "body")

        else:
            # --- Fallback for missing info_data.
            total_lines += insert_text("No detailed information available for this feature.", "body")

        # --- Calculate the required height: lines * line height (font size + padding).
        line_height = abs(self.fonts["normal"].cget("size")) + 4  # Use abs to handle negative font sizes in tkinter.
        required_height = total_lines * line_height + 30  # Add padding for aesthetics.
        textbox.configure(height=max(50, required_height))  # Ensure a minimum height for small content.

    def _create_svchost_config_panel(self):
        """Creates the advanced, multi-step configuration panel for the SvcHost Tweak."""
        # --- This method's internal logic remains unchanged. ---
        self.config_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        self.config_frame.grid_columnconfigure(0, weight=1)
        self.analysis_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        self.analysis_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        self.analysis_frame.grid_columnconfigure(0, weight=1)
        loading_label = ctk.CTkLabel(self.analysis_frame, text="Analyzing System RAM...", font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY)
        loading_label.grid(row=0, column=0, pady=10)
        def _fetch_ram_and_update_ui():
            detected_ram_gb = self.tweak_logic.get_total_physical_ram_gb()
            if self.app.shutdown_event.is_set(): return
            self.after(0, self._populate_svchost_analysis_ui, loading_label, detected_ram_gb)
        threading.Thread(target=_fetch_ram_and_update_ui, daemon=True).start()

    def _create_gpu_config_panel(self):
        """Creates the GPU configuration panel with a close button and updated logic."""
        # Create the configuration panel frame with consistent styling
        self.config_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        self.config_frame.grid_columnconfigure(0, weight=1)

        # Add informational textbox
        textbox = ctk.CTkTextbox(
            self.config_frame,
            fg_color="transparent",
            text_color=Theme.TEXT_SECONDARY,
            wrap="word",
            height=350,
            activate_scrollbars=True,
            border_width=0,
            font=self.fonts["normal"]
        )
        textbox.pack(in_=self.config_frame, padx=20, pady=15, fill="both", expand=True)

        # Define text styling tags
        tags = {
            "title": {'foreground': Theme.TEXT, 'underline': True},
            "nvidia_h": {'foreground': "#76B900"},
            "amd_h": {'foreground': "#ED1C24"},
            "intel_h": {'foreground': "#0071C5"},
            "body": {'foreground': Theme.TEXT_SECONDARY},
            "pros": {'foreground': Theme.SUCCESS},
            "cons": {'foreground': Theme.STATE_OFF_FG},
            "note": {'foreground': Theme.WARNING_DARK}
        }
        for tag, config in tags.items():
            textbox.tag_config(tag, **config)

        # Insert beginner-friendly informational content
        info_content = [
            ("What is Hardware-Accelerated GPU Scheduling?\n\n", "title"),
            ("This feature lets your graphics card (the part that shows images and videos) work smarter. It handles its own tasks, so your computer's main processor doesn't have to work as hard. This can make games, videos, or heavy apps run smoother with less delay. Here's what it means for you.\n\n", "body"),
            ("🟢 For NVIDIA GPUs (like GeForce GTX 1060, RTX 2060, or newer)\n", "nvidia_h"),
            ("    ✅ Benefits: Turn it on for smoother gameplay in most new games. It can make your mouse and keyboard feel quicker.\n", "pros"),
            ("    ⚠️ Downsides: Older games might have small issues. Test it to check if it works well for your games.\n\n", "cons"),
            ("🔴 For AMD GPUs (like Radeon RX 5700, 6700, or newer)\n", "amd_h"),
            ("    ✅ Benefits: Good for games that use a lot of your computer's power. It can make controls feel faster.\n", "pros"),
            ("    ⚠️ Downsides: Not all games improve. Try it and see if it helps your favorite games.\n\n", "cons"),
            ("🔵 For Intel Integrated Graphics (like Iris Xe in laptops)\n", "intel_h"),
            ("    ✅ Benefits: Helps apps like video editors or light games run a bit faster by easing the load on your processor.\n", "pros"),
            ("    ⚠️ Downsides: Might use more battery on laptops. The boost may be small compared to stronger graphics cards.\n\n", "cons"),
            ("‼️ IMPORTANT: You must restart your computer after turning this on or off for it to work.\n\n", "note"),
            ("📝 Should You Turn It On? Turn it on if you play new games or use apps like video editors and have a modern graphics card. If you play older games or notice problems, turn it off and test again.", "body")
        ]
        textbox.configure(state="normal")
        for text, tag in info_content:
            textbox.insert("end", text, tag)
        textbox.configure(state="disabled")

        # Create button frame for action buttons
        button_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        button_frame.pack(pady=(10, 20), padx=20, fill="x")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # [CORRECTED] Add Turn On button with a command that calls the new, reliable action handler.
        on_button = ctk.CTkButton(
            button_frame,
            text="Turn On GPU Scheduling",
            font=self.fonts["button"],
            height=40,
            corner_radius=12,
            border_width=2,
            command=lambda: self._execute_config_action(
                action=self.tweak_logic.turn_on,
                feedback_text="Enabling...",
                sound_name='turn_on'
            ),
            fg_color=Theme.SUCCESS,
            hover_color=Theme.SUCCESS_HOVER,
            border_color=Theme.SUCCESS_BORDER
        )
        on_button.grid(row=0, column=0, padx=5, sticky="ew")

        # [CORRECTED] Add Turn Off button with a command that calls the new, reliable action handler.
        off_button = ctk.CTkButton(
            button_frame,
            text="Turn Off GPU Scheduling",
            font=self.fonts["button"],
            height=40,
            corner_radius=12,
            border_width=2,
            command=lambda: self._execute_config_action(
                action=self.tweak_logic.turn_off,
                feedback_text="Disabling...",
                sound_name='turn_off'
            ),
            fg_color=Theme.STATE_OFF_FG,
            hover_color=Theme.STATE_OFF_HOVER,
            border_color=Theme.STATE_OFF_BORDER
        )
        off_button.grid(row=0, column=1, padx=5, sticky="ew")

        # Add Close button with Mouse-Click-Ok.mp3 sound
        close_button = ctk.CTkButton(
            button_frame,
            text="Close",
            font=self.fonts["button"],
            height=40,
            corner_radius=12,
            border_width=2,
            command=lambda: (
                self.sound_manager.play_sound('ok_click'),
                self.close_all_panels()
            ),
            fg_color=Theme.ACCENT_DARK,
            hover_color=Theme.ACCENT_HOVER_DARK,
            border_color=Theme.ACCENT_ACTIVE_DARK
        )
        close_button.grid(row=1, column=0, columnspan=2, padx=100, pady=(10, 0), sticky="ew")

    def _populate_svchost_analysis_ui(self, loading_label: ctk.CTkLabel, ram_gb: float):
        """Populates the UI with detected RAM and handles floating-point display."""
        # --- This method's internal logic remains unchanged. ---
        if not loading_label.winfo_exists(): return
        loading_label.destroy()
        if ram_gb == 0.0:
            error_label = ctk.CTkLabel(self.analysis_frame, text="⚠️ Could not automatically detect system RAM.", font=self.fonts["bold"], text_color=Theme.ERROR_DARK)
            error_label.grid(row=0, column=0, pady=(0, 10))
            self._svchost_show_manual_input_frame(self.analysis_frame, 16)
            return
        formatted_ram_gb = f"{ram_gb:.1f}"
        recommended_value_kb = self.tweak_logic.get_svchost_threshold_kb()
        formatted_value_dec = f"{recommended_value_kb:,}"
        formatted_value_hex = f"0x{recommended_value_kb:X}"
        ctk.CTkLabel(self.analysis_frame, text=f"🖥️ Your System's Detected RAM: {formatted_ram_gb} GB", font=self.fonts["bold"]).grid(row=0, column=0, pady=(0, 15))
        ctk.CTkLabel(self.analysis_frame, text=f"📈 Recommended Threshold (Decimal): {formatted_value_dec}", font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY).grid(row=1, column=0)
        ctk.CTkLabel(self.analysis_frame, text=f"🔢 Recommended Threshold (Hex): {formatted_value_hex}", font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY).grid(row=2, column=0, pady=(0, 15))
        ctk.CTkLabel(self.analysis_frame, text="This optimization Reduces the Stress on CPU by reducing number of Processes [SVChost processes], by using slightly more RAM, (Non-noticeable on Modern Computers), Ultimately Increasing CPU performance in Games and Overall Use  It is highly recommended for systems with 8GB or more RAM.", font=self.fonts["small"], wraplength=400, justify="center").grid(row=3, column=0, pady=(0, 20))
        ctk.CTkLabel(self.analysis_frame, text=f"❓ Is the detected RAM amount of {formatted_ram_gb} GB correct?", font=self.fonts["bold"]).grid(row=4, column=0, pady=(10, 10))
        button_frame = ctk.CTkFrame(self.analysis_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, pady=10)
        yes_button = ctk.CTkButton(button_frame, text="✅ Yes, Apply This Optimization", font=self.fonts["button"], fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, command=lambda: self._svchost_apply_and_finalize())
        yes_button.pack(side="left", padx=5)
        no_button = ctk.CTkButton(button_frame, text="❌ No, Let Me Enter It Manually", font=self.fonts["button"], fg_color=Theme.WARNING, hover_color=Theme.WARNING_HOVER, command=lambda: self._svchost_show_manual_input_frame(self.analysis_frame, int(ram_gb)))
        no_button.pack(side="left", padx=5)
        close_button = ctk.CTkButton( self.analysis_frame, text="Close", font=self.fonts["button"], fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, command=self.close_all_panels )
        close_button.grid(row=6, column=0, pady=(15, 0), padx=100, sticky="ew")

    def _svchost_show_manual_input_frame(self, parent_frame: ctk.CTkFrame, current_ram_gb: int):
        """
        [CORRECTED v3.6] Hides the consent UI and shows the manual RAM input UI.
        This version includes a new "Close" button for a complete user workflow,
        and uses a dedicated button frame for perfect side-by-side layout.
        """
        # --- Destroy all existing widgets within the parent frame to create a clean slate.
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # --- Display the critical warning message to the user about potential system instability.
        warning_text = "⚠️ WARNING: Entering an incorrect value can lead to system instability. Please double-check your system's specifications."
        ctk.CTkLabel(parent_frame, text=warning_text, font=self.fonts["bold"], text_color=Theme.WARNING_DARK, wraplength=450, justify="center").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # --- Create a container to hold the input label and entry field for clean alignment.
        input_container_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        input_container_frame.grid(row=1, column=0, columnspan=2, pady=0)

        # --- The descriptive label for the input field.
        ctk.CTkLabel(input_container_frame, text="Enter your total system RAM in GB:", font=self.fonts["normal"]).pack(side="left", padx=5)

        # --- The user entry field for manual RAM input, pre-populated with the detected value.
        manual_ram_entry = ctk.CTkEntry(input_container_frame, font=self.fonts["normal"], width=80, justify="center")
        manual_ram_entry.insert(0, str(current_ram_gb))
        manual_ram_entry.pack(side="left", padx=5)

        # --- [NEW] Create a dedicated frame to hold the action buttons side-by-side.
        # --- This is the paradigm solution for ensuring a stable, centered button layout.
        button_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, pady=25)

        # --- The primary action button to apply the user's manually entered value.
        apply_button = ctk.CTkButton(
            button_frame,
            text="Apply Manual Value",
            font=self.fonts["button"],
            # --- The command lambda correctly captures the entry widget's value at the moment of the click.
            command=lambda: self._svchost_apply_and_finalize(manual_ram_gb=int(manual_ram_entry.get()))
        )
        # --- Place the 'Apply' button within the button frame.
        apply_button.pack(side="left", padx=10)

        # --- [CRITICAL ADDITION] The new "Close" button, providing the required UI escape pathway.
        close_button = ctk.CTkButton(
            button_frame,
            text="Close",
            font=self.fonts["button"],
            # --- This button's command directly calls the method to close the dropdown panel.
            command=self.close_all_panels,
            # --- Use a distinct, non-destructive color scheme for the close button.
            fg_color=Theme.STATE_OFF_FG,
            hover_color=Theme.STATE_OFF_HOVER
        )
        # --- Place the 'Close' button next to the 'Apply' button.
        close_button.pack(side="left", padx=10)

    def _svchost_apply_and_finalize(self, manual_ram_gb: Optional[int] = None):
        """A unified function to apply the tweak and show the final confirmation."""
        # --- This method's internal logic remains unchanged. ---
        if self.sound_manager:
            self.sound_manager.play_sound('turn_on')
        self.close_all_panels()
        if manual_ram_gb is not None:
            action = self.tweak_logic.apply_manual
            kwargs = {'ram_gb': manual_ram_gb}
        else:
            action = self.tweak_logic.apply
            kwargs = {}
        self._execute_tweak_action(action, "Applying...", **kwargs)

    def _create_config_dropdown_panel(self):
        """Creates the generic configuration dropdown panel (e.g., for JPEG quality)."""
        # --- This method's internal logic remains unchanged. ---
        self.config_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        desc_text = ("Windows compresses JPEG wallpapers to about 85% to save memory. You can set a custom quality from 0% (lowest) to 100% (original).\n\nHigher quality may use slightly more RAM but looks much sharper. Lower quality can improve performance on very old hardware.")
        ctk.CTkLabel(self.config_frame, text=desc_text, justify="center", wraplength=500, font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY).pack(padx=20, pady=15, anchor="center")
        input_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        input_frame.pack(pady=10, anchor="center")
        vcmd = (self.register(self._validate_char), '%P')
        self.quality_entry = ctk.CTkEntry(input_frame, font=self.fonts["normal"], width=100, justify="center", border_color=Theme.BORDER, validate='key', validatecommand=vcmd)
        self.quality_entry.pack(side="left")
        if self.current_tweak_value is not None: self.quality_entry.insert(0, str(self.current_tweak_value))
        else: self.quality_entry.insert(0, "85")
        ctk.CTkLabel(input_frame, text="Quality (0-100)%", font=self.fonts["small"], text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=10)
        button_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        button_frame.pack(pady=10, anchor="center", padx=20)
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", font=self.fonts["button"], fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, command=lambda: self.toggle_panel('config'))
        cancel_button.pack(side="left", padx=5)
        apply_button = ctk.CTkButton(button_frame, text="Apply", font=self.fonts["button"], fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, command=self._apply_config_change)
        apply_button.pack(side="left", padx=5)

    def _validate_char(self, new_value: str) -> bool:
        """Validates character input for numeric entry fields."""
        # --- This method's internal logic remains unchanged. ---
        if new_value == "": return True
        try:
            num = int(new_value)
            return 0 <= num <= 100 and len(new_value) <= 3
        except ValueError:
            return False

    def _apply_config_change(self):
        """Applies a configuration change from a dropdown panel."""
        # --- This method's internal logic remains unchanged. ---
        if not self.tweak_logic: return
        try:
            value = int(self.quality_entry.get())
            if 0 <= value <= 100:
                if self.sound_manager:
                    self.sound_manager.play_sound('turn_on')
                self.close_all_panels()
                self._execute_tweak_action(self.tweak_logic.apply, "Applying...", quality_value=value)
            else:
                self.quality_entry.configure(border_color=Theme.STATE_OFF_BORDER)
        except (ValueError, TypeError):
                self.quality_entry.configure(border_color=Theme.STATE_OFF_BORDER)

    def update_ui_scaling(self, fonts):
        """Propagates font scaling updates to all child widgets."""
        # --- This method's internal logic remains unchanged. ---
        self.fonts = fonts
        self.title_label.configure(font=fonts["bold"])
        self.desc_label.configure(font=fonts["small"])
        self.action_button.configure(font=fonts["button"])
        self.reset_button.configure(font=fonts["button"])
        if self.info_frame and self.info_frame.winfo_exists():
            for widget in self.info_frame.winfo_children():
                if isinstance(widget, ctk.CTkTextbox):
                    widget.configure(font=fonts["normal"])
        if self.config_frame and self.config_frame.winfo_exists():
            for child in self.config_frame.winfo_children():
                if isinstance(child, ctk.CTkLabel):
                    child.configure(font=fonts["normal"])
                elif isinstance(child, ctk.CTkFrame):
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, (ctk.CTkEntry, ctk.CTkLabel, ctk.CTkButton)):
                            font_key = "normal"
                            if isinstance(grandchild, ctk.CTkButton): font_key = "button"
                            if isinstance(grandchild, ctk.CTkLabel) and "Quality" in grandchild.cget("text"):
                                font_key = "small"
                            grandchild.configure(font=fonts[font_key])
