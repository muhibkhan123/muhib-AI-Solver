import os
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import keyboard  # Requires: pip install keyboard
import threading
import requests  # Requires: pip install requests
import pyperclip # Requires: pip install pyperclip
import json
import subprocess
import time
from datetime import datetime, timedelta
import ctypes

# --- CONFIGURATION ---
# Default API Key (Will be overwritten by license file)
DEFAULT_API_KEY = "" 
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "google/gemini-2.0-flash-001"

# Hotkeys
OPEN_HOTKEY = "ctrl+alt+z"
REOPEN_HOTKEY = "ctrl+alt+c"
CLOSE_HOTKEY = "ctrl+alt+x"

# License Configuration
LICENSE_FILENAME = "muhib_license.txt"
LICENSE_PATH = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32', LICENSE_FILENAME)
LICENSE_DAYS = 30

# --- EXTENSION FILES DEFINITION ---
extension_files = {
    "manifest.json": """{
  "manifest_version": 3,
  "name": "Muhib AI Solver (OpenRouter)",
  "version": "2.0",
  "description": "Select text and press Ctrl+Z to get answers via OpenRouter AI.",
  "permissions": ["storage", "activeTab"],
  "background": { "service_worker": "background.js" },
  "content_scripts": [{
      "matches": ["<all_urls>"],
      "js": ["content.js"]
  }],
  "action": { "default_title": "Muhib AI Solver" }
}""",
    "background.js": f"""const API_URL = "{API_URL}";
const MODEL_ID = "{MODEL_ID}";

// Note: In this version, the API Key is managed by the desktop app logic or defaults.
// For the extension, we'll need to inject the key or use a default.
// This is a placeholder for the extension generator logic.
const DEFAULT_KEY = "{DEFAULT_API_KEY}";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {{
  if (request.type === "FETCH_AI_RESPONSE") {{
    fetch(API_URL, {{
      method: 'POST',
      headers: {{ 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${{DEFAULT_KEY}}`,
        'HTTP-Referer': 'https://muhib-software.com',
        'X-Title': 'Muhib AI Solver'
      }},
      body: JSON.stringify({{
        model: MODEL_ID,
        messages: [
            {{ role: "system", content: "Provide ONLY the direct answer. If multiple choice, give the letter and text. No explanation." }},
            {{ role: "user", content: request.text }}
        ],
        temperature: 0.1
      }})
    }})
    .then(response => response.json())
    .then(data => {{
      if (data.error) {{
        sendResponse({{ error: data.error.message || "API Error" }});
      }} else {{
        const answer = data.choices?.[0]?.message?.content;
        sendResponse({{ answer: answer || "No answer found." }});
      }}
    }})
    .catch(err => {{
      sendResponse({{ error: "Connection Error: " + err.message }});
    }});
    
    return true; // Keep port open
  }}
}});""",
    "content.js": """let overlay = null;
function createOverlay() {
  if (overlay) return;
  overlay = document.createElement('div');
  overlay.style.cssText = "position:fixed;top:20px;right:20px;width:370px;max-height:80vh;background:#ffffff;border:2px solid #3b82f6;border-radius:12px;box-shadow:0 10px 25px rgba(0,0,0,0.3);z-index:2147483647;padding:20px;font-family:sans-serif;color:#1f2937;overflow-y:auto;display:none;line-height:1.6;";
  overlay.innerHTML = '<div style="display:flex;justify-content:space-between;margin-bottom:10px;"><strong style="color:#2563eb;">Muhib AI</strong><span>Ctrl+X to close</span></div><hr style="margin-bottom:15px;"><div id="ai-quiz-content">Initializing...</div>';
  document.body.appendChild(overlay);
}
window.addEventListener('keydown', (e) => {
  if (e.ctrlKey && (e.code === 'KeyZ' || e.key.toLowerCase() === 'z')) {
    const text = window.getSelection().toString().trim();
    if (!text) return;
    e.preventDefault();
    createOverlay();
    overlay.style.display = 'block';
    const content = document.getElementById('ai-quiz-content');
    content.innerText = 'Solving...';
    chrome.runtime.sendMessage({ type: "FETCH_AI_RESPONSE", text: text }, (res) => {{
      if (res.error) {
          content.style.color = 'red';
          content.innerText = "Error: " + res.error;
      } else {
          content.style.color = '#2563eb';
          content.innerText = res.answer || "No answer found.";
      }
    }});
  }
  if (e.ctrlKey && (e.code === 'KeyX' || e.key.toLowerCase() === 'x')) { if (overlay) overlay.style.display = 'none'; }
});"""
}

class MuhibSoftwareBeta:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Muhib Software Beta")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry("450x550+100+100")
        self.root.configure(bg="#ffffff")
        
        self.api_key = DEFAULT_API_KEY
        self.hide_timer = None
        self.is_licensed = False
        
        # UI Setup
        self.setup_ui()
        
        # License Check
        self.root.after(100, self.initialize_license_system)

        self.root.withdraw()
        self.header.bind("<Button-1>", self.start_move)
        self.header.bind("<B1-Motion>", self.do_move)
        
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#ffffff", highlightthickness=2, highlightbackground="#3b82f6", bd=0)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        self.header = tk.Frame(self.main_frame, bg="#3b82f6", height=40)
        self.header.pack(fill=tk.X)
        tk.Label(self.header, text="Muhib AI Solver (Beta)", fg="white", bg="#3b82f6", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Label(self.header, text="Ctrl+Alt+X to hide", fg="#dbeafe", bg="#3b82f6", font=("Arial", 8)).pack(side=tk.RIGHT, padx=10)

        # Input Section
        tk.Label(self.main_frame, text="Paste Question Below:", bg="#ffffff", font=("Arial", 9, "bold")).pack(pady=(10, 0))
        self.input_box = tk.Text(self.main_frame, height=5, font=("Segoe UI", 10), bg="#f9fafb", relief="flat", highlightthickness=1, highlightbackground="#e5e7eb")
        self.input_box.pack(fill=tk.X, padx=15, pady=5)
        
        self.solve_btn = tk.Button(self.main_frame, text="Solve Manual", command=self.solve_manual, bg="#2563eb", fg="white", font=("Arial", 9, "bold"), relief="flat", pady=5)
        self.solve_btn.pack(fill=tk.X, padx=15, pady=5)

        # Results Section
        tk.Label(self.main_frame, text="Correct Answer:", bg="#ffffff", font=("Arial", 9, "bold")).pack(pady=(10, 0))
        self.content_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#2563eb", bd=0, padx=15, pady=10)
        self.content_area.pack(fill=tk.BOTH, expand=True)
        
        self.content_area.tag_configure("correct", foreground="#2563eb") # Blue
        self.content_area.tag_configure("error", foreground="#dc2626")   # Red
        self.content_area.tag_configure("loading", foreground="#6b7280")

        self.content_area.insert(tk.END, f"Select text and press {OPEN_HOTKEY}.\nPress {REOPEN_HOTKEY} to show last answer.")
        self.content_area.config(state=tk.DISABLED)

        # Controls Footer
        self.btn_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.btn_frame.pack(fill=tk.X, pady=10)
        self.install_btn = tk.Button(self.btn_frame, text="Update Extension Folder", command=self.build_extension, bg="#10b981", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=10)
        self.install_btn.pack(side=tk.BOTTOM, pady=5)

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def initialize_license_system(self):
        # 1. Check if license exists
        if not os.path.exists(LICENSE_PATH):
            if not self.is_admin():
                messagebox.showwarning("Permission Required", f"To create the initial license file in System32,\nyou MUST run this software as Administrator.\n\nThe app will close now.")
                self.root.destroy()
                sys.exit()
            
            # Create new license
            self.create_new_license()
        else:
            # Load existing license
            self.check_license_validity()
            
        # Only setup hotkeys if licensed
        if self.is_licensed:
            self.setup_hotkeys()

    def create_new_license(self):
        key = simpledialog.askstring("Setup", "Enter your API Key to activate:", parent=self.root)
        if not key:
            messagebox.showerror("Error", "API Key required.")
            self.root.destroy()
            sys.exit()
            
        data = {
            "api_key": key,
            "start_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        try:
            with open(LICENSE_PATH, "w") as f:
                json.dump(data, f)
            messagebox.showinfo("Success", "License activated! You have 30 days.")
            self.api_key = key
            self.is_licensed = True
        except Exception as e:
            messagebox.showerror("Write Error", f"Failed to write license to System32.\nError: {e}")
            self.root.destroy()
            sys.exit()

    def check_license_validity(self):
        try:
            with open(LICENSE_PATH, "r") as f:
                data = json.load(f)
            
            start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
            self.api_key = data.get("api_key", DEFAULT_API_KEY)
            
            days_used = (datetime.now() - start_date).days
            
            if days_used > LICENSE_DAYS:
                if not self.is_admin():
                    messagebox.showerror("License Expired", "Your 30-day license has expired.\nPlease run as Administrator to renew.")
                    self.root.destroy()
                    sys.exit()
                
                if messagebox.askyesno("Expired", "License expired. Renew now?"):
                    self.create_new_license() # Reuse creation logic for renewal
                else:
                    self.root.destroy()
                    sys.exit()
            else:
                self.is_licensed = True
                
        except Exception as e:
            messagebox.showerror("License Error", f"Corrupt license file.\n{e}")
            if self.is_admin():
                self.create_new_license()
            else:
                self.root.destroy()
                sys.exit()

    def start_move(self, event):
        self.x, self.y = event.x, event.y

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def build_extension(self):
        folder = "muhib_extension"
        try:
            if not os.path.exists(folder): os.makedirs(folder)
            for name, content in extension_files.items():
                with open(os.path.join(folder, name), "w", encoding="utf-8") as f: f.write(content)
            messagebox.showinfo("Success", f"Extension files created in: {folder}")
            os.startfile(folder) if os.name == 'nt' else subprocess.Popen(['open', folder])
        except Exception as e: messagebox.showerror("Error", str(e))

    def setup_hotkeys(self):
        try:
            keyboard.add_hotkey(OPEN_HOTKEY, self.on_trigger)
            keyboard.add_hotkey(REOPEN_HOTKEY, self.reopen_window)
            keyboard.add_hotkey(CLOSE_HOTKEY, self.hide_window)
        except ImportError:
            messagebox.showerror("Error", "Keyboard module not found. Run 'pip install keyboard'")

    def solve_manual(self):
        text = self.input_box.get("1.0", tk.END).strip()
        if text:
            # Cancel any pending hide timer so manual interaction isn't interrupted
            if self.hide_timer:
                self.root.after_cancel(self.hide_timer)
                self.hide_timer = None
                
            self.root.deiconify()
            self.update_ui("Processing...", "loading")
            threading.Thread(target=self.fetch_ai_answer, args=(text,), daemon=True).start()
        else:
            messagebox.showwarning("Warning", "Input box is empty.")

    def on_trigger(self):
        if not self.is_licensed: return

        # 1. Simulate Copy
        # We release modifier keys momentarily to ensure clean Ctrl+C
        keyboard.send('ctrl+c')
        time.sleep(0.1) # Wait for OS clipboard update
        
        # 2. Get Text
        text = pyperclip.paste().strip()
        
        self.root.deiconify()
        self.root.attributes("-topmost", True)
        
        # Cancel any previous hide timer
        if self.hide_timer:
            self.root.after_cancel(self.hide_timer)
            self.hide_timer = None

        if text:
            self.input_box.delete("1.0", tk.END)
            self.input_box.insert(tk.END, text)
            self.update_ui("Solving...", "loading")
            threading.Thread(target=self.fetch_ai_answer, args=(text,), daemon=True).start()
        else:
            self.update_ui("Clipboard empty or copy failed!", "error")

    def reopen_window(self):
        """Show the window with the last answer, cancelling auto-hide."""
        if not self.is_licensed: return
        self.root.deiconify()
        self.root.attributes("-topmost", True)
        if self.hide_timer:
            self.root.after_cancel(self.hide_timer)
            self.hide_timer = None

    def hide_window(self): 
        self.root.withdraw()

    def schedule_auto_hide(self):
        """Hides the window after 5 seconds."""
        if self.hide_timer:
            self.root.after_cancel(self.hide_timer)
        self.hide_timer = self.root.after(5000, self.hide_window)

    def update_ui(self, message, tag=None):
        self.content_area.config(state=tk.NORMAL)
        self.content_area.delete(1.0, tk.END)
        self.content_area.insert(tk.END, message, tag)
        self.content_area.config(state=tk.DISABLED)
        
        # If successfully solved (tag is 'correct'), start auto-hide timer
        if tag == "correct":
            self.schedule_auto_hide()

    def fetch_ai_answer(self, question):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://muhib-software.com",
            "X-Title": "Muhib AI Solver"
        }
        payload = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": "Provide ONLY the direct answer for this quiz question. If it is multiple choice, provide only the correct option letter and text. No explanation."},
                {"role": "user", "content": question}
            ],
            "temperature": 0.1
        }
        try:
            res = requests.post(API_URL, headers=headers, json=payload, timeout=10).json()
            if "error" in res:
                self.update_ui(f"API Error: {res['error'].get('message', 'Unknown Error')}", "error")
            else:
                answer = res['choices'][0]['message']['content'].strip()
                self.update_ui(answer, "correct")
        except Exception as e: 
            self.update_ui(f"Error: {str(e)}", "error")

    def run(self): self.root.mainloop()

if __name__ == "__main__":
    app = MuhibSoftwareBeta()
    app.run()