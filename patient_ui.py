import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import platform
import subprocess
import json
import os

# Utility to check dark mode on Mac
def is_dark_mode():
    if platform.system() == "Darwin":
        try:
            result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], capture_output=True, text=True)
            return 'Dark' in result.stdout
        except Exception:
            return False
    return False

# Theme setup
DARK_MODE = is_dark_mode()
THEME = {
    "bg_color": "#1e1e1e" if DARK_MODE else "#ffffff",
    "text": "#f8fafc" if DARK_MODE else "#1e293b",
    "primary": "#60a5fa" if DARK_MODE else "#2563eb",
    "accent": "#334155" if DARK_MODE else "#eff6ff",
    "button": "#2563eb" if DARK_MODE else "#3b82f6",
    "entry_bg": "#1f2937" if DARK_MODE else "#ffffff"
}

# Time slots setup
TIME_BRACKETS = {
    f"{hour:02}:00 - {hour+1:02}:00": [
        datetime.strptime(f"{hour:02}:00", "%H:%M") + timedelta(minutes=10 * i) for i in range(6)
    ] for hour in range(10, 13)
}

QUEUE_FILE = "queue_data.json"

# Queue management
def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r") as file:
            return json.load(file)
    return []

def save_queue(queue):
    with open(QUEUE_FILE, "w") as file:
        json.dump(queue, file, indent=4)

def book_slot(name, age, gender, bracket):
    if not (name and age and bracket and gender):
        messagebox.showwarning("Missing Info", "Please fill all the fields.")
        return

    queue = load_queue()
    booked_slots = {entry["slot"] for entry in queue}

    for slot in TIME_BRACKETS[bracket]:
        slot_str = slot.strftime("%H:%M")
        if slot_str not in booked_slots:
            queue.append({"name": name, "age": age, "gender": gender, "slot": slot_str, "status": "Pending"})
            save_queue(queue)
            messagebox.showinfo("Booking Confirmed", f"Hi {name},\nYour slot is booked at: {slot_str}")
            return

    messagebox.showerror("Full", "No available slot in this time bracket. Please try another.")

# Clear input fields
def clear_fields(*fields):
    for field in fields:
        field.delete(0, tk.END)

# UI setup
def setup_ui():
    window = tk.Tk()
    window.title("PatientFlow - Book Appointment")
    window.geometry("600x500")
    window.configure(bg=THEME["bg_color"])

    # Header
    tk.Label(window, text="PatientFlow", font=("Helvetica", 20, "bold"), bg=THEME["bg_color"], fg=THEME["primary"]).pack(pady=10)
    tk.Label(window, text="Book Your OPD Appointment", font=("Helvetica", 14), bg=THEME["bg_color"], fg=THEME["text"]).pack(pady=5)

    # Form
    form_frame = tk.Frame(window, bg=THEME["accent"], padx=20, pady=20, bd=1, relief="ridge")
    form_frame.pack(pady=20)

    inputs = {}
    fields = [("Full Name:", "name"), ("Age:", "age"), ("Gender:", "gender"), ("Preferred Time Bracket:", "bracket")]
    for i, (label, key) in enumerate(fields):
        tk.Label(form_frame, text=label, bg=THEME["accent"], fg=THEME["text"], font=("Helvetica", 12)).grid(row=i, column=0, sticky='w', pady=5)
        if key == "gender":
            inputs[key] = tk.StringVar()
            options = tk.OptionMenu(form_frame, inputs[key], "Male", "Female", "Other")
            options.config(font=("Helvetica", 11), bg="white", width=28)
            options.grid(row=i, column=1, pady=5)
        elif key == "bracket":
            inputs[key] = tk.StringVar()
            options = tk.OptionMenu(form_frame, inputs[key], *TIME_BRACKETS.keys())
            options.config(font=("Helvetica", 11), bg="white", width=28)
            options.grid(row=i, column=1, pady=5)
        else:
            inputs[key] = tk.Entry(form_frame, width=30, font=("Helvetica", 11), bg=THEME["entry_bg"], fg=THEME["text"], insertbackground=THEME["text"])
            inputs[key].grid(row=i, column=1, pady=5)

    # Book Slot Button
    def on_book_slot():
        book_slot(inputs["name"].get(), inputs["age"].get(), inputs["gender"].get(), inputs["bracket"].get())
        clear_fields(inputs["name"], inputs["age"])

    book_btn = tk.Button(window, text="Book Slot", font=("Helvetica", 13, "bold"), bg=THEME["button"], fg="white", command=on_book_slot)
    book_btn.pack(pady=20)

    # Footer
    tk.Label(window, text="Powered by PatientFlow", font=("Helvetica", 9), bg=THEME["bg_color"], fg="#94A3B8").pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    setup_ui()
