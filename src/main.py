import pandas as pd
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import threading
import webbrowser

# Sample data
data = pd.DataFrame({
    "Country/Region": ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola"],
    "Province": ["", "", "", "", ""],
    "Date": ["24/03/2020", "08/03/2020", "24/03/2020", "16/03/2020", "24/03/2020"],
    "Type": ["Full", "Full", "Full", "Full", "Full"],
    "Reference": [
        "https://www.thestatesman.com/world/afghan-govt-imposes-lockdown-coronavirus-cases-increase-15-1502870945.html",
        "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Albania",
        "https://www.garda.com/crisis24/news-alerts/325896/algeria-government-implements-lockdown-and-curfew-in-blida-and-algiers-march-23-update-7",
        "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Andorra",
        "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Angola",
    ]
})
data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y")

# GUI and threading
class App:
    def __init__(self, root):
        self.root = root
        self.treeview = None
        self.country_entry = None
        self.date_entry = None
        self.init_ui()

    def init_ui(self):
        # Load themes
        self.root.tk.call("source", "../theme/forest-light.tcl")  # Adjust the path to your .tcl files
        self.root.tk.call("source", "../theme/forest-dark.tcl")
        style = ttk.Style(self.root)
        style.theme_use("forest-dark")  # Choose "forest-dark" or "forest-light"

        # Create TreeView
        self.treeview = ttk.Treeview(
            self.root, columns=("Country/Region", "Province", "Date", "Type", "Reference"), show="headings"
        )
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=150, anchor="center")
        self.treeview.pack(fill="both", expand=True)

        # Bind double-click event to open the link in the "Reference" column
        self.treeview.bind("<Double-1>", self.on_double_click)

        # Filters
        filter_frame = ttk.LabelFrame(self.root, text="Filters")
        filter_frame.pack(pady=10, padx=10, fill="x")

        # Country filter
        ttk.Label(filter_frame, text="Country:").grid(row=0, column=0, padx=5, pady=5)
        self.country_entry = ttk.Entry(filter_frame)
        self.country_entry.grid(row=0, column=1, padx=5, pady=5)

        # Date filter
        ttk.Label(filter_frame, text="Date (dd/mm/yyyy):").grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(filter_frame)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        # Search button
        search_button = ttk.Button(filter_frame, text="Search", command=self.search_data_threaded)
        search_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Load initial data
        self.load_data_threaded()

    def load_data_threaded(self):
        threading.Thread(target=self.load_data, daemon=True).start()

    def load_data(self):
        self.treeview.delete(*self.treeview.get_children())
        for _, row in data.iterrows():
            self.treeview.insert("", "end", values=row.tolist())

    def search_data_threaded(self):
        threading.Thread(target=self.search_data, daemon=True).start()

    def search_data(self):
        country = self.country_entry.get().strip()
        date = self.date_entry.get().strip()
        filtered_data = data.copy()
        if country:
            filtered_data = filtered_data[
                filtered_data["Country/Region"].str.contains(country, case=False, na=False)
            ]
        if date:
            try:
                filtered_data = filtered_data[
                    filtered_data["Date"] == pd.to_datetime(date, format="%d/%m/%Y")
                ]
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a valid date in dd/mm/yyyy format.")
                return

        self.treeview.delete(*self.treeview.get_children())
        for _, row in filtered_data.iterrows():
            self.treeview.insert("", "end", values=row.tolist())

    def on_double_click(self, event):
        """Open the link in the Reference column when double-clicked."""
        # Get the selected item
        item_id = self.treeview.selection()
        if not item_id:
            return

        # Retrieve the row data
        item = self.treeview.item(item_id[0])
        values = item.get("values", [])
        if len(values) > 4:  # Ensure the "Reference" column exists
            url = values[4]
            if url.startswith("http"):  # Check if the URL is valid
                webbrowser.open(url)
            else:
                messagebox.showerror("Invalid URL", "The selected reference is not a valid URL.")
        else:
            messagebox.showerror("Error", "No valid reference link found.")

# Start the application
root = tk.Tk()
root.title("Data Viewer")
app = App(root)
root.mainloop()



