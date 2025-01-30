import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3

# Expedite Entry Tab
def expedite_entry_tab(tab_control):
    frame = ttk.Frame(tab_control)
    tab_control.add(frame, text="Expedite Entry")

    # Expedite Entry Form
    form_frame = ttk.LabelFrame(frame, text="Add Expedite Entry")
    form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Customer Code Input
    ttk.Label(form_frame, text="Customer Code:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    code_entry = ttk.Entry(form_frame, width=25)
    code_entry.grid(row=0, column=1, padx=5, pady=5)

    # Date Input
    ttk.Label(form_frame, text="Date:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    date_entry = ttk.Entry(form_frame, width=25)
    date_entry.grid(row=1, column=1, padx=5, pady=5)

    def show_calendar():
        calendar_window = tk.Toplevel(frame)
        cal = Calendar(calendar_window, date_pattern="yyyy-mm-dd")
        cal.pack(padx=10, pady=10)

        def select_date():
            date_entry.delete(0, tk.END)
            date_entry.insert(0, cal.get_date())
            calendar_window.destroy()

        ttk.Button(calendar_window, text="Select Date", command=select_date).pack(pady=5)

    ttk.Button(form_frame, text="Select Date", command=show_calendar).grid(row=1, column=2, padx=5, pady=5)

    # Cost Type Dropdown
    ttk.Label(form_frame, text="Cost Type:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    cost_type = tk.StringVar(value="Customer Cost")
    cost_dropdown = ttk.Combobox(form_frame, textvariable=cost_type, values=["Customer Cost", "No Charge"], state="readonly", width=22)
    cost_dropdown.grid(row=2, column=1, padx=5, pady=5)

    # Notes Input
    ttk.Label(form_frame, text="Notes:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    notes_entry = ttk.Entry(form_frame, width=25)
    notes_entry.grid(row=3, column=1, padx=5, pady=5)

    # Add Expedite to Database
    def add_expedite():
        customer_code = code_entry.get()
        date = date_entry.get()
        notes = notes_entry.get()
        cost_type_value = cost_type.get()

        if not customer_code or not date:
            messagebox.showerror("Error", "Customer Code and Date are required!")
            return

        # Fetch customer details
        conn = sqlite3.connect("database/pft.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, expedite_cost FROM customers WHERE customer_code = ?", (customer_code,))
        customer = cursor.fetchone()

        if not customer:
            messagebox.showerror("Error", "Invalid Customer Code!")
            return

        customer_id, expedite_cost = customer
        if cost_type_value == "No Charge":
            expedite_cost = 0

        # Insert expedite into database
        cursor.execute("INSERT INTO expedites (date, customer_id, notes, expedite_cost, no_charge) VALUES (?, ?, ?, ?, ?)",
                       (date, customer_id, notes, expedite_cost, int(cost_type_value == "No Charge")))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Expedite added successfully!")
        refresh_table()

    ttk.Button(form_frame, text="Add Expedite", command=add_expedite).grid(row=4, column=0, columnspan=3, pady=10)

    # Expedite Table
    table_frame = ttk.LabelFrame(frame, text="Expedite List")
    table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    expedite_table = ttk.Treeview(table_frame, columns=("ID", "Date", "Customer", "Cost", "Notes", "No Charge"), show="headings", height=15)
    expedite_table.heading("ID", text="ID")
    expedite_table.heading("Date", text="Date")
    expedite_table.heading("Customer", text="Customer")
    expedite_table.heading("Cost", text="Cost")
    expedite_table.heading("Notes", text="Notes")
    expedite_table.heading("No Charge", text="No Charge")
    expedite_table.column("ID", anchor="w", width=30)
    expedite_table.column("Date", anchor="w", width=150)
    expedite_table.column("Customer", anchor="w", width=200)
    expedite_table.column("Cost", anchor="w", width=100)
    expedite_table.column("Notes", anchor="w", width=300)
    expedite_table.column("No Charge", anchor="w", width=100)
    expedite_table.pack(fill="both", expand=True, padx=10, pady=10)

    # Refresh Expedite Table
    def refresh_table():
        for row in expedite_table.get_children():
            expedite_table.delete(row)

        conn = sqlite3.connect("database/pft.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT e.id, e.date, c.name, e.expedite_cost, e.notes, e.no_charge
                          FROM expedites e
                          JOIN customers c ON e.customer_id = c.id
                          ORDER BY e.date DESC''')
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            expedite_table.insert("", "end", values=row)

    refresh_table()

    # Edit Entry
    def edit_entry():
        selected_item = expedite_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No entry selected!")
            return

        item = expedite_table.item(selected_item, "values")
        entry_id, date, customer, cost, notes, no_charge = item

        # Populate form fields
        code_entry.delete(0, tk.END)
        code_entry.insert(0, customer)

        date_entry.delete(0, tk.END)
        date_entry.insert(0, date)

        notes_entry.delete(0, tk.END)
        notes_entry.insert(0, notes)

        cost_type.set("No Charge" if no_charge == "1" else "Customer Cost")

        def save_edit():
            new_date = date_entry.get()
            new_notes = notes_entry.get()
            new_cost_type = cost_type.get()
            is_no_charge = int(new_cost_type == "No Charge")

            conn = sqlite3.connect("database/pft.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE expedites SET date = ?, notes = ?, no_charge = ? WHERE id = ?",
                           (new_date, new_notes, is_no_charge, entry_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Expedite updated successfully!")
            refresh_table()

        ttk.Button(form_frame, text="Save Changes", command=save_edit).grid(row=5, column=0, columnspan=3, pady=5)

    ttk.Button(table_frame, text="Edit Selected", command=edit_entry).pack(side="left", padx=5, pady=5)

    # Delete Entry
    def delete_entry():
        selected_item = expedite_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No entry selected!")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
        if not confirm:
            return

        entry_id = expedite_table.item(selected_item, "values")[0]

        conn = sqlite3.connect("database/pft.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expedites WHERE id = ?", (entry_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Entry deleted successfully!")
        refresh_table()

    ttk.Button(table_frame, text="Delete Selected", command=delete_entry).pack(side="left", padx=5, pady=5)

    frame.grid_columnconfigure(0, weight=1)  # Make the column stretch to match full length
    frame.grid_rowconfigure(1, weight=1)
