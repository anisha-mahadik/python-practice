import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create SQLite database
conn = sqlite3.connect('reservations.db')
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

    conn = sqlite3.connect('reservations.db')
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

def show_reservations():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, phone, destination, date, airline FROM reservations')
    reservations = cursor.fetchall()
    conn.close()

    reservation_text = "\n".join([f"Name: {res[0]}, Phone: {res[1]}, Destination: {res[2]}, Date: {res[3]}, Airline: {res[4]}\n" for res in reservations])
    messagebox.showinfo("Reservations", reservation_text)

def delete_reservation():
    selected_id = selected_id_var.get()
    if not selected_id:
        messagebox.showerror("Error", "Please select a reservation to delete.")
        return

    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this reservation?")
    if confirmation:
        conn = sqlite3.connect('reservations.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reservations WHERE id = ?', (selected_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deletion Successful", "The reservation has been deleted.")
    else:
        messagebox.showinfo("Deletion Canceled", "The reservation has not been deleted.")

# Create the main window
root = tk.Tk()
root.title("Reservation Management System")

# Login Page
tk.Label(root, text="Admin Login").pack()
tk.Label(root, text="Username:").pack()
username_entry = tk.Entry(root)
username_entry.pack()
tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Reservation Input Fields
name_entry = tk.Entry(root)
name_entry.pack()
phone_entry = tk.Entry(root)
phone_entry.pack()
dest_entry = tk.Entry(root)
dest_entry.pack()
date_entry = tk.Entry(root)
date_entry.pack()

airline_var = tk.StringVar()
airline_var.set("Indigo")  # Default airline selection
airline_dropdown = tk.OptionMenu(root, airline_var, "Indigo", "Vistara", "Akasa", "Deccan", "SpiceJet")
airline_dropdown.pack()

submit_button = tk.Button(root, text="Submit Reservation", command=submit_reservation)
submit_button.pack()
show_reservations_button = tk.Button(root, text="Show Reservations", command=show_reservations)
show_reservations_button.pack()
delete_button = tk.Button(root, text="Delete Reservation", command=delete_reservation)
delete_button.pack()

# Create a "Back to Login" button for returning to the login page
back_to_login_button = tk.Button(root, text="Back to Login")
back_to_login_button.pack()

root.mainloop()
