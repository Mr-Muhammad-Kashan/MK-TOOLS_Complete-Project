# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: BuyMeACoffeeButton (v2.6 - Definitive Aesthetic Protocol)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive, zero-defect implementation of the support button. It has
# been aesthetically re-calibrated to provide a perfect "capsule" shape with bold,
# yet proportionally smaller, text for a visually appealing and highly-readable result.
#
# CORE ENHANCEMENTS:
#
#   1. [CAPSULE SHAPE GEOMETRY] The button's geometry is now dynamically calculated.
#      The `corner_radius` is set to exactly half of the button's `height`,
#      guaranteeing a perfect, aesthetically pleasing capsule shape for both the
#      large and small variants of the button.
#
#   2. [RE-CALIBRATED FONT & SIZE] The small variant (used in the NavigationRail)
#      now uses the `bold` font for clear, readable text. Its `height` has been
#      reduced from 40 to 36 pixels, creating a sleeker, more refined appearance
#      that integrates perfectly into the layout.
#
#   3. [MODULARITY & TIMED FEEDBACK] This version retains the superior timed
#      auditory feedback and custom text injection protocols from the previous
#      version, ensuring it remains a powerful and reusable component.
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


class BuyMeACoffeeButton(ctk.CTkButton):
    """
    A reusable, styled button with a timed, stateful auditory feedback system,
    now featuring a perfectly calibrated capsule shape and font hierarchy.
    """
    _hover_sound_played_this_session: bool = False

    def __init__(self, master, fonts, is_large: bool = True, command: Optional[Callable] = None, sound_manager: Optional['SoundManager'] = None, custom_text: Optional[str] = None):
        # --- Store a reference to the global sound manager.
        self.sound_manager = sound_manager

        # --- [AESTHETIC & SIZE CALIBRATION PROTOCOL] ---
        if is_large:
            # --- Settings for the larger button variant (e.g., in the About page).
            self.font_obj = fonts["h2"] # Prominent, bold text
            height = 48
            corner_radius = 24 # Perfect capsule shape (height / 2)
        else:
            # --- Settings for the smaller, sleeker button (e.g., in the Navigation Rail).
            self.font_obj = fonts["bold"] # Bold text, as requested
            height = 36 # Reduced height for a more refined size
            corner_radius = 18 # Perfect capsule shape (height / 2)

        # --- Use custom text if provided, otherwise default to "Buy Me a Coffee".
        display_text = custom_text if custom_text is not None else "Buy Me a Coffee"
        final_text = f"☕  {display_text}"

        # --- Use the injected command or the internal default link-opening method.
        final_command = command if command is not None else self._open_link

        # --- Base Class Initialization with new calibrated geometry and fonts.
        super().__init__(master, text=final_text, font=self.font_obj, height=height,
                         corner_radius=corner_radius, fg_color=Theme.COFFEE_BUTTON_FG,
                         text_color=Theme.COFFEE_BUTTON_TEXT, hover_color=Theme.COFFEE_BUTTON_HOVER,
                         command=final_command)

        # --- State variables for the timed hover sound protocol.
        self._sound_job = None
        self._is_mouse_inside = False
        self._leave_check_job = None
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _open_link(self):
        """
        The default action: cancels any pending hover sound, plays the click sound,
        and then safely opens the support link.
        """
        if self._sound_job:
            self.after_cancel(self._sound_job)
            self._sound_job = None
        if self.sound_manager:
            self.sound_manager.play_sound('support_click')
        try:
            webbrowser.open_new_tab(AppConfig.BUY_ME_A_COFFEE_URL)
        except Exception as e:
            logging.error(f"Failed to open link. Error: {e}", exc_info=True)

    def _play_delayed_hover_sound(self):
        """
        This method is called ONLY after the 0.9-second delay.
        """
        if not BuyMeACoffeeButton._hover_sound_played_this_session:
            if self.sound_manager:
                self.sound_manager.stop_and_play_sound('support_hover')
            BuyMeACoffeeButton._hover_sound_played_this_session = True

    def _on_enter(self, event=None):
        """
        Handles the mouse entering the button, scheduling the delayed auditory feedback.
        """
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        if not self._is_mouse_inside:
            self._is_mouse_inside = True
            self._sound_job = self.after(900, self._play_delayed_hover_sound)

    def _on_leave(self, event=None):
        """
        Schedules a delayed check to verify if the mouse has truly exited the component's boundary.
        """
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    def _check_if_truly_left(self):
        """
        Performs a definitive check of the cursor's position and cancels the scheduled sound if the mouse has left.
        """
        if not self.winfo_exists(): return
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        x1, y1 = self.winfo_rootx(), self.winfo_rooty()
        x2, y2 = x1 + self.winfo_width(), y1 + self.winfo_height()
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)
        if is_truly_outside and self._is_mouse_inside:
            self._is_mouse_inside = False
            if self._sound_job:
                self.after_cancel(self._sound_job)
                self._sound_job = None


# ===================================================================================
# CLASS: SocialButton (v6.1 - Command-Injectable & Stateful)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component is engineered with a command injection protocol, making it a
# truly modular and reusable military-grade component.
# ===================================================================================
class SocialButton(ctk.CTkButton):
    """A specialized, icon-driven button, with an injectable command protocol."""

    def __init__(self, master, fonts, text: str, icon_path: str,
                 link: Optional[str] = None,
                 color_config: dict = None,
                 sound_manager: Optional['SoundManager'] = None,
                 click_sound_name: Optional[str] = None,
                 command: Optional[Callable] = None):

        # --- Store Core Properties ---
        self.sound_manager = sound_manager
        self.click_sound_name = click_sound_name
        self.link = link

        # --- State variables for the robust hover detection system.
        self._is_mouse_inside = False
        self._leave_check_job = None

        # --- [DPI SCALING] Calculate scaled geometry and icon sizes.
        scale_factor = ScreenManager.get_scaling_factor()
        scaled_icon_size = int(30 * scale_factor)
        scaled_height = int(60 * scale_factor)
        scaled_corner_radius = int(22 * scale_factor)
        scaled_border_width = max(1, int(2 * scale_factor)) # Ensure border is at least 1px.

        # --- Icon Loading and Processing with scaled size.
        try:
            # --- [MODIFIED] Use resource_path to get the absolute path to the icon.
            image = Image.open(resource_path(os.path.join("assets", "icons", icon_path)))
            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(scaled_icon_size, scaled_icon_size))
        except FileNotFoundError:
            logging.error(f"CRITICAL: Icon asset not found at path: {icon_path}. Rendering button without icon.")
            ctk_image = None

        # --- Command Resolution Protocol ---
        final_command = command if command is not None else self._default_on_click

        # --- Base Class Initialization with scaled geometry.
        super().__init__(
            master,
            image=ctk_image,
            text=text,
            font=fonts["h2"],
            height=scaled_height,
            corner_radius=scaled_corner_radius,
            border_width=scaled_border_width,
            command=final_command,
            compound="left",
            text_color_disabled="#A8A5C5"
        )

        # --- Dynamic Color and Event Binding ---
        if color_config: self.configure(**color_config)
        for widget in (self, self._image_label, self._text_label):
            if widget:
                widget.bind("<Enter>", self._on_enter)
                widget.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        """Handles the mouse entering ANY part of the button, triggering the hover-on action exactly once."""
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        if not self._is_mouse_inside:
            self._is_mouse_inside = True
            if self.sound_manager: self.sound_manager.play_sound('hover')
            self.configure(border_width=4)

    def _on_leave(self, event=None):
        """Schedules a delayed check to verify if the mouse has truly exited the component's boundary."""
        if self._leave_check_job: self.after_cancel(self._leave_check_job)
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    def _check_if_truly_left(self):
        """Performs a definitive check of the cursor's position to trigger the hover-off state correctly."""
        if not self.winfo_exists(): return
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        x1, y1 = self.winfo_rootx(), self.winfo_rooty()
        x2, y2 = x1 + self.winfo_width(), y1 + self.winfo_height()
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)
        if is_truly_outside and self._is_mouse_inside:
            self._is_mouse_inside = False
            self.configure(border_width=2)

    def _default_on_click(self):
        """Plays the button-specific click sound and safely opens the provided link."""
        if self.sound_manager and self.click_sound_name:
            self.sound_manager.play_sound(self.click_sound_name)

        if self.link:
            try:
                logging.info(f"Dispatching to external link: {self.link}")
                webbrowser.open_new_tab(self.link)
            except Exception as e:
                logging.error(f"Failed to open external link '{self.link}'. Error: {e}", exc_info=True)


# ===================================================================================
# CLASS: CircularActionButton (v3.1 - Zero-Defect & Fully Encapsulated)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component has been re-architected into a fully self-sufficient, state-aware
# entity. It now encapsulates its own auditory and visual feedback logic,
# eliminating all external dependencies for state management and resolving the
# hover-sound anomaly at a fundamental level.
#
# STATEFUL HOVER PROTOCOL (ZERO-SPAM):
#
#   [Mouse Enters ANY Child Widget] -> [_on_enter()]
#        |
#        +-- Is `_is_mouse_inside` False? --(YES)--> 1. Set `_is_mouse_inside` = True
#        |                                           2. Play 'fix_windows_hover' sound (EXACTLY ONCE)
#        |                                           3. Change border color to ACCENT
#        |
#        '--(NO)--> Do nothing. (Prevents sound/visual spam)
#
#   [Mouse Leaves ANY Child Widget] -> [_on_leave()]
#        |
#        +-- Schedule `_check_if_truly_left()` to run in 1ms.
#
# This protocol guarantees the hover sound is dispatched exactly once upon entry
# and is not re-triggered by mouse movements between the button's internal elements.
# ===================================================================================
class CircularActionButton(ctk.CTkFrame):
    """
    A self-contained, circular, icon-driven button with a 3D glassy effect,
    animated hover glow, and a robust, error-free UI scaling method. This version
    is fully sound-aware and manages its own state.
    """
    def __init__(self, master, fonts, emoji: str, text: str, style: str, command: Callable[[], None], sound_manager: Optional['SoundManager'] = None):
        # --- Base Class Initialization ---
        super().__init__(master, fg_color="transparent")

        # --- Property & State Storage ---
        self.sound_manager = sound_manager
        self._is_mouse_inside = False
        self._leave_check_job = None

        # --- Internal Grid Configuration ---
        self.grid_columnconfigure(0, weight=1)

        # --- [DPI SCALING] Style & Sizing Constants ---
        scale_factor = ScreenManager.get_scaling_factor()
        DIAMETER = int(140 * scale_factor) # Scale the base diameter
        RADIUS = DIAMETER // 2
        style_map = {
            "success": {"fg_color": "#287D32", "hover_color": "#4CAF50", "border_color": "#388E3C"},
            "accent":  {"fg_color": Theme.ACCENT_ACTIVE_DARK, "hover_color": Theme.ACCENT, "border_color": Theme.ACCENT_HOVER_DARK}
        }
        self.active_style = style_map.get(style, style_map["accent"])

        # --- Widget Creation: Circular Button ---
        self.button = ctk.CTkButton(
            self,
            text=emoji,
            font=fonts["emoji_large"], # Use pre-scaled font from Theme
            command=command,
            width=DIAMETER, height=DIAMETER, corner_radius=RADIUS,
            border_width=int(4 * scale_factor), **self.active_style # Scale border width
        )
        self.button.grid(row=0, column=0, padx=int(10 * scale_factor), pady=int(10 * scale_factor))

        # --- Widget Creation: Text Label ---
        self.label = ctk.CTkLabel(
            self, text=text, font=fonts["h3"], text_color=Theme.TEXT_SECONDARY
        )
        self.label.grid(row=1, column=0, padx=int(10 * scale_factor), pady=(0, int(10 * scale_factor)))

        # --- Unified Event Binding Protocol ---
        for widget in (self, self.button, self.label):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            if widget is not self.button:
                widget.bind("<Button-1>", lambda e, c=command: c())

    def _on_enter(self, event=None):
        """Activates the hover state, playing the sound and changing the border exactly once."""
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
            self._leave_check_job = None

        if not self._is_mouse_inside:
            self._is_mouse_inside = True

            # --- Dispatch Auditory Feedback ---
            if self.sound_manager:
                self.sound_manager.play_sound('fix_windows_hover')

            # --- Dispatch Visual Feedback ---
            self.button.configure(border_color=Theme.GLASS_BORDER_HOVER)

    def _on_leave(self, event=None):
        """Schedules a delayed check to verify if the mouse has truly exited the component's boundary."""
        if self._leave_check_job:
            self.after_cancel(self._leave_check_job)
        self._leave_check_job = self.after(1, self._check_if_truly_left)

    def _check_if_truly_left(self):
        """Performs a definitive check of the cursor's position to trigger the hover-off state correctly."""
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        x1, y1 = self.winfo_rootx(), self.winfo_rooty()
        x2, y2 = x1 + self.winfo_width(), y1 + self.winfo_height()

        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)

        if is_truly_outside and self._is_mouse_inside:
            self._is_mouse_inside = False
            # Revert the visual feedback to its default state.
            self.button.configure(border_color=self.active_style["border_color"])

    def update_ui_scaling(self, fonts: dict):
        """The definitive, encapsulated method for updating this component's internal fonts."""
        if self.winfo_exists():
            self.label.configure(font=fonts["h3"])


# ===================================================================================
# CLASS: GlassButton (v1.0 - Premium Visual Protocol)
#
# ARCHITECTURAL BLUEPRINT:
# This class defines a custom, high-fidelity button widget with a glassy, 3D aesthetic,
# engineered for seamless integration into a premium UI environment. It leverages the
# customtkinter library to create a visually striking button with animated hover effects,
# optimized to prevent rendering artifacts and ensure a consistent user experience.
#
# DESIGN PRINCIPLES:
#  1. VISUAL EXCELLENCE: The button combines a gradient-like glassy background, rounded
#     corners, and a dynamic border color change on hover to create a premium, 3D effect.
#  2. PERFORMANCE OPTIMIZATION: By extending `ctk.CTkButton`, it inherits optimized
#     rendering pipelines, avoiding redraw artifacts common in custom Tkinter widgets.
#  3. MODULAR EVENT HANDLING: Hover effects are implemented via explicit event bindings,
#     ensuring precise control over the border animation without relying on default hover
#     behaviors, which may introduce visual inconsistencies.
#  4. CONFIGURABLE AESTHETICS: The button's appearance (colors, font, size, and emoji)
#     is fully customizable through the `Theme` configuration, allowing seamless adaptation
#     to the application's visual identity.
#
# This class serves as a reusable, standalone component for navigation or action triggers
# in a high-end UI, such as the MK-Tools application, with a focus on user engagement
# through visual and interactive feedback.
# ===================================================================================
class GlassButton(ctk.CTkButton):
    """
    A premium, animated, and highly optimized button with a glassy, 3D effect.
    This version is a single, optimized widget that prevents rendering artifacts.
    """
    def __init__(self, master, text, emoji, font, command=None):
        button_text = f"{emoji}  {text}"

        # --- [DPI SCALING] Calculate all geometry based on the system's scaling factor.
        scale_factor = ScreenManager.get_scaling_factor()
        scaled_height = int(70 * scale_factor)
        scaled_corner_radius = int(25 * scale_factor)
        scaled_border_width = max(1, int(2 * scale_factor)) # Ensure border is at least 1px.

        # --- Base Class Initialization with scaled geometry.
        super().__init__(
            master,
            text=button_text,
            font=font,
            command=command,
            height=scaled_height,
            corner_radius=scaled_corner_radius,
            border_width=scaled_border_width,
            fg_color=Theme.GLASS_BG_START,
            text_color=Theme.GLASS_TEXT,
            border_color=Theme.GLASS_BORDER,
            hover_color=Theme.GLASS_BG_END
        )

        # --- Event Bindings for Animations ---
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        """Handles the mouse enter event to animate the border color."""
        self.configure(border_color=Theme.GLASS_BORDER_HOVER)

    def _on_leave(self, event=None):
        """Handles the mouse leave event to revert the border color."""
        self.configure(border_color=Theme.GLASS_BORDER)
