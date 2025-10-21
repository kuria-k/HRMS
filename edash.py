import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from main import logins
import sqlite3
import hashlib



# Back function
def go_back(current_window, previous_window):
    current_window.destroy()
    previous_window.deiconify()
def confirmation(current_window, previous_window):
    result = messagebox.askyesno(title="Logout" , message="Are you sure you want to log out?")
    if result:
        go_back(current_window, previous_window)

def back(current_window, previous_window):
    current_window.destroy()
    previous_window.deiconify()

def clockin(attendance_window, username, previous_window):
    clock = tk.Toplevel(attendance_window)
    clock.title("Checkin")
    clock.geometry("1920x1080")
    attendance_window.withdraw()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("datas.db")
    data_insert_query = '''INSERT INTO attendance_data (User, Clockin) VALUES (?, ?)'''
    data_insert_tuple = (username, current_time)
    cursor = conn.cursor()
    cursor.execute(data_insert_query, data_insert_tuple)
    conn.commit()
    conn.close()

    label_result = tk.Label(clock, text="")
    label_result.pack()

    label_result.config(text=f"{username} checked in at {current_time}")

    back_button = tk.Button(clock, text="Back", command=lambda: back(clock, previous_window))
    back_button.pack(pady=20)


def clockout(attendance_window, username, previous_window):
    clock = tk.Toplevel(attendance_window)
    clock.title("Checkout")
    clock.geometry("1920x1080")
    attendance_window.withdraw()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("datas.db")
    cursor = conn.cursor()

    # Get the latest clock-in time for this user
    cursor.execute("SELECT Clockin FROM attendance_data WHERE User = ? AND Clockout IS NULL ORDER BY Clockin DESC LIMIT 1", (username,))
    result = cursor.fetchone()

    if result:
        clockin_time = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        clockout_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
        hours_worked = round((clockout_time - clockin_time).total_seconds() / 3600, 2)

        # Update the row with Clockout and Hours
        cursor.execute('''
            UPDATE attendance_data
            SET Clockout = ?, Hours = ?
            WHERE User = ? AND Clockin = ?
        ''', (current_time, hours_worked, username, result[0]))

        conn.commit()

        label_result = tk.Label(clock, text=f"{username} checked out at {current_time}\nTotal hours: {hours_worked}")
        label_result.pack(pady=20)
    else:
        label_result = tk.Label(clock, text="No active check-in found.")
        label_result.pack(pady=20)

    conn.close()

    back_button = tk.Button(clock, text="Back", command=lambda: back(clock, previous_window))
    back_button.pack(pady=20)

def review(attendance_window, username):
    view = tk.Toplevel(attendance_window)
    view.title("Attendance Review")
    view.geometry("1920x1080")
    attendance_window.withdraw()

    # Title
    title_label = tk.Label(view, text=f"Attendance for {username}", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Back button
    back_button = tk.Button(view, text="Back", width=15, command=lambda: back(view, attendance_window))
    back_button.pack(pady=10)

    # Frame for table
    table_frame = tk.Frame(view)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Scrollbar
    scrollbar = ttk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    # Treeview widget
    tree = ttk.Treeview(table_frame, columns=("Clockin", "Clockout", "Hours"), show="headings", yscrollcommand=scrollbar.set)
    tree.pack(fill="both", expand=True)

    scrollbar.config(command=tree.yview)

    # Define column headings
    tree.heading("Clockin", text="Clock In")
    tree.heading("Clockout", text="Clock Out")
    tree.heading("Hours", text="Hours Worked")

    # Set column widths
    tree.column("Clockin", width=120)
    tree.column("Clockout", width=120)
    tree.column("Hours", width=100)

    # Fetch attendance records
    conn = sqlite3.connect("datas.db")
    cursor = conn.cursor()
    query = '''SELECT Clockin, Clockout, Hours FROM attendance_data WHERE User = ?'''
    cursor.execute(query, (username,))
    records = cursor.fetchall()
    conn.close()

    # Insert records into table
    for record in records:
        tree.insert("", "end", values=record)

    # # Back button
    # back_button = tk.Button(view, text="Back", width=15, command=lambda: back(view, attendance_window))
    # back_button.pack(pady=10)




def contact(attendance_window, username):
    info = tk.Toplevel(attendance_window)
    info.title("Contact")
    info.geometry("1920x1080")
    attendance_window.withdraw()

    # Create table
    conn = sqlite3.connect("datas.db")
    cursor = conn.cursor()
    table_create_query = '''
    CREATE TABLE IF NOT EXISTS contact_data (id INTEGER PRIMARY KEY AUTOINCREMENT, User TEXT, Contact TEXT, Email TEXT, Backup TEXT)'''
    cursor.execute(table_create_query)
    conn.commit()
    conn.close()

    # Form fields
    contact_label = tk.Label(info, text="Contact", pady=5) 
    contact_label.pack() 
    contact_entry = tk.Entry(info, width=30) 
    contact_entry.pack() 
    email_label = tk.Label(info, text="Email", pady=5) 
    email_label.pack() 
    email_entry = tk.Entry(info, width=30) 
    email_entry.pack() 
    backup_label = tk.Label(info, text="Backup", pady=5) 
    backup_label.pack() 
    backup_entry = tk.Entry(info, width=30) 
    backup_entry.pack()

    def save_contact():
        contact = contact_entry.get()
        email = email_entry.get()
        backup = backup_entry.get()

        conn = sqlite3.connect("datas.db")
        cursor = conn.cursor()

        # Check if user already has a record
        cursor.execute("SELECT * FROM contact_data WHERE User = ?", (username,))
        existing = cursor.fetchone()

        if existing:
            # Update existing record
            cursor.execute('''
                UPDATE contact_data
                SET Contact = ?, Email = ?, Backup = ?
                WHERE User = ?
            ''', (contact, email, backup, username))
        else:
            # Insert new record
            cursor.execute('''
                INSERT INTO contact_data (User, Contact, Email, Backup)
                VALUES (?, ?, ?, ?)
            ''', (username, contact, email, backup))

        conn.commit()
        conn.close()

        tk.Label(info, text="Contact info saved!", fg="green").pack(pady=10)
         
       # Display contact info at the bottom
    conn = sqlite3.connect("datas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Contact, Email, Backup FROM contact_data WHERE User = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        contact_display_frame = tk.Frame(info, bg="white")
        contact_display_frame.pack(pady=20)

        tk.Label(contact_display_frame, text="Saved Contact Info:", font=("Arial", 12, "bold"), bg="#00BFFF", fg="white").pack(anchor="w")

        labels = ["Phone:", "Email:", "Backup:"]
        for i, value in enumerate(result):
            tk.Label(contact_display_frame, text=f"{labels[i]} {value}", bg="white", font=("Arial", 11)).pack(anchor="w")

    submit_button = tk.Button(info, width=25, text="Submit", bg="#87CEEB", fg="white", activebackground="#00BFFF", activeforeground="white",command=save_contact)
    submit_button.pack(pady=10)


    back_button = tk.Button(info, text="Back", command=lambda: back(info, attendance_window))
    back_button.pack(pady=20)


   
def attendance(dashboard_window, employee_name,):
    attend = tk.Toplevel(dashboard_window)
    attend.title("Attendance")
    attend.geometry("1920x1080")
    dashboard_window.withdraw()


    # Table creation on db
    conn = sqlite3.connect("datas.db")
    table_create_query = '''CREATE TABLE IF NOT EXISTS attendance_data (id INTEGER PRIMARY KEY AUTOINCREMENT, User TEXT, Clockin TEXT, Clockout TEXT, Hours REAL )'''
    conn.execute(table_create_query)
    conn.close()

    button_style = {
        "width": 25,
        "height": 2,
        "font": ("Arial", 12, "bold"),
        "bg": "#4682B4",
        "fg": "white",
        "activebackground": "#5A9BD5",
        "activeforeground": "white",
        "bd": 0,
        "relief": "ridge"
    }


    welcome_label = tk.Label(attend, text="Add Employee Details", font=("Arial", 14))
    welcome_label.pack(pady=20)

    checkin_button = tk.Button(attend, text="Check in" , command=lambda: clockin(attend, employee_name, attend), **button_style)
    checkin_button.pack(pady=25)

    checkout_button = tk.Button(attend, text="Check out", command=lambda: clockout(attend, employee_name, attend), **button_style)
    checkout_button.pack(pady=25)

    review_button = tk.Button(attend, text="Review attendance", command=lambda: review(attend, employee_name), **button_style)
    review_button.pack(pady=25)

    back_button = tk.Button(attend, text="Back", command=lambda: back(attend, dashboard_window))
    back_button.pack(pady=20)

def profile(dashboard_window, employee_name, employee_age, employee_gender, employee_department):
    prof = tk.Toplevel(dashboard_window)
    prof.title("Profile")
    prof.geometry("1920x1080")
    prof.configure(bg="white")
    dashboard_window.withdraw()

    # Title
    welcome_label = tk.Label(prof, text="Employee Profile", font=("Arial", 16, "bold"), bg="white")
    welcome_label.pack(pady=15)

    # Connect to database
    conn = sqlite3.connect("datas.db")
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
    # Create a styled frame to hold profile info
      profile_frame = tk.Frame(table_frame, bg="white", bd=2, relief="groove")
    profile_frame.pack(pady=20, padx=20, fill="x")

    # Section title
    tk.Label(profile_frame, text="Employee Profile", font=("Arial", 16, "bold"),
             bg="white", fg="#4682B4").grid(row=0, column=0, columnspan=2, pady=(10, 20))

    fields = ["Name", "Age", "Gender", "Department"]
    for i, field in enumerate(fields):
        tk.Label(profile_frame, text=f"{field}:", font=("Arial", 12, "bold"),
                 bg="white", anchor="w", width=15).grid(row=i+1, column=0, padx=10, pady=8, sticky="w")

        tk.Label(profile_frame, text=result[i], font=("Arial", 12),
                 bg="white", anchor="w", width=30).grid(row=i+1, column=1, padx=10, pady=8, sticky="w")
    else:
        tk.Label(prof, text="No matching profile found.", font=("Arial", 12, "italic"),
             bg="white", fg="red").pack(pady=20)


    # Back Button
    back_button = tk.Button(prof, text="Back", width=15, command=lambda: back(prof, dashboard_window))
    back_button.pack(pady=20)

def apply_leave(attendance_window, username):
    apply = tk.Toplevel(attendance_window)
    apply.title("Leave Application")
    apply.geometry("1920x1080")
    apply.configure(bg="white")
    attendance_window.withdraw()

    # Leave Type
    tk.Label(apply, text="Leave Type", bg="white").pack(pady=(15, 4))
    leave_types = [
        "Annual Leave", 
        "Sick Leave", 
        "Maternity Leave", 
        "Paternity Leave",
        "Compassionate Leave", 
        "Study Leave", 
        "Unpaid Leave"
    ]
    leave_type_combo = ttk.Combobox(apply, values=leave_types, state="readonly", width=30)
    leave_type_combo.set("-- Select Leave Type --")
    leave_type_combo.pack(pady=5)

    # Leave From
    tk.Label(apply, text="Leave From (YYYY-MM-DD)", bg="white").pack(pady=(15, 4))
    date_from_entry = tk.Entry(apply, width=32)
    date_from_entry.pack(pady=5)

    # Leave To
    tk.Label(apply, text="Leave To (YYYY-MM-DD)", bg="white").pack(pady=(15, 4))
    date_to_entry = tk.Entry(apply, width=32)
    date_to_entry.pack(pady=5)

    # Purpose
    tk.Label(apply, text="Purpose", bg="white").pack(pady=(15, 4))
    purpose_entry = tk.Entry(apply, width=36,)
    purpose_entry.pack(pady=5)

    # Leave Period
    tk.Label(apply, text="Leave Period", bg="white").pack(pady=(15, 2))
    leave_period = [
        "Jan 1 2024 - Dec 31 2024",
        "Jan 1 2025 - Dec 31 2025"
    ]
    period_combo = ttk.Combobox(apply, values=leave_period, state="readonly", width=30)
    period_combo.set("-- Select Leave Period --")
    period_combo.pack(pady=5)

    def submit_leave():
        leave_type = leave_type_combo.get()
        date_from = date_from_entry.get()
        date_to = date_to_entry.get()
        purpose = purpose_entry.get()
        period = period_combo.get()
        status = "Pending"

        print(f"{username} applied for {leave_type} from {date_from} to {date_to} for '{purpose}' during {period}")

        conn = sqlite3.connect("datas.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leave_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT, Type TEXT, FromDate TEXT, ToDate TEXT, Purpose TEXT, Period TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO leave_data (Name, Type, FromDate, ToDate, Purpose, Period, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, leave_type, date_from, date_to, purpose, period, status))
        conn.commit()
        conn.close()

        messagebox.showinfo("Leave Submitted", "Your leave application has been successfully submitted.")
        apply.destroy()
        attendance_window.deiconify()

    submit_button = tk.Button(apply, width=25, text="Submit", bg="#87CEEB", fg="white",
                              activebackground="#00BFFF", activeforeground="white", command=submit_leave)
    submit_button.pack(pady=10)

    back_button = tk.Button(apply, text="Back", width=15, command=lambda: back(apply, attendance_window))
    back_button.pack(pady=5)

def leave_review(attendance_window, username):
    reviews = tk.Toplevel(attendance_window)
    reviews.title("Leave Review")
    reviews.geometry("1920x1080")
    attendance_window.withdraw()

    conn = sqlite3.connect("datas.db")
    cursor = conn.cursor()

    # Fetch leave records for the logged-in user
    query = '''SELECT * FROM leave_data WHERE Name = ?'''
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    conn.close()

    # Display results
    if result:
        tk.Label(reviews, text="Your Leave Records", font=("Arial", 14, "bold")).pack(pady=10)

        table_frame = tk.Frame(reviews, bg="white")
        table_frame.pack(pady=10, padx=10, fill="x")

        # Define headers
        headers = ["ID", "Name", "Type", "From", "To", "Purpose", "Period", "Status"]
        for col, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=("Arial", 11, "bold"), bg="#87CEEB", fg="white", width=15, anchor="w").grid(row=0, column=col, padx=2, pady=5)

        # Populate table rows
        for row_num, record in enumerate(result, start=1):
            for col_num in range(len(record)):
                tk.Label(table_frame, text=record[col_num], font=("Arial", 10), bg="white", anchor="w", width=20).grid(row=row_num, column=col_num, padx=2, pady=5)
    else:
        tk.Label(reviews, text="No leave records found.", font=("Arial", 12), fg="red").pack(pady=20)

    # Back button
    back_button = tk.Button(reviews, text="Back", width=15, command=lambda: back(reviews, attendance_window))
    back_button.pack(pady=5)



def leaves(attendance_window, username):
    apply = tk.Toplevel(attendance_window)
    apply.title("Leave Application")
    apply.geometry("1920x1080")
    attendance_window.withdraw()

    # Button styling dictionary
    button_style = {
        "width": 25,
        "height": 2,
        "font": ("Arial", 12, "bold"),
        "bg": "#4682B4",
        "fg": "white",
        "activebackground": "#5A9BD5",
        "activeforeground": "white",
        "bd": 0,
        "relief": "ridge"
    }

    # Header section
    header_frame = tk.Frame(apply, bg="#87CEEB")
    header_frame.pack(fill="x")

    tk.Label(header_frame, text="LEAVE APPLICATION", font=("Arial", 18, "bold"), pady=20).pack()

    # Content section
    content_frame = tk.Frame(apply, bg="#F0F8FF")
    content_frame.pack(pady=60)

    apply_button = tk.Button(content_frame, text="APPLY FOR LEAVE", command=lambda: apply_leave(apply, username), **button_style)
    apply_button.pack(pady=20)

    review_button = tk.Button(content_frame, text="REVIEW LEAVES",  command=lambda: leave_review(apply, username), **button_style)
    review_button.pack(pady=20)

    back_button = tk.Button(apply, text="Back", width=15, command=lambda: back(apply, attendance_window))
    back_button.pack(pady=20)



def feedback(main_window, username):
    fb = tk.Toplevel(main_window)
    fb.title("Feedback Form")
    fb.geometry("1920x1080")
    fb.configure(bg="white")
    main_window.withdraw()

    # Title
    title_label = tk.Label(fb, text="Feedback Form", font=("Arial", 16, "bold"), bg="white")
    title_label.pack(pady=15)

    # Name
    name_label = tk.Label(fb, text="Your Name", bg="white")
    name_label.pack(pady=(10, 2))
    name_entry = tk.Entry(fb, width=32)
    name_entry.insert(0, username)
    name_entry.pack(pady=5)

    # Department
    dept_label = tk.Label(fb, text="Department", bg="white")
    dept_label.pack(pady=(10, 2))
    dept_entry = tk.Entry(fb, width=32)
    dept_entry.pack(pady=5)

    # Experience Rating
    rating_label = tk.Label(fb, text="Overall Experience", bg="white")
    rating_label.pack(pady=(10, 2))
    ratings = ["Excellent", "Good", "Fair", "Poor"]
    rating_combo = ttk.Combobox(fb, values=ratings, state="readonly", width=30)
    rating_combo.set("-- Select Rating --")
    rating_combo.pack(pady=5)

    # Comments
    comments_label = tk.Label(fb, text="Comments / Suggestions", bg="white")
    comments_label.pack(pady=(10, 2))
    comments_entry = tk.Text(fb, width=32, height=5)
    comments_entry.pack(pady=5)

    # Contact Preference
    contact_label = tk.Label(fb, text="Would you like to be contacted?", bg="white")
    contact_label.pack(pady=(10, 2))
    contact_var = tk.StringVar()
    contact_combo = ttk.Combobox(fb, values=["Yes", "No"], textvariable=contact_var, state="readonly", width=30)
    contact_combo.set("-- Select Option --")
    contact_combo.pack(pady=5)

    contact_info_label = tk.Label(fb, text="Email or Phone (if Yes)", bg="white")
    contact_info_label.pack(pady=(10, 2))
    contact_info_entry = tk.Entry(fb, width=32)
    contact_info_entry.pack(pady=5)

    # Submit Feedback
    def submit_feedback():
        name = name_entry.get()
        dept = dept_entry.get()
        rating = rating_combo.get()
        comments = comments_entry.get("1.0", tk.END).strip()
        contact = contact_combo.get()
        contact_info = contact_info_entry.get()
        
        # Table creation on db
        conn = sqlite3.connect("datas.db")
        table_create_query = '''CREATE TABLE IF NOT EXISTS feedback_data(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Department TEXT, Ratings TEXT, Comments TEXT, Contact TEXT, Info TEXT)'''
        conn.execute(table_create_query)
        conn.commit()
        conn.close()

        # Data rendering on db
        conn = sqlite3.connect("datas.db")
        data_insert_query = '''INSERT INTO feedback_data (Name, Department, Ratings, Comments, Contact, Info)VALUES(?,?,?,?,?,?)'''
        data_insert_tuple = (name,  dept, rating, comments, contact, contact_info)
        cursor = conn.cursor()
        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()

        print("Feedback submitted successfully!")

    submit_btn = tk.Button(fb, text="Submit", width=25, bg="#87CEEB", fg="white",activebackground="#00BFFF", activeforeground="white",command=submit_feedback)
    submit_btn.pack(pady=20)

    # Back Button
    back_btn = tk.Button(fb, text="Back", width=15, command=lambda: back(fb, main_window))
    back_btn.pack(pady=5)



def passwords(attendance_window, username, password):
    # change = tk.Toplevel(attendance_window)
    # change.title("Change Password")
    # change.geometry("1920x1080")
    attendance_window.withdraw()

    conn = sqlite3.connect("datas.db")
    cursor = conn.cursor()
    query = '''SELECT Password FROM credentials_data WHERE Username = ?'''
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password_hash = result[0]
        entered_password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        if entered_password_hash == stored_password_hash:
            print("Credentials verified")
            open_window(attendance_window, username) 
        else:
            print("Invalid password")
            messagebox.showerror("Error", "Incorrect current password.")
            attendance_window.destroy()
    else:
        print("Username not found")
        messagebox.showerror("Error", "Username not found.")
        attendance_window.destroy()

def open_window(change, username):
    updater = tk.Toplevel(change)
    updater.title("Set New Password")
    updater.geometry("1925x1085")
    
    tk.Label(updater, text=f"Logged in as {username}").pack()
    tk.Label(updater, text="Enter New Password", font=("Arial", 12)).pack(pady=10)

    password_entry = tk.Entry(updater, width=40, show="*")
    password_entry.pack(pady=10)

    tk.Label(updater, text="Confirm New Password", font=("Arial", 12)).pack(pady=10)
    confirm_entry = tk.Entry(updater, width=40, show="*")
    confirm_entry.pack(pady=10)

    def save_updates():
        new_password = password_entry.get()
        confirm_password = confirm_entry.get()
        

        if not new_password or not confirm_password:
            messagebox.showwarning("Input Error", "Both fields are required.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        new_password_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

        conn = sqlite3.connect("datas.db")
        cursor = conn.cursor()
        query = '''UPDATE credentials_data SET Password = ? WHERE Username = ?'''
        cursor.execute(query, (new_password_hash, username))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Password successfully changed.")
        updater.destroy()
        change.destroy()

    tk.Button(updater, text="Submit", width=25, bg="#87CEEB", fg="white", activebackground="#00BFFF", activeforeground="white", command=save_updates).pack(pady=20)
    # Back Button
    back_btn = tk.Button(updater, text="Back", width=15, command=lambda: back(updater, change))
    back_btn.pack(pady=5)





# Function to open employee dashboard
def open_employee_dashboard(employee_name, employee_age, employee_gender, employee_department, password):
    dashboard = tk.Toplevel(logins)
    dashboard.title("Employee Dashboard")
    dashboard.geometry("1920x1080")
    logins.withdraw()

    button_style = {
        "width": 25,
        "height": 2,
        "font": ("Arial", 12, "bold"),
        "bg": "#4682B4",
        "fg": "white",
        "activebackground": "#5A9BD5",
        "activeforeground": "white",
        "bd": 0,
        "relief": "ridge"
    }

    welcome_label = tk.Label(dashboard, text="Welcome to the Employee Dashboard!", font=("Arial", 14))
    welcome_label.pack(pady=20)

    view_profile_button = tk.Button(dashboard, text="VIEW PROFILE", command=lambda: profile(dashboard, employee_name, employee_age, employee_gender, employee_department), **button_style)
    view_profile_button.pack(pady=10)

    attendance_button = tk.Button(dashboard, text="ATTENDANCE", command=lambda:attendance(dashboard, employee_name), **button_style)
    attendance_button.pack(pady=10)

    view_memo_button = tk.Button(dashboard, text="VIEW MEMO", **button_style)
    view_memo_button.pack(pady=10)

    view_report_button = tk.Button(dashboard, text="VIEW PAYSLIP", **button_style)
    view_report_button.pack(pady=10)

    feedback_button = tk.Button(dashboard, text="FEEDBACK FORM", command=lambda:feedback(dashboard, employee_name), **button_style)
    feedback_button.pack(pady=10)

    apply_leave_button = tk.Button(dashboard, text="APPLY LEAVE",  command=lambda: leaves(dashboard, employee_name), **button_style)
    apply_leave_button.pack(pady=10)

    contact_button = tk.Button(dashboard, text="CONTACT INFO", command=lambda: contact(dashboard, employee_name), **button_style)
    contact_button.pack(pady=10)

    change_pass_button = tk.Button(dashboard, text="CHANGE PASSWORD", command=lambda: passwords(dashboard, employee_name, password), **button_style)
    change_pass_button.pack(pady=10)


    back_button = tk.Button(dashboard, text="Logout", command=lambda: confirmation(dashboard, logins), **button_style)
    back_button.pack(pady=20)


    