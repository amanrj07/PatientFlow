import tkinter as tk
from tkinter import messagebox
import json
import os
import platform
import subprocess
from datetime import datetime

# ----------------- Theme Setup -----------------

IS_MAC = platform.system() == "Darwin"
DARK_MODE = False

if IS_MAC:
    try:
        result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                                capture_output=True, text=True)
        if 'Dark' in result.stdout:
            DARK_MODE = True
    except:
        pass

# Colors for light and dark mode
if DARK_MODE:
    BG = "#1e1e1e"
    FG = "#f8fafc"
    PRIMARY = "#60a5fa"
    ACCENT = "#334155"
    BUTTON = "#2563eb"
    ENTRY_BG = "#1f2937"
    STATUS_COLORS = {"Pending": "#9ca3af", "Checked": "#22c55e", "Absent": "#ef4444"}
else:
    BG = "#ffffff"
    FG = "#1e293b"
    PRIMARY = "#2563eb"
    ACCENT = "#eff6ff"
    BUTTON = "#3b82f6"
    ENTRY_BG = "#ffffff"
    STATUS_COLORS = {"Pending": "#6b7280", "Checked": "#16a34a", "Absent": "#dc2626"}

QUEUE_FILE = "queue_data.json"

# ----------------- Data Handling -----------------

# Load queue from file
def load_queue():
    if os.path.exists(QUEUE_FILE) and os.path.getsize(QUEUE_FILE) > 0:
        with open(QUEUE_FILE, "r") as f:
            data = json.load(f)
            data.sort(key=lambda x: datetime.strptime(x["slot"], "%H:%M"))
            return data
    return []

# Save queue to file
def save_queue(queue):
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=4)

# Update the patient list on screen
def update_display():
    for widget in patient_frame.winfo_children():
        widget.destroy()

    query = search_var.get().lower()

    for idx, patient in enumerate(queue):
        if query in patient["name"].lower():
            card = tk.Frame(patient_frame, bg=ACCENT, pady=5, padx=10)
            card.pack(fill="x", pady=5)

            # Patient Info
            info = f"{patient['name']} ({patient['age']} yrs, {patient['gender']})"
            tk.Label(card, text=info, font=("Helvetica", 11, "bold"), bg=ACCENT, fg=FG).grid(row=0, column=0, sticky="w")
            tk.Label(card, text=f"Slot: {patient['slot']}", font=("Helvetica", 10), bg=ACCENT, fg=FG).grid(row=1, column=0, sticky="w")

            # Status Display
            status = patient["status"]
            tk.Label(card, text=f"Status: {status}", font=("Helvetica", 10, "italic"),
                     fg=STATUS_COLORS[status], bg=ACCENT).grid(row=0, column=1, padx=10)

            # Action buttons (only if pending)
            if status == "Pending":
                def mark_checked(e, i=idx): mark_patient(i, "Checked")
                def mark_absent(e, i=idx): mark_patient(i, "Absent")

                check_btn = tk.Label(card, text="Checked", font=("Helvetica", 10),
                                     bg=BUTTON, fg="white", padx=10, pady=5, cursor="hand2")
                check_btn.grid(row=1, column=1, padx=5)
                check_btn.bind("<Button-1>", mark_checked)

                absent_btn = tk.Label(card, text="Absent", font=("Helvetica", 10),
                                      bg="#ef4444", fg="white", padx=10, pady=5, cursor="hand2")
                absent_btn.grid(row=1, column=2, padx=5)
                absent_btn.bind("<Button-1>", mark_absent)

# Update a patient's status
def mark_patient(index, status):
    queue[index]["status"] = status
    save_queue(queue)
    update_display()

# Clear search
def reset_search():
    search_var.set("")
    update_display()

# Auto-refresh queue
def refresh_queue():
    global queue
    queue = load_queue()
    update_display()
    window.after(3000, refresh_queue)  # refresh every 3 seconds

# ----------------- GUI Setup -----------------

window = tk.Tk()
window.title("PatientFlow - Doctor View")
window.geometry("700x600")
window.configure(bg=BG)

# Header
tk.Label(window, text="PatientFlow", font=("Helvetica", 20, "bold"), bg=BG, fg=PRIMARY).pack(pady=10)
tk.Label(window, text="Today's Appointments", font=("Helvetica", 14), bg=BG, fg=FG).pack(pady=5)

# Search Bar
search_frame = tk.Frame(window, bg=BG)
search_frame.pack(pady=10)

search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Helvetica", 11),
                        bg=ENTRY_BG, fg=FG, insertbackground=FG, width=40)
search_entry.pack(side="left", padx=10)

# Search Button
search_btn = tk.Label(search_frame, text="Search", font=("Helvetica", 11, "bold"),
                      bg=BUTTON, fg="white", padx=15, pady=8, cursor="hand2")
search_btn.pack(side="left")
search_btn.bind("<Button-1>", lambda e: update_display())

# Reset Button
reset_btn = tk.Label(search_frame, text="Reset", font=("Helvetica", 11, "bold"),
                     bg=BUTTON, fg="white", padx=15, pady=8, cursor="hand2")
reset_btn.pack(side="left", padx=10)
reset_btn.bind("<Button-1>", lambda e: reset_search())

# Scrollable patient list
canvas = tk.Canvas(window, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=BG)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
scrollbar.pack(side="right", fill="y")

patient_frame = scrollable_frame

# Footer
tk.Label(window, text="Powered by PatientFlow", font=("Helvetica", 9), bg=BG, fg="#94A3B8").pack(pady=5)

# ----------------- Start App -----------------

queue = load_queue()
update_display()
refresh_queue()

window.mainloop()
