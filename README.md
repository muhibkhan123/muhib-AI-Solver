🤖 Muhib AI Solver (Beta)

Muhib AI Solver is a powerful, dual-mode productivity tool designed to provide instant AI-generated answers for quizzes, tests, and general queries. Powered by the Gemini 2.0 Flash model via OpenRouter, it operates as both a stealthy Desktop Application and a Chrome Browser Extension.

🚀 Features

🖥️ Desktop Application

Global Hotkeys: Control the app from anywhere without switching windows.

Ctrl + Alt + Z: Copy & Solve. Automatically copies selected text and fetches the answer.

Ctrl + Alt + C: Reopen. Shows the last answer window if hidden.

Ctrl + Alt + X: Hide. Instantly minimizes the application to the tray/background.

Stealth Mode: The window uses a custom, borderless design (overrideredirect) and stays on top of other windows.

Auto-Hide: The interface automatically vanishes 5 seconds after providing a correct answer to keep your screen clutter-free.

System32 Licensing: Implements a secure, local 30-day license verification system stored in the Windows System directory.

🧩 Browser Extension Generator

Built-in Generator: The desktop app can generate a fully functional Chrome Extension with a single click.

Web Integration: Adds an overlay to your browser. Select text and press Ctrl + Z (default extension hotkey) to get answers directly on the webpage.

🛠️ Installation

Method 1: Automatic Installer (Recommended)

Download the repository.

Important: Ensure your main Python script is named correctly. The installer looks for muhib_software.py. If your file is named muhib_soft.pyw, please rename it to muhib_software.py or edit the .bat file to match.

Run the install_and_run.bat file.

It will automatically check for Python.

It installs required dependencies (keyboard, requests, pyperclip).

It launches the application.

Method 2: Manual Setup

Ensure you have Python 3.10+ installed.

Install dependencies:

pip install -r requirements.txt


Run the application:

python muhib_soft.pyw


⚙️ Configuration & Activation (First Run)

Note: This application requires Administrator Privileges on the first run to generate the license file.

Launch the App: Double-click on Muhib AI Solver.exe.

Enter API Key: A new window will appear asking for your OpenRouter API Key.

Paste your key into the input field.

Click the Activate button.

Confirmation: A success window will appear confirming that your software is now active for 30 days.

Renewal: After the 30-day period expires, you will be prompted to re-enter your API key to reactivate the software.

Need Help? If you do not understand how to activate the software or encounter issues, please contact us for support.

🌐 Setting up the Chrome Extension

The desktop app includes a feature to "build" the extension for you.

Open the Desktop App and click "Update Extension Folder".

A folder named muhib_extension will be created in the app's directory.

CRITICAL STEP:

Open the muhib_extension folder.

Open background.js with a text editor (Notepad, VS Code).

Find the line const DEFAULT_KEY = "";.

Paste your OpenRouter API Key inside the quotes: const DEFAULT_KEY = "sk-or-v1-xxxxxxxx";.

Save the file.

Open Google Chrome and go to chrome://extensions/.

Enable Developer Mode (toggle in the top right).

Click Load unpacked and select the muhib_extension folder.

📦 Pre-built EXE & Building from Source

Use the Provided EXE:
A pre-compiled Muhib AI Solver.exe is already provided. Simply run this file as Administrator to use the application immediately—no Python installation required.

Building from Source (Optional):
If you prefer to compile the Python script yourself:

Install PyInstaller:

pip install pyinstaller


Run the build command using the provided spec file:

pyinstaller "Muhib AI Solver.spec"


The output executable will be located in the dist folder.

⚠️ Disclaimer & Troubleshooting

Antivirus Flags: Because this software writes a license file to the System32 folder (to ensure the license persists securely), some Antivirus software may flag this as suspicious behavior. You may need to add an exclusion for the application or run it as Administrator to allow this operation.

Educational Use Only: The developers are not responsible for any misuse of this tool in academic evaluations or competitive environments.

📞 Support

If you encounter issues (e.g., "Permission Denied"), ensure you are running the application as Administrator, as the hotkey listener and System32 file operations require elevated privileges.