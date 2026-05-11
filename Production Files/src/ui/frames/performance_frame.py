# ========================================================================
# Auto-generated extraction from main.py
# ========================================================================

# ===================================================================================
# CLASS: PerformanceFrame (v1.8 - Shutdown-Aware)
#
# ARCHITECTURAL BLUEPRINT (UPGRADE):
# This component has been upgraded to be a shutdown-aware dependency injector.
# It now accepts the master `app_instance` from the application core.
#
# CORE ENHANCEMENTS:
#  1. CONSTRUCTOR MODIFICATION: The `__init__` method now accepts `app_instance`
#     as a mandatory argument.
#
#  2. DEPENDENCY PROPAGATION: When instantiating child `AnimatedTweakCard`
#     components, it now passes the `app_instance` reference down the hierarchy.
#     This ensures every component with background threads has a direct line to the
#     application's global shutdown signal, completing its role in the graceful
#     shutdown protocol.
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



class PerformanceFrame(BaseContentFrame):
    """
    Page dedicated to performance-related tweaks, now fully integrated with the
    application's graceful shutdown protocol.
    """
    # [MODIFIED] The constructor now accepts the app_instance.
    def __init__(self, master, fonts, app_instance, sound_manager: Optional['SoundManager'] = None):
        # --- Base class initialization. ---
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
        self.header_label = ctk.CTkLabel(header_container, text="Performance Tweaks", font=self.fonts["title"], text_color=Theme.TEXT)
        self.header_label.grid(row=0, column=1, sticky="w")

        # --- Initial call to load and scale the icon.
        self.update_ui_scaling(self.fonts)

        # --- Logic Controller Instantiation ---
        svchost_logic = SvcHostSplitTweak()
        foreground_priority_logic = ForegroundPriorityController()
        gpu_scheduling_logic = GPUSchedulingTweak()
        fast_startup_logic = DisableFastStartupTweak()
        compressed_memory_logic = DisableCompressedMemoryTweak()

        # --- Foreground Application Priority Information Payload ---
        FOREGROUND_PRIORITY_INFO = {
            'title': "🎯 Prioritize Foreground Applications",
            'description': (
                "This Windows optimization gives more CPU and system resources to the application or game "
                "you are actively using, while slightly reducing resources for background apps. "
                "It can make your current tasks feel smoother and more responsive, especially on systems "
                "that run many apps at once."
            ),
            'pros': [
                "Makes active apps and games feel faster and more responsive.",
                "Can reduce stuttering and input lag in foreground applications.",
                "Improves overall experience on PCs with limited CPU power.",
                "A safe, native Windows setting that can be easily reverted."
            ],
            'cons': [
                "Background processes, like downloads or video rendering, may run slower.",
                "Benefits may be less noticeable on high-end CPUs with many cores.",
                "Requires a system restart to fully apply the changes."
            ]
        }
        # --- GPU Scheduling Information Payload ---
        GPU_SCHEDULING_INFO = {
            'title': "🎮 Hardware-Accelerated GPU Scheduling",
            'description': (
                "Hardware-Accelerated GPU Scheduling is a Windows feature that lets your graphics card (GPU) "
                "manage its own video memory (VRAM) instead of relying heavily on the CPU. "
                "This can reduce input lag and improve performance in games and GPU-heavy tasks. "
                "However, the benefits depend on your GPU type, driver support, and the applications you use."
            ),
            'pros': [
                "Can reduce input latency in games, making controls feel more responsive.",
                "May slightly improve performance in GPU-intensive games and creative applications.",
                "Helps the CPU by offloading some graphics-related work to the GPU itself.",
                "A lightweight feature that is easy to enable or disable through Windows settings."
            ],
            'cons': [
                "Performance improvements are often small or unnoticeable in many games.",
                "Can occasionally cause stutters, crashes, or other instability on some systems.",
                "Requires a system restart after enabling or disabling to take effect."
            ],
        }
        # --- Fast Startup and Compressed Memory Information Payloads ---
        FAST_STARTUP_INFO = {
            'title': "⏱️ Disable Fast Startup",
            'description': (
                "Fast Startup is a Windows feature that makes your computer start faster after shutting it down. "
                "Instead of completely turning off, Windows saves part of itself (the system core) to the disk and "
                "uses that saved state to start faster next time. When you disable Fast Startup, Windows will perform "
                "a full shutdown and a clean startup every time. This can make your system more stable, fully refresh "
                "your hardware, and avoid certain performance or compatibility problems, but it may start a bit slower."
            ),
            'pros': [
                "Fully resets the CPU and system memory, which can improve long-term stability and performance.",
                "Can fix issues with USB devices, Wi-Fi, or other hardware not being detected after shutdown.",
                "Better for dual-boot systems because your Windows drive is fully unlocked and safe to access.",
                "Reduces the chance of driver conflicts or small system glitches caused by partial shutdowns.",
                "Helps ensure system updates or BIOS/firmware changes apply correctly without problems."
            ],
            'cons': [
                "Your computer may take a little longer to start from a complete shutdown.",
                "More power and resources are used during startup compared to Fast Startup.",
                "Not ideal for users who shut down and start up their computer many times a day.",
                "Modern SSDs already boot very quickly, so the speed difference may not be worth it for some users.",
                "After a shutdown or power loss, Windows will take a bit longer to be ready to use."
            ]
        }
        # --- Disable Compressed Memory Information Payload ---
        COMPRESSED_MEMORY_INFO = {
            'title': "🧠 Disable Compressed Memory",
            'description': (
                "Windows uses a feature called Memory Compression to store more data in RAM by compressing "
                "less-used memory pages. This reduces the need to use the page file on your disk, which can help "
                "on systems with limited RAM. However, compressing and decompressing memory uses CPU power. "
                "Disabling it can improve real-time performance and responsiveness on systems with plenty of RAM "
                "(16GB or more), but it is not recommended for PCs with low memory."
            ),
            'pros': [
                "Reduces background CPU usage, freeing resources for games and creative apps.",
                "Can improve responsiveness on systems with 16GB or more RAM.",
                "Helps prevent micro-stutters in latency-sensitive applications like gaming or music production.",
                "Gives more consistent performance if your CPU is often near 100% usage."
            ],
            'cons': [
                "Not recommended for PCs with less than 16GB RAM because it may cause faster memory exhaustion.",
                "If you run out of RAM, system performance will drop more sharply without compression.",
                "Requires a system restart for the change to take effect."
            ]
        }


        # --- Master Data Structure for UI Cards ---
        tweaks_data = [
                {
                    'title': "Disable Fast Startup", 'description': "Ensures a Full Shutdown of Your Computer 🖥️", 'emoji': "⏱️",
                    'view_mode': 'toggle', 'tweak_logic': fast_startup_logic, 'info_data': FAST_STARTUP_INFO
                },
                {
                    'title': "Disable Compressed Memory", 'description': "Reduces CPU usage on systems with 16GB+ RAM.", 'emoji': "🧠",
                    'view_mode': 'toggle', 'tweak_logic': compressed_memory_logic, 'info_data': COMPRESSED_MEMORY_INFO
                },
                {
                    'title': "Hardware-Accelerated GPU Scheduling", 'description': "Allows the GPU to manage its own memory.", 'emoji': "🎮",
                    'view_mode': 'config_dropdown', 'tweak_logic': gpu_scheduling_logic, 'info_data': GPU_SCHEDULING_INFO
                },
                {
                    'title': "Prioritize Foreground Applications", 'description': "Allocates more processor resources to the active app.", 'emoji': "🎯",
                    'view_mode': 'toggle', 'tweak_logic': foreground_priority_logic, 'info_data': FOREGROUND_PRIORITY_INFO
                },
                {
                    'title': "Optimize SvcHost Combining",
                    'description': "Reduces stress on your CPU and improves performance",
                    'emoji': "🔗",
                    'view_mode': 'config_dropdown',
                    'tweak_logic': svchost_logic,
                    'info_data': {
                        'title': "⚙️ SvcHost Combining Explained",
                        'description': (
                            "This feature fine-tunes how Windows manages background services by grouping more of them together, "
                            "so your CPU has fewer processes to handle. This is especially helpful if you have plenty of RAM but a processor with fewer cores.\n\n"
                            "Our application uses next-generation, military-grade optimization algorithms to ensure every change is safe, precise, "
                            "and tailored to your system’s performance profile. The process is fully automated, thoroughly tested, and designed to boost speed "
                            "while keeping your computer stable and protected."
                        ),
                        'pros': [
                            "✅ Reduces the number of running processes, lowering CPU workload.",
                            "✅ Can make the system feel smoother and more responsive.",
                            "✅ Uses safe, precision-engineered algorithms with built-in protection.",
                            "✅ Ideal for systems with high RAM and lower-end CPUs.",
                            "✅ Fully reversible — your system can be restored to default instantly."
                        ],
                        'cons': [
                            "❌ In rare cases, may slightly affect service stability depending on configuration.",
                            "❌ Uses a small amount of extra RAM, which is negligible on modern systems."
                        ],
                    }
                }
        ]
        # --- Card Instantiation ---
        self.cards = [AnimatedTweakCard(self, self.fonts, app_instance=self.app, sound_manager=self.sound_manager, **data) for data in tweaks_data]

        # --- Post-Instantiation Wiring Protocol ---
        svchost_card = next((card for card in self.cards if "SvcHost" in card.title_label.cget("text")), None)
        if svchost_card: svchost_card.custom_config_panel_builder = svchost_card._create_svchost_config_panel

        gpu_card = next((card for card in self.cards if "GPU Scheduling" in card.title_label.cget("text")), None)
        if gpu_card: gpu_card.custom_config_panel_builder = gpu_card._create_gpu_config_panel

        # --- Final UI Rendering ---
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

    def reset_state(self):
        """Implements the master reset protocol for this frame."""
        logging.info("Resetting PerformanceFrame state: Closing all open panels.")
        for card in self.cards:
            if hasattr(card, 'close_all_panels'):
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
                    Image.open(resource_path(os.path.join("assets", "icons", "Rocket.png"))),
                    size=(new_icon_size, new_icon_size)
                )
                # --- Apply the new, rescaled image to the label.
                self.header_icon.configure(image=self.header_icon_image)
            except Exception as e:
                logging.error(f"Failed to load or resize header icon: {e}")
                self.header_icon.configure(image=None, text="⚠️") # Fallback
