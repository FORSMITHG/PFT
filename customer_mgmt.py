import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from utils import resource_path

# Customer Management Tab
def customer_management_tab(tab_control):
    frame = ttk.Frame(tab_control)
    tab_control.add(frame, text="Customer Management")

    # Customer Entry Form
    form_frame = ttk.LabelFrame(frame, text="Add / Edit Customer")
    form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Name Input
    ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = ttk.Entry(form_frame, width=25)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Address Input
    ttk.Label(form_frame, text="Address:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    address_entry = ttk.Entry(form_frame, width=25)
    address_entry.grid(row=1, column=1, padx=5, pady=5)

    # Expedite Cost Input
    ttk.Label(form_frame, text="Cost:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    cost_entry = ttk.Entry(form_frame, width=25)
    cost_entry.grid(row=2, column=1, padx=5, pady=5)

    # Customer Code Input
    ttk.Label(form_frame, text="Code:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    code_entry = ttk.Entry(form_frame, width=25)
    code_entry.grid(row=3, column=1, padx=5, pady=5)

    # Add / Update Customer
    def add_or_update_customer():
        name = name_entry.get()
        address = address_entry.get()
        cost = cost_entry.get()
        code = code_entry.get()

        if not name or not address or not cost or not code:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = sqlite3.connect(resource_path("database/pft.db"))
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO customers (name, address, expedite_cost, customer_code) VALUES (?, ?, ?, ?)",
                (name, address, float(cost), code.zfill(5))  # Ensure the code is always 5 digits
            )
            conn.commit()
            conn.close()

            refresh_table()
            clear_form()
            messagebox.showinfo("Success", "Customer added/updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid cost value!")

    def clear_form():
        name_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        cost_entry.delete(0, tk.END)
        code_entry.delete(0, tk.END)

    ttk.Button(form_frame, text="Add / Update Customer", command=add_or_update_customer).grid(row=4, column=0, columnspan=3, pady=10)

    # Customer Table
    table_frame = ttk.LabelFrame(frame, text="Customer List")
    table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    customer_table = ttk.Treeview(table_frame, columns=("ID", "Name", "Address", "Expedite Cost", "Customer Code"), show="headings", height=15)
    customer_table.heading("ID", text="ID")
    customer_table.heading("Name", text="Name")
    customer_table.heading("Address", text="Address")
    customer_table.heading("Expedite Cost", text="Expedite Cost")
    customer_table.heading("Customer Code", text="Customer Code")
    customer_table.column("ID", anchor="w", width=30)
    customer_table.column("Name", anchor="w", width=150)
    customer_table.column("Address", anchor="w", width=200)
    customer_table.column("Expedite Cost", anchor="w", width=100)
    customer_table.column("Customer Code", anchor="w", width=100)
    customer_table.pack(fill="both", expand=True, padx=10, pady=10)

    # Refresh Table
    def refresh_table():
        for row in customer_table.get_children():
            customer_table.delete(row)

        conn = sqlite3.connect(resource_path("database/pft.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            customer_table.insert("", "end", values=row)

    refresh_table()

    # Delete Customer
    def delete_customer():
        selected_item = customer_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No customer selected!")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected customer?")
        if not confirm:
            return

        item = customer_table.item(selected_item, "values")
        customer_id = item[0]

        conn = sqlite3.connect(resource_path("database/pft.db"))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        conn.close()

        refresh_table()
        messagebox.showinfo("Success", "Customer deleted successfully!")

    ttk.Button(frame, text="Delete Customer", command=delete_customer).grid(row=2, column=0, sticky="w", padx=10, pady=10)

    frame.grid_columnconfigure(0, weight=1)  # Make the column stretch to match full length
    frame.grid_rowconfigure(1, weight=1)
