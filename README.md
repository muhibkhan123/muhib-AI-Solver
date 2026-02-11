# 🤖 Muhib AI Solver (Beta)

**Muhib AI Solver** is a powerful, dual-mode productivity tool designed to provide instant AI-generated answers for quizzes, tests, and general queries. Powered by the **Gemini 2.0 Flash** model via OpenRouter, it operates as both a stealthy Desktop Application and a Chrome Browser Extension.

---

## 🚀 Features

### 🖥️ Desktop Application
* **Global Hotkeys:** Control the app from anywhere without switching windows.
    * `Ctrl + Alt + Z`: **Copy & Solve**. Automatically copies selected text and fetches the answer.
    * `Ctrl + Alt + C`: **Reopen**. Shows the last answer window if hidden.
    * `Ctrl + Alt + X`: **Hide**. Instantly minimizes the application to the tray/background.
* **Stealth Mode:** The window uses a custom, borderless design (`overrideredirect`) and stays on top of other windows.
* **Auto-Hide:** The interface automatically vanishes 5 seconds after providing a correct answer to keep your screen clutter-free.
* **System32 Licensing:** Implements a secure, local 30-day license verification system stored in the Windows System directory.

### 🧩 Browser Extension Generator
* **Built-in Generator:** The desktop app can generate a fully functional Chrome Extension with a single click.
* **Web Integration:** Adds an overlay to your browser. Select text and press `Ctrl + Z` (default extension hotkey) to get answers directly on the webpage.

---

## 🛠️ Installation

### Method 1: Automatic Installer (Recommended)
1.  Download the repository.
2.  Run the `install_and_run.bat` file.
    > **Note:** The installer is configured to look for `muhib_soft.pyw`. Ensure your file is named correctly.
3.  The installer will:
    * Automatically check for Python.
    * Install required dependencies (`keyboard`, `requests`, `pyperclip`).
    * Launch the application.

### Method 2: Manual Setup
1.  Ensure you have **Python 3.10+** installed.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python muhib_soft.pyw
    ```

---

## ⚙️ Configuration & Activation (First Run)

> [!IMPORTANT]  
> This application requires **Administrator Privileges** on the first run to generate the license file.

1.  **Launch the App:** Double-click on `Muhib AI Solver.exe` (or run the script).
2.  **Enter API Key:** A new window will appear asking for your **OpenRouter API Key**.
3.  **Activate:** Paste your key into the input field and click the **Activate** button.
4.  **Confirmation:** A success window will appear confirming that your software is now active for 30 days.
5.  **Renewal:** After the 30-day period expires, you will be prompted to re-enter your API key to reactivate the software.
6.	**Need help?** Contact us for support if you encounter activation issues.

---

## 🌐 Setting up the Chrome Extension

The desktop app includes a feature to "build" the extension for you.

1.  Open the Desktop App and click **"Update Extension Folder"**.
2.  A folder named `muhib_extension` will be created in the app's directory.
3.  **CRITICAL STEP:**
    * Open the `muhib_extension` folder.
    * Open `background.js` with a text editor (Notepad, VS Code).
    * Find the line: `const DEFAULT_KEY = "";`
    * Paste your OpenRouter API Key inside the quotes: `const DEFAULT_KEY = "sk-or-v1-xxxxxxxx";`
    * Save the file.
4.  Open **Google Chrome** and go to `chrome://extensions/`.
5.  Enable **Developer Mode** (toggle in the top right).
6.  Click **Load unpacked** and select the `muhib_extension` folder.

---

## 📦 Pre-built EXE & Building from Source

### Use the Provided EXE
A pre-compiled `Muhib AI Solver.exe` is already provided. Simply run this file as **Administrator** to use the application immediately—no Python installation required.

### Building from Source (Optional)
If you prefer to compile the Python script yourself:
1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2.  Run the build command using the provided spec file:
    ```bash
    pyinstaller "Muhib AI Solver.spec"
    ```
3.  The output executable will be located in the `dist` folder.

---

## ⚠️ Disclaimer & Troubleshooting

* **Antivirus Flags:** Because this software writes a license file to the `System32` folder, some Antivirus software may flag this as suspicious behavior. You may need to add an exclusion or run as Administrator.
* **Educational Use Only:** The developers are not responsible for any misuse of this tool in academic evaluations or competitive environments.
* **Support:** If you encounter issues (e.g., "Permission Denied"), ensure you are running the application as **Administrator**, as the hotkey listener and System32 file operations require elevated privileges.