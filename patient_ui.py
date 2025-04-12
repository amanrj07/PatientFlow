import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import platform
import subprocess
import json
import os

# Detect dark mode on Mac
IS_MAC = platform.system() == "Darwin"
DARK_MODE = False
if IS_MAC:
    try:
        result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], capture_output=True, text=True)
        if 'Dark' in result.stdout:
            DARK_MODE = True
    except Exception:
        DARK_MODE = False

# Theme setup
if DARK_MODE:
    BG_COLOR = "#1e1e1e"
    TEXT = "#f8fafc"
    PRIMARY = "#60a5fa"
    ACCENT = "#334155"
    BUTTON = "#2563eb"
    ENTRY_BG = "#1f2937"
else:
    BG_COLOR = "#ffffff"
    TEXT = "#1e293b"
    PRIMARY = "#2563eb"
    ACCENT = "#eff6ff"
    BUTTON = "#3b82f6"
    ENTRY_BG = "#ffffff"

# Time brackets (10-min slots)
time_brackets = {
    "10:00 - 11:00": [datetime.strptime("10:00", "%H:%M") + timedelta(minutes=10 * i) for i in range(6)],
    "11:00 - 12:00": [datetime.strptime("11:00", "%H:%M") + timedelta(minutes=10 * i) for i in range(6)],
    "12:00 - 01:00": [datetime.strptime("12:00", "%H:%M") + timedelta(minutes=10 * i) for i in range(6)],
}

QUEUE_FILE = "queue_data.json"

def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r") as file:
            return json.load(file)
    return []

def save_queue(queue):
    with open(QUEUE_FILE, "w") as file:
        json.dump(queue, file, indent=4)

def book_slot():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    bracket = bracket_var.get()

    if not (name and age and bracket and gender):
        messagebox.showwarning("Missing Info", "Please fill all the fields.")
        return

    queue = load_queue()
    current_booked = {entry["slot"] for entry in queue}

    for slot in time_brackets[bracket]:
        slot_str = slot.strftime("%H:%M")
        if slot_str not in current_booked:
            queue.append({
                "name": name,
                "age": age,
                "gender": gender,
                "slot": slot_str,
                "status": "Pending"
            })
            save_queue(queue)
            messagebox.showinfo("Booking Confirmed", f"Hi {name},\nYour slot is booked at: {slot_str}")
            clear_fields()
            return

    messagebox.showerror("Full", "No available slot in this time bracket. Please try another.")

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    bracket_var.set("")
    gender_var.set("")

# UI setup
window = tk.Tk()
window.title("PatientFlow - Book Appointment")
window.geometry("600x500")
window.configure(bg=BG_COLOR)

# Header
tk.Label(window, text="PatientFlow", font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg=PRIMARY).pack(pady=10)
tk.Label(window, text="Book Your OPD Appointment", font=("Helvetica", 14), bg=BG_COLOR, fg=TEXT).pack(pady=5)

# Form
form_frame = tk.Frame(window, bg=ACCENT, padx=20, pady=20, bd=1, relief="ridge")
form_frame.pack(pady=20)

tk.Label(form_frame, text="Full Name:", bg=ACCENT, fg=TEXT, font=("Helvetica", 12)).grid(row=0, column=0, sticky='w', pady=5)
entry_name = tk.Entry(form_frame, width=30, font=("Helvetica", 11), bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Age:", bg=ACCENT, fg=TEXT, font=("Helvetica", 12)).grid(row=1, column=0, sticky='w', pady=5)
entry_age = tk.Entry(form_frame, width=30, font=("Helvetica", 11), bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT)
entry_age.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Gender:", bg=ACCENT, fg=TEXT, font=("Helvetica", 12)).grid(row=2, column=0, sticky='w', pady=5)
gender_var = tk.StringVar()
gender_dropdown = tk.OptionMenu(form_frame, gender_var, "Male", "Female", "Other")
gender_dropdown.config(font=("Helvetica", 11), bg="white", width=28)
gender_dropdown.grid(row=2, column=1, pady=5)

tk.Label(form_frame, text="Preferred Time Bracket:", bg=ACCENT, fg=TEXT, font=("Helvetica", 12)).grid(row=3, column=0, sticky='w', pady=5)
bracket_var = tk.StringVar()
bracket_dropdown = tk.OptionMenu(form_frame, bracket_var, *time_brackets.keys())
bracket_dropdown.config(font=("Helvetica", 11), bg="white", width=28)
bracket_dropdown.grid(row=3, column=1, pady=5)

# Styled Button
def on_enter(e): book_btn.config(bg="#1d4ed8")
def on_leave(e): book_btn.config(bg=BUTTON)

book_btn = tk.Label(
    window,
    text="Book Slot",
    font=("Helvetica", 13, "bold"),
    bg=BUTTON,
    fg="white",
    padx=20,
    pady=10,
    bd=0,
    cursor="hand2"
)
book_btn.pack(pady=20)
book_btn.bind("<Button-1>", lambda e: book_slot())
book_btn.bind("<Enter>", on_enter)
book_btn.bind("<Leave>", on_leave)

# Footer
tk.Label(window, text="Powered by PatientFlow", font=("Helvetica", 9), bg=BG_COLOR, fg="#94A3B8").pack(pady=10)

window.mainloop()