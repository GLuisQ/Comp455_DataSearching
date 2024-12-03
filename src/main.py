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
root = tk.Tk()

def search_start():
    #This is a template.
    print("search_pass")
# Apply custom themes (light and dark)
style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")  # Load light theme
root.tk.call("source", "forest-dark.tcl")   # Load dark theme
style.theme_use("forest-light")              # Set active theme to dark


style.configure("RedX.TButton", 
    background="red",       # Set the background to red
    foreground="red",     # Set the text (X) to white
    font=("Arial", 10, "bold"),
    padding=5)              # Add some padding around the button text

root.title("Data Viewer")
# Main frame setup
frame = ttk.Frame(root)
frame.pack()

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
name_clear_button.grid(row=1, column=1, padx=5)  # Position the button next to the entry


age_label = ttk.Label(widgets_frame, text="Age:")
age_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)  # Add padding for spacing
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
date_clear_button = ttk.Button(date_frame, text="❌", width=2, command=clear_date, style="RedX.TButton")
date_clear_button.pack(side="right" , padx=5)  # Position the button next to the date entry


# Button to open the calendar popup
date_button = ttk.Button(date_frame, text="📅", width=2, command=lambda: open_calendar(root, date_entry)) #lambda waits for user to finish button click
date_button.pack(side="right")

date_entry.insert(0, "Enter Date:")



search_button = ttk.Button(widgets_frame, text="Search",  command = search_start)
search_button.grid(row=6,column=0, sticky="nsew",pady=5, padx=8 )

separator = ttk.Separator(widgets_frame)
separator.grid(row=7, column=0, padx=(20, 10), pady=10, sticky="ew")

treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0,column=1, pady=10)
cols = ("Column 1, Column 2, Column 3, Column 4")
treeview = ttk.Treeview(treeFrame, show="headings", column=cols, height=13)
treeview.pack()
root.mainloop()
