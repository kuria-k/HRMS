import tkinter as tk
from tkinter import filedialog, ttk
from main import logins
import os
import webbrowser
import shutil
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

def review(attendance_window, username):
    view = tk.Toplevel(attendance_window)
    view.title("Attendance Review")
    view.geometry("450x400")
    attendance_window.withdraw()

    # Title
    title_label = tk.Label(view, text=f"Attendance for Employees", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # # Frame for table
    table_frame = tk.Frame(view)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # # Scrollbar
    scrollbar = ttk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    # # Treeview widget
    tree = ttk.Treeview(table_frame, columns=("User", "Clockin", "Clockout", "Hours"), show="headings", yscrollcommand=scrollbar.set)
    tree.pack(fill="both", expand=True)

    scrollbar.config(command=tree.yview)

    # # Define column headings
    tree.heading("User", text="User")
    tree.heading("Clockin", text="Clock In")
    tree.heading("Clockout", text="Clock Out")
    tree.heading("Hours", text="Hours Worked")

    # # Set column widths
    tree.column("User", width=120)
    tree.column("Clockin", width=120)
    tree.column("Clockout", width=120)
    tree.column("Hours", width=100)

    # Fetch attendance records
    conn = sqlite3.connect("datas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT User, Clockin, Clockout, Hours FROM attendance_data")
    results = cursor.fetchall()
    conn.close()

    # # Insert records into table
    for result in results:
        tree.insert("", "end", values=result)

    # Back button
    back_button = tk.Button(view, text="Back", width=15, command=lambda: go_back(view, attendance_window))
    back_button.pack(pady=10)


def leave(attendance_window, username):
    application = tk.Toplevel(attendance_window)
    application.title("Attendance Review")
    application.geometry("450x400")
    attendance_window.withdraw()

    # Title
    title_label = tk.Label(application, text=f"Leave Applications", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # # Frame for table
    table_frame = tk.Frame(application)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # # Scrollbar
    scrollbar = ttk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    # # Treeview widget
    tree = ttk.Treeview(table_frame, columns=("Name", "Type", "From", "To", "Purpose", "Period"), show="headings", yscrollcommand=scrollbar.set)
    tree.pack(fill="both", expand=True)

    scrollbar.config(command=tree.yview)

    # # Define column headings
    tree.heading("Name", text="User")
    tree.heading("Type", text="Type")
    tree.heading("From", text="From")
    tree.heading("To", text="To")
    tree.heading("Purpose", text="Purpose")
    tree.heading("Period", text="Period")

    # # Set column widths
    tree.column("Name", width=120)
    tree.column("Type", width=120)
    tree.column("From", width=120)
    tree.column("To", width=100)
    tree.column("Purpose", width=120)
    tree.column("Period", width=120)

    # Fetch attendance records
    conn = sqlite3.connect("datas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Type, FromDate, ToDate, Purpose, Period FROM leave_data")
    results = cursor.fetchall()
    conn.close()

    # # Insert records into table
    for result in results:
        tree.insert("", "end", values=result)

    # Back button
    back_button = tk.Button(application, text="Back", width=15, command=lambda: go_back(application, attendance_window))
    back_button.pack(pady=10)



def profile(dashboard_window):
    prof = tk.Toplevel(dashboard_window)
    prof.title("Employee Profiles")
    prof.geometry("500x400")
    prof.configure(bg="white")
    dashboard_window.withdraw()

    welcome_label = tk.Label(prof, text="Employee Profiles", font=("Arial", 16, "bold"), bg="white")
    welcome_label.pack(pady=10)

    # Frame for table
    table_frame = tk.Frame(prof)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Scrollbar
    scrollbar = ttk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    # Treeview table
    tree = ttk.Treeview(table_frame, columns=("Name", "Age", "Gender", "Department"), show="headings", yscrollcommand=scrollbar.set)
    tree.pack(fill="both", expand=True)

    scrollbar.config(command=tree.yview)

    # Define column headings
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Gender", text="Gender")
    tree.heading("Department", text="Department")

    tree.column("Name", width=120)
    tree.column("Age", width=60)
    tree.column("Gender", width=80)
    tree.column("Department", width=120)

    # Fetch data from database
    conn = sqlite3.connect("datas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Age, Gender, Department FROM student_data")
    results = cursor.fetchall()
    conn.close()

    # Insert data into table
    for row in results:
        tree.insert("", "end", values=row)

    # Back button
    back_button = tk.Button(prof, text="Back", width=15, command=lambda: go_back(prof, dashboard_window))
    back_button.pack(pady=10)


def memo(dashboard_window):
    memo_window = tk.Toplevel(logins)
    memo_window.title("Upload Memo")
    memo_window.geometry("400x500")
    dashboard_window.withdraw()

    title_label = tk.Label(memo_window, text="Upload a PDF Memo File", font=("Arial", 14))
    title_label.pack(pady=20)

    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if file_path:
        filename = os.path.basename(file_path)
        file_label = tk.Label(memo_window, text=f"File selected:\n{filename}", wraplength=350, justify="left")
        file_label.pack(pady=10)

        # Save the uploaded PDF to a local folder
        destination_folder = "uploaded_memos"
        os.makedirs(destination_folder, exist_ok=True)
        destination_path = os.path.join(destination_folder, filename)
        shutil.copy(file_path, destination_path)

        confirm_label = tk.Label(memo_window, text="Memo uploaded successfully!", fg="green", font=("Arial", 11))
        confirm_label.pack(pady=5)

        # Button to open the folder where the PDF was saved
        def open_folder():
            webbrowser.open(destination_folder)

        open_button = tk.Button(memo_window, text="Open Uploaded Memos Folder", command=open_folder)
        open_button.pack(pady=10)

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
    conn = sqlite3.connect("datas.db")
    table_create_query = '''CREATE TABLE IF NOT EXISTS credentials_data (id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT)'''
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

        conn = sqlite3.connect("datas.db")
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
    conn = sqlite3.connect("datas.db")
    table_create_query = '''CREATE TABLE IF NOT EXISTS student_data
    (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Age INT, Gender TEXT, Department TEXT)'''
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

        conn = sqlite3.connect("datas.db")
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





def open_dashboard(username):
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

    view_att_button = tk.Button(dashboard, text="ATTENDANCE REVIEW" , command=lambda: review(dashboard, username))
    view_att_button.pack(pady=10)

    leave_application_button = tk.Button(dashboard, text="LEAVE APPLICATIONS" , command=lambda: leave(dashboard, username))
    leave_application_button.pack(pady=10)


    back_button = tk.Button(dashboard, text="Logout", command=lambda: confirmation(dashboard, logins))
    back_button.pack(pady=20)
    
    # # Employee adding table creation on db
    # conn = sqlite3.connect("datas.db")
    # table_create_query = '''CREATE TABLE IF NOT EXISTS employee_data
    # (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Age INT, Gender TEXT, Department TEXT)
    # '''
    # conn.execute(table_create_query)

  

     

    

    # conn.close()

