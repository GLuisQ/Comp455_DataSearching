# calendar_popup.py
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from tkcalendar import Calendar


def open_calendar(parent, entry_widget):
    # Create a new window (Toplevel) for the calendar
    
    top = tk.Toplevel(parent)
    top.title("Calendar Set")
    top.grab_set()  # Make the calendar modal to prevent interaction with the main window
    
    # Initialize the calendar widget with the current date
    today = datetime.today()
    
    # Create a frame for the month and year selectors
    selection_frame = ttk.Frame(top)
    selection_frame.pack(pady=5)

    # Month selector (Combobox)
    month_var = tk.StringVar(value=today.strftime("%B"))  # Set default to current month
    months = [datetime(2000, i, 1).strftime("%B") for i in range(1, 13)]  # List of month names
    month_combobox = ttk.Combobox(selection_frame, textvariable=month_var, values=months, state="readonly")
    month_combobox.pack(side="left", padx=5)
    
    # Year selector (Combobox)
    year_var = tk.StringVar(value=str(today.year))  # Set default to current year
    years = [str(year) for year in range(1900, 2101)]  # List of years from 1900 to 2100
    year_combobox = ttk.Combobox(selection_frame, textvariable=year_var, values=years, state="readonly")
    year_combobox.pack(side="left", padx=5)

    # Create a calendar frame to hold the actual calendar widget
    calendar_frame = ttk.Frame(top)
    calendar_frame.pack(pady=10)

    # Initialize the calendar with the current date
    cal = Calendar(calendar_frame, selectmode='day', year=today.year, month=today.month, day=today.day)
    cal.pack()

    # Update the calendar display when month or year is changed
    def update_calendar(*args): #args used in case of using combobox
        month = months.index(month_var.get()) + 1  # Convert selected month to a number
        year = int(year_var.get())  # Get selected year as an integer
        cal.selection_set(datetime(year, month, 1))  # Set calendar to the 1st day of the selected month/year

    # Bind comboboxes to update the calendar when selection changes
    month_combobox.bind("<<ComboboxSelected>>", update_calendar) #triggered when user selects item from combobox, it would update the calendar.
    year_combobox.bind("<<ComboboxSelected>>", update_calendar) #triggered when user selects item from combobox, it would update the calendar.

    # Function to handle date selection and close the popup
    def select_date():
        entry_widget.config(state="normal")
        entry_widget.delete(0, 'end')  # Clear existing text in the date entry
        entry_widget.insert(0, cal.get_date())  # Insert the selected date
        top.destroy()  # Close the calendar popup window
        entry_widget.config(state="readonly")

    # Button to confirm date selection
    ttk.Button(top, text="Select Date", command=select_date).pack(pady=5)
