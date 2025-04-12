import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import json
import os
import platform
import subprocess

# ----------------- Theme Setup -----------------

# Check if the system is Mac and in dark mode
IS_MAC = platform.system() == "Darwin"
DARK_MODE = False

if IS_MAC:
    try:
        result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], capture_output=True, text=True)
        if 'Dark' in result.stdout:
            DARK_MODE = True
    except:
        pass

# Set theme colors based on dark mode
if DARK_MODE:
    BG = "#1e1e1e"
    FG = "#f8fafc"
    PRIMARY = "#60a5fa"
    ACCENT = "#334155"
    BUTTON = "#2563eb"
    ENTRY_BG = "#1f2937"
else:
    BG = "#ffffff"
    FG = "#1e293b"
    PRIMARY = "#2563eb"
    ACCENT = "#eff6ff"
    BUTTON = "#3b82f6"
    ENTRY_BG = "#ffffff"

# ----------------- Time Slot Data -----------------

# Time brackets with 10-minute slots
time_brackets = {
    "10:00 - 11:00": [datetime.strptime("10:00", "%H:%M") + timedelta(minutes=10 * i) for i in range(6)],
    "11:00 - 12:00": [datetime.strptime("11:00", "%H:%M") + timedelta(minutes=10 * i) for i in range(6)],
    "12:00 - 01:00": [datetime.strptime("12:00", "%H:%M") + timedelta(minutes=10 * i) for i in range(6)],
}

QUEUE_FILE = "queue_data.json"

# ----------------- Queue Functions -----------------

# Load saved bookings from file
def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r") as f:
            return json.load(f)
    return []

# Save bookings to file
def save_queue(queue):
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=4)

# ----------------- Slot Booking Function -----------------

def book_slot():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    bracket = bracket_var.get()

    # Check all fields are filled
    if not (name and age and gender and bracket):
        messagebox.showwarning("Missing Info", "Please fill all fields.")
        return

    queue = load_queue()
    booked_slots = {entry["slot"] for entry in queue}

    # Find first available slot in selected time bracket
    for slot in time_brackets[bracket]:
        slot_str = slot.strftime("%H:%M")
        if slot_str not in booked_slots:
            queue.append({
                "name": name,
                "age": age,
                "gender": gender,
                "slot": slot_str,
                "status": "Pending"
            })
            save_queue(queue)
            messagebox.showinfo("Success", f"{name}, your appointment is at {slot_str}")
            clear_fields()
            return

    messagebox.showerror("Full", "No available slots in this bracket. Try another one.")

# ----------------- Clear Form Fields -----------------

def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_var.set("")
    bracket_var.set("")

# ----------------- UI Setup -----------------

root = tk.Tk()
root.title("PatientFlow - Book Appointment")
root.geometry("600x500")
root.configure(bg=BG)

# Header
tk.Label(root, text="PatientFlow", font=("Helvetica", 20, "bold"), bg=BG, fg=PRIMARY).pack(pady=10)
tk.Label(root, text="Book Your OPD Appointment", font=("Helvetica", 14), bg=BG, fg=FG).pack()

# Form Frame
form = tk.Frame(root, bg=ACCENT, padx=20, pady=20, bd=1, relief="ridge")
form.pack(pady=20)

# Full Name
tk.Label(form, text="Full Name:", bg=ACCENT, fg=FG).grid(row=0, column=0, sticky="w", pady=5)
name_entry = tk.Entry(form, width=30, bg=ENTRY_BG, fg=FG, insertbackground=FG)
name_entry.grid(row=0, column=1, pady=5)

# Age
tk.Label(form, text="Age:", bg=ACCENT, fg=FG).grid(row=1, column=0, sticky="w", pady=5)
age_entry = tk.Entry(form, width=30, bg=ENTRY_BG, fg=FG, insertbackground=FG)
age_entry.grid(row=1, column=1, pady=5)

# Gender Dropdown
tk.Label(form, text="Gender:", bg=ACCENT, fg=FG).grid(row=2, column=0, sticky="w", pady=5)
gender_var = tk.StringVar()
tk.OptionMenu(form, gender_var, "Male", "Female", "Other").grid(row=2, column=1, pady=5)

# Time Bracket Dropdown
tk.Label(form, text="Preferred Time Bracket:", bg=ACCENT, fg=FG).grid(row=3, column=0, sticky="w", pady=5)
bracket_var = tk.StringVar()
tk.OptionMenu(form, bracket_var, *time_brackets.keys()).grid(row=3, column=1, pady=5)

# Book Slot Button
def on_hover(e): book_btn.config(bg="#1d4ed8")
def on_leave(e): book_btn.config(bg=BUTTON)

book_btn = tk.Label(root, text="Book Slot", font=("Helvetica", 13, "bold"), bg=BUTTON, fg="white", padx=20, pady=10, cursor="hand2")
book_btn.pack(pady=20)
book_btn.bind("<Button-1>", lambda e: book_slot())
book_btn.bind("<Enter>", on_hover)
book_btn.bind("<Leave>", on_leave)

# Footer
tk.Label(root, text="Powered by PatientFlow", font=("Helvetica", 9), bg=BG, fg="#94A3B8").pack(pady=10)

# Start the GUI loop
root.mainloop()
