from tkinter import *
from tkinter import messagebox
from requests import *
root = Tk()
root.title("Live CC By Anisha ")
root.geometry("1000x700+50+50")
f = ("Times New Roman", 30, "bold")

lab_header = Label(root, text="Live CC By Anisha" , font=f)
lab_header.pack(pady=30)

def convert_currency():
    try:
        rupees = float(rupees_entry.get())
        if rupees < 0:
            messagebox.showerror("Error", "Rupee amount cannot be negative")
            return
        rubles = rupees * conversion_rate
        rubles_entry.delete(0, tk.END)
        rubles_entry.insert(0, round(rubles, 2))
    except ValueError:
        messagebox.showerror("Error", "Rupees amount must be a valid number")

# Create the main window
window = tk.Tk()
window.title("Currency Converter")

# Create labels and entry fields for Rupees and Rubles
rupees_label = tk.Label(window, text="Indian Rupees (INR):")
rupees_label.pack()

rupees_entry = tk.Entry(window)
rupees_entry.pack()

rubles_label = tk.Label(window, text="Russian Rubles (RUB):")
rubles_label.pack()

rubles_entry = tk.Entry(window)
rubles_entry.pack()

# Create the Convert button
convert_button = tk.Button(window, text="Convert", command=convert_currency)
convert_button.pack()

# Run the Tkinter main loop
window.mainloop()
