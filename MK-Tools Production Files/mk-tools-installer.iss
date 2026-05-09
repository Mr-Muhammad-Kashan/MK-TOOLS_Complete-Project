; ===================================================================================
; MK-TOOLS (v1.0) - PARADIGM INSTALLER SCRIPT (v4.0 - Definitive Failsafe)
; Authored by: Singularity
; Description: This is the definitive, military-grade Inno Setup script for the
;              MK-Tools application. It is engineered for a zero-defect, professional
;              user installation experience with maximum compression and stability.
; Change Log:
;   - Re-architected font installation to use a direct file placement protocol,
;     placing TTF files alongside the executable. This bypasses all compiler
;     incompatibilities and aligns with the application's internal path resolution.
;   - Removed the "Run at Startup" task and associated registry entries as directed.
;   - Updated architecture directive to the modern 'x64compatible' standard.
; ===================================================================================

; ===================================================================================
; SECTION [Setup]: GLOBAL INSTALLER DEFINITIONS
; ===================================================================================
[Setup]
; --- Application Identity ---
AppName=MK-Tools
AppVersion=1.0
AppPublisher=Mohammed Kashan Tariq
AppPublisherURL=https://github.com/Mr-Muhammad-Kashan
AppSupportURL=https://github.com/Mr-Muhammad-Kashan/MK-Tools/issues
AppUpdatesURL=https://github.com/Mr-Muhammad-Kashan/MK-Tools

; --- Installation Directory ---
DefaultDirName={autopf64}\MK-Tools
DefaultGroupName=MK-Tools

; --- Privileges & Security ---
PrivilegesRequired=admin

; --- Output Configuration ---
OutputBaseFilename=setup_MK-Tools(v1.0)
Compression=lzma2/ultra64
SolidCompression=yes

; --- User Interface & Aesthetics ---
WizardStyle=modern
SetupIconFile=Icons\Logo.ico
UninstallDisplayIcon={app}\MK-Tools(v1.0).exe

; --- License & Legal ---
LicenseFile=License.txt

; --- Architecture Protocol ---
ArchitecturesInstallIn64BitMode=x64compatible

; ===================================================================================
; SECTION [Languages]: LOCALIZATION
; ===================================================================================
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

; ===================================================================================
; SECTION [Tasks]: USER-SELECTABLE OPTIONS
; ===================================================================================
[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional shortcuts:"; Flags: checkedonce
Name: "startmenuentry"; Description: "Create a Start Menu entry"; GroupDescription: "Additional shortcuts:"; Flags: checkedonce
; NOTE: The "runatstartup" task has been removed as per the directive.

; ===================================================================================
; SECTION [Files]: SOURCE FILE MANIFEST
; ===================================================================================
[Files]
; --- Core Application Files ---
Source: "MK-Tools(v1.0).exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "License.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "Readme.txt"; DestDir: "{app}"; Flags: ignoreversion

; --- [DEFINITIVE FIX] Font files are now copied directly into the application directory.
; --- This is the most robust method and aligns with the app's resource_path() logic.
Source: "NotoColorEmoji-Regular.ttf"; DestDir: "{app}"; Flags: ignoreversion
Source: "Roboto-Bold.ttf"; DestDir: "{app}"; Flags: ignoreversion

; --- Asset Directories ---
Source: "gifs\*"; DestDir: "{app}\gifs"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Group Policy Editor Tools\*"; DestDir: "{app}\Group Policy Editor Tools"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Icons\*"; DestDir: "{app}\Icons"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Sound Effects\*"; DestDir: "{app}\Sound Effects"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Svg\*"; DestDir: "{app}\Svg"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Version\*"; DestDir: "{app}\Version"; Flags: ignoreversion recursesubdirs createallsubdirs
; Note: The 'main.py' file is correctly excluded as it is not listed here.

; ===================================================================================
; SECTION [Icons]: START MENU & DESKTOP SHORTCUTS
; ===================================================================================
[Icons]
Name: "{group}\MK-Tools"; Filename: "{app}\MK-Tools(v1.0).exe"; Tasks: startmenuentry
Name: "{autodesktop}\MK-Tools"; Filename: "{app}\MK-Tools(v1.0).exe"; Tasks: desktopicon
Name: "{group}\Uninstall MK-Tools"; Filename: "{uninstallexe}"

; ===================================================================================
; SECTION [Run]: POST-INSTALLATION ACTIONS
; ===================================================================================
[Run]
Filename: "{app}\MK-Tools(v1.0).exe"; Description: "Launch MK-Tools"; Flags: nowait postinstall shellexec skipifsilent
Filename: "{app}\Readme.txt"; Description: "View the Readme file"; Flags: nowait postinstall shellexec skipifsilent

; ===================================================================================
; SECTION [Code]: CUSTOM INSTALLER LOGIC
; ===================================================================================
[Code]
// --- This function runs after files are copied during installation.
procedure CurStepChanged(CurStep: TSetupStep);
begin
  // --- Check if the current step is the one immediately after file installation.
  if CurStep = ssPostInstall then
  begin
    // --- Create an empty 'logs' directory inside the application's installation folder.
    if not DirExists(ExpandConstant('{app}\logs')) then
    begin
      CreateDir(ExpandConstant('{app}\logs'));
    end;
  end;
end;