[Setup]
AppName=Windows Disk Cleaner
AppVersion=1.0.0
AppPublisher=benreattofficial
DefaultDirName={autopf}\WindowsDiskCleaner
DefaultGroupName=Windows Disk Cleaner
OutputDir=.
OutputBaseFilename=WindowsDiskCleaner_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
; PyInstaller ile tek dosya çıktı aldığında dist klasöründeki .exe buraya eklenir
Source: "dist\DiskCleaner.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Windows Disk Cleaner"; Filename: "{app}\DiskCleaner.exe"
Name: "{autodesktop}\Windows Disk Cleaner"; Filename: "{app}\DiskCleaner.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\DiskCleaner.exe"; Description: "Launch Windows Disk Cleaner"; Flags: nowait postinstall skipifsilent