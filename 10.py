import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a database connection
conn = sqlite3.connect('reservations.db')
c = conn.cursor()

# Create a table to store reservations
c.execute('''CREATE TABLE IF NOT EXISTS reservations
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             phone TEXT NOT NULL,
             destination TEXT NOT NULL,
             airline TEXT NOT NULL,
             date TEXT NOT NULL)''')

# Function to validate name
def validate_name(name):
    if not name:
        return False
    if any(char.isdigit() for char in name):
        return False
    if any(char.isspace() for char in name):
        return False
    if any(char.isalnum() or char.isspace() for char in name):
        return False
    if len(name) < 2 or len(name) > 50:
        return False
    return True

# Function to validate phone number
def validate_phone(phone):
    if not phone:
        return False
    if any(char.isalpha() for char in phone):
        return False
    if any(char.isspace() for char in phone):
        return False
    if any(char.isalnum() or char.isspace() for char in phone):
        return False
    if len(phone) != 10:
        return False
    return True

# Function to validate destination
def validate_destination(destination):
    if not destination:
        return False
    if destination.isdigit():
        return False
    if destination.isalpha():
        return False
    if any(char.isspace() for char in destination):
        return False
    if any(char.isalnum() or char.isspace() for char in destination):
        return False
    if len(destination) < 2 or len(destination) > 50:
        return False
    return True

# Function to handle reservation submission
def submit_reservation():
    name = name_entry.get()
    phone = phone_entry.get()
    destination = destination_entry.get()
    airline = airline_var.get()
    date = date_entry.get()

    if not validate_name(name):
        messagebox.showerror("Error", "Invalid name")
        return
    if not validate_phone(phone):
        messagebox.showerror("Error", "Invalid phone number")
        return
    if not validate_destination(destination):
        messagebox.showerror("Error", "Invalid destination")
        return
    if not airline:
        messagebox.showerror("Error", "Please select an airline")
        return

    # Insert reservation into the database
    c.execute("INSERT INTO reservations (name, phone, destination, airline, date) VALUES (?, ?, ?, ?, ?)",
              (name, phone, destination, airline, date))
    conn.commit()

    messagebox.showinfo("Success", "Reservation submitted successfully")

# Function to handle reservation deletion
def delete_reservation():
    reservation_id = reservation_id_entry.get()

    if not reservation_id:
        messagebox.showerror("Error", "Please enter a reservation ID")
        return

    # Check if reservation exists
    c.execute("SELECT * FROM reservations WHERE id=?", (reservation_id,))
    reservation = c.fetchone()
    if not reservation:
        messagebox.showerror("Error", "Reservation not found")
        return

    # Confirm deletion
    confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this reservation?")
    if confirm:
        # Delete reservation from the database
        c.execute("DELETE FROM reservations WHERE id=?", (reservation_id,))
        conn.commit()
        messagebox.showinfo("Success", "Reservation deleted successfully")

# Function to handle logout
def logout():
    # Clear input fields
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    destination_entry.delete(0, tk.END)
    airline_var.set("")
    date_entry.delete(0, tk.END)
    reservation_id_entry.delete(0, tk.END)

    # Hide reservation form and show login form
    reservation_frame.pack_forget()
    login_frame.pack()

# Function to handle show reservations
def show_reservations():
    # Fetch all reservations from the database
    c.execute("SELECT * FROM reservations")
    reservations = c.fetchall()

    # Display reservations in a messagebox
    messagebox.showinfo("Reservations", "\n".join(str(reservation) for reservation in reservations))

# Create the main window
window = tk.Tk()
window.title("Reservation Management System")

# Create the login frame
login_frame = tk.Frame(window)

# Create login labels and entries
login_label = tk.Label(login_frame, text="Admin Login")
login_label.pack()

username_label = tk.Label(login_frame, text="Username:")
username_label.pack()
username_entry = tk.Entry(login_frame)
username_entry.pack()

password_label = tk.Label(login_frame, text="Password:")
password_label.pack()
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if username and password are correct
    if username == "admin" and password == "password":
        # Hide login frame and show reservation form
        login_frame.pack_forget()
        reservation_frame.pack()
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Create login button
login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack()

# Pack the login frame
login_frame.pack()

# Create the reservation frame
reservation_frame = tk.Frame(window)

# Create reservation labels and entries
name_label = tk.Label(reservation_frame, text="Name:")
name_label.pack()
name_entry = tk.Entry(reservation_frame)
name_entry.pack()

phone_label = tk.Label(reservation_frame, text="Phone:")
phone_label.pack()
phone_entry = tk.Entry(reservation_frame)
phone_entry.pack()

destination_label = tk.Label(reservation_frame, text="Destination:")
destination_label.pack()
destination_entry = tk.Entry(reservation_frame)
destination_entry.pack()

airline_label = tk.Label(reservation_frame, text="Airline:")
airline_label.pack()
airline_var = tk.StringVar()
airline_choices = ["Indigo", "Vistara", "Akasa", "Deccan", "SpiceJet"]
airline_dropdown = tk.OptionMenu(reservation_frame, airline_var, *airline_choices)
airline_dropdown.pack()

date_label = tk.Label(reservation_frame, text="Date:")
date_label.pack()
date_entry = tk.Entry(reservation_frame)
date_entry.pack()

# Create reservation button
submit_button = tk.Button(reservation_frame, text="Submit Reservation", command=submit_reservation)
submit_button.pack()

# Create reservation ID label and entry for deletion
reservation_id_label = tk.Label(reservation_frame, text="Reservation ID:")
reservation_id_label.pack()
reservation_id_entry = tk.Entry(reservation_frame)
reservation_id_entry.pack()

# Create delete reservation button
delete_button = tk.Button(reservation_frame, text="Delete Reservation", command=delete_reservation)
delete_button.pack()

# Create show reservations button
show_reservations_button = tk.Button(reservation_frame, text="Show Reservations", command=show_reservations)
show_reservations_button.pack()

# Create logout button
logout_button = tk.Button(reservation_frame, text="Logout", command=logout)
logout_button.pack()

# Pack the reservation frame
reservation_frame.pack()

# Start the main loop
window.mainloop()

# Close the database connection
conn.close()

