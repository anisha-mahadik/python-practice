import tkinter as tk
import sqlite3

# Create a database or connect to an existing one
conn = sqlite3.connect('reservations.db')

# Create a cursor
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS reservations
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             phone TEXT NOT NULL,
             destination TEXT NOT NULL,
             airline TEXT NOT NULL,
             date TEXT NOT NULL)''')

# Function to add reservation to the database
def add_reservation():
    name = name_entry.get()
    phone = phone_entry.get()
    destination = destination_entry.get()
    airline = airline_var.get()
    date = date_entry.get()

    # Insert reservation into the database
    c.execute("INSERT INTO reservations (name, phone, destination, airline, date) VALUES (?, ?, ?, ?, ?)",
              (name, phone, destination, airline, date))
    conn.commit()

# Function to delete reservation from the database
def delete_reservation():
    id = id_entry.get()

    # Delete reservation from the database
    c.execute("DELETE FROM reservations WHERE id=?", (id,))
    conn.commit()

# Create GUI window
root = tk.Tk()
root.title("Reservation Management System")

# Create labels and entries for user input
name_label = tk.Label(root, text="Name:")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

phone_label = tk.Label(root, text="Phone:")
phone_label.grid(row=1, column=0)
phone_entry = tk.Entry(root)
phone_entry.grid(row=1, column=1)

destination_label = tk.Label(root, text="Destination:")
destination_label.grid(row=2, column=0)
destination_entry = tk.Entry(root)
destination_entry.grid(row=2, column=1)

airline_label = tk.Label(root, text="Airline:")
airline_label.grid(row=3, column=0)
airline_var = tk.StringVar(root)
airline_var.set("Indigo")
airline_dropdown = tk.OptionMenu(root, airline_var, "Indigo", "Vistara", "Akasa", "Deccan", "SpiceJet")
airline_dropdown.grid(row=3, column=1)

date_label = tk.Label(root, text="Date:")
date_label.grid(row=4, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=4, column=1)

# Create buttons for adding and deleting reservations
add_button = tk.Button(root, text="Add Reservation", command=add_reservation)
add_button.grid(row=5, column=0)

id_label = tk.Label(root, text="ID:")
id_label.grid(row=6, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=6, column=1)

delete_button = tk.Button(root, text="Delete Reservation", command=delete_reservation)
delete_button.grid(row=7, column=0)

# Run the GUI window
root.mainloop()

# Close the database connection
conn.close()
