import tkinter as tk
from tkinter import messagebox

# Function to submit a reservation
def submit_reservation():
    # Validate input here
    # If input is valid, save it to the database
    # Display a confirmation message
    pass

# Function to delete a reservation
def delete_reservation():
    # Display a list of reservations and allow the admin to select one to delete
    # Confirm deletion and remove the selected reservation from the database
    pass

# Create the main application window
app = tk.Tk()
app.title("Reservation Management System")
app.geometry("800x600")  # Set the window size

# Create a frame for the login page
login_frame = tk.Frame(app)
login_frame.pack(pady=20)

# Login Page
tk.Label(login_frame, text="Admin Login", font=('Helvetica', 20)).grid(row=0, column=0)
tk.Label(login_frame, text="Username:", font=('Helvetica', 16)).grid(row=1, column=0)
tk.Label(login_frame, text="Password:", font=('Helvetica', 16)).grid(row=2, column=0)

username_entry = tk.Entry(login_frame)
password_entry = tk.Entry(login_frame, show="*")

username_entry.grid(row=1, column=1)
password_entry.grid(row=2, column=1)

# Create a frame for the reservation page
reservation_frame = tk.Frame(app)

# Reservation Page
name_label = tk.Label(reservation_frame, text="Name:", font=('Helvetica', 16))
name_entry = tk.Entry(reservation_frame)
phone_label = tk.Label(reservation_frame, text="Phone:", font=('Helvetica', 16))
phone_entry = tk.Entry(reservation_frame)
dest_label = tk.Label(reservation_frame, text="Destination:", font=('Helvetica', 16))
dest_entry = tk.Entry(reservation_frame)
date_label = tk.Label(reservation_frame, text="Date:", font=('Helvetica', 16))
date_entry = tk.Entry(reservation_frame)
airline_label = tk.Label(reservation_frame, text="Airline:", font=('Helvetica', 16))
airline_var = tk.StringVar()
airline_var.set("")
airline_dropdown = tk.OptionMenu(reservation_frame, airline_var, "Indigo", "Vistara", "Akasa", "Deccan", "SpiceJet")

name_label.grid(row=0, column=0)
name_entry.grid(row=0, column=1)
phone_label.grid(row=1, column=0)
phone_entry.grid(row=1, column=1)
dest_label.grid(row=2, column=0)
dest_entry.grid(row=2, column=1)
date_label.grid(row=3, column=0)
date_entry.grid(row=3, column=1)
airline_label.grid(row=4, column=0)
airline_dropdown.grid(row=4, column=1)

reservation_button = tk.Button(reservation_frame, text="Submit Reservation", font=('Helvetica', 16), command=submit_reservation)
reservation_button.grid(row=5, column=0, columnspan=2)

# Create a frame for the delete reservation page
delete_frame = tk.Frame(app)

# Delete Reservation Page
# Implement the list of reservations and delete functionality here

# Initially, hide reservation and delete frames
reservation_frame.pack_forget()
delete_frame.pack_forget()

# Function to switch to the reservation page
def open_reservation_page():
    login_frame.pack_forget()
    reservation_frame.pack(pady=20)

# Function to switch to the delete reservation page
def open_delete_reservation_page():
    # Implement switching to the delete page
    pass

# Function to switch back to the login page
def back_to_login():
    reservation_frame.pack_forget()
    login_frame.pack(pady=20)

# Add buttons to switch between pages
reservation_button = tk.Button(login_frame, text="Reservation", font=('Helvetica', 16), command=open_reservation_page)
delete_button = tk.Button(login_frame, text="Delete Reservation", font=('Helvetica', 16), command=open_delete_reservation_page)
back_button = tk.Button(reservation_frame, text="Back to Login", font=('Helvetica', 16), command=back_to_login)

reservation_button.grid(row=3, column=0, columnspan=2, pady=10)
delete_button.grid(row=4, column=0, columnspan=2, pady=10)
back_button.grid(row=6, column=0, columnspan=2, pady=10)

app.mainloop()
