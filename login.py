import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from main import logins
import sqlite3
import hashlib
from hrdash import open_dashboard
from edash import open_employee_dashboard 


def login_user():
    username = username_entry.get()
    password = password_entry.get()
    role = role_combo.get()
    

    if not username or not password or not role:
        messagebox.showerror("Missing Input", "Please fill in all fields.")
        return

    if role == "HR":
        if username == "ADMIN" and password == "12345":
            messagebox.showinfo(title="Login success", message="You have been successfully logged in")
            open_dashboard(username)
        else:
            messagebox.showerror(title="Invalid input", message="Invalid HR credentials, please try again")

    elif role == "Employee":
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        #Validate credentials from credentials_data
        conn = sqlite3.connect("datas.db")
        cursor = conn.cursor()
        query = '''SELECT * FROM credentials_data WHERE Username = ? AND Password = ?'''
        cursor.execute(query, (username, hashed_password))
        result = cursor.fetchone()
        conn.close()

        if result:
            #Getting employee profile from student_data
            conn = sqlite3.connect("datas.db")
            cursor = conn.cursor()
            query = '''SELECT Name, Age, Gender, Department FROM student_data WHERE Name = ?'''
            cursor.execute(query, (username,))
            profile_result = cursor.fetchone()
            conn.close()

            if profile_result:
                employee_name, employee_age, employee_gender, employee_department = profile_result
                messagebox.showinfo("Login Successful", f"Welcome, {employee_name}!")
                open_employee_dashboard(employee_name, employee_age, employee_gender, employee_department,password)
            else:
                messagebox.showerror("Profile Error", "Employee profile not found.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")




#login page

title_label = tk.Label(logins, text="LOGIN", bg="#87CEEB", fg="#FFFFFF", padx=4, pady=9, width=100, font=("Arial", 20))
title_label.pack()

username_label = tk.Label(logins, text="Username", pady=11)
username_label.pack()
username_entry = tk.Entry(logins, width=30)
username_entry.pack()

password_label = tk.Label(logins, text="Password", pady=11)
password_label.pack()
password_entry = tk.Entry(logins, show="*", width=30)
password_entry.pack()

role_label = tk.Label(logins, text="Select Role", pady=11)
role_label.pack()
role_combo = ttk.Combobox(logins, values=["HR", "Employee"], state="readonly", width=28)
role_combo.pack()

submit_button = tk.Button(logins, text="Login", command=login_user)
submit_button.pack(pady=10)

logins.mainloop()

