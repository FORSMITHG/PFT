import tkinter as tk
from tkinter import ttk, messagebox
import traceback
from customer_mgmt import customer_management_tab
from eet import expedite_entry_tab
from vt import visuals_tab
from utils import resource_path

# Debugging: Print start message
print("Starting Premium Freight Tracker...")

# Log file path
log_file = "error_log.txt"

def log_error(e):
    """Log errors to a file for debugging."""
    with open(log_file, "a") as f:
        f.write(f"Error:\n{traceback.format_exc()}\n")
    print(f"Error logged to {log_file}")

# Main Application
def main_app():
    print("Initializing application...")
    try:
        root = tk.Tk()
        root.title("Premium Freight Tracker")

        # Set window size and center it
        app_width, app_height = 1200, 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (app_width // 2)
        y = (screen_height // 2) - (app_height // 2)
        root.geometry(f"{app_width}x{app_height}+{x}+{y}")
        root.minsize(app_width, app_height)

        # Set logo as the app icon
        try:
            root.iconbitmap(resource_path("favicon.ico"))
            print("Icon loaded successfully.")
        except Exception as e:
            log_error(e)

        # Tab Control
        tab_control = ttk.Notebook(root)
        customer_management_tab(tab_control)
        expedite_entry_tab(tab_control)
        visuals_tab(tab_control)
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        print("Application initialized. Running main loop...")
        root.mainloop()
        print("Application closed.")

    except Exception as e:
        log_error(e)

if __name__ == "__main__":
    try:
        main_app()
    except Exception as e:
        log_error(e)
