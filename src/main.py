import pandas as pd
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import threading
import webbrowser

#reads the csv database we have containing all the countries and data
def load_countries():
    #read
    try:
        df = pd.read_csv("countries.csv")
        df.columns = df.columns.str.strip().str.replace("/", "_")
        return df  # Return the full DataFrame
    except FileNotFoundError:
        print("countries.csv not found. Ensure the file is in the project directory.")
        return pd.DataFrame()
    except KeyError as e:
        print(f"Missing column in CSV: {e}")
        return pd.DataFrame()

# load data from csv
df = load_countries()

# making sure that required columns are present
if not all(col in df.columns for col in ["Country_Region", "Province", "Date", "Type", "Reference"]):
    raise ValueError("The CSV file must contain the columns: Country/Region, Province, Date, Type, Reference.")

# prepare frame containing data for display
data = df.copy()
data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y", errors="coerce")  # Handle invalid dates

# GUI creation happens here 
class App:
    def __init__(self, root):
        self.root = root
        self.treeview = None
        self.country_entry = None
        self.province_entry = None
        self.date_entry = None
        self.init_ui()

    def init_ui(self):
        # load the themes we want to use
        self.root.tk.call("source", "../theme/forest-light.tcl")  
        self.root.tk.call("source", "../theme/forest-dark.tcl")
        style = ttk.Style(self.root)
        style.theme_use("forest-dark")# we chose forest-dark but can choose dark or light. should implement the ability to choose. 

        # create a frame for the treeview and a scrollbar
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True)

        # scrollbar creation
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # create treeview
        # basic outline of the UI
        self.treeview = ttk.Treeview(
            tree_frame,
            columns=("Country/Region", "State/Province", "Date", "Type", "Reference"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=150, anchor="center")
        self.treeview.pack(fill="both", expand=True)

        # add scrollbar to the frame 
        scrollbar.config(command=self.treeview.yview)

        # this makes the double-click an event that opens the link in the "Reference" column
        self.treeview.bind("<Double-1>", self.on_double_click)

        # filters
        filter_frame = ttk.LabelFrame(self.root, text="Filters")
        filter_frame.pack(pady=10, padx=10, fill="x")

        # country filter
        ttk.Label(filter_frame, text="Country:").grid(row=0, column=0, padx=5, pady=5)
        self.country_entry = ttk.Entry(filter_frame)
        self.country_entry.grid(row=0, column=1, padx=5, pady=5)

        # province filter
        ttk.Label(filter_frame, text="Province:").grid(row=1, column=0, padx=5, pady=5)
        self.province_entry = ttk.Entry(filter_frame)
        self.province_entry.grid(row=1, column=1, padx=5, pady=5)

        # date filter
        ttk.Label(filter_frame, text="Date (dd/mm/yyyy):").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(filter_frame)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # search button
        search_button = ttk.Button(filter_frame, text="Search", command=self.search_data_threaded)
        search_button.grid(row=3, column=0, pady=10)

        # reset button
        reset_button = ttk.Button(filter_frame, text="Reset", command=self.reset_data)
        reset_button.grid(row=3, column=1, pady=10)

        # load initial data
        self.load_data_threaded()

    #loads the threaded data
    def load_data_threaded(self):
        threading.Thread(target=self.load_data, daemon=True).start()

    #takes threaded data and actually shows the rest
    def load_data(self):
        self.treeview.delete(*self.treeview.get_children())
        for _, row in data.iterrows():
            self.treeview.insert("", "end", values=row.tolist())

    #search filter
    def search_data_threaded(self):
        threading.Thread(target=self.search_data, daemon=True).start()

    #this actually does the searching
    def search_data(self):
        country = self.country_entry.get().strip()
        province = self.province_entry.get().strip()
        date = self.date_entry.get().strip()

        filtered_data = data.copy()
        #if country is there, shows it
        if country:
            filtered_data = filtered_data[
                filtered_data["Country_Region"].str.contains(country, case=False, na=False)
            ]
        #if province is there, shows it
        if province:
            filtered_data = filtered_data[
                filtered_data["Province"].str.contains(province, case=False, na=False)
            ]
        #if valid date, shows it
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

    #this is what makes the reset button work
    def reset_data(self):
        self.country_entry.delete(0, tk.END)
        self.province_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.load_data()

    #this is what makes the double click work
    #if user clicks on the country, its corresponding link opens up 
    def on_double_click(self, event):
        # get the selected item
        item_id = self.treeview.selection()
        if not item_id:
            return

        # retrieve the row data
        item = self.treeview.item(item_id[0])
        values = item.get("values", [])
        if len(values) > 4:  # make the "Reference" column exists
            url = values[4]
            if url.startswith("http"):  # check if the url is valid
                webbrowser.open(url)
            else:
                messagebox.showerror("Invalid URL", "The selected reference is not a valid URL.")
        else:
            messagebox.showerror("Error", "No valid reference link found.")


# make the appolication work
root = tk.Tk()
root.title("Data Viewer")
app = App(root)
root.mainloop()
