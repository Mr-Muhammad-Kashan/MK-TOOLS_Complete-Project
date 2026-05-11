# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: PolicyFrame (v3.5 - Fully Sound-Aware Command Center)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This class is the definitive UI command center for all Group Policy operations.
# This version has been re-engineered to be a fully sound-aware component,
# orchestrating auditory feedback for every key user interaction.
#
# CORE ENHANCEMENTS:
#   1. AUDITORY FEEDBACK INTEGRATION: The component now accepts the master
#      `sound_manager` instance. All primary action methods (`_start_apply_operation`,
#      `_start_reset_operation`, `toggle_info_panel`) are now wired into the
#      Auditory Feedback Engine, dispatching the correct sound event upon execution.
#
#   2. STATEFUL HOVER PROTOCOL: A zero-spam hover sound protocol has been
#      implemented for the "Apply" and "Reset" buttons. This system uses state
#      flags and a delayed verification check to ensure the 'feature_hover' sound
#      is dispatched exactly once upon entering a button's boundary, preventing
#      auditory spam.
#
#   3. COMMAND & CONTROL: The frame's core responsibility remains unchanged. It
#      delegates all backend operations to the `GroupPolicyController` in a
#      non-blocking thread and locks the main application navigation during
#      critical operations to ensure process integrity.
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


class PolicyFrame(BaseContentFrame):
    """
    The UI command center for all Group Policy operations, now featuring an
    integrated information panel and a complete auditory feedback soundscape.
    """
    # The constructor is upgraded to accept the main app_instance and sound_manager.
    def __init__(self, master, fonts, app_instance, sound_manager: Optional['SoundManager'] = None):
        # --- Base class initialization. ---
        super().__init__(master, fonts)
        # --- Store a reference to the main App controller to command the navigation lock.
        self.app = app_instance
        # --- [NEW] Store a reference to the Auditory Feedback Engine.
        self.sound_manager = sound_manager
        # --- State and Logic Controller Instantiation ---
        self.state_controller = ApplicationStateController()
        self.policy_logic = GroupPolicyController(self.state_controller)

        # --- State Management Variables ---
        self.is_working = False
        self.is_info_expanded = False
        self.terminal = None
        self.apply_button = None
        self.reset_button = None
        self.cancel_button = None
        self.active_overlay = None
        self.info_frame = None

        # --- [PNG REFACTOR] Add placeholders for the header icon widgets/objects.
        self.header_icon = None
        self.header_icon_image = None

        # --- [NEW] State variables for the stateful hover sound protocol.
        self._is_apply_hover = False
        self._is_reset_hover = False
        self._leave_check_job = None

        # --- UI Construction Protocol ---
        self._create_widgets()
        # --- Asynchronously check the initial state of the policies on startup. ---
        self._initialize_state()

    def _create_widgets(self):
        """
        [RE-ARCHITECTED] Creates and places all UI elements for both idle and working
        states, and binds their respective sound events.
        """
        # --- Header container for an icon and text.
        header_container = ctk.CTkFrame(self, fg_color="transparent")
        header_container.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 20))
        header_container.grid_columnconfigure(0, weight=1)

        # --- Sub-frame to group the title icon and text together.
        title_container = ctk.CTkFrame(header_container, fg_color="transparent")
        title_container.grid(row=0, column=0, sticky="w")

        # --- Icon and text labels for the header.
        self.header_icon = ctk.CTkLabel(title_container, text="")
        self.header_icon.pack(side="left", padx=(0, 10))
        self.header_label = ctk.CTkLabel(title_container, text="Windows Local Group Policy Editor", font=self.fonts["title"], text_color=Theme.TEXT)
        self.header_label.pack(side="left")

        # --- Info button for right-alignment.
        self.info_button = ctk.CTkButton(header_container, text="❓", width=30, height=30, corner_radius=15, fg_color=Theme.NAV_RAIL, hover_color=Theme.CARD, command=self.toggle_info_panel)
        self.info_button.grid(row=0, column=1, sticky="e", padx=(10, 5))

        # --- Initial call to load and scale the icon.
        self.update_ui_scaling(self.fonts)

        # --- Main Action Card ---
        policy_card = ctk.CTkFrame(self, fg_color=Theme.CARD, corner_radius=25, border_width=1, border_color=Theme.BORDER)
        policy_card.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        policy_card.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(policy_card, text="Apply Optimized Policies", font=self.fonts["h2"], text_color=Theme.TEXT).grid(row=0, column=0, columnspan=2, padx=30, pady=20, sticky="w")
        ctk.CTkLabel(policy_card, text="This will apply a curated set of Group Policies to enhance system performance and security. This operation requires administrative privileges and uses the Microsoft LGPO utility. \n\n\n [!NOTE: This Feature Will Not Work on 🪟Windows 10/11 - 🏠HOME Editions]", wraplength=800, justify="left", font=self.fonts["normal"], text_color=Theme.TEXT_SECONDARY).grid(row=1, column=0, columnspan=2, padx=30, pady=(0, 20), sticky="w")

        # --- Action Buttons ---
        self.apply_button = ctk.CTkButton(policy_card, text="Apply Optimized Policies", height=45, corner_radius=15, font=self.fonts["bold"], fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER, command=self._start_apply_operation)
        self.apply_button.grid(row=2, column=0, padx=30, pady=20, sticky="ew")
        self.reset_button = ctk.CTkButton(policy_card, text="Reset Policies to Default", height=45, corner_radius=15, font=self.fonts["bold"], fg_color=Theme.RESET_BUTTON_FG, text_color=Theme.RESET_BUTTON_TEXT, hover_color=Theme.RESET_BUTTON_HOVER, command=self._start_reset_operation)
        self.reset_button.grid(row=2, column=1, padx=30, pady=20, sticky="ew")

        self.cards = [policy_card]

        # --- Bind hover events for the stateful sound protocol.
        self.apply_button.bind("<Enter>", lambda e: self._on_hover_enter(self.apply_button))
        self.apply_button.bind("<Leave>", lambda e: self._on_hover_leave(self.apply_button))
        self.reset_button.bind("<Enter>", lambda e: self._on_hover_enter(self.reset_button))
        self.reset_button.bind("<Leave>", lambda e: self._on_hover_leave(self.reset_button))

        # --- [NEW] Pre-create 'working state' widgets and hide them.
        self.terminal = TerminalWidget(policy_card, self.fonts)
        self.terminal.grid(row=1, column=0, columnspan=2, padx=30, pady=10, sticky="ew")
        self.terminal.grid_remove() # --- Hide it immediately.

        self.cancel_button = ctk.CTkButton(policy_card, text="Cancel Operation", height=45, corner_radius=15, font=self.fonts["bold"], fg_color=Theme.STATE_OFF_FG, hover_color=Theme.STATE_OFF_HOVER, command=self.reset_state)
        self.cancel_button.grid(row=2, column=0, columnspan=2, padx=150, pady=20, sticky="ew")
        self.cancel_button.grid_remove() # --- Hide it immediately.

    # [NEW] Stateful hover-enter handler to prevent sound spam.
    def _on_hover_enter(self, widget):
        """Handles the mouse entering a button, triggering the hover sound exactly once."""
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
            self._leave_check_job = None

        is_hovered = self._is_apply_hover if widget == self.apply_button else self._is_reset_hover
        if not is_hovered:
            if widget == self.apply_button: self._is_apply_hover = True
            else: self._is_reset_hover = True

            if self.sound_manager:
                self.sound_manager.play_sound('feature_hover')

    # [NEW] Stateful hover-leave handler that schedules a verification check.
    def _on_hover_leave(self, widget):
        """Schedules a delayed check to verify if the mouse has truly exited the button's boundary."""
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
        self._leave_check_job = self.after(5, lambda w=widget: self._check_if_truly_left(w))

    # [NEW] Forensic check to confirm the cursor's position relative to the button's boundary.
    def _check_if_truly_left(self, widget):
        """Performs a definitive check of the cursor's position to trigger the hover-off state correctly."""
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        x1, y1 = widget.winfo_rootx(), widget.winfo_rooty()
        x2, y2 = x1 + widget.winfo_width(), y1 + widget.winfo_height()
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)

        is_hovered = self._is_apply_hover if widget == self.apply_button else self._is_reset_hover
        if is_truly_outside and is_hovered:
            if widget == self.apply_button: self._is_apply_hover = False
            else: self._is_reset_hover = False

    # [MODIFIED] Plays the question mark sound and then toggles the info panel.
    def toggle_info_panel(self):
        """Toggles the visibility of the intelligence briefing panel."""
        if self.sound_manager:
            self.sound_manager.play_sound('question_mark')

        if self.info_frame is None:
            self._create_info_panel()
        self.is_info_expanded = not self.is_info_expanded
        if self.is_info_expanded:
            self.info_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        else:
            self.info_frame.grid_forget()

    # [MODIFIED] Plays the click sound before starting the apply operation.
    def _start_apply_operation(self):
        """Initiates the policy application process."""
        if self.is_working: return

        if self.sound_manager:
            self.sound_manager.play_sound('click')

        self.app.set_navigation_lock(True)
        self.is_working = True
        self._transition_to_working_ui("Apply Optimized Policies")
        def task():
            result_message = self.policy_logic.apply_optimized_policies()
            if self.is_working:
                is_applied = self.state_controller.check_policy_status()
                self.after(0, self._finalize_operation, result_message, "Policies Applied", is_applied)
        threading.Thread(target=task, daemon=True).start()

    # [MODIFIED] Plays the reset sound before starting the reset operation.
    def _start_reset_operation(self):
        """Initiates the policy reset process."""
        if self.is_working: return

        if self.sound_manager:
            self.sound_manager.play_sound('reset')

        self.app.set_navigation_lock(True)
        self.is_working = True
        self._transition_to_working_ui("Reset Policies to Default")
        def task():
            result_message = self.policy_logic.reset_to_default()
            if self.is_working:
                is_applied = self.state_controller.check_policy_status()
                self.after(0, self._finalize_operation, result_message, "Policies Reset", is_applied)
        threading.Thread(target=task, daemon=True).start()

    # --- The methods below are unchanged as their logic is already robust and correct ---

    def _create_info_panel(self):
        """Lazily creates the rich-text intelligence briefing from a structured data payload."""
        self.info_frame = ctk.CTkFrame(self, fg_color=Theme.INFO_PANEL, corner_radius=20)
        textbox = ctk.CTkTextbox(self.info_frame, fg_color="transparent", text_color=Theme.TEXT_SECONDARY, wrap="word", height=600, border_width=0, font=self.fonts["normal"])
        textbox.pack(padx=20, pady=15, fill="both", expand=True)

        tags = {
            "heading":      {'foreground': Theme.ACCENT, 'underline': True},
            "subheading":   {'foreground': Theme.TEXT},
            "body":         {'foreground': Theme.TEXT_SECONDARY},
            "emoji_bullet": {'foreground': Theme.TEXT_SECONDARY}
        }
        for tag, config in tags.items(): textbox.tag_config(tag, **config)

        info_content = [
            ("🧠 Your System, Optimized: A Privacy-First Briefing\n\n", "heading"),
            ("Welcome to your enhanced Windows Pro experience! The applied Local Group Policy settings optimize your standalone workstation for privacy, security, and performance. Below is a detailed breakdown of what these configurations do for you.\n\n", "body"),
            ("🛡️ Enhanced Security\n", "subheading"),
            ("   🔹 Disables AI-Powered Monitoring: The `AllowRecallEnablement` policy is disabled (0). This prevents Windows Recall from taking continuous snapshots of your screen, ensuring sensitive data like passwords or financial details is never stored, reducing the risk of data exposure.\n\n", "emoji_bullet"),
            ("   🔹 Local-Only Search: Policies like `ConnectedSearchUseWeb` and `AllowCloudSearch` are disabled (0). This restricts Windows Search to local results only, preventing queries from being sent to Bing and reducing exposure to potentially malicious web content.\n\n", "emoji_bullet"),
            ("🔒 Maximized Privacy & Minimal Telemetry\n", "subheading"),
            ("   🔸 Blocks AI Data Analysis: The `DisableAIDataAnalysis` policy is enabled (1) for both computer and user settings. This prevents Windows from analyzing your app usage or system data, keeping your digital footprint private.\n\n", "emoji_bullet"),
            ("   🔸 Deactivates Cortana Completely: Policies such as `AllowCortana` are disabled (0). This ensures Cortana does not collect data like contacts, calendar, or location, enhancing user privacy.\n\n", "emoji_bullet"),
            ("   🔸 Restricts Telemetry: Policies like `DisableTailoredExperiencesWithDiagnosticData` are configured to minimize diagnostic data sent to Microsoft, giving you greater control over your data.\n\n", "emoji_bullet"),
            ("🚀 Performance Optimization\n", "subheading"),
            ("   🔹 Reduces Background Resource Usage: Disabling features like `AllowNewsAndInterests` (0) eliminates unnecessary background processes, freeing up CPU and RAM for smoother performance and faster boot times.\n\n", "emoji_bullet"),
            ("🗑️ Cleaner, Ad-Free Experience\n", "subheading"),
            ("   🔸 Prevents Sponsored Apps: The `DisableWindowsConsumerFeatures` and `DisableCloudOptimizedContent` policies are enabled (1). These block Windows from auto-installing promotional apps or games, reducing bloatware and keeping your system clean.\n\n", "emoji_bullet"),
            ("   🔸 Disables Windows Copilot: The `TurnOffWindowsCopilot` policy is enabled (1), turning off the integrated AI assistant to minimize visual clutter and background resource usage.\n\n", "emoji_bullet"),
        ]
        textbox.configure(state="normal")
        for text, tag in info_content: textbox.insert("end", text, tag)
        textbox.configure(state="disabled")

    def _initialize_state(self):
        """Checks the initial state of the policies in a background thread."""
        self.apply_button.configure(text="Checking Status...", state="disabled")
        self.reset_button.configure(state="disabled")
        def _background_check():
            is_applied = self.state_controller.check_policy_status()
            self.after(0, self._update_ui_state, is_applied)
        threading.Thread(target=_background_check, daemon=True).start()

    def _update_ui_state(self, is_applied: bool):
        """Updates the UI buttons based on the current policy state."""
        if not self.winfo_exists(): return
        if is_applied:
            self.apply_button.configure(text="Policies Applied", fg_color=Theme.SUCCESS, hover_color=Theme.SUCCESS_HOVER, state="disabled")
        else:
            self.apply_button.configure(text="Apply Optimized Policies", fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER, state="normal")
        self.reset_button.configure(state="normal")

    def _finalize_operation(self, message: str, title: str, new_state: bool):
        """Shows a final notification and resets the UI after the user acknowledges it."""
        def on_close_action():
            self._reset_to_idle()
            self._update_ui_state(new_state)
            self.app.set_navigation_lock(False)

        style = "success" if "successfully" in message or "completed" in message else "danger"
        emoji = "✅" if style == "success" else "❌"
        self._show_inline_notification(
            title=title, message=message, emoji=emoji,
            buttons_config=[{'text': 'OK', 'style': style, 'command': on_close_action}]
        )

    def _reset_to_idle(self):
        """
        [RE-ARCHITECTED] Resets the UI from a 'working' state back to 'idle' by hiding
        and showing the pre-built widgets.
        """
        self.is_working = False

        # --- Hide the 'working state' widgets.
        if self.terminal: self.terminal.grid_remove()
        if self.cancel_button: self.cancel_button.grid_remove()
        if self.active_overlay: self.active_overlay.destroy(); self.active_overlay = None

        # --- Show the 'idle state' widgets.
        self.apply_button.grid()
        self.reset_button.grid()

    def reset_state(self):
        """A master reset command called when the user navigates away from this frame."""
        self.app.set_navigation_lock(False)
        if self.is_working:
            self.is_working = False
        self._reset_to_idle()
        if self.is_info_expanded: self.toggle_info_panel()
        self._initialize_state()

    def _transition_to_working_ui(self, title: str):
        """
        [RE-ARCHITECTED] Hides the idle action buttons and reveals the pre-built
        terminal view for ongoing operations.
        """
        # --- Hide the 'idle state' buttons.
        self.apply_button.grid_remove()
        self.reset_button.grid_remove()

        # --- Show the 'working state' widgets.
        self.terminal.grid()
        self.terminal.clear() # --- Ensure terminal is empty before use.
        self.terminal.append_text(f"Initializing: {title}...")
        self.terminal.append_text("Please wait, this may take a moment...")
        self.cancel_button.grid()

    def update_ui_scaling(self, fonts):
        """
        Propagates font updates to all child cards and rescales the header icon.
        """
        super().update_ui_scaling(fonts)
        if self.winfo_exists():
            # --- Rescale the header icon image ---
            try:
                # --- Calculate the new icon size relative to the scaled title font size.
                new_font_size = self.fonts["title"].cget("size")
                new_icon_size = int(new_font_size * 1.2)

                # --- Create a new CTkImage object with the updated size.
                self.header_icon_image = ctk.CTkImage(
                    Image.open(resource_path(os.path.join("assets", "icons", "Group-Policy.png"))),
                    size=(new_icon_size, new_icon_size)
                )
                # --- Apply the new, rescaled image to the label.
                self.header_icon.configure(image=self.header_icon_image)
            except Exception as e:
                logging.error(f"Failed to load or resize header icon: {e}")
                self.header_icon.configure(image=None, text="⚠️") # Fallback

    def _show_inline_notification(self, title, message, emoji, buttons_config):
        """Displays a modal notification overlay within the frame."""
        if self.active_overlay: self.active_overlay.destroy()
        self.active_overlay = InlineNotificationOverlay(
            master=self, fonts=self.fonts, title=title, message=message,
            emoji=emoji, buttons_config=buttons_config
        )
        self.active_overlay.show()
