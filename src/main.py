import tkinter as tk
from tkinter import ttk


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
    print("Search button clicked!")


def toggle_second_date():
    if date_if_between.get() == "BETWEEN":
        second_date_label.grid(row=4, column=0, pady=2)
        second_date_frame.grid(row=4, column=2, sticky="ew", padx=8)
        second_date_entry.pack(side="left", fill="x", expand=True)
        second_date_button.pack(side="right")
        second_date_clear_button.grid(row=4, column=3, padx=5)
    else:
        second_date_label.grid_forget()
        second_date_frame.grid_forget()
        second_date_entry.pack_forget()
        second_date_button.pack_forget()
        second_date_clear_button.grid_forget()


def treeview_sort_column(treeview, col, reverse):
    """Sort the Treeview column data."""
    # Extract data from the column
    data_list = [(treeview.set(child, col), child) for child in treeview.get_children('')]
    try:
        # Try to sort as numbers if possible
        data_list.sort(key=lambda x: float(x[0]), reverse=reverse)
    except ValueError:
        # Otherwise sort as strings
        data_list.sort(key=lambda x: x[0], reverse=reverse)
    # Reorder rows in Treeview
    for index, (_, child) in enumerate(data_list):
        treeview.move(child, '', index)
    # Toggle the sort order for the column
    treeview.heading(col, command=lambda: treeview_sort_column(treeview, col, not reverse))


# Main window
root = tk.Tk()
root.title("Data Viewer")

# Style customization
style = ttk.Style(root)
style.configure("RedX.TButton", foreground="red", font=("Arial", 10, "bold"), padding=5)

# Main frame setup
frame = ttk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Label frame for search functionality
widgets_frame = ttk.LabelFrame(frame, text="---Filter Data---")
widgets_frame.grid(row=0, column=0, padx=5, pady=5)

# Country row
country_label = ttk.Label(widgets_frame, text="Country:")
country_label.grid(row=0, column=0, pady=2)

country_entry = ttk.Entry(widgets_frame)
country_entry.grid(row=0, column=2, sticky="ew", padx=6, pady=2)
country_entry.insert(0, "Country Name")
country_entry.bind("<FocusIn>", lambda e: country_entry.delete(0, 'end'))

country_clear_button = ttk.Button(widgets_frame, text="X", width=2, command=clear_country, style="RedX.TButton")
country_clear_button.grid(row=0, column=3, padx=6, pady=2)

# Province row
province_label = ttk.Label(widgets_frame, text="Province:")
province_label.grid(row=1, column=0, pady=2)

province_entry = ttk.Entry(widgets_frame)
province_entry.grid(row=1, column=2, sticky="ew", padx=6, pady=2)
province_entry.insert(0, "Province Name")
province_entry.bind("<FocusIn>", lambda e: province_entry.delete(0, 'end'))

province_clear_button = ttk.Button(widgets_frame, text="X", width=2, command=clear_province, style="RedX.TButton")
province_clear_button.grid(row=1, column=3, padx=6, pady=2)

# Date row
date_label = ttk.Label(widgets_frame, text="Date:")
date_label.grid(row=3, column=0, pady=2)

date_if_between = ttk.Combobox(widgets_frame, values=["IF", "NOT", "BETWEEN"], state="readonly", width=10)
date_if_between.grid(row=3, column=1, padx=(0, 0), pady=2, sticky="w")
date_if_between.set("IF")
date_if_between.bind("<<ComboboxSelected>>", lambda event: toggle_second_date())

date_frame = ttk.Frame(widgets_frame)
date_frame.grid(row=3, column=2, sticky="ew", padx=8)

date_entry = ttk.Entry(date_frame, state="readonly")
date_entry.pack(side="left", fill="x", expand=True)
date_entry.insert(0, "Enter Date:")

date_button = ttk.Button(date_frame, text="📅", width=2, command=lambda: print("Calendar popup here"))
date_button.pack(side="right")

date_clear_button = ttk.Button(widgets_frame, text="X", width=2, command=clear_date, style="RedX.TButton")
date_clear_button.grid(row=3, column=3, padx=5)

second_date_label = ttk.Label(widgets_frame, text="And date:")
second_date_frame = ttk.Frame(widgets_frame)
second_date_entry = ttk.Entry(second_date_frame, state="readonly")
second_date_button = ttk.Button(second_date_frame, text="📅", width=2, command=lambda: print("Second calendar popup"))
second_date_clear_button = ttk.Button(widgets_frame, text="❌", width=2, command=clear_second_date, style="RedX.TButton")

# Search button
search_button = ttk.Button(widgets_frame, text="Search", command=search_start)
search_button.grid(row=6, column=0, columnspan=4, pady=10)

# Treeview for displaying data
treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10)

cols = ("Column 1", "Column 2", "Column 3", "Column 4")
treeview = ttk.Treeview(treeFrame, show="headings", columns=cols, height=10)
treeview.pack(fill="both", expand=True)

# Add headings with sorting functionality
for col in cols:
    treeview.heading(col, text=col, anchor="center",
                     command=lambda _col=col: treeview_sort_column(treeview, _col, False))
    treeview.column(col, anchor="center")

# Insert sample data
sample_data = [
    ("Item 3", "25", "Data Z", "3.5"),
    ("Item 1", "10", "Data X", "1.5"),
    ("Item 2", "15", "Data Y", "2.5"),
]

for row in sample_data:
    treeview.insert("", "end", values=row)

root.mainloop()
