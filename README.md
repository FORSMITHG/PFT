# Expedite Tracker

Expedite Tracker is a Python-based tracking application that helps manage customer data, expedite tracking, and other logistics-related tasks. This repository contains all necessary files, including scripts, assets, and database files, to ensure seamless execution.

## Features
- Customer management
- Expedite tracking
- Preloaded database (`pft.db`)
- Easy-to-use graphical interface

## Installation (For Beginners)

### 1. Install Git
If you see an error like:
```
'git' is not recognized as an internal or external command,
operable program or batch file.
```
Git is not installed on your computer. To install Git:
- Go to [Git for Windows](https://git-scm.com/download/win) and download the installer.
- Run the installer and follow the default installation steps.
- Restart your computer after installation.

### 2. Install Python
- Download Python from [python.org](https://www.python.org/downloads/).
- Run the installer and ensure you **check the box** that says `Add Python to PATH` before installing.
- Restart your computer after installation.
- Verify the installation by opening **Command Prompt** and running:
  ```sh
  python --version
  ```
  If it displays a version number, Python is installed correctly.

### 3. Clone the Repository
Once Git is installed, open **Command Prompt** or **PowerShell** and run:
```sh
git clone https://github.com/FORSMITHG/PFT.git
cd PFT
```

### 4. Install Dependencies
Ensure Python is installed, then run:
```sh
pip install -r requirements.txt
```
If you see an error about `pip` not being recognized, try:
```sh
python -m pip install -r requirements.txt
```

### 5. Run the Application
```sh
python PFT.py
```

## File Structure
```
PFT/
│── PFT.py                   # Main application script
│── customer_mgmt.py          # Customer management module
│── eet.py                    # Expedite tracking module
│── utils.py                  # Utility functions
│── vt.py                     # Additional features module
│── pft.db                    # Preloaded SQLite database
│── assets/
│   ├── images/
│   │   ├── favicon.ico
│   │   ├── logo.png
│   │   ├── favicon/
│   │   │   ├── android-chrome-192x192.png
│   │   │   ├── android-chrome-512x512.png
│   │   │   ├── apple-touch-icon.png
│   │   │   ├── favicon-16x16.png
│   │   │   ├── favicon-32x32.png
│   │   │   ├── favicon.ico
│   │   │   ├── site.webmanifest
│── database/
│   ├── pft.db                # Database backup
│── requirements.txt          # Dependencies
│── README.md                 # Project documentation
```

## requirements.txt
```
tkcalendar
```

## Notes
- Ensure `pft.db` is in the correct directory before running the script.
- If you encounter issues, check for missing dependencies or permissions.

## License
This project is open-source under the MIT License.