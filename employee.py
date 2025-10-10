import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from main import logins
import sqlite3



# Back function
def go_back(current_window, previous_window):
    current_window.destroy()
    previous_window.deiconify()

def confirmation(current_window, previous_window):
    result = messagebox.askyesno(title="Logout" , message="Are you sure you want to log out?")
    if result:
        go_back(current_window, previous_window)

def clockin(attendance_window, username, previous_window):
    clock = tk.Toplevel(attendance_window)
    clock.title("Checkin")
    clock.geometry("350x460")
    attendance_window.withdraw()

    label_result = tk.Label(clock, text="")
    label_result.pack()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label_result.config(text=f"{username} checked in at {current_time}")

    back_button = tk.Button(clock, text="Back", command=lambda: confirmation(clock, previous_window))
    back_button.pack(pady=20)


def clockout(attendance_window, username, previous_window):
    clock = tk.Toplevel(attendance_window)
    clock.title("Checkin")
    clock.geometry("350x460")
    attendance_window.withdraw()

    label_result = tk.Label(clock, text="")
    label_result.pack()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label_result.config(text=f"{username} checked out at {current_time}")

    back_button = tk.Button(clock, text="Back", command=lambda: confirmation(clock, previous_window))
    back_button.pack(pady=20)


   
def attendance(dashboard_window, employee_name,):
    attend = tk.Toplevel(dashboard_window)
    attend.title("Attendance")
    attend.geometry("350x460")
    dashboard_window.withdraw()



    # Table creation on db
    conn = sqlite3.connect("data.db")
    table_create_query = '''CREATE TABLE IF NOT EXISTS attendance_data (User TEXT, Clockin TEXT, Clockout TEXT)'''
    conn.execute(table_create_query)
    conn.close()

    welcome_label = tk.Label(attend, text="Add Employee Details", font=("Arial", 14))
    welcome_label.pack(pady=20)

    checkin_button = tk.Button(attend, text="Check in" , command=lambda: clockin(attend, employee_name, attend))
    checkin_button.pack(pady=25)

    checkout_button = tk.Button(attend, text="Check out", command=lambda: clockout(attend, employee_name, attend))
    checkout_button.pack(pady=25)

    review_button = tk.Button(attend, text="Review attendance")
    review_button.pack(pady=25)

def profile(dashboard_window, employee_name, employee_age, employee_gender, employee_department):
    prof = tk.Toplevel(dashboard_window)
    prof.title("Profile")
    prof.geometry("350x460")
    dashboard_window.withdraw()

    welcome_label = tk.Label(prof, text="Employee Profile", font=("Arial", 14))
    welcome_label.pack(pady=20)

    # Connect to database
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # Query for matching employee
    query = '''SELECT Name, Age, Gender, Department FROM student_data 
               WHERE Name = ? AND Age = ? AND Gender = ? AND Department = ?'''
    cursor.execute(query, (employee_name, employee_age, employee_gender, employee_department))
    result = cursor.fetchone()

    conn.close()

    # Display result
    if result:
        name, age, gender, department = result
        tk.Label(prof, text=f"Name: {name}").pack(pady=5)
        tk.Label(prof, text=f"Age: {age}").pack(pady=5)
        tk.Label(prof, text=f"Gender: {gender}").pack(pady=5)
        tk.Label(prof, text=f"Department: {department}").pack(pady=5)
    else:
        tk.Label(prof, text="No matching profile found.").pack(pady=10)

# Function to open employee dashboard
def open_employee_dashboard(employee_name, employee_age, employee_gender, employee_department):
    dashboard = tk.Toplevel(logins)
    dashboard.title("Employee Dashboard")
    dashboard.geometry("350x450")
    logins.withdraw()

    welcome_label = tk.Label(dashboard, text="Welcome to the Employee Dashboard!", font=("Arial", 14))
    welcome_label.pack(pady=20)

    view_profile_button = tk.Button(dashboard, text="VIEW PROFILE", command=lambda: profile(dashboard, employee_name, employee_age, employee_gender, employee_department))
    view_profile_button.pack(pady=10)

    attendance_button = tk.Button(dashboard, text="ATTENDANCE", command=lambda:attendance(dashboard, employee_name))
    attendance_button.pack(pady=10)

    view_memo_button = tk.Button(dashboard, text="VIEW MEMO")
    view_memo_button.pack(pady=10)

    view_report_button = tk.Button(dashboard, text="VIEW PAYSLIP")
    view_report_button.pack(pady=10)

    feedback_button = tk.Button(dashboard, text="FEEDBACK FORM")
    feedback_button.pack(pady=10)

    apply_leave_button = tk.Button(dashboard, text="APPLY LEAVE")
    apply_leave_button.pack(pady=10)

    back_button = tk.Button(dashboard, text="Logout", command=lambda: confirmation(dashboard, logins))
    back_button.pack(pady=20)