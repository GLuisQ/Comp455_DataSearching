'''import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pandas as pd 

# Example data
data = [
    ["Afghanistan", "", "24/03/2020", "Full", "https://www.thestatesman.com/world/afghan-govt-imposes-lockdown-coronavirus-cases-increase-15-1502870945.html"],
    ["Albania", "", "08/03/2020", "Full", "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Albania"],
    ["Algeria", "", "24/03/2020", "Full", "https://www.garda.com/crisis24/news-alerts/325896/algeria-government-implements-lockdown-and-curfew-in-blida-and-algiers-march-23-update-7"],
    ["Andorra", "", "16/03/2020", "Full", "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Andorra"],
    ["Angola", "", "24/03/2020", "Full", "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Angola"],
]

# Sorting state for each column
headers = {
    0: {"text": "Country/Region", "reverse": False},
    1: {"text": "Province", "reverse": False},
    2: {"text": "Date", "reverse": False},
    3: {"text": "Type", "reverse": False},
    4: {"text": "Reference", "reverse": False},
}

# Example data converted to a DataFrame
data = pd.DataFrame(
    {
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
        ],
    }
)

# Ensure Date is in datetime format for better operations
data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y")


# Functions for sorting
def update_treeview(treeview, data):
    """Clears and repopulates the TreeView with updated DataFrame data."""
    for row in treeview.get_children():
        treeview.delete(row)
    for item in data:
        treeview.insert("", "end", values=item)

def sort_treeview(treeview, column_index, reverse):
    """Sorts the TreeView data."""
    global data
    if column_index == 2:  # Date column
        sorted_data = sorted(
            data,
            key=lambda x: datetime.strptime(x[column_index], "%d/%m/%Y") if x[column_index] else datetime.min,
            reverse=reverse
        )
    else:  # Text columns
        sorted_data = sorted(data, key=lambda x: x[column_index], reverse=reverse)

    update_treeview(treeview, sorted_data)
    headers[column_index]["reverse"] = not reverse  # Toggle reverse order

# Functions for calendar
def open_calendar(root, date_entry):
    """Opens a calendar popup for selecting a date."""
    top = tk.Toplevel(root)
    top.title("Select a Date")
    
    from tkcalendar import Calendar  # Import here to avoid dependency issues
    cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy")
    cal.pack(pady=10)
    
    def select_date():
        date_entry.config(state="normal")
        date_entry.delete(0, "end")
        date_entry.insert(0, cal.get_date())
        date_entry.config(state="readonly")
        top.destroy()
    
    ttk.Button(top, text="OK", command=select_date).pack(pady=5)

# Main Application
root = tk.Tk()
root.title("Data Viewer")
style = ttk.Style(root)

#Apply themes (modify paths to match your directory if needed)
root.tk.call("source", "../theme/forest-light.tcl")  # Load light theme
root.tk.call("source", "../theme/forest-dark.tcl")   # Load dark theme
style.theme_use("forest-dark")

# Main frame setup
frame = ttk.Frame(root)
frame.pack(fill="both", expand=True)

treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10)

# Define TreeView columns
cols = ("Country/Region", "Province", "Date", "Type", "Reference")
treeview = ttk.Treeview(treeFrame, show="headings", column=cols, height=13)

# Configure each column
for col_idx, col_name in enumerate(cols):
    treeview.heading(
        col_name,
        text=col_name,
        command=lambda c=col_idx: sort_treeview(treeview, c, headers[c]["reverse"])
    )
    treeview.column(col_name, width=150, anchor="center")

treeview.pack(fill="both", expand=True)

# Populate initial data
update_treeview(treeview, data)

# Widgets for Filters
widgets_frame = ttk.LabelFrame(frame, text="---Filter Data---")
widgets_frame.grid(row=0, column=0, padx=10, pady=10)

# Country Filter
country_label = ttk.Label(widgets_frame, text="Country:")
country_label.grid(row=0, column=0, padx=5, pady=5)

country_entry = ttk.Entry(widgets_frame)
country_entry.grid(row=0, column=1, padx=5, pady=5)

# Date Filter
date_label = ttk.Label(widgets_frame, text="Date:")
date_label.grid(row=1, column=0, padx=5, pady=5)

date_entry = ttk.Entry(widgets_frame, state="readonly")
date_entry.grid(row=1, column=1, padx=5, pady=5)

date_button = ttk.Button(widgets_frame, text="📅", command=lambda: open_calendar(root, date_entry))
date_button.grid(row=1, column=2, padx=5, pady=5)

# Search Button
search_button = ttk.Button(widgets_frame, text="Search", command=lambda: print("Search functionality pending!"))
search_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
'''

'''import pandas as pd
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import threading
import webbrowser

# Sample data
data = pd.DataFrame({
    "Country/Region": ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Canada"],
    "Province": ["", "", "", "", "", ""],
    "Date": ["24/03/2020", "08/03/2020", "24/03/2020", "16/03/2020", "24/03/2020", "24/05/2021"],
    "Type": ["Full", "Full", "Full", "Full", "Full", "Full"],
    "Reference": [
        "https://www.thestatesman.com/world/afghan-govt-imposes-lockdown-coronavirus-cases-increase-15-1502870945.html",
        "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Albania",
        "https://www.garda.com/crisis24/news-alerts/325896/algeria-government-implements-lockdown-and-curfew-in-blida-and-algiers-march-23-update-7",
        "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Andorra",
        "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Angola",
        "https://www.google.ca/"
    ]
})
data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y")

# GUI creation
class App:
    def __init__(self, root):
        self.root = root
        self.treeview = None
        self.country_entry = None
        self.date_entry = None
        self.init_ui()

    #styling of the UI using themes. 
    def init_ui(self):
        # loading of the themes from the source is done here. 
        # using .tcl file type themes. 
        self.root.tk.call("source", "../theme/forest-light.tcl")  # Adjust the path to your .tcl files
        self.root.tk.call("source", "../theme/forest-dark.tcl")
        style = ttk.Style(self.root)
        style.theme_use("forest-dark")  # we chose forest-dark but can choose dark or light. should implement the ability to choose. 

        # treeview: this is what we see on the screen 
        self.treeview = ttk.Treeview(
            self.root, columns=("Country/Region", "Province", "Date", "Type", "Reference"), show="headings"
        )
        #styling, placements
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=150, anchor="center")
        self.treeview.pack(fill="both", expand=True)

        # binding the double-click event to open the link shown in the "Reference" column
        self.treeview.bind("<Double-1>", self.on_double_click)

        # filters section
        filter_frame = ttk.LabelFrame(self.root, text="Filters")
        filter_frame.pack(pady=10, padx=10, fill="x")

        # filter for country
        ttk.Label(filter_frame, text="Country:").grid(row=0, column=0, padx=5, pady=5)
        self.country_entry = ttk.Entry(filter_frame)
        self.country_entry.grid(row=0, column=1, padx=5, pady=5)

        # filter for date 
        ttk.Label(filter_frame, text="Date (dd/mm/yyyy):").grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(filter_frame)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        # search button - and its onclick commands. 
        # onclick --> performs commands entered in the search_data_threaded function. 
        search_button = ttk.Button(filter_frame, text="Search", command=self.search_data_threaded)
        search_button.grid(row=2, column=0, columnspan=2, pady=10)

        # this shows the initial data - if query left empty and search is clicked, brings back original directory 
        self.load_data_threaded()

    #shows beginning screen 
    def load_data_threaded(self):
        threading.Thread(target=self.load_data, daemon=True).start()

    #loads data
    def load_data(self):
        self.treeview.delete(*self.treeview.get_children())
        for _, row in data.iterrows():
            self.treeview.insert("", "end", values=row.tolist())

    # user enters query --> list of countries is searched. 
    # piggy backs off of search_data
    def search_data_threaded(self):
        threading.Thread(target=self.search_data, daemon=True).start()

    #this is our search data function. 
    #goes based off country name or date. 
    def search_data(self):
        country = self.country_entry.get().strip()
        date = self.date_entry.get().strip()
        filtered_data = data.copy()
        #if country in query matches, shows corresponding data. 
        if country:
            filtered_data = filtered_data[
                filtered_data["Country/Region"].str.contains(country, case=False, na=False)
            ]
        #if data in query matches, shows corresponding data. 
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

    #handling the double click options. 
    # we want the link showing up on GUI to be clickable, therefore gave it the double click option in order for it to work. 
    def on_double_click(self, event):
        # get selected item
        item_id = self.treeview.selection()
        if not item_id:
            return

        # retrieve row data
        item = self.treeview.item(item_id[0])
        values = item.get("values", [])
        if len(values) > 4:  # making sure that the "references" column actually exists 
            url = values[4]
            if url.startswith("http"):  # is the URL valid? some variance here because some URLs may not use http. 
                #opens url if valid 
                webbrowser.open(url)
            #doesnt open url if invalid 
            else:
                messagebox.showerror("Invalid URL", "The selected reference is not a valid URL.")
        else:
            messagebox.showerror("Error", "No valid reference link found.")

# start app
root = tk.Tk()
root.title("Data Viewer")
app = App(root)
root.mainloop()
'''