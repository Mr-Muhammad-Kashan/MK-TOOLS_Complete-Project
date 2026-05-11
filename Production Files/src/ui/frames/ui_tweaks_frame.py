# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: UITweaksFrame (v1.8 - Shutdown-Aware)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component has been upgraded to be a shutdown-aware dependency injector,
# mirroring the architecture of the PerformanceFrame. It now accepts the master
# `app_instance` from the application core and propagates it down to its child
# `AnimatedTweakCard` components. This ensures every component with background
# threads has a direct line to the application's global shutdown signal,
# completing its role in the graceful shutdown protocol.
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


class UITweaksFrame(BaseContentFrame):
    """
    Page for UI tweaks, now fully integrated with the application's graceful
    shutdown protocol.
    """
    # [MODIFIED] The constructor now accepts the app_instance.
    def __init__(self, master, fonts, app_instance, sound_manager: Optional['SoundManager'] = None):
        super().__init__(master, fonts)
        # --- Store a reference to the main App controller for the shutdown signal.
        self.app = app_instance
        # --- Store a reference to the Auditory Feedback Engine.
        self.sound_manager = sound_manager

        # --- [PNG REFACTOR] Create a container for the header icon and text.
        header_container = ctk.CTkFrame(self, fg_color="transparent")
        header_container.grid(row=0, column=0, padx=10, pady=(0, 20), sticky="w")

        # --- Create the icon label, which will be populated by update_ui_scaling.
        self.header_icon_image = None # Placeholder for the CTkImage object
        self.header_icon = ctk.CTkLabel(header_container, text="")
        self.header_icon.grid(row=0, column=0, padx=(0, 10))

        # --- Create the main header text label, now without the emoji.
        self.header_label = ctk.CTkLabel(header_container, text="UI & Responsiveness", font=self.fonts["title"], text_color=Theme.TEXT)
        self.header_label.grid(row=0, column=1, sticky="w")

        # --- Initial call to load and scale the icon.
        self.update_ui_scaling(self.fonts)

        # --- Instantiate ALL backend logic controllers for this section. ---
        classic_menu_logic = ClassicContextMenuTweak()
        menu_delay_logic = MenuShowDelayTweak()
        jpeg_quality_logic = JPEGQualityTweak()
        web_search_logic = DisableWebSearchTweak()

        # --- Master Data Structure with Rich Info for Each Tweak ---
        tweaks_data = [
            {
                'title': "Enable Win10 Right-Click Menu on Win11",
                'description': "Restores Windows 10 context menu on Windows 11",
                'emoji': "📔",
                'view_mode': 'toggle',
                'tweak_logic': classic_menu_logic,
                'info_data': {
                        'title': "📔 Classic Right-Click Menu",
                        'description': (
                            "This tweak brings back the classic Windows 10-style right-click context menu in Windows 11. "
                            "The default Windows 11 menu hides many options behind a 'Show more options' button, which can "
                            "slow down tasks like copying, extracting, or managing files. Enabling this tweak shows all options "
                            "immediately, making the menu faster and more familiar for long-time Windows users."
                        ),
                        'pros': [
                            "Faster access to all context menu options without extra clicks.",
                            "Improves workflow efficiency for power users and frequent file managers.",
                            "Restores a familiar experience for users upgrading from Windows 10.",
                            "Works well with older apps that rely on classic context menu entries."
                        ],
                        'cons': [
                            "Removes the cleaner, modern design of the Windows 11 context menu.",
                            "Slightly more cluttered appearance for casual users.",
                            "Requires restarting Windows Explorer or signing out to apply the change."
                        ],
                    }
            },
            {
                'title': "Instant Right-Click Mouse Menu Display",
                'description': "Removes the artificial delay when opening menus.",
                'emoji': "⚡",
                'view_mode': 'toggle',
                'tweak_logic': menu_delay_logic,
                'info_data': {
                        'title': "⚡ Instant Menu Display",
                        'description': (
                            "By default, Windows adds a small delay (typically 400 milliseconds) before displaying menus "
                            "such as right-click context menus or drop-downs. This delay is controlled by the registry "
                            "value `MenuShowDelay` located in:\n\n"
                            "HKEY_CURRENT_USER\\Control Panel\\Desktop\n\n"
                            "• Default Value: 400 ms (0.4 seconds)\n"
                            "• Optimized Value (applied by this tweak): 0 ms for instant display\n\n"
                            "Reducing this value to 0 makes all menus open instantly. This tweak affects the Start Menu, "
                            "taskbar menus, File Explorer context menus, and other standard Windows menus. "
                            "The result is a much faster and more responsive user experience, especially noticeable "
                            "on older or slower computers."
                        ),
                        'pros': [
                            "Menus appear instantly, improving overall desktop responsiveness.",
                            "Removes unnecessary waiting time, making Windows feel faster and more fluid.",
                            "Great for power users or productivity-focused workflows with frequent menu actions.",
                            "Simple registry-level tweak that can be reverted anytime by restoring the default value (400 ms)."
                        ],
                        'cons': [
                            "The speed improvement may be subtle for casual users with fast PCs.",
                            "Menus opening instantly can lead to occasional accidental selections if you misclick.",
                            "A logoff or system restart is required for the change to fully apply."
                        ]
                    }
            },
            {
                'title': "Use 100% JPEG Wallpaper Quality",
                'description': "Prevents Windows from compressing your wallpaper.",
                'emoji': "💎",
                'view_mode': 'config_dropdown',
                'tweak_logic': jpeg_quality_logic,
                'info_data': {
                        'title': "💎 JPEG Wallpaper Quality",
                        'description': (
                            "Windows automatically compresses JPEG wallpapers to around 85% quality to save a small "
                            "amount of memory and improve performance. This can make detailed images look slightly blurry "
                            "or show compression artifacts, especially on 1080p, 2K, or 4K monitors.\n\n"
                            "This tweak modifies the registry value:\n"
                            "HKEY_CURRENT_USER\\Control Panel\\Desktop\\JPEGImportQuality\n\n"
                            "• Default Value: 85 (approximately 85% quality)\n"
                            "• Optimized Value: 100 (lossless for JPEG wallpapers)\n\n"
                            "After enabling this tweak, Windows will display your wallpapers in their original, crisp quality. "
                            "You can also set custom values (between 60–100) for a balance between performance and visuals."
                        ),
                        'pros': [
                            "Restores wallpapers to their full, pixel-perfect quality with no extra compression.",
                            "Ideal for high-resolution displays (2K, 4K, or ultrawide monitors).",
                            "Prevents visible artifacts or blurriness in detailed images.",
                            "Allows adjusting the quality to balance memory usage and visual fidelity."
                        ],
                        'cons': [
                            "Using 100% quality slightly increases RAM and storage use for cached wallpapers.",
                            "Benefit is mostly noticeable on large or high-resolution displays.",
                            "Requires logging off or re-applying the wallpaper to see the effect."
                        ]
                    }
            },
            {
                'title': "Disable Web Search in Start Menu",
                'description': "Limits searches to your local files and apps.",
                'emoji': "🔍",
                'view_mode': 'toggle',
                'tweak_logic': web_search_logic,
                'info_data': {
                        'title': "🔍 Disable Web Search",
                        'description': (
                            "By default, the Windows 10 and 11 Start Menu can show web results from Bing whenever you search "
                            "for something. This means your search terms are sent to Microsoft servers to fetch online suggestions. "
                            "While convenient, this can slow down search performance and send unnecessary data over the internet.\n\n"
                            "This tweak disables web search entirely, so the Start Menu only searches for local files, folders, "
                            "apps, and settings. Your searches stay private and typically respond faster.\n"
                        ),
                        'pros': [
                            "Improves privacy by stopping Windows from sending search queries to Microsoft.",
                            "Speeds up Start Menu searches by avoiding online lookups.",
                            "Reduces unnecessary network traffic and data usage.",
                            "Prevents accidentally opening a browser when searching for local files or apps."
                        ],
                        'cons': [
                            "You lose the ability to perform quick web searches directly from the Start Menu.",
                            "Some features like Bing-powered weather or search suggestions will be disabled.",
                            "Requires a system restart or logoff to take full effect."
                        ]
                    }
            }
        ]

        # [MODIFIED] The master app_instance is now passed into the constructor data for each card.
        self.cards = [AnimatedTweakCard(self, self.fonts, app_instance=self.app, sound_manager=self.sound_manager, **data) for data in tweaks_data]
        for i, card in enumerate(self.cards):
            card.grid(row=i + 1, column=0, sticky="ew", padx=10, pady=10)

    def manage_card_panels(self, toggled_card: 'AnimatedTweakCard'):
        """
        Ensures only one info/config panel is open at a time across all cards
        in this frame. This is the central orchestrator for the exclusive panel logic.
        """
        # --- Iterate through all the AnimatedTweakCard instances managed by this frame.
        for card in self.cards:
            # --- If the card in the loop is not the one that was just clicked...
            if card is not toggled_card:
                # --- ...command it to close any panels it might have open.
                card.close_all_panels()

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
                new_icon_size = int(new_font_size * 1.2) # Scaling multiplier for visual balance

                # --- Create a new CTkImage object with the updated size.
                self.header_icon_image = ctk.CTkImage(
                    Image.open(resource_path(os.path.join("assets", "icons", "UI-Tweaks.png"))),
                    size=(new_icon_size, new_icon_size)
                )
                # --- Apply the new, rescaled image to the label.
                self.header_icon.configure(image=self.header_icon_image)
            except Exception as e:
                logging.error(f"Failed to load or resize header icon: {e}")
                self.header_icon.configure(image=None, text="⚠️") # Fallback

    def reset_state(self):
        """
        Implements the master reset protocol for this frame. This is called
        automatically when the user navigates to a different page.
        """
        logging.info("Resetting UITweaksFrame state: Closing all open panels.")
        # Iterate through all cards and command them to close any open panels.
        for card in self.cards:
            if hasattr(card, 'close_all_panels'):
                card.close_all_panels()
