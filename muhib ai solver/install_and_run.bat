@echo off
setlocal enabledelayedexpansion

:: --- CONFIGURATION ---
set "SCRIPT_NAME=muhib_software.py"
set "PYTHON_URL=https://www.google.com/search?q=https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe"

echo ======================================================
echo           Muhib Software - Auto Installer
echo ======================================================

:: Check for Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
echo [!] Python not found. Downloading installer...
curl -L -o python_installer.exe %PYTHON_URL%
echo [!] Starting Python Installer...
echo [!] IMPORTANT: Please check "Add Python to PATH" in the installer!
start /wait python_installer.exe
del python_installer.exe

:: Refresh path without restarting cmd
set "PATH=%PATH%;%USERPROFILE%\AppData\Local\Programs\Python\Python312;%USERPROFILE%\AppData\Local\Programs\Python\Python312\Scripts"

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python installation failed or PATH not updated. 
    echo [X] Please restart your laptop and run this file again.
    pause
    exit /b
)


) else (
echo [+] Python is already installed.
)

:: Install Dependencies
echo [+] Installing required libraries (keyboard, requests, pyperclip)...
python -m pip install --upgrade pip
python -m pip install keyboard requests pyperclip

:: Check if the python script exists in the folder
if not exist "%SCRIPT_NAME%" (
echo [X] ERROR: %SCRIPT_NAME% not found in this folder!
echo [!] Make sure this .bat file is in the same folder as your Python script.
pause
exit /b
)

echo.
echo ======================================================
echo [+] SETUP COMPLETE!
echo [!] Starting Muhib Software...
echo [!] Note: To use global hotkeys, this may require Admin.
echo ======================================================
echo.

:: Run the software
python "%SCRIPT_NAME%"

pause