import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database Connection
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",       # Change this to your MySQL username
            password="root",  # Change this to your MySQL password
            database="loan_db"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
        return None

# Loan Calculation Function
def calculate_loan():
    try:
        loan_type = loan_type_var.get()
        principal = float(principal_entry.get())
        annual_rate = float(interest_entry.get())
        years = int(years_entry.get())

        monthly_rate = (annual_rate / 100) / 12
        months = years * 12

        if monthly_rate == 0:
            monthly_payment = principal / months
        else:
            monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -months)

        monthly_payment_label.config(text=f"Monthly Payment: ₹{monthly_payment:.2f}")

        # Insert data into MySQL
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO loans (loan_type, principal, annual_rate, years, monthly_payment) VALUES (%s, %s, %s, %s, %s)",
                (loan_type, principal, annual_rate, years, monthly_payment)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Loan details saved successfully!")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Function to View Loans in MySQL
def view_loans():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM loans")
        records = cursor.fetchall()
        conn.close()

        view_window = tk.Toplevel(root)
        view_window.title("Stored Loan Records")

        tree = ttk.Treeview(view_window, columns=("ID", "Type", "Amount", "Rate", "Years", "Payment"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Type", text="Loan Type")
        tree.heading("Amount", text="Principal (₹)")
        tree.heading("Rate", text="Interest Rate (%)")
        tree.heading("Years", text="Years")
        tree.heading("Payment", text="Monthly Payment (₹)")
        tree.pack(fill="both", expand=True)

        for record in records:
            tree.insert("", "end", values=record)

# GUI Setup
root = tk.Tk()
root.title("Loan Calculator")
root.geometry("400x450")

tk.Label(root, text="Loan Type:", font=("Arial", 12)).pack(pady=5)
loan_type_var = tk.StringVar()
loan_types = ["Personal Loan", "Car Loan", "Home Loan", "Land Loan"]
loan_dropdown = ttk.Combobox(root, textvariable=loan_type_var, values=loan_types, state="readonly")
loan_dropdown.pack()

tk.Label(root, text="Principal Amount (₹):", font=("Arial", 12)).pack(pady=5)
principal_entry = tk.Entry(root, font=("Arial", 12))
principal_entry.pack()

tk.Label(root, text="Annual Interest Rate (%):", font=("Arial", 12)).pack(pady=5)
interest_entry = tk.Entry(root, font=("Arial", 12))
interest_entry.pack()

tk.Label(root, text="Loan Term (Years):", font=("Arial", 12)).pack(pady=5)
years_entry = tk.Entry(root, font=("Arial", 12))
years_entry.pack()

tk.Button(root, text="Calculate Loan", command=calculate_loan, bg="blue", fg="white", font=("Arial", 12)).pack(pady=10)
monthly_payment_label = tk.Label(root, text="Monthly Payment: ₹0.00", font=("Arial", 12, "bold"))
monthly_payment_label.pack(pady=5)

tk.Button(root, text="View Loans", command=view_loans, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

root.mainloop()
