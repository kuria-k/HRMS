import tkinter as tk
from tkinter import messagebox
from main import logins

# Back function
def go_back(current_window, previous_window):
    current_window.destroy()
    previous_window.deiconify()

def confirmation(current_window, previous_window):
    result = messagebox.askyesno(title="Logout" , message="Are you sure you want to log out?")
    if result:
        go_back(current_window, previous_window)
   

def open_employee_dashboard():
    dashboard = tk.Toplevel(logins)
    dashboard.title("HR Dashboard")
    dashboard.geometry("350x450")
    logins.withdraw()

    welcome_label = tk.Label(dashboard, text="Welcome to the Employee Dashboard!", font=("Arial", 14))
    welcome_label.pack(pady=20)

    view_profile_button = tk.Button(dashboard, text="VIEW PROFILE")
    view_profile_button.pack(pady=10)

    attendance_button = tk.Button(dashboard, text="ATTENDANCE")
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