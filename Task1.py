import tkinter as tk
from tkinter import messagebox


conversion_rate = 1.13 

def convert_currency():
    try:
        rupees = rupees_entry.get()
        if rupees == ' ' :
            messagebox.showerror("Error", "Rupees amount cannot be blank")
            return

        rupees = float(rupees)
        if rupees < 0:
            messagebox.showerror("Error", "Rupee amount cannot be negative")
            return

        rubles = rupees * conversion_rate
        rubles_entry.delete(0, tk.END)
        rubles_entry.insert(0, round(rubles, 2))
    except ValueError:
        messagebox.showerror("Error", "Rupees amount must be a valid number")

window = tk.Tk()
window.title("Currency Converter")

rupees_label = tk.Label(window, text="Enter amount in Indian Rupees:")
rupees_label.pack()

rupees_entry = tk.Entry(window)
rupees_entry.pack()

rubles_label = tk.Label(window, text="Russian Rubles:")
rubles_label.pack()

rubles_entry = tk.Entry(window)
rubles_entry.pack()

convert_button = tk.Button(window, text="Convert", command=convert_currency)
convert_button.pack()

window.mainloop()
