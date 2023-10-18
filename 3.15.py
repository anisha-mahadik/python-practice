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
ADMIN_PASSWORD = "demo"

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


def show_reservations():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, phone, destination, date, airline FROM reservations')
    reservations = cursor.fetchall()
    conn.close()

    reservation_text = "\n".join([f"Name: {res[0]}, Phone: {res[1]}, Destination: {res[2]}, Date: {res[3]}, Airline: {res[4]}\n" for res in reservations])
    messagebox.showinfo("Reservations", reservation_text)

def back_to_main():
    main_frame.grid()
    reservation_frame.grid_remove()

def admin_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        admin_window()
        admin_root.deiconify()
        login_root.withdraw()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")


def delete_reservation():
    if confirmation:
        conn = sqlite3.connect('reservation.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reservations WHERE id = ?', (selected_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deletion Successful", "The reservation has been deleted.")
        refresh_reservations()
    else:
        messagebox.showinfo("Deletion Canceled", "The reservation has not been deleted.")

def open_delete_reservation_page():
    # Create a new window for the delete reservation page
    delete_window = tk.Toplevel()
    delete_window.title("Delete Reservation Page")

    tk.Label(delete_window, text="Delete Reservation").grid(row=0, column=0, columnspan=2)

def admin_window():
    admin_root.title("Admin Panel")

    tk.Label(admin_root, text="Reservations List:").grid(row=0, column=0, columnspan=2)
    reservations_listbox.grid(row=1, column=0, columnspan=2)


    tk.Button(admin_root, text="Delete Reservation", command=delete_reservation).grid(row=3, column=0, columnspan=2)

def quit_app():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        login_root.destroy()
        admin_root.destroy()
        conn.close()

# Create the main login window
login_root = tk.Tk()
login_root.title("Reservation Management System")

admin_root = tk.Tk()
admin_root.withdraw()

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
login_button = tk.Button(main_frame, text="Login", command=admin_login, font=("Helvetica", 12))
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
submit_button = tk.Button(reservation_frame, text="Submit Reservation", command=submit_reservation, font=("Helvetica", 12))
submit_button.grid(row=6, column=0, columnspan=2)

back_button = tk.Button(reservation_frame, text="Back to Main", command=back_to_main,font=("Helvetica", 12))
back_button.grid(row=7, column=0, columnspan=2)

# Add a "Reservation" button to open the reservation page
show_reservation_button = tk.Button(reservation_frame, text="Reservation", command=show_reservations, font=("Helvetica", 12))
show_reservation_button.grid(row=9, column=0)

# Add a "Delete Reservation" button to open the delete reservation page
delete_button = tk.Button(reservation_frame, text="Delete Reservation", command=open_delete_reservation_page, font=("Helvetica", 12))
delete_button.grid(row=9, column=1)

reservations_listbox = tk.Listbox(reservation_frame, selectmode=tk.SINGLE)
selected_id_var = tk.StringVar()

login_root.protocol("WM_DELETE_WINDOW", quit_app)
admin_root.protocol("WM_DELETE_WINDOW", quit_app)

login_root.geometry("400x400")
admin_root.geometry("500x500")

login_root.mainloop()
