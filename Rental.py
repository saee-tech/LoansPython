import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Setup
def init_db():
    conn = sqlite3.connect("retail.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        stock INTEGER NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        phone TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin')")
    conn.commit()
    conn.close()

class RetailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Management System")
        self.root.geometry("800x500")
        self.show_login()
    
    def show_login(self):
        self.clear_window()
        ttk.Label(self.root, text="Login", font=("Arial", 20, "bold")).pack(pady=20)
        
        ttk.Label(self.root, text="Username").pack()
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.pack()
        
        ttk.Label(self.root, text="Password").pack()
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.pack()
        
        ttk.Button(self.root, text="Login", command=self.login).pack(pady=10)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = sqlite3.connect("retail.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Credentials")
    
    def show_dashboard(self):
        self.clear_window()
        ttk.Label(self.root, text="Retail Management System", font=("Arial", 20, "bold")).pack(pady=20)
        
        ttk.Button(self.root, text="Manage Products", command=self.manage_products).pack(pady=10)
        ttk.Button(self.root, text="Manage Customers", command=self.manage_customers).pack(pady=10)
        ttk.Button(self.root, text="Billing System", command=self.billing_system).pack(pady=10)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def manage_products(self):
        product_win = tk.Toplevel(self.root)
        product_win.title("Manage Products")
        product_win.geometry("500x400")
        
        ttk.Label(product_win, text="Product Name").pack()
        name_entry = ttk.Entry(product_win)
        name_entry.pack()
        
        ttk.Label(product_win, text="Price").pack()
        price_entry = ttk.Entry(product_win)
        price_entry.pack()
        
        ttk.Label(product_win, text="Stock").pack()
        stock_entry = ttk.Entry(product_win)
        stock_entry.pack()
        
        def add_product():
            name = name_entry.get()
            price = float(price_entry.get())
            stock = int(stock_entry.get())
            conn = sqlite3.connect("retail.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Product Added")
            product_win.destroy()
        
        ttk.Button(product_win, text="Add Product", command=add_product).pack(pady=10)
    
    def manage_customers(self):
        customer_win = tk.Toplevel(self.root)
        customer_win.title("Manage Customers")
        customer_win.geometry("400x300")
        
        ttk.Label(customer_win, text="Customer Name").pack()
        name_entry = ttk.Entry(customer_win)
        name_entry.pack()
        
        ttk.Label(customer_win, text="Phone Number").pack()
        phone_entry = ttk.Entry(customer_win)
        phone_entry.pack()
        
        def add_customer():
            name = name_entry.get()
            phone = phone_entry.get()
            conn = sqlite3.connect("retail.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Customer Added")
            customer_win.destroy()
        
        ttk.Button(customer_win, text="Add Customer", command=add_customer).pack(pady=10)
    
    def billing_system(self):
        bill_win = tk.Toplevel(self.root)
        bill_win.title("Billing System")
        bill_win.geometry("500x400")
        
        ttk.Label(bill_win, text="Enter Product ID").pack()
        product_id_entry = ttk.Entry(bill_win)
        product_id_entry.pack()
        
        ttk.Label(bill_win, text="Enter Quantity").pack()
        qty_entry = ttk.Entry(bill_win)
        qty_entry.pack()
        
        def generate_bill():
            product_id = int(product_id_entry.get())
            qty = int(qty_entry.get())
            conn = sqlite3.connect("retail.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name, price, stock FROM products WHERE id=?", (product_id,))
            product = cursor.fetchone()
            if product and product[2] >= qty:
                total_price = product[1] * qty
                cursor.execute("UPDATE products SET stock=stock-? WHERE id=?", (qty, product_id))
                conn.commit()
                messagebox.showinfo("Invoice", f"Product: {product[0]}\nQuantity: {qty}\nTotal Price: {total_price}")
            else:
                messagebox.showerror("Error", "Invalid Product ID or Stock Unavailable")
            conn.close()
        
        ttk.Button(bill_win, text="Generate Bill", command=generate_bill).pack(pady=10)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = RetailApp(root)
    root.mainloop()
