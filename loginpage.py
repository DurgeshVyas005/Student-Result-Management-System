# loginpage.py

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import sys
import os
from tkinter import Tk # Import Tk for launch_dashboard
import json # Import the JSON module for persistent storage

# --- Configuration for Persistent Storage ---
USER_DATA_FILE = "users.json"

def load_users():
    """Loads user data from the JSON file."""
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Return initial users if file is corrupted or empty
            return {"admin": "1234", "user1": "pass"}
    # Return initial users if file does not exist
    return {"admin": "1234", "user1": "pass"}

def save_users(data):
    """Saves user data to the JSON file."""
    try:
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        messagebox.showerror("File Error", "Could not save user data to disk.")


# Load users before the application starts
users = load_users() 


try:
    # Ensure dashboard.py is in the same directory
    from dashboard import RMS
except ImportError:
    messagebox.showerror("Import Error", "Could not find 'dashboard.py'. Ensure all files are in the same directory.")
    sys.exit()

# --- Application Functions ---

def launch_dashboard(username):
    # Close the login window
    root.destroy()
    
    # Launch the main application
    main_root = Tk()
    RMS(main_root)
    main_root.mainloop()


def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Use the more specific login logic from the previous update
    if username not in users:
        messagebox.showerror("Login Failed", "Invalid username.")
    elif users[username] == password:
        messagebox.showinfo("Login Success", f"Welcome back, {username}!")
        launch_dashboard(username)
    else:
        messagebox.showerror("Login Failed", "Invalid password for this user.")

def show_register():
    frame_login.place_forget()
    frame_register.place(relx=0.72, rely=0.5, anchor="center") 

def show_login():
    frame_register.place_forget()
    frame_login.place(relx=0.72, rely=0.5, anchor="center") 

def register():
    global users # Declare global to modify the dictionary
    username = entry_username_reg.get()
    password = entry_password_reg.get()
    
    if username in users:
        messagebox.showwarning("Already Exists", "User already registered!")
    elif username == "" or password == "":
        messagebox.showwarning("Invalid", "Please fill all fields")
    else:
        # Add the new user
        users[username] = password
        # Save the updated dictionary to the file
        save_users(users) 
        
        messagebox.showinfo("Success", "Registration successful! You can now log in.")
        show_login()

def toggle_login_password():
    entry_password.configure(show="" if show_login_pw_var.get() else "*")

def toggle_register_password():
    entry_password_reg.configure(show="" if show_register_pw_var.get() else "*")

# --- GUI Setup ---

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("SRMS - Student Management System Login")
root.state('zoomed')
root.configure(bg="#377dff")

main_frame = ctk.CTkFrame(master=root, fg_color="#377dff", corner_radius=0)
main_frame.pack(fill="both", expand=True)

def resize_outer_box(event=None):
    win_w = root.winfo_width()
    win_h = root.winfo_height()
    outer_w = int(min(win_w * 0.7, 950)) 
    outer_h = int(min(win_h * 0.6, 500))
    outer_box.configure(width=outer_w, height=outer_h)
    outer_box.place(relx=0.5, rely=0.5, anchor="center")
    
    if frame_login.winfo_ismapped():
        frame_login.place(relx=0.72, rely=0.5, anchor="center")
    elif frame_register.winfo_ismapped():
        frame_register.place(relx=0.72, rely=0.5, anchor="center")

root.bind("<Configure>", resize_outer_box)

# Outer box for login/register
outer_box = ctk.CTkFrame(master=main_frame, corner_radius=28, fg_color="#e3eafc")
outer_box.place(relx=0.5, rely=0.5, anchor="center") 

# Place image
try:
    student_img = Image.open("images/logo.png") 
    student_img = student_img.resize((320, 320), Image.LANCZOS)
    student_photo = ImageTk.PhotoImage(student_img)
except Exception:
    placeholder = Image.new('RGB', (320, 320), color = 'lightgray')
    d = ImageDraw.Draw(placeholder)
    d.text((10,150), "Image Missing", fill='black')
    student_photo = ImageTk.PhotoImage(placeholder)

img_label = ctk.CTkLabel(master=outer_box, image=student_photo, text="", width=320, height=320)
img_label.place(relx=0.28, rely=0.5, anchor="center") 

# Login Frame
frame_login = ctk.CTkFrame(master=outer_box, corner_radius=18, fg_color="#f7f9fc", width=420, height=400)

title_login = ctk.CTkLabel(master=frame_login, text="Student Management System", font=("Segoe UI", 24, "bold"), text_color="#2556a8")
title_login.pack(pady=(28, 8))
subtitle_login = ctk.CTkLabel(master=frame_login, text="Sign in to your account", font=("Segoe UI", 14), text_color="#377dff")
subtitle_login.pack(pady=(0, 18))
entry_username = ctk.CTkEntry(master=frame_login, placeholder_text="Username (admin)", width=260, height=36, font=("Segoe UI", 13))
entry_username.pack(pady=8)
entry_password = ctk.CTkEntry(master=frame_login, placeholder_text="Password (1234)", show="*", width=260, height=36, font=("Segoe UI", 13))
entry_password.pack(pady=8)

show_login_pw_var = ctk.BooleanVar()
show_login_pw_checkbox = ctk.CTkCheckBox(master=frame_login, text="Show Password", variable=show_login_pw_var, command=toggle_login_password, font=("Segoe UI", 11))
show_login_pw_checkbox.pack(pady=4)

btn_login = ctk.CTkButton(master=frame_login, text="Log In", width=120, height=36, font=("Segoe UI", 13, "bold"), fg_color="#377dff", text_color="#fff", hover_color="#2556a8", corner_radius=10, command=login)
btn_login.pack(pady=14)

switch_to_register = ctk.CTkButton(master=frame_login, text="Sign Up", fg_color="transparent", text_color="#2556a8", hover=False, font=("Segoe UI", 11), command=show_register)
switch_to_register.pack(pady=2)

# Register Frame
frame_register = ctk.CTkFrame(master=outer_box, corner_radius=18, fg_color="#f7f9fc", width=420, height=400)

title_register = ctk.CTkLabel(master=frame_register, text="Create Account", font=("Segoe UI", 24, "bold"), text_color="#2556a8")
title_register.pack(pady=(28, 8))
subtitle_register = ctk.CTkLabel(master=frame_register, text="Sign up to get started", font=("Segoe UI", 14), text_color="#377dff")
subtitle_register.pack(pady=(0, 18))
entry_username_reg = ctk.CTkEntry(master=frame_register, placeholder_text="Username", width=260, height=36, font=("Segoe UI", 13))
entry_username_reg.pack(pady=8)
entry_password_reg = ctk.CTkEntry(master=frame_register, placeholder_text="Password", show="*", width=260, height=36, font=("Segoe UI", 13))
entry_password_reg.pack(pady=8)

show_register_pw_var = ctk.BooleanVar()
show_register_pw_checkbox = ctk.CTkCheckBox(master=frame_register, text="Show Password", variable=show_register_pw_var, command=toggle_register_password, font=("Segoe UI", 11))
show_register_pw_checkbox.pack(pady=4)

btn_register = ctk.CTkButton(master=frame_register, text="Sign Up", width=120, height=36, font=("Segoe UI", 13, "bold"), fg_color="#377dff", text_color="#fff", hover_color="#2556a8", corner_radius=10, command=register)
btn_register.pack(pady=14)

switch_to_login = ctk.CTkButton(master=frame_register, text="Back to Login", fg_color="transparent", text_color="#2556a8", hover=False, font=("Segoe UI", 11), command=show_login)
switch_to_login.pack(pady=2)

show_login()
root.mainloop()