# main.py
import tkinter as tk
from tkinter import ttk

from calendar_use import \
    open_calendar  # Import the calendar function from other file


def clear_country():
    country_entry.delete(0, 'end')
def clear_province():
    province_entry.delete(0, 'end')


def clear_date():
    date_entry.config(state="normal")
    date_entry.delete(0, 'end')  # Clears the content of the date entry
    date_entry.config(state="readonly")
def clear_second_date():
    second_date_entry.config(state="normal")
    second_date_entry.delete(0, 'end')
    second_date_entry.config(state="readonly")
def search_start():
    #This is a template.
    print("search_pass")


def open_search_modal():
    modal = tk.Toplevel(root)  # Create a new window
    modal.title("Search Data")
    modal.geometry("400x300")  # Set size of the pop-up window

    search_country_label = ttk.Label(modal, text="Country:")
    search_country_label.grid(row=0, column=0 )  # Minimal padding

    #Start of Country Name Column
    search_country_if_not = ttk.Combobox(modal, values=["IF", "NOT"], state="readonly", width=10)
    search_country_if_not.grid(row=0, column=1, padx=(0, 0), pady=2, sticky="w")
    search_country_if_not.set("IF")

    search_country_entry = ttk.Entry(modal)
    search_country_entry.grid(row=0, column=2, sticky="w", padx=6, pady=2)  # Small padding only at the right edge
    search_country_entry.insert(0, "Country Name")
    search_country_entry.bind("<FocusIn>", lambda e: country_entry.delete(0, 'end'))  # Clear placeholder on focus

    # Clear button for name
    search_country_clear_button = ttk.Button(modal, text="❌", width=2, command=clear_country, style="RedX.TButton")
    search_country_clear_button.grid(row=0, column=3, padx=20)  # Position the button next to the spinbox

    #to add everything else here.
    




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
widgets_frame = ttk.LabelFrame(frame, text="---Filter Data---")
widgets_frame.grid(row=0, column=0)
widgets_frame.grid(padx=5, pady=5)  # Minimal padding around the frame
# Configure grid columns in widgets_frame
widgets_frame.grid_columnconfigure(0, weight=0)  # For labels (Country, Province, Date)
widgets_frame.grid_columnconfigure(1, weight=0)  # For comboboxes (IF, NOT)
widgets_frame.grid_columnconfigure(2, weight=1)  # For entry widgets (Country Name, Province Name)
widgets_frame.grid_columnconfigure(3, weight=0)  # For clear buttons

# Make sure rows have appropriate configurations if you have more dynamic content
widgets_frame.grid_rowconfigure(3, weight=1)  # For date row, adjust as needed



country_label = ttk.Label(widgets_frame, text="Country:")
country_label.grid(row=0, column=0 )  # Minimal padding

#Start of Country Name Column
country_if_not = ttk.Combobox(widgets_frame, values=["IF", "NOT"], state="readonly", width=10)
country_if_not.grid(row=0, column=1, padx=(0, 0), pady=2, sticky="w")
country_if_not.set("IF")

country_entry = ttk.Entry(widgets_frame)
country_entry.grid(row=0, column=2, sticky="w", padx=6, pady=2)  # Small padding only at the right edge
country_entry.insert(0, "Country Name")
country_entry.bind("<FocusIn>", lambda e: country_entry.delete(0, 'end'))  # Clear placeholder on focus

# Clear button for name
country_clear_button = ttk.Button(widgets_frame, text="❌", width=2, command=clear_country, style="RedX.TButton")
country_clear_button.grid(row=0, column=3, padx=6)  # Position the button next to the spinbox
#End  of Country Name Column

#Start of Province Name Column
province_label = ttk.Label(widgets_frame, text="Province:")
province_label.grid(row=1, column=0, )  # Minimal padding


province_if_not = ttk.Combobox(widgets_frame, values=["IF", "NOT"], state="readonly", width=10)
province_if_not.grid(row=1, column=1, padx=(0, 0), pady=2, sticky="w")
province_if_not.set("IF")

province_entry = ttk.Entry(widgets_frame)
province_entry.grid(row=1, column=2, sticky="w", padx=6, pady=2)  # Small padding only at the right edge
province_entry.insert(0, "Province Name")
province_entry.bind("<FocusIn>", lambda e: province_entry.delete(0, 'end'))  # Clear placeholder on focus

# Clear button for province
province_clear_button = ttk.Button(widgets_frame, text="❌", width=2, command=clear_province, style="RedX.TButton")
province_clear_button.grid(row=1, column=3, padx=6)  # Position the button next to the spinbox

#End of Province Column


#Start of Date Column
date_label = ttk.Label(widgets_frame, text="Date:")
date_label.grid(row=3, column=0, pady = 2 )  # Add padding for spacing


date_if_between = ttk.Combobox(widgets_frame, values=["IF", "NOT", "BETWEEN"], state="readonly", width=10)
date_if_between.grid(row=3, column=1, padx=(0, 0), pady=2, sticky="w")
date_if_between.set("IF")


# Date Entry and Button Frame
date_frame = ttk.Frame(widgets_frame)
date_frame.grid(row=3, column=2, sticky="ew", padx=8)
# Entry widget to display selected date
date_entry = ttk.Entry(date_frame, state="readonly")  #read-only, so that user can't input date normally
date_entry.pack(side="left", fill="x", expand=True)

# Clear button for date
date_clear_button = ttk.Button(widgets_frame, text="❌", width=2, command=clear_date, style="RedX.TButton")
date_clear_button.grid(row=3, column=3, padx=5)  # Position the button next to the spinbox


# Button to open the calendar popup
date_button = ttk.Button(date_frame, text="📅", width=2, command=lambda: open_calendar(root, date_entry)) #lambda waits for user to finish button click
date_button.pack(side="right")

date_entry.insert(0, "Enter Date:")

date_condition_value = "IF"
date_if_between.bind("<<ComboboxSelected>>", lambda event: date_condition_value == "BETWEEN" if date_if_between.get() == "BETWEEN" else None)

second_date_label = ttk.Label(widgets_frame, text="And date:")
second_date_label.grid(row=5, column=0, pady = 2 )  # Add padding for spacing
second_date_label.grid_forget()
second_date_frame = ttk.Frame(widgets_frame)
second_date_frame.grid(row=4, column=2, sticky="ew", padx=8)
second_date_frame.grid_forget()
# Entry widget to display selected date
second_date_entry = ttk.Entry(second_date_frame, state="readonly")  #read-only, so that user can't input date normally
second_date_entry.pack(side="left", fill="x", expand=True)
#second_date_entry.pack_forget()
#Clear button for date
second_date_clear_button = ttk.Button(widgets_frame, text="❌", width=2, command=clear_second_date, style="RedX.TButton")
second_date_clear_button.grid(row=4, column=3, padx=5)  # Position the button next to the spinbox
second_date_clear_button.grid_forget()
second_date_entry.insert(0, "Enter Date:")


# Button to open the calendar popup
second_date_button = ttk.Button(second_date_frame, text="📅", width=2, command=lambda: open_calendar(root, second_date_entry)) #lambda waits for user to finish button click
second_date_button.pack(side="right")
#second_date_button.pack_forget()


date_if_between.bind("<<ComboboxSelected>>", lambda event: toggle_second_date())

def toggle_second_date():
    # Check if the selected value is 'BETWEEN'
    if date_if_between.get() == "BETWEEN":
        # Show second date fields
        second_date_label.grid(row=4, column=0, pady=2)  # Show second date label in row 4
        second_date_frame.grid(row=4, column=2, sticky="ew", padx=8)  # Show second date entry in row 4
        second_date_entry.pack(side="left", fill="x", expand=True)  # Show second date entry
        second_date_button.pack(side="right")  # Show second date button
        second_date_clear_button.grid(row=4, column=3, padx=5)  # Show second date clear button in row 4
    else:
        # Hide second date fields if not 'BETWEEN'
        second_date_label.grid_forget()  # Hide second date label
        second_date_frame.grid_forget()  # Hide second date entry frame
        second_date_entry.pack_forget()  # Hide second date entry
        second_date_button.pack_forget()  # Hide second date button
        second_date_clear_button.grid_forget()  # Hide second date clear button
        

search_button = ttk.Button(widgets_frame, text="Search:  ",  command = search_start)
search_button.grid(row=6,column=0, columnspan=4,sticky="nsew",pady=5, padx=8 )

treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0,column=1, pady=10)
cols = ("Column 1, Column 2, Column 3, Column 4")
treeview = ttk.Treeview(treeFrame, show="headings", column=cols, height=13)
treeview.pack()

# Frame for the filter button (placed below the widgets_frame)
filter_frame = ttk.LabelFrame(frame, text="Other Options:")
filter_frame.grid(row=1, column=0, padx = 10, pady = 10)  # Adjust 'row=1' to place it below widgets_frame

# Filter button inside the new frame
filter_button = ttk.Button(filter_frame, text="Search Data", command=open_search_modal)
filter_button.grid(sticky="nsew",pady=5, padx=8 )  # Center the button in the new frame




root.mainloop()
