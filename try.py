import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create SQLite database
conn = sqlite3.connect('reservation.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        destination TEXT NOT NULL,
        date TEXT NOT NULL,
        airline TEXT NOT NULL
    )
''')
conn.commit()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

def validate_input(name, phone, destination, airline):
    if not (name and name.isalpha() and 1 <= len(name) <= 50):
        return "Invalid name."

    if not (phone and phone.isdigit() and 10 <= len(phone) <= 15):
        return "Invalid phone number."

    if not (destination and 1 <= len(destination) <= 100):
        return "Invalid destination."

    if not airline:
        return "Please select an airline."

    return None

def submit_reservation():
    name = name_entry.get()
    phone = phone_entry.get()
    destination = dest_entry.get()
    date = date_entry.get()
    airline = airline_var.get()

    validation_result = validate_input(name, phone, destination, airline)
    if validation_result:
        messagebox.showerror("Input Error", validation_result)
        return

    conn = sqlite3.connect('reservation.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reservations (name, phone, destination, date, airline) VALUES (?, ?, ?, ?, ?)',
                   (name, phone, destination, date, airline))
    conn.commit()
    conn.close()

    messagebox.showinfo("Reservation Submitted", "Your reservation has been submitted.")
    clear_inputs()

def clear_inputs():
    name_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')
    dest_entry.delete(0, 'end')
    date_entry.delete(0, 'end')
    airline_var.set("")

def open_reservation_page():
    main_frame.grid_remove()
    reservation_frame.grid()
    clear_inputs()

def back_to_main():
    main_frame.grid()
    reservation_frame.grid_remove()

# Create the main login window
login_root = tk.Tk()
login_root.title("Reservation Management System")

# Create a main frame for the login page
main_frame = tk.Frame(login_root)
main_frame.grid(row=0, column=0)

# Create labels and entry fields for login
tk.Label(main_frame, text="Admin Login").grid(row=0, column=0, columnspan=2)
tk.Label(main_frame, text="Username:").grid(row=1, column=0)
tk.Label(main_frame, text="Password:").grid(row=2, column=0)

username_entry = tk.Entry(main_frame)
password_entry = tk.Entry(main_frame, show="*")
username_entry.grid(row=1, column=1)
password_entry.grid(row=2, column=1)

# Create a button to log in
login_button = tk.Button(main_frame, text="Login", command=open_reservation_page)
login_button.grid(row=3, column=0, columnspan=2)

# Create a reservation frame
reservation_frame = tk.Frame(login_root)
reservation_frame.grid(row=0, column=0)
reservation_frame.grid_remove()

# Create labels and entry fields for reservation
tk.Label(reservation_frame, text="Submit a New Reservation").grid(row=0, column=0, columnspan=2)

tk.Label(reservation_frame, text="Name:").grid(row=1, column=0)
name_entry = tk.Entry(reservation_frame)
tk.Label(reservation_frame, text="Phone:").grid(row=2, column=0)
phone_entry = tk.Entry(reservation_frame)
tk.Label(reservation_frame, text="Destination:").grid(row=3, column=0)
dest_entry = tk.Entry(reservation_frame)
tk.Label(reservation_frame, text="Date:").grid(row=4, column=0)
date_entry = tk.Entry(reservation_frame)
tk.Label(reservation_frame, text="Airline:").grid(row=5, column=0)
airline_var = tk.StringVar()
airline_var.set("")
airline_dropdown = tk.OptionMenu(reservation_frame, airline_var, "Indigo", "Vistara", "Akasa", "Deccan", "SpiceJet")

name_entry.grid(row=1, column=1)
phone_entry.grid(row=2, column=1)
dest_entry.grid(row=3, column=1)
date_entry.grid(row=4, column=1)
airline_dropdown.grid(row=5, column=1)

# Create a "Submit Reservation" button and a "Back to Main" button
submit_button = tk.Button(reservation_frame, text="Submit Reservation", command=submit_reservation)
submit_button.grid(row=6, column=0, columnspan=2)
back_button = tk.Button(reservation_frame, text="Back to Main", command=back_to_main)
back_button.grid(row=7, column=0, columnspan=2)

login_root.mainloop()
