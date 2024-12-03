# main.py
import tkinter as tk
from tkinter import ttk

from calendar_use import \
    open_calendar  # Import the calendar function from other file


def clear_name():
    name_entry.delete(0, 'end')
def clear_num():
    num_spinbox.delete(0, 'end')  # Clears the content of the spinbox
def clear_date():
    date_entry.config(state="normal")
    date_entry.delete(0, 'end')  # Clears the content of the date entry
    date_entry.config(state="readonly")
def search_start():
    #This is a template.
    print("search_pass")

def open_filter_modal():
    modal = tk.Toplevel(root)  # Create a new window
    modal.title("Filter Data")
    modal.geometry("300x300")  # Set size of the pop-up window

    # Create a LabelFrame for filter widgets
    search_widgets_frame = ttk.LabelFrame(modal, text="Filter Criteria:")
    search_widgets_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    # Name input field
    ttk.Label(search_widgets_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    search_name_entry = ttk.Entry(search_widgets_frame)
    search_name_entry.grid(row=1, column=0, sticky="ew", padx=5)
    search_name_entry.insert(0, "Name")  # Placeholder text

    search_name_clear_button = ttk.Button(search_widgets_frame, text="❌", width=2, command=clear_name, style="RedX.TButton")
    search_name_clear_button.grid(row=1, column=1, padx=5)  # Position the button next to the entry

    # Age input field
    ttk.Label(search_widgets_frame, text="Age:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    search_num_spinbox = ttk.Spinbox(search_widgets_frame, from_=18, to=100)
    search_num_spinbox.grid(row=3, column=0, sticky="ew", padx=5)

    # Date input field
    ttk.Label(search_widgets_frame, text="Date:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    search_date_entry = ttk.Entry(search_widgets_frame, state="readonly")
    search_date_entry.grid(row=5, column=0, sticky="ew", padx=5)

    # Close button
    search_close_button = ttk.Button(search_widgets_frame, text="Close", command=modal.destroy)
    search_close_button.grid(row=6, column=0, pady=10, sticky="ew")




root = tk.Tk()
root.title("Data Viewer")
style = ttk.Style(root)

# Apply custom themes (light and dark)
root.tk.call("source", "../theme/forest-light.tcl")  # Load light theme
root.tk.call("source", "../theme/forest-dark.tcl")   # Load dark theme
# Set active theme to dark
style.theme_use("forest-dark")

style.configure("RedX.TButton", 
    foreground="red",  # Set the text color to red
    font=("Arial", 10, "bold"),
    padding=5
    )

# Main frame setup
frame = ttk.Frame(root)
frame.pack(fill="both", expand=True)
frame.grid_columnconfigure(0, weight=1)
# Label frame for search functionality
widgets_frame = ttk.LabelFrame(frame, text="Search:")
widgets_frame.grid(row=0, column=0)

name_label = ttk.Label(widgets_frame, text="Name:")
name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)  # Add padding for spacing
name_entry = ttk.Entry(widgets_frame)
# Entry widget for entering a name
name_entry = ttk.Entry(widgets_frame)
name_entry.grid(row=1, column=0, sticky="ew", padx=8)
name_entry.insert(0, "Name")  # Set initial placeholder text
name_entry.bind("<FocusIn>", lambda e: name_entry.delete(0, 'end'))  # Clear placeholder on focus
# Clear button for name
name_clear_button = ttk.Button(widgets_frame, text="❌", width=2, command=clear_name, style="RedX.TButton")
name_clear_button.grid(row=1, column=1, padx=5)  # Position the button next to the spinbox


num_label = ttk.Label(widgets_frame, text="Age:")
num_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)  # Add padding for spacing
# Spinbox for number
num_spinbox = ttk.Spinbox(widgets_frame, from_=18, to=100)
num_spinbox.grid(row=3, column=0, sticky="ew", padx=8 )

#Clear button for number
num_clear_button = ttk.Button(widgets_frame, text="❌", width=2, command=clear_num, style="RedX.TButton")
num_clear_button.grid(row=3, column=1, padx=5)  # Position the button next to the spinbox


date_label = ttk.Label(widgets_frame, text="Date:")
date_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)  # Add padding for spacing
# Date Entry and Button Frame
date_frame = ttk.Frame(widgets_frame)
date_frame.grid(row=5, column=0, sticky="ew" , padx=8 )

# Entry widget to display selected date
date_entry = ttk.Entry(date_frame, state="readonly")  #read-only, so that user can't input date normally
date_entry.pack(side="left", fill="x", expand=True)


# Clear button for date
num_clear_button = ttk.Button(widgets_frame, text="❌", width=2, command=clear_date, style="RedX.TButton")
num_clear_button.grid(row=5, column=1, padx=5)  # Position the button next to the spinbox


# Button to open the calendar popup
date_button = ttk.Button(date_frame, text="📅", width=2, command=lambda: open_calendar(root, date_entry)) #lambda waits for user to finish button click
date_button.pack(side="right")

date_entry.insert(0, "Enter Date:")




search_button = ttk.Button(widgets_frame, text="Search:  ",  command = search_start)
search_button.grid(row=6,column=0, columnspan=2,sticky="nsew",pady=5, padx=8 )

separator = ttk.Separator(widgets_frame)
separator.grid(row=8, column=0, padx=(20, 10), pady=10, sticky="ew")

treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0,column=1, pady=10)
cols = ("Column 1, Column 2, Column 3, Column 4")
treeview = ttk.Treeview(treeFrame, show="headings", column=cols, height=13)
treeview.pack()

# Frame for the filter button (placed below the widgets_frame)
filter_frame = ttk.LabelFrame(frame, text="Other Options:")
filter_frame.grid(row=1, column=0, padx = 10, pady = 10)  # Adjust 'row=1' to place it below widgets_frame

# Filter button inside the new frame
filter_button = ttk.Button(filter_frame, text="Filter", command=open_filter_modal)
filter_button.grid(sticky="nsew",pady=5, padx=8 )  # Center the button in the new frame

root.mainloop()
