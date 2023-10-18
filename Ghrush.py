import tkinter as tk
from tkinter import messagebox
import sqlite3

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

def admin_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        admin_window()
        admin_root.deiconify()
        login_root.withdraw()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")

def admin_window():
    admin_root.title("Admin Panel")

    tk.Label(admin_root, text="Reservations List:").grid(row=0, column=0, columnspan=2)
    reservations_listbox.grid(row=1, column=0, columnspan=2)
    refresh_reservations()

    tk.Label(admin_root, text="Select ID to delete:").grid(row=2, column=0)
    tk.Entry(admin_root, textvariable=selected_id_var).grid(row=2, column=1)
    tk.Button(admin_root, text="Delete Reservation", command=delete_reservation).grid(row=3, column=0, columnspan=2)

def validate_input(name, phone, destination, airline):
    if not name or not name.strip() or not name.isalpha():
        return "Invalid name."

    if not phone or not phone.strip() or not phone.isdigit() or len(phone) != 10:
        return "Invalid phone number."

    if not destination or not destination.strip():
        return "Invalid destination."

    if not airline or not airline.strip():
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

def delete_reservation():
    print("delete function call")
    selected_id = selected_id_var.get()
    print("selected_id",selected_id_var)
    if not selected_id:
        messagebox.showerror("Error", "Please select a reservation to delete.")
        return

    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this reservation?")
    if confirmation:
        conn = sqlite3.connect('reservation.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reservations WHERE id = ?', (selected_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deletion Successful", "The reservation has been deleted.")
        refresh_reservations()
    else:
        messagebox.showinfo("Deletion Canceled", "The reservation has not been deleted.")

def refresh_reservations():
    reservations_listbox.delete(0, 'end')
    conn = sqlite3.connect('reservation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, destination, date, airline FROM reservations')
    reservations = cursor.fetchall()
    for reservation in reservations:
        reservations_listbox.insert('end', f"ID: {reservation[0]}, Name: {reservation[1]}, Destination: {reservation[2]}, Date: {reservation[3]}, Airline: {reservation[4]}")
    conn.close()

def quit_app():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        login_root.destroy()
        admin_root.destroy()
        conn.close()

login_root = tk.Tk()
login_root.title("Reservation Management System")

admin_root = tk.Tk()
admin_root.withdraw()

tk.Label(login_root, text="Admin Login").grid(row=0, column=0)
tk.Label(login_root, text="Username:").grid(row=1, column=0)
tk.Label(login_root, text="Password:").grid(row=2, column=0)
tk.Button(login_root, text="Login", command=admin_login).grid(row=8, column=0, columnspan=2)

username_entry = tk.Entry(login_root)
password_entry = tk.Entry(login_root, show="*")
username_entry.grid(row=1, column=1)
password_entry.grid(row=2, column=1)


tk.Label(admin_root, text="Name:").grid(row=4, column=0)
name_entry = tk.Entry(admin_root)
tk.Label(admin_root, text="Phone:").grid(row=5, column=0)
phone_entry = tk.Entry(admin_root)
tk.Label(admin_root, text="Destination:").grid(row=6, column=0)
dest_entry = tk.Entry(admin_root)
tk.Label(admin_root, text="Date:").grid(row=7, column=0)
date_entry = tk.Entry(admin_root)
tk.Label(admin_root, text="Airline:").grid(row=8, column=0)
airline_var = tk.StringVar()
airline_var.set("Indigo")  # Default airline selection
airline_dropdown = tk.OptionMenu(admin_root, airline_var, "Indigo", "Vistara", "Akasa", "Deccan", "SpiceJet")

name_entry.grid(row=4, column=1)
phone_entry.grid(row=5, column=1)
dest_entry.grid(row=6, column=1)
date_entry.grid(row=7, column=1)
airline_dropdown.grid(row=8, column=1)

submit_button = tk.Button(admin_root, text="Submit Reservation", command=submit_reservation)
submit_button.grid(row=9, column=0, columnspan=2)

reservations_listbox = tk.Listbox(admin_root, selectmode=tk.SINGLE)
selected_id_var = tk.StringVar()

login_root.protocol("WM_DELETE_WINDOW", quit_app)
admin_root.protocol("WM_DELETE_WINDOW", quit_app)

login_root.geometry("400x400")
admin_root.geometry("500x500")

login_root.mainloop()
