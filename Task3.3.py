import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a SQLite database
conn = sqlite3.connect('reservation.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NOT NULL,
        phone TEXT NOT NULL,
        destination TEXT NOT NULL,
        date TEXT NOT NULL,
        airline TEXT NOT NULL
    )
''')
conn.commit()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

# Define a function to validate the input
def validate_input(name: str, phone: str, destination: str, airline: str):
    if not name or not name.strip() or not name.isalpha():
        return "Invalid name."

    if not phone or not phone.strip() or not phone.isdigit() or len(phone) != 10:
        return "Invalid phone number."

    if not destination or not destination.strip() or not any(c.isalpha() for c in destination) or not any(c.isdigit() for c in destination):
        return "Invalid destination."

    if not airline or not airline.strip():
        return "Please select an airline."

    return None

# Define a function to submit the reservation
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

    # Save the reservation in the database
    conn = sqlite3.connect('reservation.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reservations (name, phone, destination, date, airline) VALUES (?, ?, ?, ?, ?)',
                   (name, phone, destination, date, airline))
    conn.commit()
    conn.close()

    messagebox.showinfo("Reservation Submitted", "Your reservation has been submitted.")
    clear_inputs()

# Define a function to clear the input fields
def clear_inputs():
    name_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')
    dest_entry.delete(0, 'end')
    date_entry.delete(0, 'end')
    airline_var.set("")

# Define a function to log in as admin
def admin_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        admin_window()
        admin_root.deiconify()
        login_root.withdraw()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")

# Define a function to delete a reservation
def delete_reservation():
    selected_id = selected_id_var.get()
    if not selected_id:
        messagebox.showerror("Error", "Please select a reservation to delete.")
        return

    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this reservation?")
    if confirmation:
        cursor.execute('DELETE FROM reservations WHERE id = ?', (selected_id,))
        conn.commit()

        messagebox.showinfo("Deletion Successful", "The reservation has been deleted.")
        refresh_reservations()
    else:
        messagebox.showinfo("Deletion Canceled", "The reservation has not been deleted.")

# Define a function to refresh the list of reservations
def refresh_reservations():
    reservations_listbox.delete(0, 'end')
    cursor.execute('SELECT id, name, destination, date, airline FROM reservations')
    reservations = cursor.fetchall()

    for reservation in reservations:
        reservations_listbox.insert('end', f"ID: {reservation[0]}, Name: {reservation[1]}, Destination: {reservation[2]}, Date: {reservation[3]}, Airline: {reservation[4]}")

# Define a function to quit the app
def quit_app():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        login_root.destroy()
        admin_root.destroy()
        conn.close()

# Create the main login window
login_root = tk.Tk()
login_root.title("Reservation Management System")

# Create the admin window (initially withdrawn)
admin_root = tk.Tk()
admin_root.title("Admin Panel")
admin_root.withdraw()

# Label and entry fields for admin login
tk.Label(login_root, text="Admin Login").grid(row=0, column=0)
tk.Label(login_root, text="Username:").grid(row=1, column=0)
tk.Label(login_root, text="Password:").grid(row=2, column=0)

username_entry = tk.Entry(login_root)
password_entry = tk.Entry(login_root, show="*")
username_entry.grid(row=1, column=1)
password_entry.grid(row=2, column=1)

# Label, entry fields, and dropdown for reservation details
tk.Label(login_root, text="Name:").grid(row=3, column=0)
name_entry = tk.Entry(login_root)
tk.Label(login_root, text="Phone:").grid(row=4, column=0)
phone_entry = tk.Entry(login_root)
tk.Label(login_root, text="Destination:").grid(row=5, column=0)
dest_entry = tk.Entry(login_root)
tk.Label(login_root, text="Date:").grid(row=6, column=0)
date_entry = tk.Entry(login_root)
tk.Label(login_root, text="Airline:").grid(row=7, column=0)
airline_var = tk.StringVar()
airline_var.set("Indigo")  # Default airline selection
airline_dropdown = tk.OptionMenu(login_root, airline_var, "Indigo", "Vistara", "Akasa", "Deccan", "SpiceJet")

name_entry.grid(row=3, column=1)
phone_entry.grid(row=4, column=1)
dest_entry.grid(row=5, column=1)
date_entry.grid(row=6, column=1)
airline_dropdown.grid(row=7, column=1)

# Buttons for admin login and reservation submission
tk.Button(login_root, text="Login", command=admin_login).grid(row=8, column=0, columnspan=2)
submit_button = tk.Button(login_root, text="Submit Reservation", command=submit_reservation)
submit_button.grid(row=9, column=0, columnspan=2)

# Listbox for displaying reservations
reservations_listbox = tk.Listbox(admin_root, selectmode=tk.SINGLE)
selected_id_var = tk.StringVar()

login_root.protocol("WM_DELETE_WINDOW", quit_app)
admin_root.protocol("WM_DELETE_WINDOW", quit_app)

# Set window sizes
login_root.geometry("500x400")
admin_root.geometry("500x400")

# Start the main loop
login_root.mainloop()