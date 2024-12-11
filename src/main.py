import tkinter as tk
from tkinter import ttk
from calendar_use import open_calendar


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
    # Collect filters from the UI
    filters = {
        "country": country_entry.get().strip() if country_entry.get() != "Country Name" else "",
        "province": province_entry.get().strip() if province_entry.get() != "Province Name" else "",
        "date": date_entry.get().strip() if date_entry.get() != "Enter Date:" else "",
        "date_if": date_if_between.get(),
        "second_date": second_date_entry.get().strip() if date_if_between.get() == "BETWEEN" else ""
    }

    # Apply filters to the sample data
    filtered_data = apply_filters(sample_data, filters)

    # Clear existing rows in the Treeview
    for row in treeview.get_children():
        treeview.delete(row)

    # Populate Treeview with filtered data
    for row in filtered_data:
        treeview.insert("", "end", values=row)

    print("Filters applied:", filters)


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


def apply_filters(data, filters):
    """
    Apply filters dynamically to the dataset.

    Args:
        data (list of tuples): The dataset to filter.
        filters (dict): A dictionary of filter criteria.

    Returns:
        list of tuples: Filtered dataset.
    """
    def match_row(row):
        # Check each filter condition
        if filters.get("country") and filters["country"].lower() not in row[0].lower():
            return False
        if filters.get("province") and filters["province"].lower() not in row[1].lower():
            return False
        
        # Handle date filtering
        if filters.get("date"):
            if filters["date_if"] == "BETWEEN":
                if filters.get("second_date"):
                    if not (filters["date"] <= row[2] <= filters["second_date"]):
                        return False
            elif filters["date_if"] == "IF":
                if filters["date"] != row[2]:
                    return False
            elif filters["date_if"] == "NOT":
                if filters["date"] == row[2]:
                    return False

        # If no filters fail, the row matches
        return True

    return list(filter(match_row, data))


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

# Country field
country_label = ttk.Label(widgets_frame, text="Country:")
country_label.grid(row=0, column=0, pady=2)

country_entry = ttk.Entry(widgets_frame)
country_entry.grid(row=0, column=2, sticky="ew", padx=6, pady=2)
country_entry.insert(0, "Country Name")
country_entry.bind("<FocusIn>", lambda e: country_entry.delete(0, 'end'))

country_clear_button = ttk.Button(widgets_frame, text="X", width=2, command=clear_country, style="RedX.TButton")
country_clear_button.grid(row=0, column=3, padx=6, pady=2)

# Province field
province_label = ttk.Label(widgets_frame, text="Province:")
province_label.grid(row=1, column=0, pady=2)

province_entry = ttk.Entry(widgets_frame)
province_entry.grid(row=1, column=2, sticky="ew", padx=6, pady=2)
province_entry.insert(0, "Province Name")
province_entry.bind("<FocusIn>", lambda e: province_entry.delete(0, 'end'))

province_clear_button = ttk.Button(widgets_frame, text="X", width=2, command=clear_province, style="RedX.TButton")
province_clear_button.grid(row=1, column=3, padx=6, pady=2)

# Date fields
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

date_button = ttk.Button(date_frame, text="📅", width=2, command=lambda: open_calendar(root, date_entry, search_start))
date_button.pack(side="right")

date_clear_button = ttk.Button(widgets_frame, text="X", width=2, command=clear_date, style="RedX.TButton")
date_clear_button.grid(row=3, column=3, padx=5)

second_date_label = ttk.Label(widgets_frame, text="And date:")
second_date_frame = ttk.Frame(widgets_frame)
second_date_entry = ttk.Entry(second_date_frame, state="readonly")
second_date_button = ttk.Button(second_date_frame, text="📅", width=2, command=lambda: open_calendar(root, second_date_entry, search_start))
second_date_clear_button = ttk.Button(widgets_frame, text="❌", width=2, command=clear_second_date, style="RedX.TButton")

# Search button
search_button = ttk.Button(widgets_frame, text="Search", command=search_start)
search_button.grid(row=6, column=0, columnspan=4, pady=10)

# Treeview for displaying data
treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10)

cols = ("Country", "Province", "Date", "Value")
treeview = ttk.Treeview(treeFrame, show="headings", columns=cols, height=10)
treeview.pack(fill="both", expand=True)

# Add headings
for col in cols:
    treeview.heading(col, text=col, anchor="center")
    treeview.column(col, anchor="center")

# Sample data
sample_data = [
    ("USA", "California", "2023-01-01", "100"),
    ("Canada", "Ontario", "2023-02-15", "200"),
    ("USA", "Texas", "2023-03-10", "150"),
    ("Canada", "Quebec", "2023-04-20", "250"),
]

for row in sample_data:
    treeview.insert("", "end", values=row)

root.mainloop()
