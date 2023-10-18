
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to validate name
def validate_name(name):
    if not name:
        return False
    if not name.isalpha():
        return False
    return True

# Function to validate phone number
def validate_phone_number(phone_number):
    if not phone_number:
        return False
    if not phone_number.isdigit():
        return False
    return True

# Function to validate destination
def validate_destination(destination):
    if not destination:
        return False
    if destination.isdigit():
        return False
    return True

# Function to handle form submission
def submit_form():
    name = name_entry.get()
    phone_number = phone_entry.get()
    destination = destination_entry.get()
    
    # Validate inputs
    if not validate_name(name):
        messagebox.showerror("Error", "Invalid name")
        return
    if not validate_phone_number(phone_number):
        messagebox.showerror("Error", "Invalid phone number")
        return
    if not validate_destination(destination):
        messagebox.showerror("Error", "Invalid destination")
        return
    
    # Get selected airline
    airline = airline_var.get()
    
    # Save reservation to database
    conn = sqlite3.connect('reservations.db')
    c = conn.cursor()
    c.execute("INSERT INTO reservations (name, phone_number, destination, airline) VALUES (?, ?, ?, ?)",
              (name, phone_number, destination, airline))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Reservation saved successfully")

# Function to handle admin login
def admin_login():
    username = username_entry.get()
    password = password_entry.get()
    
    # Check admin credentials
    if username == "admin" and password == "admin123":
        # Open admin window
        admin_window = tk.Toplevel(root)
        admin_window.title("Admin Panel")
        
        # Function to delete entry
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
        
        # Function to refresh entries listbox
        def refresh_entries():
            conn = sqlite3.connect('reservations.db')
            c = conn.cursor()
            c.execute("SELECT rowid, * FROM reservations")
            rows = c.fetchall()
            reservations_listbox.delete(0, tk.END)
            for row in rows:
                reservations_listbox.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}")
            conn.close()
        
        # Create reservations listbox
        reservations_listbox = tk.Listbox(admin_window, width=60)
        reservations_listbox.pack(padx=10, pady=10)
        
        # Create delete button
        delete_button = tk.Button(admin_window, text="Delete Entry", command=delete_entry)
        delete_button.pack(pady=10)
        
        # Refresh entries
        refresh_entries()
    else:
        messagebox.showerror("Error", "Invalid admin credentials")

# Create main window
root = tk.Tk()
root.title("Reservation Management System")

# Create name label and entry
name_label = tk.Label(root, text="Name:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack(padx=10, pady=5)

# Create phone number label and entry
phone_label = tk.Label(root, text="Phone Number:")
phone_label.pack()
phone_entry = tk.Entry(root)
phone_entry.pack(padx=10, pady=5)

# Create destination label and entry
destination_label = tk.Label(root, text="Destination:")
destination_label.pack()
destination_entry = tk.Entry(root)
destination_entry.pack(padx=10, pady=5)

# Create airline label and dropdown
airline_label = tk.Label(root, text="Airline:")
airline_label.pack()
airlines = ["Indigo", "Vistara", "Akasa", "Deccan", "SpiceJet"]
airline_var = tk.StringVar(root)
airline_dropdown = tk.OptionMenu(root, airline_var, *airlines)
airline_dropdown.pack(padx=10, pady=5)

# Create submit button
submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.pack(pady=10)

# Create admin login label and entry
admin_label = tk.Label(root, text="Admin Login")
admin_label.pack()
username_entry = tk.Entry(root)
username_entry.pack(padx=10, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(padx=10, pady=5)

# Create admin login button
admin_button = tk.Button(root, text="Login", command=admin_login)
admin_button.pack(pady=10)

# Run the GUI
root.mainloop()


