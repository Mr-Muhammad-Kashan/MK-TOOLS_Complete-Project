# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: AboutFrame (v7.4 - Definitive Visual Hierarchy Protocol)
#
# ARCHITECTURAL BLUEPRINT (FINAL):
# This is the definitive, zero-defect implementation of the About page. It has
# been re-engineered to establish a clear and powerful visual hierarchy, ensuring
# maximum readability and aesthetic impact on all displays and scaling levels.
#
# CORE ENHANCEMENTS:
#
#   1. RE-CALIBRATED FONT HIERARCHY:
#      - Section Headers ("About The Creator", etc.): Now use the largest, boldest
#        `fonts["title"]` for maximum impact and clear distinction.
#      - Descriptive Paragraphs: Now use the `fonts["bold"]` style. This provides
#        a thick, highly readable body text that is visually subordinate to the
#        main headers, as per your directive.
#      - Sub-Headers ("Mohammed Kashan Tariq..."): Use the `fonts["h2"]` style,
#        creating a perfect intermediate step in the visual hierarchy.
#
#   2. IMAGE-BASED EMOJI INTEGRITY: The complex "technologist" emoji (🧑‍💻)
#      continues to be rendered via the 'Programmer.png' image asset, the only
#      protocol that guarantees 100% visual consistency across all platforms.
#
#   3. ROBUST SCALING: The `update_ui_scaling` method is synchronized with the
#      new font hierarchy and continues to dynamically resize all image assets,
#      ensuring the layout remains flawless at any resolution.
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


class AboutFrame(BaseContentFrame):
    """
    A comprehensive 'About' page featuring an image-based emoji protocol,
    re-calibrated font weights, and dynamic image scaling.
    """
    def __init__(self, master, fonts, app_instance, sound_manager: Optional['SoundManager'] = None):
        # --- Base Class Initialization ---
        super().__init__(master, fonts)

        # --- Property Storage ---
        self.app = app_instance
        self.fonts = fonts
        self.sound_manager = sound_manager

        # --- State and Widget Handles ---
        self.buy_me_a_coffee_button = None
        self.left_yippee_gif = None
        self.right_yippee_gif = None
        self._is_coffee_hover_inside = False
        self._coffee_leave_check_job = None

        # --- [DEFINITIVE FIX & PATH CORRECTION] Load the technologist emoji image asset using the resource_path resolver.
        try:
            programmer_icon_path = resource_path(os.path.join("assets", "icons", "Programmer.png"))
            self.technologist_image = ctk.CTkImage(Image.open(programmer_icon_path), size=(40, 40))
        except Exception as e:
            logging.error(f"FATAL: Could not load Programmer.png asset: {e}")
            self.technologist_image = None

        # --- UI Construction Protocol ---
        self.grid_columnconfigure(0, weight=1)
        self._create_content_stack()

    def _on_external_link_click(self, link: str, click_sound: Optional[str] = None, minimize: bool = False):
        """Plays a sound, optionally minimizes the app, and opens a web link."""
        if self.sound_manager and click_sound:
            self.sound_manager.play_sound(click_sound)

        if minimize:
            self.app.iconify()

        try:
            logging.info(f"Dispatching to external link: {link}")
            webbrowser.open_new_tab(link)
        except Exception as e:
            logging.error(f"Failed to open external link '{link}'. Error: {e}", exc_info=True)

    def _create_content_stack(self):
        """
        [v7.5 CORRECTED] Creates and packs all UI elements with a definitive image-based
        emoji fix, re-calibrated font weights, and robust asset path resolution
        for a zero-defect compiled executable.
        """
        # --- Helper function to create consistent headers with normalized emojis.
        def create_header(parent, emoji_text: str, main_text: str, image=None):
            header_frame = ctk.CTkFrame(parent, fg_color="transparent")

            if image:
                ctk.CTkLabel(header_frame, text="", image=image).pack(side="left", padx=5)
            else:
                ctk.CTkLabel(header_frame, text=emoji_text, font=self.fonts["emoji_large"]).pack(side="left", padx=5)

            # --- [FONT FIX] Use the largest "title" font for main section headings.
            ctk.CTkLabel(header_frame, text=main_text, font=self.fonts["title"], text_color=Theme.TEXT).pack(side="left", padx=10)

            if image:
                ctk.CTkLabel(header_frame, text="", image=image).pack(side="left", padx=5)
            else:
                ctk.CTkLabel(header_frame, text=emoji_text, font=self.fonts["emoji_large"]).pack(side="left", padx=5)

            return header_frame

        # --- Section 1: About the Creator ---
        create_header(self, "", "About The Creator", image=self.technologist_image).pack(pady=(20, 10), padx=20)

        # --- [FONT FIX] Ensure the name remains bold and prominent using "h2".
        ctk.CTkLabel(self, text="Mohammed Kashan Tariq - Software Engineer", font=self.fonts["h2"], text_color=Theme.ACCENT).pack(pady=(0, 20), padx=20)

        # --- [FONT FIX] Use the thicker "bold" font for readable descriptions.
        ctk.CTkLabel(self, text="A lifelong enthusiast with a deep love and passion for technology, software architecture, and creating tools that make a real difference. 💻",
                     font=self.fonts["bold"], text_color=Theme.TEXT_SECONDARY, wraplength=800).pack(pady=(0, 20), padx=50)

        # --- Section 2: The Mission ---
        create_header(self, "🚀", "The Mission").pack(pady=(20, 10), padx=20)
        ctk.CTkLabel(self, text="With over 10+ years of hands-on experience in Computers, Tech-hardware, and the inner workings of Windows Operating Systems, MK-Tools was created with a single, clear goal: To empower everyone. For too long, deep system optimization has been a complex world reserved for 'nerds' and power users. MK-Tools changes that. It's built on the belief that powerful tweaking capabilities should be accessible, safe, and easy for all users, giving you one-click control over your machine's performance and privacy. ✨",
                     font=self.fonts["bold"], text_color=Theme.TEXT_SECONDARY, wraplength=800, justify="left").pack(pady=(0, 30), padx=50)

        # --- Section 3: Contact Me ---
        create_header(self, "📞", "Contact Me").pack(pady=(20, 10), padx=20)
        contact_frame = ctk.CTkFrame(self, fg_color="transparent")
        contact_frame.pack(pady=(10, 20), fill="x")
        button_group = ctk.CTkFrame(contact_frame, fg_color="transparent")
        button_group.pack()

        # --- [PATH CORRECTION] All icon paths are now wrapped with resource_path() ---
        SocialButton(master=button_group, fonts=self.fonts, text="LinkedIn", icon_path="LinkedIn.ico",
                     command=lambda: self._on_external_link_click(AppConfig.LINKEDIN_URL, "linkedin_click", minimize=True),
                     color_config={"fg_color": Theme.LINKEDIN_BUTTON_FG_DARK, "hover_color": Theme.LINKEDIN_BUTTON_HOVER_DARK, "border_color": "#004182"},
                     sound_manager=self.sound_manager, click_sound_name="linkedin_click").pack(side="left", padx=15)

        SocialButton(master=button_group, fonts=self.fonts, text="GitHub", icon_path="Github.ico",
                     command=lambda: self._on_external_link_click(AppConfig.GITHUB_URL, "github_click", minimize=True),
                     color_config={"fg_color": Theme.GITHUB_BUTTON_FG_DARK, "hover_color": Theme.GITHUB_BUTTON_HOVER_DARK, "text_color": Theme.GITHUB_BUTTON_TEXT_DARK, "border_color": Theme.TEXT_SECONDARY},
                     sound_manager=self.sound_manager, click_sound_name="github_click").pack(side="left", padx=15)

        SocialButton(master=button_group, fonts=self.fonts, text="Email", icon_path="Email.ico",
                     command=lambda: self._on_external_link_click(AppConfig.CONTACT_EMAIL, "email_click"),
                     color_config={"fg_color": Theme.GMAIL_BUTTON_FG_DARK, "hover_color": Theme.GMAIL_BUTTON_HOVER_DARK, "border_color": "#C5221F"},
                     sound_manager=self.sound_manager, click_sound_name="email_click").pack(side="left", padx=15)

        # --- Section 4: Support This Project ---
        create_header(self, "💖", "Support This Project").pack(pady=(20, 10), padx=20)
        support_container = ctk.CTkFrame(self, fg_color="transparent")
        support_container.pack(pady=(10, 40))

        initial_font_size = self.fonts["h2"].cget("size")
        initial_gif_size = int(initial_font_size * 1.5)

        # --- [PATH CORRECTION] All GIF paths are now wrapped with resource_path() ---
        yippee_gif_path = resource_path(os.path.join("assets", "gifs", "Yipee.gif"))
        self.left_yippee_gif = AnimatedGIFLabel(support_container, gif_path=yippee_gif_path, size=(initial_gif_size, initial_gif_size))

        self.buy_me_a_coffee_button = BuyMeACoffeeButton(support_container, self.fonts, is_large=True,
                                                         command=lambda: self._on_external_link_click(AppConfig.BUY_ME_A_COFFEE_URL, "money", minimize=True))
        self.buy_me_a_coffee_button.pack(side="left", padx=10)

        self.right_yippee_gif = AnimatedGIFLabel(support_container, gif_path=yippee_gif_path, size=(initial_gif_size, initial_gif_size))

        self.buy_me_a_coffee_button.bind("<Enter>", self._on_coffee_hover_enter)
        self.buy_me_a_coffee_button.bind("<Leave>", self._on_coffee_hover_leave)

    def _on_coffee_hover_enter(self, event=None):
        if self._coffee_leave_check_job: self.after_cancel(self._coffee_leave_check_job)
        if not self._is_coffee_hover_inside:
            self._is_coffee_hover_inside = True
            if self.sound_manager: self.sound_manager.play_sound('coin_hover')
            if self.left_yippee_gif and self.right_yippee_gif:
                self.left_yippee_gif.pack(side="left", before=self.buy_me_a_coffee_button, padx=20, pady=10)
                self.right_yippee_gif.pack(side="right", padx=20, pady=10)
                self.left_yippee_gif.start_animation()
                self.right_yippee_gif.start_animation()

    def _on_coffee_hover_leave(self, event=None):
        if self._coffee_leave_check_job: self.after_cancel(self._coffee_leave_check_job)
        self._coffee_leave_check_job = self.after(1, self._check_if_coffee_left)

    def _check_if_coffee_left(self):
        if not self.buy_me_a_coffee_button or not self.buy_me_a_coffee_button.winfo_exists(): return
        pointer_x, pointer_y = self.winfo_pointerx(), self.winfo_pointery()
        x1, y1 = self.buy_me_a_coffee_button.winfo_rootx(), self.buy_me_a_coffee_button.winfo_rooty()
        x2, y2 = x1 + self.buy_me_a_coffee_button.winfo_width(), y1 + self.buy_me_a_coffee_button.winfo_height()
        is_truly_outside = not (x1 <= pointer_x < x2 and y1 <= pointer_y < y2)
        if is_truly_outside and self._is_coffee_hover_inside:
            self._is_coffee_hover_inside = False
            if self.left_yippee_gif and self.right_yippee_gif:
                self.left_yippee_gif.stop_animation()
                self.right_yippee_gif.stop_animation()
                self.left_yippee_gif.pack_forget()
                self.right_yippee_gif.pack_forget()

    def update_ui_scaling(self, fonts):
        """Propagates font updates and rescales all dynamic image assets."""
        super().update_ui_scaling(fonts)
        if self.winfo_exists():
            # --- Rescale the technologist emoji image asset.
            if self.technologist_image:
                new_font_size = fonts["title"].cget("size")
                new_image_size = int(new_font_size * 1.1) # Scale image relative to the title font
                self.technologist_image.configure(size=(new_image_size, new_image_size))

            # --- Rescale the animated GIFs relative to the new font size.
            if self.left_yippee_gif and self.right_yippee_gif:
                new_font_size = fonts["h2"].cget("size")
                new_gif_size = int(new_font_size * 1.5)
                self.left_yippee_gif.resize_and_reload((new_gif_size, new_gif_size))
                self.right_yippee_gif.resize_and_reload((new_gif_size, new_gif_size))

    def reset_state(self):
        """
        Resets the scroll position of the frame to the top and stops any
        hover-based animations.
        """
        # This command moves the vertical scrollbar back to the very top (0.0).
        if hasattr(self, '_parent_canvas'):
            self._parent_canvas.yview_moveto(0.0)

        # This resets the state of the "Support This Project" button's hover effect.
        if hasattr(self, '_check_if_coffee_left'):
            self._check_if_coffee_left()
