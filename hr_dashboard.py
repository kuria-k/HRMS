import tkinter as tk
from tkinter import filedialog, ttk
from main import logins
import sqlite3
from tkinter import messagebox
import hashlib


# Reusable back function
def go_back(current_window, previous_window):
    current_window.destroy()
    previous_window.deiconify()

def confirmation(current_window, previous_window):
    result = messagebox.askyesno(title="Logout" , message="Are you sure you want to log out?")
    if result:
        go_back(current_window, previous_window)

def profile(dashboard_window, employee_name, employee_age, employee_gender, employee_department):
    prof = tk.Toplevel(dashboard_window)
    prof.title("Profile")
    prof.geometry("360x300")
    prof.configure(bg="white")
    dashboard_window.withdraw()

    # Title
    welcome_label = tk.Label(prof, text="Employee Profile", font=("Arial", 16, "bold"), bg="white")
    welcome_label.pack(pady=15)

    # Connect to database
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    query = '''SELECT Name, Age, Gender, Department FROM student_data 
               WHERE Name = ? AND Age = ? AND Gender = ? AND Department = ?'''
    cursor.execute(query, (employee_name, employee_age, employee_gender, employee_department))
    result = cursor.fetchone()
    conn.close()

    # Table Frame
    table_frame = tk.Frame(prof, bg="white")
    table_frame.pack(pady=10)

    if result:
        fields = ["Name", "Age", "Gender", "Department"]
        for i, field in enumerate(fields):
            tk.Label(table_frame, text=field + ":", font=("Arial", 12, "bold"), bg="white", anchor="w", width=12).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            tk.Label(table_frame, text=result[i], font=("Arial", 12), bg="white", anchor="w", width=20).grid(row=i, column=1, padx=10, pady=5, sticky="w")
    else:
        tk.Label(prof, text="No matching profile found.", font=("Arial", 12), bg="white").pack(pady=10)

    # Back Button
    back_button = tk.Button(prof, text="Back", width=15, command=lambda: confirmation(prof, dashboard_window))
    back_button.pack(pady=20)

def memo(dashboard_window):
    memo_window = tk.Toplevel(logins)
    memo_window.title("Upload Memo")
    memo_window.geometry("400x500")
    dashboard_window.withdraw()

    title_label = tk.Label(memo_window, text="Upload a Memo File", font=("Arial", 14))
    title_label.pack(pady=20)

    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("CSV Files", "*.csv")]
    )

    if file_path:
        file_label = tk.Label(memo_window, text=f"File selected:\n{file_path}", wraplength=350, justify="left")
        file_label.pack(pady=10)

        with open(file_path, 'r') as file:
            content = file.read()

        preview_label = tk.Label(memo_window, text="File Preview:", font=("Arial", 12, "bold"))
        preview_label.pack(pady=5)

        preview_text = tk.Text(memo_window, height=15, width=45)
        preview_text.insert(tk.END, content[:500])
        preview_text.config(state=tk.DISABLED)
        preview_text.pack(pady=10)
    else:
        no_file_label = tk.Label(memo_window, text="No file selected.", fg="red")
        no_file_label.pack(pady=10)

    back_button = tk.Button(memo_window, text="Back", command=lambda: go_back(memo_window, dashboard_window))
    back_button.pack(pady=20)

def create(dashboard_window):
    create_window = tk.Toplevel(logins)
    create_window.title("Create Credentials")
    create_window.geometry("350x450")
    dashboard_window.withdraw()

    welcome_label = tk.Label(create_window, text="Add Employee Credentials", font=("Arial", 14))
    welcome_label.pack(pady=20)

    username_label = tk.Label(create_window, text="Username", pady=5)
    username_label.pack()
    username_entry = tk.Entry(create_window, width=30)
    username_entry.pack()

    password_label = tk.Label(create_window, text="Password", pady=5)
    password_label.pack()
    password_entry = tk.Entry(create_window, show="*", width=30)
    password_entry.pack()

    back_button = tk.Button(create_window, text="Back", command=lambda: go_back(create_window, dashboard_window))
    back_button.pack(pady=10)

    # Create table if not exists
    conn = sqlite3.connect("data.db")
    table_create_query = '''CREATE TABLE IF NOT EXISTS credentials_data (Username TEXT, Password TEXT)'''
    conn.execute(table_create_query)
    conn.commit()
    conn.close()

    # Function to handle submission
    def credentials():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror(title="No inputs", message="Kindly fill in the spaces required")
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("data.db")
        data_insert_query = '''INSERT INTO credentials_data (Username, Password) VALUES (?, ?)'''
        data_insert_tuple = (username, hashed_password)
        conn.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Employee credentials added successfully!")
        create_window.destroy()
        dashboard_window.deiconify()

    # Submit button with correct command
    submit_button = tk.Button(create_window, text="Submit", pady=10, width=15, bg="#87CEEB", fg="#FFFFFF", command=credentials)
    submit_button.pack(pady=20)

      
     


def adding(dashboard_window):
    add_window = tk.Toplevel(logins)
    add_window.title("Add Employee")
    add_window.geometry("350x450")
    dashboard_window.withdraw()

    welcome_label = tk.Label(add_window, text="Add Employee Details", font=("Arial", 14))
    welcome_label.pack(pady=20)

    name_label = tk.Label(add_window, text="Name", pady=5)
    name_label.pack()
    name_entry = tk.Entry(add_window, width=30)
    name_entry.pack()

    age_label = tk.Label(add_window, text="Age", pady=5)
    age_label.pack()
    age_entry = tk.Entry(add_window, width=30)
    age_entry.pack()

    gender_label = tk.Label(add_window, text="Gender", pady=5)
    gender_label.pack()
    gender_combo = ttk.Combobox(add_window, values=["Male", "Female"], width=30, state='readonly')
    gender_combo.pack(pady=5)

    department_label = tk.Label(add_window, text="Department", pady=5)
    department_label.pack()
    department_entry = tk.Entry(add_window, width=30)
    department_entry.pack()

    # Create table if not exists
    conn = sqlite3.connect("data.db")
    table_create_query = '''CREATE TABLE IF NOT EXISTS student_data
    (Name TEXT, Age INT, Gender TEXT, Department TEXT)'''
    conn.execute(table_create_query)
    conn.close()

    # submission
    def submit_data():
        employee_name = name_entry.get()
        employee_age = age_entry.get()
        employee_gender = gender_combo.get()
        employee_department = department_entry.get()

        if not employee_name or not employee_age or not employee_gender or not employee_department:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            employee_age = int(employee_age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return

        conn = sqlite3.connect("data.db")
        data_insert_query = '''INSERT INTO student_data (Name, Age, Gender, Department) VALUES (?, ?, ?, ?)'''
        data_insert_tuple = (employee_name, employee_age, employee_gender, employee_department)
        conn.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Employee added successfully!")
        add_window.destroy()
        dashboard_window.deiconify()

    #Submit button
    submit_button = tk.Button(add_window, text="Submit", pady=10, width=15, bg="#87CEEB", fg="#FFFFFF", command=submit_data)
    submit_button.pack(pady=20)

    back_button = tk.Button(add_window, text="Back", command=lambda: go_back(add_window, dashboard_window))
    back_button.pack(pady=10)





def open_dashboard():
    dashboard = tk.Toplevel(logins)
    dashboard.title("HR Dashboard")
    dashboard.geometry("350x450")
    logins.withdraw()

    welcome_label = tk.Label(dashboard, text="Welcome to the HR Dashboard!", font=("Arial", 14))
    welcome_label.pack(pady=20)

    add_employee_button = tk.Button(dashboard, text="ADD EMPLOYEE", command=lambda: adding(dashboard))
    add_employee_button.pack(pady=10)

    create_credentials_button = tk.Button(dashboard, text="CREATE EMPLOYEE", command=lambda: create(dashboard))
    create_credentials_button.pack(pady=10)

    add_memo_button = tk.Button(dashboard, text="ADD MEMO", command=lambda: memo(dashboard))
    add_memo_button.pack(pady=10)

    add_report_button = tk.Button(dashboard, text="ADD REPORT")
    add_report_button.pack(pady=10)

    view_profile_button = tk.Button(dashboard, text="VIEW EMPLOYEES" , command=lambda: profile(dashboard))
    view_profile_button.pack(pady=10)

    back_button = tk.Button(dashboard, text="Logout", command=lambda: go_back(dashboard, logins))
    back_button.pack(pady=20)
    
    # Employee adding table creation on db
    conn = sqlite3.connect("data.db")
    table_create_query = '''CREATE TABLE IF NOT EXISTS student_data
    (Name TEXT, Age INT, Gender TEXT, Department TEXT)
    '''
    conn.execute(table_create_query)

     

    

    conn.close()

