import tkinter as tk
from tkinter import messagebox
import json
import os

DB_FILE = "users.json"
REMEMBER_FILE = "remember_me.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_remembered_user():
    if os.path.exists(REMEMBER_FILE):
        with open(REMEMBER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_remembered_user(username):
    with open(REMEMBER_FILE, "w") as f:
        json.dump({"username": username}, f)

def clear_remembered_user():
    if os.path.exists(REMEMBER_FILE):
        os.remove(REMEMBER_FILE)

def login():
    username = entry_username.get()
    password = entry_password.get()
    users = load_users()

    if username in users and users[username] == password:
        if remember_var.get():
            save_remembered_user(username)
        else:
            clear_remembered_user()
        messagebox.showinfo("Login", f"Welcome back, {username}!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def register():
    username = entry_username.get()
    password = entry_password.get()
    users = load_users()

    if username in users:
        messagebox.showerror("Register Failed", "Username already exists.")
    else:
        users[username] = password
        save_users(users)
        messagebox.showinfo("Register", "User registered successfully!")

# --- UI Setup ---
root = tk.Tk()
root.title("Login Interface")
root.geometry("400x320")
root.configure(bg="#2d0033")

# Configure root resizing
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame = tk.Frame(root, bg="#2d0033")
frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Configure frame resizing
for i in range(5):
    frame.rowconfigure(i, weight=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=2)

label_title = tk.Label(frame, text="Login", fg="white", bg="#2d0033", font=("Arial", 18))
label_title.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

tk.Label(frame, text="Username:", fg="white", bg="#2d0033").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_username = tk.Entry(frame, highlightbackground="white", highlightthickness=1)
entry_username.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

tk.Label(frame, text="Password:", fg="white", bg="#2d0033").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_password = tk.Entry(frame, show="*", highlightbackground="white", highlightthickness=1)
entry_password.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

remember_var = tk.BooleanVar()
check_remember = tk.Checkbutton(frame, text="Remember Me", variable=remember_var,
                                 fg="white", bg="#2d0033",
                                 activebackground="#2d0033", activeforeground="white",
                                 selectcolor="#2d0033")
check_remember.grid(row=3, column=1, sticky="w", padx=5, pady=5)

btn_login = tk.Button(frame, text="Login", command=login, bg="#520057", fg="white")
btn_login.grid(row=4, column=0, sticky="ew", padx=5, pady=10)

btn_register = tk.Button(frame, text="Register", command=register, bg="#520057", fg="white")
btn_register.grid(row=4, column=1, sticky="ew", padx=5, pady=10)

# Auto-fill remembered user
remembered = load_remembered_user()
if "username" in remembered:
    entry_username.insert(0, remembered["username"])
    remember_var.set(True)

root.mainloop()
