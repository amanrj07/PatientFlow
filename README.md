# PatientFlow 🏥

PatientFlow is a desktop-based OPD appointment management system for rural clinics. It includes two interfaces — one for patients to book time slots and another for doctors to manage the queue.

---

## Features

### Patient Interface
- Book OPD slots by name, age, gender, and preferred time bracket.
- Auto-assigns the next available 10-minute slot.
- User-friendly form layout.
- Light/dark mode detection (macOS).

### Doctor Interface
- View all patient bookings.
- Search and filter patients by name.
- Mark patients as **Checked** or **Absent**.
- Color-coded status indicators.
- Reset filter button.
- Auto-refresh the queue every 3 seconds.

---

## How It Works

- Appointments are stored in a shared JSON file: `queue_data.json`.
- Patient-side writes to the file, and doctor-side reads from it.
- Simple Tkinter-based GUI with minimal dependencies.

---

## Getting Started

1. Make sure Python 3 is installed.
2. Run the patient app:
  python patient_ui.py
3. Run the doctor app:
  python doctor_ui.py

---

## Future Improvements
- Multi-device syncing using Firebase.
- Admin dashboard.
- SMS/email reminders for patients.

---

## License

- This project is open-source and free for educational and healthcare purposes.

## Developed with care to improve patient flow in rural health centers. 💙
