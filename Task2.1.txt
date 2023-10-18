import tkinter as tk
from tkinter import messagebox

def is_valid_number(input_str, min_limit=None, max_limit=None):
    try:
        num = float(input_str)
        if min_limit is not None and num < min_limit:
            return False
        if max_limit is not None and num > max_limit:
            return False
        return True
    except ValueError:
        return False

def validate_input(entry, min_limit=None, max_limit=None):
    input_value = entry.get().strip()
    if not input_value:
        return False
    if not is_valid_number(input_value, min_limit, max_limit):
        return False
    return True

def calculate_tip():
    if (
        validate_input(entry_bill_amount, min_limit=0)
        and validate_input(entry_tip_percentage, min_limit=0)
        and validate_input(entry_num_people, min_limit=1)
    ):

        bill_amount = float(entry_bill_amount.get())
        tip_percentage = float(entry_tip_percentage.get())
        num_people = int(entry_num_people.get())

        tip_amount = (bill_amount * tip_percentage) / 100
        total_amount = bill_amount + tip_amount
        amount_per_person = total_amount / num_people

       
        result_label.config(
            text=f"Tip: ${tip_amount:.2f}\nTotal: ${total_amount:.2f}\nPer Person: ${amount_per_person:.2f}"
        )
    else:
        messagebox.showerror("Error", "Invalid input. Please check your inputs.")


window = tk.Tk()
window.title("Tip Calculator")
label_bill_amount = tk.Label(window, text="Bill Amount:")
label_tip_percentage = tk.Label(window, text="Tip Percentage:")
label_num_people = tk.Label(window, text="Number of People:")
entry_bill_amount = tk.Entry(window)
entry_tip_percentage = tk.Entry(window)
entry_num_people = tk.Entry(window)
calculate_button = tk.Button(window, text="Calculate", command=calculate_tip)
result_label = tk.Label(window, text="")
label_bill_amount.grid(row=0, column=0)
entry_bill_amount.grid(row=0, column=1)
label_tip_percentage.grid(row=1, column=0)
entry_tip_percentage.grid(row=1, column=1)
label_num_people.grid(row=2, column=0)
entry_num_people.grid(row=2, column=1)
calculate_button.grid(row=3, columnspan=2)
result_label.grid(row=4, columnspan=2)
window.mainloop()
