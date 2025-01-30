import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import csv
from tkcalendar import Calendar

# Visuals Tab
def visuals_tab(tab_control):
    frame = ttk.Frame(tab_control)
    tab_control.add(frame, text="Visuals")

    ttk.Label(frame, text="Start Date").grid(row=0, column=0, padx=10, pady=5)
    start_date = ttk.Entry(frame)
    start_date.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(frame, text="End Date").grid(row=1, column=0, padx=10, pady=5)
    end_date = ttk.Entry(frame)
    end_date.grid(row=1, column=1, padx=10, pady=5)

    def show_calendar(entry):
        calendar_window = tk.Toplevel(frame)
        cal = Calendar(calendar_window, date_pattern="yyyy-mm-dd")
        cal.pack()
        ttk.Button(calendar_window, text="Select Date", command=lambda: [entry.delete(0, tk.END), entry.insert(0, cal.get_date()), calendar_window.destroy()]).pack()

    ttk.Button(frame, text="Select Start Date", command=lambda: show_calendar(start_date)).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(frame, text="Select End Date", command=lambda: show_calendar(end_date)).grid(row=1, column=2, padx=5, pady=5)

    # Export Data to CSV
    def export_data():
        start = start_date.get()
        end = end_date.get()

        if not start or not end:
            messagebox.showerror("Error", "Both start and end dates are required!")
            return

        conn = sqlite3.connect("database/pft.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT e.date, c.name, e.expedite_cost, e.notes, e.no_charge
                          FROM expedites e
                          JOIN customers c ON e.customer_id = c.id
                          WHERE e.date BETWEEN ? AND ?''', (start, end))
        data = cursor.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("No Data", "No expedites found in the selected date range!")
            return

        # Save to CSV
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Customer", "Cost", "Notes", "No Charge"])
                writer.writerows(data)
            messagebox.showinfo("Success", "Data exported successfully!")

    ttk.Button(frame, text="Export to CSV", command=export_data).grid(row=2, column=0, columnspan=3, pady=10)
