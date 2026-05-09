

                                        MK-TOOLS v1.0 - The Definitive Windows Optimization Suite
                                            Authored by: Mohammed Kashan Tariq
                                                Last Updated: August 10, 2025

========================================================================================================================
|| TABLE OF CONTENTS
========================================================================================================================

[1.0] INTRODUCTION: THE MISSION
    [1.1] What is MK-Tools?
    [1.2] The Philosophy: Power to the User
    [1.3] Core Pillars of Design

[2.0] SYSTEM REQUIREMENTS & INSTALLATION
    [2.1] Supported Operating Systems
    [2.2] A Note on Administrator Privileges
    [2.3] Installation Protocol

[3.0] GETTING STARTED: THE USER INTERFACE
    [3.1] The Navigation Rail: Your Command Center
    [3.2] The Dashboard: Your Mission Hub
    [3.3] Auditory Feedback Engine (AFE): The Sound Toggle

[4.0] CORE FEATURES: A DEEP DIVE
    [4.1] Performance Tweaks: Unleash Your PC's Potential
        [4.1.1] Disable Fast Startup
        [4.1.2] Disable Compressed Memory
        [4.1.3] Hardware-Accelerated GPU Scheduling
        [4.1.4] Prioritize Foreground Applications
        [4.1.5] Optimize SvcHost Splitting
    [4.2] UI & Responsiveness: A Snappier Experience
        [4.2.1] Enable Classic Right-Click Menu (Windows 11)
        [4.2.2] Instant Menu Display
        [4.2.3] 100% JPEG Wallpaper Quality
        [4.2.4] Disable Web Search in Start Menu
    [4.3] Fix Windows: System Integrity Operations
        [4.3.1] Scan (SFC /scannow)
        [4.3.2] Advanced Scan (DISM)
    [4.4] Clean Cache: Reclaim Your Disk Space
        [4.4.1] The "Clean All" Protocol
        [4.4.2] Manual Cleanup Operations (In-Depth)
    [4.5] Group Policy: Military-Grade System Hardening
        [4.5.1] Apply Optimized Policies
        [4.5.2] Reset Policies to Default

[5.0] TROUBLESHOOTING & SUPPORT
    [5.1] The Failsafe Protocol: "The App Crashed!"
    [5.2] "A Tweak Didn't Work or is Grayed Out"
    [5.3] Contact & Support Channels

[6.0] FREQUENTLY ASKED QUESTIONS (FAQ)

[7.0] LICENSE & CREDITS

[8.0] FINAL WORDS

========================================================================================================================
|| [1.0] INTRODUCTION: THE MISSION
========================================================================================================================

Welcome, and thank you for choosing MK-Tools. You have just installed more than a simple utility; you have installed a new paradigm for interacting with your Windows operating system.

------------------------------------------------------------------------------------------------------------------------
[1.1] What is MK-Tools?
------------------------------------------------------------------------------------------------------------------------

MK-Tools is a military-grade optimization suite designed for both novice users and seasoned IT professionals. Its singular purpose is to make the complex, often intimidating world of Windows system tweaking accessible, safe, and effective for everyone.

For too long, unlocking the true potential of a Windows PC has required obscure command-line knowledge, risky registry edits, and hours of research. MK-Tools changes that. It consolidates a curated, hand-picked selection of the most impactful and safest performance, UI, and security tweaks into a single, beautiful, and intuitive interface.

This is not a random collection of "hacks." Every feature within MK-Tools has been meticulously selected based on years of hands-on experience in system administration and performance tuning. Each tweak is reversible, well-documented, and implemented using the most reliable, industry-standard methods.

------------------------------------------------------------------------------------------------------------------------
[1.2] The Philosophy: Power to the User
------------------------------------------------------------------------------------------------------------------------

The core philosophy of MK-Tools is empowerment. The modern Windows operating system is a powerful, complex beast. Over time, it can become sluggish, cluttered, and unstable. While the tools to fix these issues exist, they are often buried deep within the system, inaccessible to the average user.

MK-Tools was born from the desire to bridge this gap. It is built on the belief that you, the user, should have ultimate control over your machine's performance, privacy, and behavior, without needing a degree in computer science.

We achieve this through:
    - **Radical Simplicity:** Transforming complex operations into one-click actions.
    - **Absolute Safety:** Ensuring every action is reversible and providing clear information about what each tweak does.
    - **Engaging Experience:** A "gamified" interface with rich visual and auditory feedback that makes system maintenance feel rewarding, not like a chore.

------------------------------------------------------------------------------------------------------------------------
[1.3] Core Pillars of Design
------------------------------------------------------------------------------------------------------------------------

Every aspect of MK-Tools is built upon four non-negotiable pillars:

    1.  **PERFORMANCE:** Unlock hidden speed, reduce latency, and allocate system resources more intelligently to make your PC feel faster and more responsive, whether you're gaming, creating, or working.

    2.  **STABILITY:** Repair corrupted system files, clean up digital clutter that can cause conflicts, and revert your system to a known-good state with powerful, integrated diagnostic tools.

    3.  **PRIVACY & SECURITY:** Take control of your data by disabling unnecessary telemetry and web-integrated features. Apply a curated set of security-hardening group policies to protect your system.

    4.  **USER EXPERIENCE:** A beautiful, modern, and intuitive interface that is a pleasure to use. Every click, hover, and transition is designed to be clear, responsive, and satisfying.

========================================================================================================================
|| [2.0] SYSTEM REQUIREMENTS & INSTALLATION
========================================================================================================================

------------------------------------------------------------------------------------------------------------------------
[2.1] Supported Operating Systems
------------------------------------------------------------------------------------------------------------------------

MK-Tools is engineered for the modern Windows ecosystem.

-   **Primary Support:** Windows 10 (Pro, Enterprise, Education) & Windows 11 (Pro, Enterprise, Education)
-   **Partial Support:** Windows 10/11 Home Editions. All features EXCEPT for the "Group Policy" section will function correctly. The Group Policy Editor is not included in Home editions of Windows.

------------------------------------------------------------------------------------------------------------------------
[2.2] A Note on Administrator Privileges
------------------------------------------------------------------------------------------------------------------------

**MK-Tools requires administrative privileges to run.** This is not optional; it is a fundamental requirement for the application to function.

**Why?**
The very nature of system optimization involves modifying settings that affect the entire operating system. This includes writing to protected areas of the Windows Registry, interacting with system services, and running diagnostic tools like SFC and DISM. Without administrator rights, Windows would block these actions, rendering the application useless.

When you launch MK-Tools, you will see a User Account Control (UAC) prompt. This is the standard, secure Windows method for granting an application the necessary permissions. Please click "Yes" to proceed.

------------------------------------------------------------------------------------------------------------------------
[2.3] Installation Protocol
------------------------------------------------------------------------------------------------------------------------

The installation process is streamlined for simplicity and transparency.

1.  **Run the Installer:** Double-click `setup_MK-Tools(v1.0).exe`.
2.  **UAC Prompt:** Accept the User Account Control prompt to allow the installer to make changes.
3.  **License Agreement:** You will be presented with the license agreement. Please read it and accept the terms to continue.
4.  **Select Destination:** Choose an installation location. The default is your Program Files directory, which is recommended.
5.  **Select Tasks:** Choose whether to create Desktop and/or Start Menu shortcuts.
6.  **Install:** The installer will copy all necessary files to the selected location.
7.  **Finish:** On the final page, you can choose to launch MK-Tools and/or view this Readme file.

========================================================================================================================
|| [3.0] GETTING STARTED: THE USER INTERFACE
========================================================================================================================

The MK-Tools interface is designed to be clean, intuitive, and powerful.

------------------------------------------------------------------------------------------------------------------------
[3.1] The Navigation Rail: Your Command Center
------------------------------------------------------------------------------------------------------------------------

The vertical panel on the left side of the application is the Navigation Rail. This is your primary method of moving between the different feature sections of MK-Tools.

-   **Dashboard:** Your home base and mission hub.
-   **Performance:** Tweaks focused on system speed and resource management.
-   **UI Tweaks:** Adjustments to make the Windows interface faster and more responsive.
-   **Fix Windows:** Powerful tools for diagnosing and repairing system file corruption.
-   **Clean Cache:** Utilities for freeing up disk space by removing temporary and unnecessary files.
-   **Group Policy:** A curated set of advanced policies for security and privacy (Pro editions only).
-   **About:** Information about the application, its creator, and how to get in touch.

------------------------------------------------------------------------------------------------------------------------
[3.2] The Dashboard: Your Mission Hub
------------------------------------------------------------------------------------------------------------------------

The Dashboard is the first screen you see. It provides a high-level overview of the available optimization categories. Each card on the dashboard serves as a quick-launch button to jump directly to that section. It also features a dynamic welcome message to inspire your optimization journey!

------------------------------------------------------------------------------------------------------------------------
[3.3] Auditory Feedback Engine (AFE): The Sound Toggle
------------------------------------------------------------------------------------------------------------------------

MK-Tools features a rich soundscape to provide satisfying feedback for your actions. At the bottom of the Navigation Rail, you will find a Sound Icon.

-   **Clicking this icon** will toggle all application sounds ON or OFF.
-   The application will remember your preference for the duration of the session.

========================================================================================================================
|| [4.0] CORE FEATURES: A DEEP DIVE
========================================================================================================================

This section provides a complete, transparent breakdown of every single feature within MK-Tools.

------------------------------------------------------------------------------------------------------------------------
[4.1] Performance Tweaks: Unleash Your PC's Potential
------------------------------------------------------------------------------------------------------------------------

This section is dedicated to modifications that directly impact your system's speed, responsiveness, and resource management.

---
[4.1.1] Disable Fast Startup
---
    - **What It Does (The "ELI5"):**
      Imagine putting your computer to "sleep" instead of fully shutting it down. That's what Fast Startup does. It makes boot times faster, but it means your system never gets a truly fresh start. Disabling it forces a full, clean shutdown every time, which can solve many strange hardware and software issues.

    - **Technical Deep Dive (The "How"):**
      This tweak modifies a single DWORD value in the Windows Registry.
      - **Path:** `HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Power`
      - **Value:** `HiberbootEnabled`
      - **Tweak ON (Fast Startup Disabled):** Sets the value to `0`.
      - **Tweak OFF (Fast Startup Enabled):** Sets the value to `1` (Windows Default).

    - **Pros:**
      - Solves issues with drivers, USB devices, or dual-boot setups not working correctly after a shutdown.
      - Ensures a complete system refresh, improving long-term stability.
      - Guarantees that pending Windows Updates are applied correctly.

    - **Cons:**
      - Your computer's startup time from a full shutdown will be slightly longer.

    - **Reversibility & Safety:** 100% reversible. This is a standard Windows setting. Safety Rating: Very High.
    - **Required Action:** A full shutdown or restart is required for the change to take effect.

---
[4.1.2] Disable Compressed Memory
---
    - **What It Does (The "ELI5"):**
      To avoid slowing down by using your hard drive, Windows sometimes "squishes" (compresses) old data in your RAM to make more room. This squishing process uses a little bit of CPU power. If you have plenty of RAM (16GB or more), turning this off can free up that CPU power for your games and applications, making them run smoother.

    - **Technical Deep Dive (The "How"):**
      This tweak interfaces with the official Windows Memory Management Agent (MMAgent) via PowerShell. It does not perform manual registry edits.
      - **Tweak ON (Compression Disabled):** Executes the `Disable-MMAgent -MemoryCompression` cmdlet.
      - **Tweak OFF (Compression Enabled):** Executes the `Enable-MMAgent -MemoryCompression` cmdlet (Windows Default).

    - **Pros:**
      - Reduces background CPU usage, which can reduce micro-stutters in games.
      - Improves performance in CPU-intensive applications on systems with sufficient RAM.

    - **Cons:**
      - **NOT RECOMMENDED** for systems with less than 16GB of RAM. Disabling it on low-memory systems can lead to worse performance as the system is forced to use the much slower page file on your disk.

    - **Reversibility & Safety:** 100% reversible. Uses official Microsoft cmdlets. Safety Rating: High (when used on appropriate hardware).
    - **Required Action:** A system restart is required for the change to take effect.

---
[4.1.3] Hardware-Accelerated GPU Scheduling
---
    - **What It Does (The "ELI5"):**
      This lets your powerful graphics card (GPU) take more control over its own schedule, like a manager handling their own team instead of waiting for instructions from the main boss (the CPU). This can reduce input lag and make games feel more responsive.

    - **Technical Deep Dive (The "How"):**
      This tweak modifies a DWORD value in the Windows Registry.
      - **Path:** `HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers`
      - **Value:** `HwSchMode`
      - **Tweak ON:** Sets the value to `2`.
      - **Tweak OFF:** Sets the value to `1`.
      - **Reset to Default:** Deletes the `HwSchMode` value entirely.

    - **Pros:**
      - Can reduce latency and improve performance in some modern, GPU-intensive games.
      - Offloads work from the CPU to the GPU.

    - **Cons:**
      - Requires a modern GPU (NVIDIA 10 series / AMD 5600 series or newer) and up-to-date drivers.
      - Performance gains can be minimal or non-existent in some titles.
      - Has been known to cause instability or crashes in a small number of older games.

    - **Reversibility & Safety:** 100% reversible. Standard Windows feature. Safety Rating: High.
    - **Required Action:** A system restart is required for the change to take effect.

---
[4.1.4] Prioritize Foreground Applications
---
    - **What It Does (The "ELI5"):**
      This tells Windows to give more "attention" (CPU resources) to the window you are currently using. It's like telling your computer, "Hey, this game I'm playing right now is the most important thing. Give it all the power it needs!"

    - **Technical Deep Dive (The "How"):**
      This tweak modifies a DWORD value in the Windows Registry.
      - **Path:** `HKLM:\SYSTEM\CurrentControlSet\Control\PriorityControl`
      - **Value:** `Win32PrioritySeparation`
      - **Tweak ON (Optimized):** Sets the value to `38` (Hex: 0x26).
      - **Tweak OFF (Default):** Sets the value to `2` (Hex: 0x2).

    - **Pros:**
      - Makes the active application feel smoother and more responsive.
      - Can reduce stuttering in games or applications on systems with high background process load.

    - **Cons:**
      - Background tasks (like file downloads or video rendering) may proceed more slowly.
      - The effect is less noticeable on high-end CPUs with many cores.

    - **Reversibility & Safety:** 100% reversible. Standard Windows feature. Safety Rating: Very High.
    - **Required Action:** A system restart is required for the change to take full effect.

---
[4.1.5] Optimize SvcHost Splitting
---
    - **What It Does (The "ELI5"):**
      Windows groups many of its background services together into a single process called "svchost.exe" to save RAM. On modern computers with plenty of RAM, this isn't necessary. This tweak tells Windows to give each service its own process. If one service crashes, it won't take others down with it, leading to a more stable system.

    - **Technical Deep Dive (The "How"):**
      This tweak modifies a DWORD value in the Windows Registry. The value is dynamically calculated to be equal to the total amount of physical RAM in kilobytes.
      - **Path:** `HKLM:\SYSTEM\CurrentControlSet\Control`
      - **Value:** `SvcHostSplitThresholdInKB`
      - **Tweak ON (Optimized):** Sets the value to `Total System RAM in KB`.
      - **Tweak OFF (Default):** Sets the value back to the Windows default.

    - **Pros:**
      - Greatly improves system stability, as a single faulty service cannot crash an entire group.
      - Makes it easier to identify resource-hungry services in Task Manager.

    - **Cons:**
      - Uses slightly more RAM, as there are more individual processes running. Not recommended for systems with less than 8GB of RAM.

    - **Reversibility & Safety:** 100% reversible. Safety Rating: High (on appropriate hardware).
    - **Required Action:** A system restart is required for the change to take effect.

------------------------------------------------------------------------------------------------------------------------
[4.2] UI & Responsiveness: A Snappier Experience
------------------------------------------------------------------------------------------------------------------------

This section focuses on tweaks that make the Windows graphical user interface (GUI) feel faster, more efficient, and less cluttered.

---
[4.2.1] Enable Classic Right-Click Menu (Windows 11)
---
    - **What It Does (The "ELI5"):**
      In Windows 11, the right-click menu is simplified, hiding many options behind a "Show more options" button. This tweak gets rid of that extra click and brings back the full, classic right-click menu from Windows 10.

    - **Technical Deep Dive (The "How"):**
      This tweak creates a specific registry key. Its presence is what triggers the classic menu behavior.
      - **Path:** `HKCU:\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32`
      - **Tweak ON:** Creates the key and sets its `(Default)` value to be empty.
      - **Tweak OFF:** Deletes the `{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}` key entirely.

    - **Pros:**
      - Saves time and clicks for users who frequently use context menu options.
      - Restores functionality for older applications that add items to the classic menu.

    - **Cons:**
      - You lose the cleaner, more modern aesthetic of the Windows 11 menu.

    - **Reversibility & Safety:** 100% reversible. Safety Rating: Very High.
    - **Required Action:** The Windows Explorer shell is automatically restarted to apply the change instantly.

---
[4.2.2] Instant Menu Display
---
    - **What It Does (The "ELI5"):**
      Windows has a tiny, built-in delay before any menu appears after you click. This tweak removes that delay completely, making all menus (right-click, application menus, etc.) appear instantly.

    - **Technical Deep Dive (The "How"):**
      This tweak modifies a string value in the Windows Registry.
      - **Path:** `HKCU:\Control Panel\Desktop`
      - **Value:** `MenuShowDelay`
      - **Tweak ON (Instant):** Sets the value to `"0"`.
      - **Tweak OFF (Default):** Sets the value to `"400"`.

    - **Pros:**
      - Makes the entire Windows UI feel significantly more responsive and snappy.

    - **Cons:**
      - The effect is purely cosmetic and does not improve raw performance.

    - **Reversibility & Safety:** 100% reversible. Safety Rating: Very High.
    - **Required Action:** A logoff/logon cycle or a system restart is required.

---
[4.2.3] 100% JPEG Wallpaper Quality
---
    - **What It Does (The "ELI5"):**
      To save a tiny amount of memory, Windows slightly compresses your beautiful desktop wallpaper, which can make it look a little blurry. This tweak tells Windows to display your JPEG wallpapers at their original, maximum quality.

    - **Technical Deep Dive (The "How"):**
      This tweak modifies a DWORD value in the Windows Registry.
      - **Path:** `HKCU:\Control Panel\Desktop`
      - **Value:** `JPEGImportQuality`
      - **Tweak ON (Optimized):** Sets the value to `100`.
      - **Tweak OFF (Default):** Deletes the value, causing Windows to revert to its default behavior (~85% quality).

    - **Pros:**
      - Makes detailed wallpapers look sharper and more vibrant, especially on high-resolution monitors.

    - **Cons:**
      - Uses a negligible amount of extra RAM.

    - **Reversibility & Safety:** 100% reversible. Safety Rating: Very High.
    - **Required Action:** You must re-apply your wallpaper after changing this setting for the effect to be visible. A logoff/logon cycle is also recommended.

---
[4.2.4] Disable Web Search in Start Menu
---
    - **What It Does (The "ELI5"):**
      When you search for something in the Start Menu, Windows also searches the internet using Bing. This can clutter your results and sends your search terms to Microsoft. This tweak turns that off, so the Start Menu only searches for files and apps on your local computer.

    - **Technical Deep Dive (The "How"):**
      This is a comprehensive tweak that modifies two separate registry keys for a complete block.
      - **Path 1 (Disables Suggestions):** `HKCU:\Software\Policies\Microsoft\Windows\Explorer`
      - **Value 1:** `DisableSearchBoxSuggestions` is set to `1` (DWORD).
      - **Path 2 (Disables Web Results):** `HKLM:\SOFTWARE\Policies\Microsoft\Windows\Windows Search`
      - **Value 2:** `ConnectedSearchUseWeb` is set to `0` (DWORD).
      - **Tweak OFF:** Both of the above registry values are deleted.

    - **Pros:**
      - Improves privacy by keeping your searches local.
      - Can make Start Menu search results appear faster.
      - Provides a cleaner, less cluttered search experience.

    - **Cons:**
      - You lose the convenience of performing quick web searches directly from the Start Menu.

    - **Reversibility & Safety:** 100% reversible. Safety Rating: Very High.
    - **Required Action:** A system restart is required for the change to take full effect.

------------------------------------------------------------------------------------------------------------------------
[4.3] Fix Windows: System Integrity Operations
------------------------------------------------------------------------------------------------------------------------

This section contains powerful, military-grade diagnostic and repair tools built directly into Windows. MK-Tools provides a safe, user-friendly interface to execute these commands.

---
[4.3.1] Scan (SFC /scannow)
---
    - **What It Does (The "ELI5"):**
      This is your go-to tool for fixing common Windows problems. It scans all of the important, protected system files and automatically replaces any that are corrupted, damaged, or missing with a fresh copy. It's like a self-repair function for the core of Windows.

    - **Technical Deep Dive (The "How"):**
      This action executes the System File Checker utility.
      - **Command:** `sfc /scannow`
      - The command is run in a hidden window, and its real-time output is streamed to the terminal widget in the UI. The final result is determined by analyzing the command's exit code and its text output.

    - **When to Use It:**
      - If Windows is crashing, freezing, or behaving erratically.
      - If you are seeing strange error messages related to system files.
      - Before and after installing major software or Windows Updates.

    - **Safety & Reversibility:** This is a 100% safe, non-destructive, read-and-repair operation. It cannot be "undone" as it is a repair, not a tweak. Safety Rating: Very High.

---
[4.3.2] Advanced Scan (DISM)
---
    - **What It Does (The "ELI5"):**
      If the normal "Scan" (SFC) finds problems but can't fix them, the "Advanced Scan" is your next step. It repairs the master library of components that SFC uses to make its repairs. It's like fixing the factory that produces the spare parts for your computer.

    - **Technical Deep Dive (The "How"):**
      This action executes the Deployment Image Servicing and Management (DISM) tool.
      - **Scan Command:** `DISM /Online /Cleanup-Image /ScanHealth` (Checks for corruption)
      - **Restore Command:** `DISM /Online /Cleanup-Image /RestoreHealth` (Performs the repair)
      - The tool connects to Windows Update to download clean, original copies of corrupted files. The process is streamed to the terminal, and the final result is determined by the exit code and text output.

    - **When to Use It:**
      - When `sfc /scannow` reports that it found corrupt files but was unable to fix some of them.
      - When Windows Update is failing or behaving incorrectly.
      - As a more thorough, deep-level system integrity check.

    - **Safety & Reversibility:** This is a 100% safe repair operation. It cannot be "undone." Safety Rating: Very High. It can take a significant amount of time (15-30+ minutes) and requires a stable internet connection.

------------------------------------------------------------------------------------------------------------------------
[4.4] Clean Cache: Reclaim Your Disk Space
------------------------------------------------------------------------------------------------------------------------

This section is dedicated to safely removing temporary and cached files that accumulate over time, freeing up valuable disk space and sometimes resolving application issues.

---
[4.4.1] The "Clean All" Protocol
---
    - **What It Does:**
      The "Clean All" button initiates a three-phase automated cleanup sequence:
      1.  **Audit Phase:** It first scans all target directories to calculate the total amount of reclaimable space.
      2.  **Execution Phase:** It then systematically deletes the contents of each target directory.
      3.  **Verification Phase:** It re-scans the directories to confirm how much space was successfully freed.
      This provides a safe, transparent, and satisfying cleanup experience.

---
[4.4.2] Manual Cleanup Operations (In-Depth)
---
    - **User Temp Folder:**
      - **Path:** `%TEMP%`
      - **What it is:** A folder where applications store temporary working files.
      - **Safety:** Very High. It is safe to clear. Some poorly designed apps might lose unsaved state if they store it here instead of a proper location.

    - **System-Wide Temp Folder:**
      - **Path:** `C:\Windows\Temp`
      - **What it is:** A temporary folder used by the Windows operating system and installers.
      - **Safety:** High. Some files may be locked and in use by the system, which MK-Tools will safely skip.

    - **Windows Update Cache:**
      - **Path:** `C:\Windows\SoftwareDistribution\Download`
      - **What it is:** Where Windows stores downloaded update files. After updates are installed, these files are often no longer needed.
      - **Safety:** High. Clearing this can free up gigabytes of space. If an update is pending, it may need to be re-downloaded.

    - **Explorer Thumbnail & Icon Cache:**
      - **Path:** `%LOCALAPPDATA%\Microsoft\Windows\Explorer`
      - **What it is:** A database of all the thumbnail images and icons for your files. This can become corrupted, leading to incorrect or blank icons.
      - **Safety:** High. This action will clear the cache and restart the Windows Explorer shell. Your icons and thumbnails will be regenerated automatically as you browse your files.

    - **WinSxS Component Store Cleanup:**
      - **Command:** `Dism.exe /Online /Cleanup-Image /StartComponentCleanup`
      - **What it is:** Cleans up old, superseded versions of Windows components.
      - **Safety:** Very High. This is a standard Windows maintenance task. It can be slow but is highly effective at freeing up space.

    - **Windows Prefetch:**
      - **Path:** `C:\Windows\Prefetch`
      - **What it is:** Contains files that help your most-used applications launch faster. Over time, it can accumulate data for apps you no longer use.
      - **Safety:** Moderate. Clearing this is safe, but your frequently used applications may launch slightly slower *one time* as their prefetch data is recreated.

------------------------------------------------------------------------------------------------------------------------
[4.5] Group Policy: Military-Grade System Hardening
------------------------------------------------------------------------------------------------------------------------

**NOTE: This feature is only available on Windows 10/11 Pro, Enterprise, and Education editions.**

This section uses Microsoft's Local Group Policy Object (LGPO) utility to apply a curated set of policies designed to enhance privacy, security, and performance.

---
[4.5.1] Apply Optimized Policies
---
    - **What It Does:**
      This action imports a master backup of GPO settings that have been hand-picked to provide a superior standalone workstation experience.

    - **Key Changes Include:**
      - **Enhanced Privacy:** Disables most forms of telemetry, data collection, Cortana, and cloud-integrated search features.
      - **Enhanced Security:** Disables potentially insecure features like Windows Recall's screen capture.
      - **Cleaner UI:** Disables consumer features, suggested apps, and ads in the Start Menu and on the lock screen.
      - **Performance:** Disables non-essential background services like the News and Interests feed.

    - **Safety & Reversibility:** 100% reversible via the "Reset Policies to Default" button. Safety Rating: High.

---
[4.5.2] Reset Policies to Default
---
    - **What It Does:**
      This action performs a complete and total reset of all Local Group Policies on your system, reverting them to the clean, out-of-the-box Windows default state.

    - **Technical Deep Dive (The "How"):**
      This is a multi-stage operation:
      1.  The Group Policy service is temporarily stopped.
      2.  The directories `C:\Windows\System32\GroupPolicy` and `GroupPolicyUsers` are deleted.
      3.  The default Windows security template (`defltbase.inf`) is re-applied using `secedit.exe`.
      4.  The Group Policy service is restarted, and the changes are forced with `gpupdate /force`.

    - **Safety & Reversibility:** This is the definitive method for reverting to a clean slate. Safety Rating: Very High.

========================================================================================================================
|| [5.0] TROUBLESHOOTING & SUPPORT
========================================================================================================================

------------------------------------------------------------------------------------------------------------------------
[5.1] The Failsafe Protocol: "The App Crashed!"
------------------------------------------------------------------------------------------------------------------------

MK-Tools is built to be anti-fragile. In the rare event of a catastrophic, unhandled error, the application will not simply disappear. Instead, it will activate its failsafe protocol:

1.  It will write a detailed error report, including a full technical "stack trace," to a log file.
2.  It will display a final message box informing you of the crash.
3.  **Crucially, this message box will show you the exact path to the log file that was just created.**

If you experience a crash, please navigate to that file path, find the most recent `.log` file, and send it to the developer. This file is the single most important piece of information for diagnosing and fixing the problem.

The log files are located in the `logs` folder within your MK-Tools installation directory.

------------------------------------------------------------------------------------------------------------------------
[5.2] "A Tweak Didn't Work or is Grayed Out"
------------------------------------------------------------------------------------------------------------------------

-   **Check for Admin Rights:** The most common cause is that the application is not running with administrator privileges. Please ensure you accepted the UAC prompt upon launch.
-   **Check your Windows Edition:** The "Group Policy" section will not function on Windows Home editions.
-   **Check for Conflicting Software:** Some antivirus or security software may interfere with system-level changes.

------------------------------------------------------------------------------------------------------------------------
[5.3] Contact & Support Channels
------------------------------------------------------------------------------------------------------------------------

For bug reports, feature requests, or general support, please use the following channels:

-   **GitHub Issues (Preferred):** https://github.com/Mr-Muhammad-Kashan/MK-Tools/issues
-   **Email:** MKATW@outlook.com
-   **LinkedIn:** https://www.linkedin.com/in/muhammad-kashan-tariq/

========================================================================================================================
|| [6.0] FREQUENTLY ASKED QUESTIONS (FAQ)
========================================================================================================================

**Q: Is MK-Tools safe to use?**
A: **Yes.** Every tweak included is a standard Windows configuration and is 100% reversible. The application is designed with safety as its highest priority. It does not modify critical system files in an unsupported way.

**Q: Will this work on my Windows 11 Home laptop?**
A: **Yes, mostly.** All features in the Performance, UI Tweaks, Fix Windows, and Clean Cache sections will work perfectly. The only section that will not function is "Group Policy," as the Group Policy Editor is not available on Windows Home editions.

**Q: Do I need to be a computer expert to use this?**
A: **Absolutely not.** MK-Tools was designed from the ground up for users of all skill levels. The interface is simple, and the "What is it?" panels provide clear, non-technical explanations for every feature.

**Q: How do I undo a change I made?**
A: Every tweak card has a "Reset Defaults" button. Clicking this will revert that specific setting to the standard Windows configuration.

**Q: Will you be adding more features in the future?**
A: **Yes.** The "Coming Soon" card on the dashboard is a promise. MK-Tools is an actively developed project, and new, safe, and effective tweaks will be added in future updates.

========================================================================================================================
|| [7.0] LICENSE & CREDITS
========================================================================================================================

MK-Tools is distributed under the license specified in the `License.txt` file included with this installation.

This application was built with Python and leverages the following incredible open-source libraries:
-   **CustomTkinter:** For the beautiful, modern user interface.
-   **Pygame:** For the Auditory Feedback Engine.
-   **Pillow (PIL Fork):** For advanced image processing.
-   **psutil:** For hardware detection.
-   **fuzzywuzzy:** For intelligent text matching.
-   **cairosvg:** For high-quality SVG icon rendering.
-   **pywin32:** For essential Windows API interactions.

========================================================================================================================
|| [8.0] FINAL WORDS
========================================================================================================================

Thank you for putting your trust in MK-Tools. This project was born from a decade of passion for technology and a genuine desire to help others get the most out of their computers. My goal was to create a tool that I would personally use after every fresh Windows installation—a tool that is powerful yet safe, complex under the hood yet simple on the surface.

I hope it empowers you to take control of your digital environment and makes your PC a more enjoyable and productive machine.

If you find this tool useful, please consider supporting its future development. You can find a support link in the "About" section of the application.

Happy tweaking!

- Mohammed Kashan Tariq

========================================================================================================================
||                                          MK-TOOLS v1.0 - End of Document                                           ||
========================================================================================================================
