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


def quit_app():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        login_root.destroy()
        admin_root.destroy()
        conn.close()

def delete_entry():
	selected_entry = reservations_listbox.curselection()
	if not selected_entry:
		messagebox.showerror("Error", "No entry selected")
		return
	confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete the entry?")
	if confirmation:
		conn = sqlite3.connect('reservations.db')
		c = conn.cursor()
		c.execute("DELETE FROM reservations WHERE rowid=?", (selected_entry[0]+1,))
		conn.commit()
		conn.close()
		messagebox.showinfo("Success", "Entry deleted successfully")
		refresh_entries()

def refresh_reservations():
    reservations_listbox.delete(0, 'end')
    conn = sqlite3.connect('reservation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, destination, date, airline FROM reservations')
    reservations = cursor.fetchall()
    for reservation in reservations:
        reservations_listbox.insert('end', f"ID: {reservation[0]}, Name: {reservation[1]}, Destination: {reservation[2]}, Date: {reservation[3]}, Airline: {reservation[4]}")
    conn.close()

    reservations_listbox.grid(row=1, column=0, columnspan=2)
    refresh_reservations()

def back_to_login():
    reservation_frame.pack_forget()
    login_frame.pack(pady=20)

login_root = tk.Tk()
login_root.title("Reservation Management System")
login_root.geometry("800x600")

admin_root = tk.Tk()
admin_root.withdraw()

tk.Label(login_root, text="Admin Login", font=('Helvetica', 20)).grid(row=0, column=0)
tk.Label(login_root, text="Username:", font=('Helvetica', 20)).grid(row=1, column=0)
tk.Label(login_root, text="Password:", font=('Helvetica', 20)).grid(row=2, column=0)
tk.Button(login_root, text="Login", font=('Helvetica', 20), command=admin_login).grid(row=8, column=0, columnspan=2)

username_entry = tk.Entry(login_root)
password_entry = tk.Entry(login_root, show="*")
username_entry.grid(row=1, column=1)
password_entry.grid(row=2, column=1)

reservation_frame = tk.Frame(login_root)

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

submit_button = tk.Button(login_root, text="Submit Reservation", command=submit_reservation)
submit_button.grid(row=9, column=0, columnspan=2)

delete_frame = tk.Frame(reservation_frame)

def delete_reservation():
    selected_id = selected_id_var.get()
    if not selected_id:
        messagebox.showerror("Error", "Please select a reservation to delete.")
        return

    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this reservation?")
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

delete_button = tk.Button(admin_window, text="Delete Entry", command=delete_entry)
back_button = tk.Button(reservation_frame, text="Back to Login", font=('Helvetica', 16), command=back_to_login)

delete_button.grid(row=4, column=0, columnspan=2, pady=10)
back_button.grid(row=6, column=0, columnspan=2, pady=10)

reservations_listbox = tk.Listbox(admin_root, selectmode=tk.SINGLE)
selected_id_var = tk.StringVar()

login_root.protocol("WM_DELETE_WINDOW", quit_app)
admin_root.protocol("WM_DELETE_WINDOW", quit_app)

login_root.geometry("400x300+100+100")
admin_root.geometry("500x500")

login_root.mainloop()
