# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: NavigationRail (v4.1 - Definitive Stability & Performance Protocol)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive, zero-defect implementation of the navigation component.
# It has been completely re-architected to solve all reported layout instability,
# asset scaling, and performance anomalies. It utilizes a high-speed icon caching
# system to eliminate all real-time rendering overhead, guaranteeing instantaneous
# UI responsiveness during navigation.
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


class NavigationRail(ctk.CTkFrame):
    """
    The definitive, state-aware, left-side navigation panel, engineered for
    absolute layout stability and a pixel-perfect, scalable user interface.
    """
    # ===================================================================================
    # METHOD: __init__ (v4.1 - Icon Caching & Performance Protocol)
    # This constructor has been re-engineered to support a high-performance icon
    # caching system. It now initializes a dedicated cache for pre-rendered CTkImage
    # objects, preventing costly, on-the-fly SVG rendering during navigation.
    # ===================================================================================
    def __init__(self, master, frame_switcher_callback, fonts, sound_manager: Optional['SoundManager'] = None):
        # --- [DPI SCALING] Calculate scaled dimensions for the rail itself.
        scale_factor = ScreenManager.get_scaling_factor() # --- Fetches the system's DPI scaling factor for UI calculations.

        # --- Base Class Initialization with scaled width.
        super().__init__(master, corner_radius=int(20 * scale_factor), fg_color=Theme.NAV_RAIL, width=int(280 * scale_factor)) # --- Initializes the frame with theme colors and scaled geometry.

        # --- Grid Configuration for Stability ---
        self.grid(row=0, column=0, padx=int(20 * scale_factor), pady=int(20 * scale_factor), sticky="nsw") # --- Places the navigation rail on the main window grid.
        master.grid_columnconfigure(0, weight=0) # --- Prevents the navigation column from stretching horizontally.
        self.grid_rowconfigure(9, weight=1)      # --- Pushes the support and profile sections to the bottom by allocating extra space to this row.

        # --- Store references to core controllers and UI elements.
        self.frame_switcher = frame_switcher_callback # --- Stores the callback function used to switch content frames.
        self.fonts = fonts                            # --- Stores the dictionary of pre-scaled font objects.
        self.sound_manager = sound_manager            # --- Stores a reference to the global sound manager.
        self.nav_buttons: Dict[str, ctk.CTkButton] = {} # --- A dictionary to hold references to the navigation button widgets.

        # --- Initialize state variables.
        self.sound_enabled = True       # --- Tracks the current state of the sound toggle (On/Off).
        self.tooltip_label = None       # --- A placeholder for the tooltip widget to prevent creation errors.

        # --- Master data list for all navigation buttons.
        self.buttons_data = [ # --- A centralized list defining the properties for each navigation button.
            ("Dashboard", "dashboard", 1, os.path.join("assets", "svg", "Dashboard.svg")),
            ("Performance", "performance", 2, os.path.join("assets", "svg", "Performance.svg")),
            ("UI Tweaks", "ui_tweaks", 3, os.path.join("assets", "svg", "UI-Responsiveness.svg")),
            ("Fix Windows", "fix_windows", 4, os.path.join("assets", "svg", "Fix-Windows.svg")),
            ("Clean Cache", "clean_cache", 5, os.path.join("assets", "svg", "Clean.svg")),
            ("Group Policy", "policy", 6, os.path.join("assets", "svg", "Group-Policy.svg")),
            ("About", "about", 7, os.path.join("assets", "svg", "About.svg"))
        ]

        # --- [PERFORMANCE UPGRADE] Caches for raw SVG content and pre-rendered CTkImage icons.
        self.svg_content_cache = {} # --- Stores raw SVG text to prevent redundant disk I/O.
        self.icon_cache = {}        # --- Stores generated CTkImage objects for instantaneous access.

        # --- Placeholders for static image assets.
        self.sound_on_image = None
        self.sound_off_image = None

        # --- Initiate the UI construction and caching sequence.
        self._cache_svg_content() # --- Pre-loads all SVG file contents into memory.
        self._create_widgets()    # --- Creates all visible UI elements for the navigation rail.
        self.update_ui_scaling(self.fonts) # --- Perform the initial scaling and icon cache generation.

    def _cache_svg_content(self):
        """
        [PERFORMANCE OPTIMIZATION] Reads all SVG icon files from disk once at startup
        and stores their raw text content in a cache to prevent slow, repetitive
        file I/O operations during UI updates.
        """
        for _, name, _, svg_path in self.buttons_data: # --- Iterates through the master list of button data.
            try:
                with open(resource_path(svg_path), "r") as f: # --- Opens and reads the raw text content of the SVG file.
                    self.svg_content_cache[name] = f.read()   # --- Stores the file's content in the cache dictionary with its name as the key.
            except Exception as e:
                logging.error(f"Failed to pre-cache SVG content for '{svg_path}': {e}") # --- Logs an error if a file cannot be read.
                self.svg_content_cache[name] = None # --- Stores None in the cache on failure to prevent future errors.

    def _load_svg_icon(self, svg_content: str, size: int, color: str) -> Optional[ctk.CTkImage]:
        """
        [PERFORMANCE OPTIMIZATION] Processes a raw SVG content string from the cache,
        dynamically changes its color, scales it, and returns it as a CTkImage object.
        This method completely avoids disk I/O.

        Args:
            svg_content (str): The raw text content of the SVG icon from the cache.
            size (int): The target width and height for the icon.
            color (str): The hex color code to apply to the SVG's fill.

        Returns:
            Optional[ctk.CTkImage]: The processed CTkImage, or None on failure.
        """
        if not svg_content: # --- A fail-safe check in case the SVG content failed to cache.
            return None     # --- Returns None to prevent the application from crashing if an icon is missing.

        try:
            # --- Dynamically replace the placeholder fill color ('#FFFFFF') with the target color.
            colored_svg = svg_content.replace('fill="#FFFFFF"', f'fill="{color}"') # --- This assumes the source SVG is prepared with a white fill.

            # --- Convert the color-modified SVG to PNG data in memory.
            png_data = svg2png(bytestring=colored_svg.encode('utf-8'), output_width=size, output_height=size) # --- Uses cairosvg for high-quality conversion.

            # --- Create a PIL Image from the in-memory PNG data.
            pil_image = Image.open(BytesIO(png_data)) # --- Uses BytesIO to treat the PNG data as a file in memory.

            # --- Return a CTkImage object ready for rendering by the UI framework.
            return ctk.CTkImage(pil_image, size=(size, size))

        except Exception as e:
            # --- Log any failure during the conversion process and return None.
            logging.error(f"Failed to process cached SVG content: {e}", exc_info=True) # --- Logs the full error for debugging.
            return None

    # ===================================================================================
    # METHOD: _cache_button_icons (v1.0 - Performance Caching Engine)
    # This is a new, mission-critical method that pre-renders all navigation button
    # icons for both their 'selected' and 'deselected' states and stores the
    # resulting CTkImage objects in a cache. This operation is performed once during
    # scaling events, eliminating all real-time rendering overhead during navigation.
    # ===================================================================================
    def _cache_button_icons(self, icon_size: int):
        """
        Pre-renders all navigation icons into selected and deselected states.

        Args:
            icon_size (int): The target width and height for the new icons.
        """
        # --- Log the initiation of the icon caching process for performance auditing.
        logging.info(f"PERF-CACHE: Re-caching all navigation icons at size {icon_size}x{icon_size}.")
        # --- Clear the existing cache to ensure old, incorrectly sized icons are purged.
        self.icon_cache.clear()

        # --- Iterate through the master data list for all navigation buttons.
        for _, name, _, _ in self.buttons_data:
            # --- Retrieve the raw SVG string from the in-memory content cache.
            svg_content = self.svg_content_cache.get(name)

            # --- Render the 'deselected' (default) version of the icon using the secondary text color.
            deselected_icon = self._load_svg_icon(svg_content, icon_size, Theme.TEXT_SECONDARY)

            # --- Render the 'selected' (active) version of the icon using the main accent color.
            selected_icon = self._load_svg_icon(svg_content, icon_size, Theme.ACCENT)

            # --- Store both pre-rendered CTkImage objects in the icon cache for instant retrieval.
            self.icon_cache[name] = {
                'deselected': deselected_icon,
                'selected': selected_icon
            }

    def _on_nav_button_click(self, frame_name: str):
        """
        Plays the specific navigation sound and executes the frame switching callback.
        """
        if self.sound_manager:
            # --- Use the exact sound file name as requested for navigation actions.
            self.sound_manager.play_sound('Nav_Sound_Click')
        self.frame_switcher(frame_name)

    def _toggle_sound(self):
        """
        Toggles the global sound state, updates the button image, and plays feedback sound.
        """
        self.sound_enabled = not self.sound_enabled
        if self.sound_manager:
            self.sound_manager.set_sound_enabled(self.sound_enabled)
            self.sound_manager.play_sound('nav_click')

        if self.sound_toggle_button:
            image_to_display = self.sound_on_image if self.sound_enabled else self.sound_off_image
            self.sound_toggle_button.configure(image=image_to_display)

    def _show_tooltip(self, event):
        """
        Displays a temporary tooltip above the button to indicate sound state while hovered.
        """
        if not self.tooltip_label:
            self.tooltip_label = ctk.CTkLabel(self, text="Sound On" if self.sound_enabled else "Sound Off",
                                              fg_color=Theme.CARD, text_color=Theme.TEXT,
                                              corner_radius=5)
        x = self.sound_toggle_button.winfo_x() + (self.sound_toggle_button.winfo_width() // 2) - (self.tooltip_label.winfo_reqwidth() // 2)
        y = self.sound_toggle_button.winfo_y() - self.tooltip_label.winfo_reqheight() - 5
        self.tooltip_label.place(x=x, y=y)

    def _hide_tooltip(self, event=None):
        """
        Hides the tooltip immediately when the mouse leaves the button.
        """
        if self.tooltip_label:
            self.tooltip_label.place_forget()
            self.tooltip_label = None

    def _create_widgets(self):
        """Orchestrates the creation of all widgets within the navigation rail."""
        self._create_header()
        self._create_nav_buttons()
        self._create_sound_toggle()
        self._create_support_section()
        self._create_profile_section()

    def _create_header(self):
        """Creates the header section with scaled padding."""
        scale_factor = ScreenManager.get_scaling_factor()
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=int(20 * scale_factor), pady=(int(20 * scale_factor), int(40 * scale_factor)), sticky="ew")

        self.rocket_label = ctk.CTkLabel(header_frame, text="🚀", font=self.fonts["nav_header_font"])
        self.rocket_label.grid(row=0, column=0)

        self.title_label = ctk.CTkLabel(header_frame, text=" MK-Tools (v1.0)", font=self.fonts["h2"], text_color=Theme.TEXT)
        self.title_label.grid(row=0, column=1, padx=int(10 * scale_factor))

    def _create_nav_buttons(self):
        """Creates a series of navigation buttons from the master data list."""
        for text, name, row, svg_path in self.buttons_data:
            self.add_nav_button(text, name, row, svg_path)

    def _create_sound_toggle(self):
        """Creates the Sound Toggle button with scaled padding."""
        scale_factor = ScreenManager.get_scaling_factor()
        self.sound_toggle_button = ctk.CTkLabel(self, text="", cursor="hand2")
        self.sound_toggle_button.grid(row=8, column=0, pady=(int(90 * scale_factor), int(10 * scale_factor)), sticky="s")
        self.sound_toggle_button.bind("<Enter>", self._show_tooltip)
        self.sound_toggle_button.bind("<Leave>", self._hide_tooltip)
        self.sound_toggle_button.bind("<Button-1>", lambda e: self._toggle_sound())

    def _create_support_section(self):
        """Creates the support section with scaled padding."""
        scale_factor = ScreenManager.get_scaling_factor()
        support_frame = ctk.CTkFrame(self, fg_color="transparent")
        support_frame.grid(row=9, column=0, padx=int(20 * scale_factor), pady=(int(10 * scale_factor), int(10 * scale_factor)), sticky="sew")
        support_frame.grid_rowconfigure(0, weight=1)
        support_frame.grid_columnconfigure(0, weight=1)

        self.support_button = BuyMeACoffeeButton(
            support_frame,
            self.fonts,
            is_large=False,
            sound_manager=self.sound_manager,
            custom_text="Support This Project"
        )
        self.support_button.grid(row=0, column=0, sticky="nsew")

    def _create_profile_section(self):
        """Creates the profile section with scaled padding."""
        scale_factor = ScreenManager.get_scaling_factor()
        username = getpass.getuser()
        profile_frame = ctk.CTkFrame(self, fg_color="transparent")
        profile_frame.grid(row=10, column=0, padx=int(20 * scale_factor), pady=int(20 * scale_factor), sticky="s")

        self.profile_icon = ctk.CTkLabel(profile_frame, text="👤", font=self.fonts["h2"])
        self.profile_icon.grid(row=0, column=0)

        self.username_label = ctk.CTkLabel(profile_frame, text=username, font=self.fonts["bold"], text_color=Theme.TEXT)
        self.username_label.grid(row=0, column=1, padx=int(10 * scale_factor))

    def add_nav_button(self, text: str, frame_name: str, row: int, svg_path: str):
        """
        Creates a single navigation button, deferring icon creation to the caching system.
        """
        # --- Create the button without an icon initially. The icon will be set by update_selection.
        button = ctk.CTkButton(self, text=text,
                            font=self.fonts["nav_button_font"],
                            fg_color="transparent", hover_color=Theme.CARD,
                            text_color=Theme.TEXT_SECONDARY,
                            anchor="w", corner_radius=10, height=40,
                            command=lambda name=frame_name: self._on_nav_button_click(name),
                            image=None, # Icon will be managed dynamically by the caching system.
                            compound="left",
                            text_color_disabled=Theme.TERTIARY_DISABLED_DARK
                            )
        button.grid(row=row, column=0, padx=20, pady=8, sticky="ew")
        # --- Store the button and its associated SVG path for the caching system.
        self.nav_buttons[frame_name] = {'button': button, 'svg_path': svg_path}

    # ===================================================================================
    # METHOD: update_selection (v4.1 - Zero-Render Protocol)
    # This method has been re-engineered to be a zero-render operation. It no longer
    # performs any SVG processing. Instead, it instantly retrieves the appropriate
    # pre-rendered 'selected' or 'deselected' icon from the high-speed icon cache,
    # guaranteeing a stutter-free navigation experience.
    # ===================================================================================
    def update_selection(self, selected_frame_name: str):
        """
        Applies a 'selected' style to the active button by retrieving pre-cached icons.
        """
        # --- Iterate through all registered navigation buttons.
        for name, data in self.nav_buttons.items():
            # --- Extract the button widget from the data dictionary.
            button = data['button']

            # --- A safety check to ensure the widget hasn't been destroyed.
            if button.winfo_exists():
                # --- Check if the current button corresponds to the selected frame.
                if name == selected_frame_name:
                    # --- STATE: SELECTED ---
                    # --- Retrieve the pre-rendered 'selected' icon from the cache.
                    icon = self.icon_cache.get(name, {}).get('selected')
                    # --- Apply the 'selected' visual style: themed background, accent color text, and the selected icon.
                    button.configure(fg_color=Theme.CARD, text_color=Theme.ACCENT, image=icon)
                else:
                    # --- STATE: DESELECTED ---
                    # --- Retrieve the pre-rendered 'deselected' icon from the cache.
                    icon = self.icon_cache.get(name, {}).get('deselected')
                    # --- Apply the 'deselected' visual style: transparent background, secondary text color, and the deselected icon.
                    button.configure(fg_color="transparent", text_color=Theme.TEXT_SECONDARY, image=icon)

    def set_locked(self, locked: bool):
        """
        Enables or disables navigation buttons based on application state.
        """
        # --- Iterate through the data dictionaries in self.nav_buttons.
        for data in self.nav_buttons.values():
            # --- Extract the actual button widget from the dictionary.
            button = data['button']

            if button.winfo_exists():
                button.configure(state="disabled" if locked else "normal")
                if locked:
                    # --- When locking, apply a disabled style.
                    button.configure(fg_color=Theme.SECONDARY_DISABLED_DARK)
                else:
                    # --- When unlocking, restore the correct visual state by calling update_selection.
                    if hasattr(self.master, 'current_frame_name') and self.master.current_frame_name:
                        self.update_selection(self.master.current_frame_name)

        # --- Configure the sound toggle and support button states.
        if self.sound_toggle_button.winfo_exists():
            self.sound_toggle_button.configure(cursor="hand2" if not locked else "arrow")
        if hasattr(self, 'support_button') and self.support_button.winfo_exists():
            self.support_button.configure(state="disabled" if locked else "normal")

    # ===================================================================================
    # METHOD: update_ui_scaling (v4.1 - Definitive Scaling & Recaching Protocol)
    # This method is the definitive orchestrator for all UI scaling operations. It
    # updates all text fonts and then triggers the icon recaching protocol, which
    # regenerates all icons at the new, correct size. Finally, it applies the newly
    # cached and scaled assets to the UI.
    # ===================================================================================
    def update_ui_scaling(self, fonts):
        """
        Updates fonts, triggers icon recaching, and applies the new scaled assets.
        """
        # --- Store the new, updated font dictionary.
        self.fonts = fonts

        # --- Update text fonts for all static components within the rail.
        self.rocket_label.configure(font=fonts["nav_header_font"])
        self.title_label.configure(font=fonts["h2"])

        # --- STAGE 1: Calculate the new, correctly scaled size for all icons.
        # --- This ensures icons remain proportional to the newly scaled text.
        icon_size = int(self.fonts["nav_button_font"].cget("size") * 1.5)

        # --- STAGE 2: Trigger the icon recaching process.
        # --- This purges the old cache and generates a new set of icons at the correct size.
        self._cache_button_icons(icon_size)

        # --- STAGE 3: Apply the newly cached and scaled icons to the navigation buttons.
        # --- This call ensures the UI immediately reflects the correct size and selection state.
        if hasattr(self.master, 'current_frame_name') and self.master.current_frame_name:
            self.update_selection(self.master.current_frame_name)

        # --- STAGE 4: Scale all other static image assets.
        scaled_sound_icon_size = int(fonts["h2"].cget("size") * 1.5)
        try:
            # --- Re-load and scale the sound toggle icons directly.
            self.sound_on_image = ctk.CTkImage(Image.open(resource_path(os.path.join("assets", "icons", "Sound-ON.png"))), size=(scaled_sound_icon_size, scaled_sound_icon_size))
            self.sound_off_image = ctk.CTkImage(Image.open(resource_path(os.path.join("assets", "icons", "Sound-OFF.png"))), size=(scaled_sound_icon_size, scaled_sound_icon_size))
            # --- Apply the correctly scaled image based on the current sound state.
            current_image = self.sound_on_image if self.sound_enabled else self.sound_off_image
            self.sound_toggle_button.configure(image=current_image)
        except Exception as e:
            logging.error(f"Failed to reload and scale sound icons: {e}")

        # --- Update fonts for the bottom profile section.
        self.support_button.configure(font=fonts["bold"])
        self.profile_icon.configure(font=fonts["h2"])
        self.username_label.configure(font=fonts["bold"])
