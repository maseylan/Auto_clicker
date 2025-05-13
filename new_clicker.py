"""
Auto Clicker GUI Tool
Author: MasEylan
Copyright © 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import pyautogui
import time
import keyboard
import webbrowser

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker - by MasEylan")
        self.root.geometry("400x430")
        self.root.configure(bg="#f0f8ff")
        self.root.resizable(False, False)

        self.clicking = False
        self.current_hotkey = "f6"

        self.build_gui()
        self.register_hotkey(self.current_hotkey)
        self.hotkey_label.config(text=f"Hotkey: {self.current_hotkey.upper()}")
        threading.Thread(target=self.hotkey_listener, daemon=True).start()

    def build_gui(self):
        # Header
        title = tk.Label(
            self.root, text="🎯 Auto Clicker",
            font=("Helvetica", 18, "bold"), fg="#3f51b5", bg="#f0f8ff"
        )
        title.pack(pady=10)

        # Input Frame
        frame = tk.Frame(self.root, bg="#f0f8ff")
        frame.pack(pady=5)

        # Click Interval
        tk.Label(frame, text="Click Interval (seconds):", font=("Segoe UI", 10),
                 fg="#222", bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=8, sticky="e")
        self.interval = ttk.Entry(frame, font=("Segoe UI", 10), width=12)
        self.interval.insert(0, "0.1")
        self.interval.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        # Mouse Button
        tk.Label(frame, text="Mouse Button:", font=("Segoe UI", 10),
                 fg="#222", bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=8, sticky="e")
        self.mouse_button = ttk.Combobox(frame, values=["left", "right"], font=("Segoe UI", 10), state="readonly", width=10)
        self.mouse_button.set("left")
        self.mouse_button.grid(row=1, column=1, padx=5, pady=8, sticky="w")

        # Start/Stop Button
        self.toggle_button = ttk.Button(self.root, text="▶ Start Clicking", command=self.toggle_clicking)
        self.toggle_button.pack(pady=12)

        # Status Label
        self.status_label = tk.Label(
            self.root, text="Status: Stopped",
            font=("Segoe UI", 10, "bold"), fg="red", bg="#f0f8ff"
        )
        self.status_label.pack()

        # Hotkey Display
        self.hotkey_label = tk.Label(
            self.root, text=f"Hotkey: {self.current_hotkey.upper()}",
            font=("Segoe UI", 10, "italic"), fg="#ff9800", bg="#f0f8ff"
        )
        self.hotkey_label.pack(pady=5)

        # Set Hotkey Button
        set_hotkey_button = ttk.Button(
            self.root, text="🛠️ Set Hotkey (Press Key)",
            command=lambda: threading.Thread(target=self.listen_for_hotkey, daemon=True).start()
        )
        set_hotkey_button.pack(pady=5)

        # Exit Button
        ttk.Button(self.root, text="❌ Exit", command=lambda: (self.stop_clicking(), self.root.quit())).pack(pady=10)

        # Footer
        copyright_frame = tk.Frame(self.root, bg="#f0f8ff")
        copyright_frame.pack(side="bottom", pady=5)

        tk.Label(
            copyright_frame,
            text="© 2025 MasEylan",
            font=("Segoe UI", 9),
            fg="#333", bg="#f0f8ff"
        ).pack()

        self.link = tk.Label(
            copyright_frame,
            text="Visit Website",
            font=("Segoe UI", 9, "underline"),
            fg="#1a73e8", bg="#f0f8ff",
            cursor="hand2"
        )
        self.link.pack()
        self.link.bind("<Button-1>", lambda e: self.open_link())

    def open_link(self):
        webbrowser.open_new("https://github.com/MasEylan")

    def click_loop(self):
        while self.clicking:
            x, y = pyautogui.position()
            pyautogui.click(x=x, y=y, button=self.mouse_button.get())
            time.sleep(float(self.interval.get()))

    def start_clicking(self):
        if not self.clicking:
            self.clicking = True
            self.status_label.config(text="Status: Running", fg="green")
            threading.Thread(target=self.click_loop, daemon=True).start()

    def stop_clicking(self):
        self.clicking = False
        self.status_label.config(text="Status: Stopped", fg="red")

    def toggle_clicking(self):
        if self.clicking:
            self.stop_clicking()
            self.toggle_button.config(text="▶ Start Clicking")
        else:
            self.start_clicking()
            self.toggle_button.config(text="⏸ Stop Clicking")

    def register_hotkey(self, hotkey):
        try:
            keyboard.remove_hotkey(self.current_hotkey)
        except:
            pass
        self.current_hotkey = hotkey
        keyboard.add_hotkey(hotkey, self.toggle_clicking)
        self.hotkey_label.config(text=f"Hotkey: {self.current_hotkey.upper()}")

    def listen_for_hotkey(self):
        messagebox.showinfo("Set Hotkey", "Tekan tombol atau kombinasi tombol untuk dijadikan hotkey...")
        recorded = keyboard.read_hotkey(suppress=True)
        self.register_hotkey(recorded)


    def hotkey_listener(self):
        keyboard.wait()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
