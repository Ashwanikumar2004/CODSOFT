import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid positive integer for length.")
        return
    
    # Character sets based on user selection
    char_sets = []
    if var_upper.get():
        char_sets.append(string.ascii_uppercase)
    if var_lower.get():
        char_sets.append(string.ascii_lowercase)
    if var_digits.get():
        char_sets.append(string.digits)
    if var_special.get():
        char_sets.append(string.punctuation)
    
    if not char_sets:
        messagebox.showerror("No character sets selected", "Please select at least one character type.")
        return
    
    all_chars = ''.join(char_sets)
    
    # Ensure password contains at least one character from each selected set
    password = [random.choice(cs) for cs in char_sets]
    
    # Fill the remaining length with random choices
    password += random.choices(all_chars, k=length - len(password))
    
    # Shuffle the password list to avoid predictable pattern
    random.shuffle(password)
    
    password_str = ''.join(password)
    password_var.set(password_str)

# Create main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")
root.resizable(False, False)

# Password Length label and entry
tk.Label(root, text="Enter password length:").pack(pady=(20,5))
length_entry = tk.Entry(root)
length_entry.pack()

# Checkbuttons for complexity
frame_checks = tk.Frame(root)
frame_checks.pack(pady=10)

var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=False)

tk.Checkbutton(frame_checks, text="Uppercase (A-Z)", variable=var_upper).grid(row=0, column=0, sticky="w")
tk.Checkbutton(frame_checks, text="Lowercase (a-z)", variable=var_lower).grid(row=1, column=0, sticky="w")
tk.Checkbutton(frame_checks, text="Digits (0-9)", variable=var_digits).grid(row=0, column=1, sticky="w")
tk.Checkbutton(frame_checks, text="Special (!@#$)", variable=var_special).grid(row=1, column=1, sticky="w")

# Generate button
generate_btn = tk.Button(root, text="Generate Password", command=generate_password)
generate_btn.pack(pady=10)

# Password display
password_var = tk.StringVar()
password_label = tk.Entry(root, textvariable=password_var, font=("Helvetica", 14), width=30, justify='center')
password_label.pack(pady=10)

# Run the GUI event loop
root.mainloop()
