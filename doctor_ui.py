import tkinter as tk
from tkinter import messagebox
import json
import os
import platform
import subprocess
from datetime import datetime

# Constants
IS_MAC = platform.system() == "Darwin"
DARK_MODE = False

if IS_MAC:
    try:
        result = subprocess.run(
            ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
            capture_output=True, text=True
        )
        DARK_MODE = 'Dark' in result.stdout
    except Exception:
        DARK_MODE = False

# Colors
DARK_THEME = {
    "BG_COLOR": "#1e1e1e", "TEXT": "#f8fafc", "PRIMARY": "#60a5fa",
    "ACCENT": "#334155", "BUTTON": "#2563eb", "ENTRY_BG": "#1f2937",
    "STATUS_COLORS": {"Pending": "#9ca3af", "Checked": "#22c55e", "Absent": "#ef4444"}
}
LIGHT_THEME = {
    "BG_COLOR": "#ffffff", "TEXT": "#1e293b", "PRIMARY": "#2563eb",
    "ACCENT": "#eff6ff", "BUTTON": "#3b82f6", "ENTRY_BG": "#ffffff",
    "STATUS_COLORS": {"Pending": "#6b7280", "Checked": "#16a34a", "Absent": "#dc2626"}
}
THEME = DARK_THEME if DARK_MODE else LIGHT_THEME

# File
QUEUE_FILE = "queue_data.json"

# Utility Functions
def load_queue():
    """Load patient queue data from file."""
    if os.path.exists(QUEUE_FILE) and os.path.getsize(QUEUE_FILE) > 0:
        with open(QUEUE_FILE, "r") as file:
            data = json.load(file)
            return sorted(data, key=lambda x: datetime.strptime(x['slot'], '%H:%M'))
    return []

def save_queue(data):
    """Save patient queue data to file."""
    with open(QUEUE_FILE, "w") as file:
        json.dump(data, file, indent=4)

def create_button(parent, text, command, bg_color=None):
    """Create a styled button."""
    button = tk.Label(
        parent, text=text, font=("Helvetica", 11, "bold"),
        bg=bg_color or THEME["BUTTON"], fg="white",
        padx=15, pady=8, cursor="hand2"
    )
    button.bind("<Button-1>", command)
    return button

# Display Logic
def update_display():
    """Update the patient list display."""
    patient_frame.destroy()
    query = search_var.get().lower()

    for idx, patient in enumerate(queue):
        if query in patient["name"].lower():
            add_patient_to_frame(patient, idx)

def add_patient_to_frame(patient, idx):
    """Add a single patient to the display frame."""
    frame = tk.Frame(patient_frame, bg=THEME["ACCENT"], pady=5, padx=10)
    frame.pack(fill="x", pady=5)

    tk.Label(
        frame, text=f"{patient['name']} ({patient['age']} yrs, {patient['gender']})",
        bg=THEME["ACCENT"], fg=THEME["TEXT"], font=("Helvetica", 11, "bold")
    ).grid(row=0, column=0, sticky="w")

    tk.Label(
        frame, text=f"Slot: {patient['slot']}", bg=THEME["ACCENT"],
        fg=THEME["TEXT"], font=("Helvetica", 10)
    ).grid(row=1, column=0, sticky="w")

    status = patient["status"]
    tk.Label(
        frame, text=f"Status: {status}",
        bg=THEME["ACCENT"], fg=THEME["STATUS_COLORS"][status],
        font=("Helvetica", 10, "italic")
    ).grid(row=0, column=1, padx=20)

    if status == "Pending":
        create_button(frame, "Mark Checked", lambda e: mark_patient(idx, "Checked")).grid(row=1, column=1, padx=5)
        create_button(frame, "Mark Absent", lambda e: mark_patient(idx, "Absent"), bg_color="#f87171").grid(row=1, column=2, padx=5)

def mark_patient(index, new_status):
    """Update patient status."""
    queue[index]["status"] = new_status
    save_queue(queue)
    update_display()

# GUI Setup
window = tk.Tk()
window.title("PatientFlow - Doctor View")
window.geometry("700x600")
window.configure(bg=THEME["BG_COLOR"])

# Header
tk.Label(window, text="PatientFlow", font=("Helvetica", 20, "bold"), bg=THEME["BG_COLOR"], fg=THEME["PRIMARY"]).pack(pady=10)
tk.Label(window, text="Today's Appointment Queue", font=("Helvetica", 14), bg=THEME["BG_COLOR"], fg=THEME["TEXT"]).pack(pady=5)

# Search Bar
search_var = tk.StringVar()
search_frame = tk.Frame(window, bg=THEME["BG_COLOR"])
search_frame.pack(pady=10)

tk.Entry(
    search_frame, textvariable=search_var, font=("Helvetica", 11),
    bg=THEME["ENTRY_BG"], fg=THEME["TEXT"], width=40, insertbackground=THEME["TEXT"]
).pack(side="left", padx=10)

create_button(search_frame, "Search", lambda e: update_display()).pack(side="left")
create_button(search_frame, "Reset", lambda e: reset_filters()).pack(side="left", padx=10)

# Patient Frame
patient_frame = tk.Frame(window, bg=THEME["BG_COLOR"])
patient_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Initial Load
queue = load_queue()
update_display()

# Footer
tk.Label(window, text="Powered by PatientFlow", font=("Helvetica", 9), bg=THEME["BG_COLOR"], fg="#94A3B8").pack(pady=5)

window.mainloop()
