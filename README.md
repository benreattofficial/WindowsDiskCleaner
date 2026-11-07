# 🗂️ Windows Disk Cleaner & Optimizer

<p align="center">
  <img src="icon.ico" width="128" height="128" alt="Windows Disk Cleaner Logo">
</p>

<p align="center">
  <b>A fast, lightweight, and modern native Windows desktop application designed to clean junk files, recover storage space, and optimize system performance.</b>
</p>

<p align="center">
  <img src="[https://img.shields.io/badge/Platform-Windows%2010%2F11-blue?style=flat-square&logo=windows](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue?style=flat-square&logo=windows)" alt="Platform">
  <img src="[https://img.shields.io/badge/Python-3.15-yellow?style=flat-square&logo=python](https://img.shields.io/badge/Python-3.15-yellow?style=flat-square&logo=python)" alt="Python">
  <img src="[https://img.shields.io/badge/PyQt6-UI-green?style=flat-square&logo=qt](https://img.shields.io/badge/PyQt6-UI-green?style=flat-square&logo=qt)" alt="PyQt6">
  <img src="[https://img.shields.io/badge/License-GPLv3.0-blue.svg?style=flat-square](https://img.shields.io/badge/License-GPLv3.0-blue.svg?style=flat-square)" alt="License: GPLv3">
</p>

---

## ✨ Features

* **🧹 System Cleaner:** Scan and securely clean temporary system files (TEMP), browser caches, system logs, and download junk.
* **📂 Custom Directory Cleaner:** Browse any custom folder on your PC, inspect its contents with checkboxes, and selectively delete unwanted files.
* **📊 Real-time Disk Storage Overview:** Dynamic circular donut gauge displaying used, free, and total disk capacity in real-time using `psutil`.
* **🌍 Multi-Language Support (i18n):** Fully localized interface supporting **5 languages** (English, Türkçe, Deutsch, Español, Français) with instant switching.
* **⚙️ Advanced Settings Panel:** Configurable preferences (Auto-start with Windows, deletion confirmation prompts, background tasks) managed via a dedicated save mechanism.
* **🔒 Safe & Secure:** Real file deletion safeguards with explicit user confirmation prompts to prevent accidental data loss.
* **📦 Native Windows Setup:** Ready-to-use executable (`.exe`) compiled via PyInstaller and packagable into a professional installer wizard using Inno Setup.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **GUI Framework:** PyQt6
* **System Monitoring:** psutil
* **Packaging:** PyInstaller & Inno Setup

---

## 🚀 Getting Started (Source Code)

If you want to run or modify the project directly from the source code:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/benreattofficial/Windows-Disk-Cleaner.git
   cd Windows-Disk-Cleaner
Install dependencies:

Bash
pip install PyQt6 psutil pyinstaller
Run the application:

Python
python main.py
📦 Building the Executable & Installer
1. Build Standalone .exe (PyInstaller)
To compile the project into a single native Windows executable with a custom icon:

Bash
pyinstaller --noconsole --onefile --icon=icon.ico --name="DiskCleaner" main.py
2. Create Setup Installer (Inno Setup)
Install Inno Setup.

Open the provided setup.iss script in Inno Setup Compiler.

Click Build > Compile (or press Ctrl + F9) to generate WindowsDiskCleaner_Setup.exe.

📂 Project Structure
Plaintext
DiskCleanerApp/
│
├── main.py            # Main application entry point and PyQt6 UI logic
├── i18n.py            # 5-language internationalization dictionary
├── setup.iss          # Inno Setup installation script configuration
└── icon.ico           # Application branding icon
👤 Developer
Developer: benreattofficial

📜 License
This project is licensed under the GNU General Public License v3.0 (GPLv3). See the LICENSE file for details.
