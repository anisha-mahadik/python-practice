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

def open_delete_reservation_page():
    delete_window = tk.Toplevel()
    delete_window.title("Delete Reservation Page")

    tk.Label(delete_window, text="Delete Reservation")

def admin_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        admin_window()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")

def admin_window():
    admin_root = tk.Toplevel()
    admin_root.title("Admin Panel")

    reservations_listbox = tk.Listbox(admin_root, selectmode=tk.SINGLE)
 

    refresh_reservations(reservations_listbox)

    delete_button = tk.Button(admin_root, text="Delete Reservation", command=open_delete_reservation_page)
   

def refresh_reservations(listbox):
    conn = sqlite3.connect('reservation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, destination, date, airline FROM reservations')
    reservations = cursor.fetchall()

    for reservation in reservations:
        listbox.insert('end', f"ID: {reservation[0]}, Name: {reservation[1]}, Destination: {reservation[2]}, Date: {reservation[3]}, Airline: {reservation[4]}")

# Create the main login window
login_root = tk.Tk()
login_root.title("Reservation Management System")

main_frame = tk.Frame(login_root)
main_frame.pack()

tk.Label(main_frame, text="Admin Login").pack()

username_entry = tk.Entry(main_frame)
password_entry = tk.Entry(main_frame, show="*")


login_button = tk.Button(main_frame, text="Login", command=admin_login)

reservation_frame = tk.Frame(login_root)

reservation_frame.grid_remove()

tk.Label(reservation_frame, text="Submit a New Reservation")

tk.Label(reservation_frame, text="Name:")
tk.Label(reservation_frame, text="Phone:")
tk.Label(reservation_frame, text="Destination:")
tk.Label(reservation_frame, text="Date:")
tk.Label(reservation_frame, text="Airline:")

name_entry = tk.Entry(reservation_frame)
phone_entry = tk.Entry(reservation_frame)
dest_entry = tk.Entry(reservation_frame)
date_entry = tk.Entry(reservation_frame)
airline_var = tk.StringVar()
airline_var.set("")
airline_dropdown = tk.OptionMenu(reservation_frame, airline_var, "Indigo", "Vistara", "Akasa", "Deccan", "SpiceJet")

name_entry.pack()
phone_entry.pack()
dest_entry.pack()
date_entry.pack()
airline_dropdown.pack()

submit_button = tk.Button(reservation_frame, text="Submit Reservation", command=submit_reservation)
submit_button.pack()
back_button = tk.Button(reservation_frame, text="Back to Main", command=back_to_main)
back_button.pack()

login_root.geometry("400x400")

login_root.mainloop()
