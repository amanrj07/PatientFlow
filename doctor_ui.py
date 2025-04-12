import tkinter as tk
from tkinter import messagebox
import json
import os
import platform
import subprocess
from datetime import datetime

# ===================== Theme and Mode Detection =====================
IS_MAC = platform.system() == "Darwin"
DARK_MODE = False

if IS_MAC:
    try:
        result = subprocess.run(
            ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
            capture_output=True, text=True
        )
        if 'Dark' in result.stdout:
            DARK_MODE = True
    except Exception:
        DARK_MODE = False

# Color palette
if DARK_MODE:
    BG_COLOR = "#1e1e1e"
    TEXT = "#f8fafc"
    PRIMARY = "#60a5fa"
    ACCENT = "#334155"
    BUTTON = "#2563eb"
    ENTRY_BG = "#1f2937"
    STATUS_COLORS = {"Pending": "#9ca3af", "Checked": "#22c55e", "Absent": "#ef4444"}
else:
    BG_COLOR = "#ffffff"
    TEXT = "#1e293b"
    PRIMARY = "#2563eb"
    ACCENT = "#eff6ff"
    BUTTON = "#3b82f6"
    ENTRY_BG = "#ffffff"
    STATUS_COLORS = {"Pending": "#6b7280", "Checked": "#16a34a", "Absent": "#dc2626"}

QUEUE_FILE = "queue_data.json"

# ===================== Data Functions =====================
def load_queue():
    if os.path.exists(QUEUE_FILE) and os.path.getsize(QUEUE_FILE) > 0:
        with open(QUEUE_FILE, "r") as file:
            data = json.load(file)
            # Sort the queue by time slot
            data.sort(key=lambda x: datetime.strptime(x['slot'], '%H:%M'))
            return data
    return []

def save_queue(data):
    with open(QUEUE_FILE, "w") as file:
        json.dump(data, file, indent=4)

def update_display():
    for widget in patient_frame.winfo_children():
        widget.destroy()

    query = search_var.get().lower()
    for idx, patient in enumerate(queue):
        if query in patient["name"].lower():
            frame = tk.Frame(patient_frame, bg=ACCENT, pady=5, padx=10)
            frame.pack(fill="x", pady=5)

            name_label = tk.Label(frame, text=f"{patient['name']} ({patient['age']} yrs, {patient['gender']})",
                                  bg=ACCENT, fg=TEXT, font=("Helvetica", 11, "bold"))
            name_label.grid(row=0, column=0, sticky="w")

            slot_label = tk.Label(frame, text=f"Slot: {patient['slot']}", bg=ACCENT, fg=TEXT, font=("Helvetica", 10))
            slot_label.grid(row=1, column=0, sticky="w")

            status = patient["status"]
            status_label = tk.Label(frame, text=f"Status: {status}", bg=ACCENT,
                                    fg=STATUS_COLORS[status], font=("Helvetica", 10, "italic"))
            status_label.grid(row=0, column=1, padx=20)

            if status == "Pending":
                # Checked button
                def on_checked(e, i=idx): mark_patient(i, "Checked")
                checked_btn = tk.Label(frame, text="Mark Checked", font=("Helvetica", 10),
                                       bg=BUTTON, fg="white", padx=10, pady=5, cursor="hand2")
                checked_btn.bind("<Button-1>", on_checked)
                checked_btn.grid(row=1, column=1, padx=5)

                # Absent button
                def on_absent(e, i=idx): mark_patient(i, "Absent")
                absent_btn = tk.Label(frame, text="Mark Absent", font=("Helvetica", 10),
                                      bg="#f87171", fg="white", padx=10, pady=5, cursor="hand2")
                absent_btn.bind("<Button-1>", on_absent)
                absent_btn.grid(row=1, column=2, padx=5)

def mark_patient(index, new_status):
    queue[index]["status"] = new_status
    save_queue(queue)
    update_display()

def reset_filters():
    search_var.set("")
    update_display()

def refresh_queue():
    global queue
    queue = load_queue()
    update_display()
    window.after(3000, refresh_queue)  # Refresh every 3 seconds

# ===================== GUI Setup =====================
window = tk.Tk()
window.title("PatientFlow - Doctor View")
window.geometry("700x600")
window.configure(bg=BG_COLOR)

# Header
tk.Label(window, text="PatientFlow", font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg=PRIMARY).pack(pady=10)
tk.Label(window, text="Today's Appointment Queue", font=("Helvetica", 14), bg=BG_COLOR, fg=TEXT).pack(pady=5)

# Search bar
search_frame = tk.Frame(window, bg=BG_COLOR)
search_frame.pack(pady=10)

search_var = tk.StringVar()

search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Helvetica", 11),
                        bg=ENTRY_BG, fg=TEXT, width=40, insertbackground=TEXT)
search_entry.pack(side="left", padx=10)

def on_search_enter(e): search_btn.config(bg="#1d4ed8")
def on_search_leave(e): search_btn.config(bg=BUTTON)

search_btn = tk.Label(search_frame, text="Search", font=("Helvetica", 11, "bold"),
                      bg=BUTTON, fg="white", padx=15, pady=8, cursor="hand2")
search_btn.pack(side="left")
search_btn.bind("<Button-1>", lambda e: update_display())
search_btn.bind("<Enter>", on_search_enter)
search_btn.bind("<Leave>", on_search_leave)

# Reset button styled same
def on_reset_enter(e): reset_btn.config(bg="#1d4ed8")
def on_reset_leave(e): reset_btn.config(bg=BUTTON)

reset_btn = tk.Label(search_frame, text="Reset", font=("Helvetica", 11, "bold"),
                     bg=BUTTON, fg="white", padx=15, pady=8, cursor="hand2")
reset_btn.pack(side="left", padx=10)
reset_btn.bind("<Button-1>", lambda e: reset_filters())
reset_btn.bind("<Enter>", on_reset_enter)
reset_btn.bind("<Leave>", on_reset_leave)

# Frame for listing patients
canvas = tk.Canvas(window, bg=BG_COLOR, highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
scrollbar.pack(side="right", fill="y")

patient_frame = scrollable_frame

# Load and display on startup
queue = load_queue()
update_display()
refresh_queue()

# Footer
tk.Label(window, text="Powered by PatientFlow", font=("Helvetica", 9), bg=BG_COLOR, fg="#94A3B8").pack(pady=5)

window.mainloop()