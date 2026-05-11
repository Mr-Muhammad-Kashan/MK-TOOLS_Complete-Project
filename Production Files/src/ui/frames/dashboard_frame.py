# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: DashboardFrame (v2.3 - Zero-Defect Final Version)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This is the definitive version of the DashboardFrame. It corrects two critical
# user experience flaws: the persistent hover-state visual bug and the unwanted
# entry animation.
#
# CORRECTION PROTOCOL:
#  1. MASTER STATE RESET: The `reset_state()` method is retained. It is
#     automatically invoked by the main `App` controller during navigation. Its
#     sole function is to cascade a reset command to all child `_DashboardCard`
#     components, guaranteeing their visual state is reverted to default when
#     the user navigates away from the dashboard. This solves the persistent
#     highlight bug.
#
#  2. ANIMATION ELIMINATION: The `run_entry_animation()` method has been
#     re-engineered. The call to `super().run_entry_animation()` has been
#     permanently removed. The method's only remaining function is to update the
#     dynamic welcome message. This eliminates the "upside-down" card animation,
#     resulting in a static, professional, and instantaneous frame presentation.
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



class DashboardFrame(BaseContentFrame):
    """
    The definitive landing page, featuring a dynamic welcome message, accurately
    calculated feature counts, and a responsive grid of navigation cards with
    auditory feedback and a robust state-reset protocol.
    """
    # The constructor for the DashboardFrame class.
    def __init__(
        self,
        master,
        fonts,
        frame_switcher_callback: Optional[Callable[[str], None]] = None,
        sound_manager: Optional['SoundManager'] = None
    ):
        # --- Base Class Initialization ---
        super().__init__(master, fonts)
        # --- Store a reference to the Auditory Feedback Engine.
        self.sound_manager = sound_manager
        # --- Data Store for Dynamic User Messages ---
        self.dynamic_messages = [
            "Ready to make your PC soar? Start optimizing now!",
            "Boost your system's speed with a single click.",
            "Have you tried Clean Cache? Free up space today!",
            "Your desktop deserves a snappier feel. Try UI Tweaks!",
            "Unleash your PC’s full potential with MK-Tools.",
            "Keep your system healthy with a Fix Windows scan.",
            "One click to a faster PC. Ready to dive in?",
            "Take control with Group Policy tweaks today.",
            "Dust off digital clutter and boost your PC.",
            "Clear your cache for a refreshed system now.",
            "Challenge yourself to speed up your PC today!",
            "A responsive desktop awaits. Explore UI Tweaks!",
            "Discover the magic of MK-Tools’ optimization tools.",
            "Build a rock-solid system with our tweaks.",
            "Fuel your creativity with a faster PC.",
            "Effortless optimization starts with MK-Tools.",
            "Have you checked Fix Windows? Keep your system stable!",
            "Clear the clutter for a focused digital life.",
            "Your optimization journey begins with one click.",
            "Make your desktop yours with UI Tweaks today.",
            "Refresh your PC with a quick cache clean.",
            "Unlock hidden speed with Performance Tweaks now.",
            "Trust MK-Tools for a reliable PC experience.",
            "Game smoother with Performance Tweaks. Try it!",
            "Speed up your PC in just a few clicks.",
            "Keep your system thriving with regular tweaks.",
            "Master your system with Group Policy controls.",
            "Today’s the day to make your PC shine.",
            "Break free from clutter with Clean Cache.",
            "Effortless power with MK-Tools’ optimization suite.",
            "Check the About section for exciting new updates!",
            "Say goodbye to lag with MK-Tools’ tools.",
            "Power your productivity with a tuned PC.",
            "Personalize your desktop with UI Tweaks now.",
            "A quick cache clean for a faster PC.",
            "Now’s the moment to optimize your system!",
            "Fix Windows keeps your PC running smoothly.",
            "Multitask like a pro with Performance Tweaks.",
            "Polish your PC to perfection with MK-Tools.",
            "Have you explored Group Policy? Powerful tweaks await!",
            "Maximize your PC with MK-Tools’ full suite.",
            "A fast PC is an efficient PC. Optimize now!",
            "Clear temp files for a speed boost today.",
            "Ready to optimize? Let’s make it happen!",
            "One-click fixes for a healthier PC.",
            "A healthy system starts with MK-Tools’ tweaks.",
            "Streamline your workflow with UI Tweaks today.",
            "Boost daily tasks with a tuned system.",
            "Optimization made simple with MK-Tools’ tools.",
            "Discover Clean Cache for a refreshed PC.",
            "Experience a seamless PC with MK-Tools.",
            "Make your PC more responsive with tweaks.",
            "A clean PC is a happy PC. Try it!",
            "Explore new tools to enhance your system.",
            "Customize your system with Group Policy tweaks.",
            "Reach peak performance with MK-Tools today.",
            "Free up disk space with a quick clean.",
            "Fix Windows scans for lightning-fast results.",
            "Optimize your PC for epic gaming sessions.",
            "Create a clutter-free digital workspace now.",
            "Modernize your desktop with UI Tweaks.",
            "Effortless system optimization with MK-Tools.",
            "Have you tried Performance Tweaks? Boost speed now!",
            "Build a reliable system with our tools.",
            "Refresh your PC with a cache cleanup.",
            "Maintain your PC for lasting performance.",
            "Start your optimization journey with MK-Tools.",
            "Stabilize your system with Fix Windows scans.",
            "Professionals, boost your PC with tweaks.",
            "Unleash the power of MK-Tools’ features.",
            "Clear digital clutter for a faster PC.",
            "Personalize your PC with UI Tweaks now.",
            "Quick tweaks for a speedy PC today.",
            "Clean Cache: Easy and effective optimization.",
            "Explore Group Policy for advanced system tweaks.",
            "Smooth system performance with MK-Tools.",
            "Daily performance boosts with our tweaks.",
            "Reliable scans with MK-Tools’ Fix Windows.",
            "Optimize for efficiency with MK-Tools now.",
            "A clean system boosts performance instantly.",
            "Get a responsive desktop with UI Tweaks.",
            "One-click tools for instant PC speed.",
            "New features await in MK-Tools’ suite.",
            "Control your system with Group Policy now.",
            "Speed up startup with a quick clean.",
            "A tuned PC enhances your daily work.",
            "Have you tried Fix Windows? Keep it healthy!",
            "Speed lovers, try Performance Tweaks today!",
            "Refresh your system with a cache clean.",
            "Easy optimizations with MK-Tools’ tools.",
            "Explore UI Tweaks for a better desktop.",
            "Fast and reliable: Optimize with MK-Tools.",
            "Multitask better with Performance Tweaks now.",
            "Clean Cache: Power up your PC today.",
            "Optimize your PC for creative projects.",
            "Seamless optimization with MK-Tools’ suite.",
            "Feel the speed with Performance Tweaks!",
            "A clean PC for a clear mind.",
            "New tools to enhance your system’s performance.",
            "Shape your system with Group Policy tweaks.",
            "Faster startups with a quick cache clean.",
            "A tuned PC you’ll love. Start now!",
            "Healthy PC with Fix Windows scans.",
            "Speed up your world with MK-Tools!",
            "A fresh system with Clean Cache today.",
            "Easy tools for a faster PC experience.",
            "Customize your desktop with UI Tweaks!",
            "Reliable performance with MK-Tools’ suite.",
            "Multitask effortlessly with Performance Tweaks.",
            "A powerful PC with Clean Cache now.",
            "Create freely with a tuned PC.",
            "Seamless tweaks for a better PC.",
            "Boost your PC’s speed with one click!",
            "Clear your cache for a smoother system.",
            "Have you checked UI Tweaks? Try them now!",
            "Your PC’s potential is waiting to shine.",
            "Keep your system stable with Fix Windows.",
            "One click to a more responsive PC.",
            "Take charge with Group Policy tweaks.",
            "Tidy up your PC with MK-Tools today.",
            "Free up space with a Clean Cache run.",
            "Speed up your PC with a single tweak!",
            "Make your desktop pop with UI Tweaks.",
            "Discover MK-Tools’ tools for a faster PC.",
            "A stable system starts with MK-Tools.",
            "Unleash creativity with a speedy PC.",
            "Optimize effortlessly with MK-Tools’ tools.",
            "Have you tried Fix Windows? Scan now!",
            "Clear clutter for a focused PC experience.",
            "Your optimization adventure starts today!",
            "Personalize your desktop with UI Tweaks.",
            "Refresh your system with Clean Cache now.",
            "Unlock speed with Performance Tweaks today.",
            "Trust MK-Tools for a dependable PC.",
            "Game better with Performance Tweaks now.",
            "Speed up tasks with a quick optimization.",
            "A healthy PC with MK-Tools’ care.",
            "Master your system with Group Policy.",
            "Make today a great day for your PC!",
            "Clear digital mess with Clean Cache.",
            "Effortless tweaks for a faster PC.",
            "Check out MK-Tools’ latest optimization tools!",
            "No lag, just speed with MK-Tools.",
            "Power your work with a tuned PC.",
            "Have you explored UI Tweaks? Start now!",
            "A snappier PC with Performance Tweaks.",
            "A clean system for a productive day.",
            "Explore MK-Tools for a better PC.",
            "Control your PC with Group Policy tweaks.",
            "Faster boot times with a quick clean.",
            "A tuned PC for a smoother workflow.",
            "Fix Windows for a healthier system today.",
            "Speed up with Performance Tweaks now!",
            "A fresh PC with Clean Cache magic.",
            "Easy optimization for a better PC.",
            "Make your desktop yours with UI Tweaks.",
            "Reliable tweaks with MK-Tools’ suite.",
            "Multitask smoothly with Performance Tweaks.",
            "Power your PC with Clean Cache today.",
            "Create without limits with a tuned PC.",
            "Seamless performance with MK-Tools’ tools.",
            "Boost speed with a single click now!",
            "Clear cache for a faster PC today.",
            "Have you tried Group Policy? Explore it!",
            "Your PC’s ready to shine with MK-Tools.",
            "Stabilize your system with Fix Windows.",
            "One-click tweaks for a responsive PC.",
            "Take control with Group Policy today.",
            "Clean up your PC with MK-Tools now.",
            "Free space with a Clean Cache sweep.",
            "Speed up your system with one tweak!",
            "Make your desktop shine with UI Tweaks.",
            "Discover MK-Tools for a smoother PC.",
            "A stable PC with MK-Tools’ tweaks.",
            "Unleash your PC’s speed with tweaks.",
            "Optimize easily with MK-Tools’ suite.",
            "Have you checked Clean Cache? Try it!",
            "Clear clutter for a snappier PC.",
            "Your optimization journey starts now!",
            "Personalize your system with UI Tweaks.",
            "Refresh your PC with a quick clean.",
            "Unlock performance with Performance Tweaks.",
            "Trust MK-Tools for a faster system.",
            "Game smoothly with Performance Tweaks today.",
            "Speed up tasks with MK-Tools’ tools.",
            "A healthy PC with regular tweaks.",
            "Master your PC with Group Policy now.",
            "Make your PC soar with MK-Tools!",
            "Clear digital clutter with Clean Cache.",
            "Effortless speed with MK-Tools’ tweaks.",
            "Check MK-Tools’ features for a better PC!",
            "No more lag with MK-Tools’ optimizations.",
            "Power your tasks with a tuned PC.",
            "Have you tried UI Tweaks? Customize now!",
            "A responsive PC with Performance Tweaks.",
            "A clean system for a better day.",
            "Explore MK-Tools for a faster system.",
            "Control your system with Group Policy.",
            "Faster startups with MK-Tools’ tools.",
            "A tuned PC for a productive day.",
            "Fix Windows for a stable PC now.",
            "Speed up with Performance Tweaks today!",
            "A fresh system with Clean Cache now.",
            "Easy tweaks for a smoother PC.",
            "Customize your desktop with UI Tweaks today.",
            "Reliable performance with MK-Tools’ tools.",
            "Multitask better with Performance Tweaks.",
            "Power up with a Clean Cache run.",
            "Create freely with a faster PC.",
            "Seamless tweaks with MK-Tools’ suite.",
            "Boost your PC with one click now!",
            "Clear cache for a responsive system.",
            "Have you checked Fix Windows? Scan today!",
            "Your PC’s ready for a speed boost.",
            "Stabilize your PC with MK-Tools’ tools.",
            "One-click optimization for a better PC.",
            "Take charge with Group Policy tweaks now.",
            "Clean your PC with MK-Tools today.",
            "Free up space with Clean Cache now.",
            "Speed up your PC with MK-Tools!",
            "Make your desktop pop with UI Tweaks.",
            "Discover MK-Tools for a stable PC.",
            "A reliable system with MK-Tools’ tweaks.",
            "Unleash speed with Performance Tweaks now.",
            "Optimize easily with MK-Tools’ tools.",
            "Have you tried Clean Cache? Start now!",
            "Clear clutter for a faster system.",
            "Your PC’s optimization starts today!",
            "Personalize your PC with UI Tweaks.",
            "Refresh your system with Clean Cache.",
            "Unlock speed with MK-Tools’ tweaks.",
            "Trust MK-Tools for a smooth PC.",
            "Game better with Performance Tweaks now.",
            "Speed up tasks with a quick tweak.",
            "A healthy system with MK-Tools’ care.",
            "Master your system with Group Policy tweaks."
        ]
        # --- Navigation Callback Configuration ---
        if frame_switcher_callback is None and hasattr(master, "select_frame_by_name"):
            frame_switcher_callback = master.select_frame_by_name
        self._navigate = frame_switcher_callback

        # --- UI Construction Protocol ---
        self._create_header()
        self._create_card_grid()

    # ───────────────────────── INTERNAL UI BUILDERS ────────────────────── #

    def _create_header(self) -> None:
        """Creates the top header and the dynamic inspirational message using the universal emoji font."""
        # --- Retrieve the current user's username with a safe fallback protocol.
        try:
            username = getpass.getuser()
        except Exception as e:
            logging.error(f"Could not get username: {e}. Defaulting to 'User'.")
            username = "User"

        # --- Create a container frame for the header elements to ensure proper alignment.
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="n")

        # --- [CRITICAL FIX] Render the welcome emoji using the universal, pre-scaled emoji font from the Theme class.
        # --- This guarantees identical rendering on all target operating systems.
        ctk.CTkLabel(header_frame, text="🎉", font=self.fonts["emoji_large"]).pack(side="left", padx=(0, 10))

        # --- Create the standard text labels using the default theme font.
        ctk.CTkLabel(header_frame, text="Welcome ", font=self.fonts["title"], text_color=Theme.TEXT).pack(side="left")
        ctk.CTkLabel(header_frame, text=username, font=self.fonts["title"], text_color=Theme.ACCENT).pack(side="left")
        ctk.CTkLabel(header_frame, text="! to MK-Tools ", font=self.fonts["title"], text_color=Theme.TEXT).pack(side="left")

        # --- [CRITICAL FIX] Render the rocket emoji using the universal emoji font for consistency.
        ctk.CTkLabel(header_frame, text="🚀", font=self.fonts["emoji_large"]).pack(side="left")

        # --- Create the dynamic message label that updates upon frame entry.
        dynamic_message_text = random.choice(self.dynamic_messages)
        self.dynamic_message_label = ctk.CTkLabel(
            self,
            text=dynamic_message_text,
            font=self.fonts["normal"],
            text_color=Theme.TEXT_SECONDARY,
        )
        self.dynamic_message_label.grid(row=1, column=0, columnspan=2, pady=(5, 20), sticky="n")


    def _create_card_grid(self) -> None:
        """Creates and arranges all interactive and static cards on a responsive grid."""
        # --- [ICON REFACTOR] The 'icon' key now holds the file path to the PNG asset.
        sections = [
            # --- [MODIFIED] Use resource_path to resolve icon paths at runtime.
            {"frame": "performance", "icon_path": resource_path(os.path.join("assets", "icons", "Performance-Icon.png")), "title": "Performance Tweaks", "features": 5},
            {"frame": "ui_tweaks",   "icon_path": resource_path(os.path.join("assets", "icons", "UI-Responsiveness.png")), "title": "UI & Responsiveness", "features": 4},
            {"frame": "fix_windows", "icon_path": resource_path(os.path.join("assets", "icons", "FixWindows.png")), "title": "Fix Windows",         "features": 2},
            {"frame": "clean_cache", "icon_path": resource_path(os.path.join("assets", "icons", "Clean-Cache.png")), "title": "Clean Cache",         "features": 6},
            {"frame": "policy",      "icon_path": resource_path(os.path.join("assets", "icons", "Group-Policy.png")), "title": "Group Policy",        "features": 2},
        ]

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Store cards in the parent class's list for state management.
        self.cards = []

        for idx, sec in enumerate(sections):
            row, col = divmod(idx, 2)
            card = _DashboardCard(
                master=self,
                fonts=self.fonts,
                icon_path=sec["icon_path"], # Pass the icon_path
                title=sec["title"],
                feature_count=sec["features"],
                command=lambda name=sec["frame"]: self._safe_nav(name),
                sound_manager=self.sound_manager
            )
            card.grid(row=row + 2, column=col, padx=25, pady=25, sticky="nsew")
            self.cards.append(card) # Add the interactive card to the list.

        final_row, final_col = divmod(len(sections), 2)
        coming_soon_card = _ComingSoonCard(master=self, fonts=self.fonts)
        coming_soon_card.grid(row=final_row + 2, column=final_col, padx=25, pady=25, sticky="nsew")
        self.cards.append(coming_soon_card)

    def _update_dynamic_message(self) -> None:
        """Selects a new random message and updates the message label."""
        if hasattr(self, 'dynamic_message_label') and hasattr(self, 'dynamic_messages'):
            new_message = random.choice(self.dynamic_messages)
            self.dynamic_message_label.configure(text=new_message)

    def _safe_nav(self, frame_name: str) -> None:
        """Safely invokes the navigation callback and plays a click sound."""
        if callable(self._navigate):
            if self.sound_manager:
                self.sound_manager.play_sound('click')
            self._navigate(frame_name)

    def run_entry_animation(self):
        """
        [RE-ENGINEERED] This method is called when the frame becomes visible.
        It now ONLY updates the dynamic message and does NOT perform any animations.
        """
        self._update_dynamic_message()
        # The call to super().run_entry_animation() has been removed to disable the animation.

    def reset_state(self):
        """
        Implements the master reset protocol for this frame. This is called
        automatically when the user navigates away from the dashboard. It commands
        all child cards to reset their visual state.
        """
        logging.info("Resetting DashboardFrame state: Reverting all card highlights.")
        # Iterate through all cards and command them to reset their hover state.
        for card in self.cards:
            # Check if the card has the reset_state method before calling it.
            # This makes the code robust, as _ComingSoonCard does not have this method.
            if hasattr(card, 'reset_state'):
                card.reset_state()

    def update_ui_scaling(self, fonts):
        """
        [NEW] Propagates font updates to all child cards, ensuring their icons
        and text are correctly rescaled.
        """
        super().update_ui_scaling(fonts)
        if self.winfo_exists():
            # --- Update the dynamic message label font.
            if hasattr(self, 'dynamic_message_label'):
                self.dynamic_message_label.configure(font=fonts["normal"])

            # --- Cascade the scaling update to all child cards.
            for card in self.cards:
                if hasattr(card, "update_ui_scaling"):
                    card.update_ui_scaling(fonts)
