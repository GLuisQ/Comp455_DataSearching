import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser

# load CSV data into sqlite
def create_database():
    conn = sqlite3.connect("countries.db")
    cursor = conn.cursor()

    # create fts5 virtual table for full-text search
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS countries USING fts5(
            Country_Region, Province, Date, Type, Reference
        )
    """)
    conn.commit()

    # check if data already exists in the fts5 table
    cursor.execute("SELECT COUNT(*) FROM countries")
    # read csv file, clean it, and load data into the table if it's empty
    if cursor.fetchone()[0] == 0:
        df = pd.read_csv("countries.csv")
        # clean up column names by stripping spaces and replacing '/' with '_'
        df.columns = df.columns.str.strip().str.replace("/", "_")
        # convert Date column to a consistent 'YYYY-MM-DD' format
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce").dt.strftime('%Y-%m-%d')
        # append the cleaned data into the fts5 table
        df.to_sql("countries", conn, if_exists="append", index=False)
        print("Data successfully loaded into the FTS table.")
    else:
        print("FTS table already initialized.")

    # create an auxiliary table to index the Date column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries_aux AS
        SELECT rowid AS id, Date FROM countries
    """)
    conn.commit()

    # create an index on the Date column in the auxiliary table for faster queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date_aux ON countries_aux(Date)")
    conn.commit()
    print("Index on 'Date' column created in auxiliary table (if it didn't already exist).")
    conn.close()


# gui application for displaying and interacting with database data
class App:
    def __init__(self, root, db_path="countries.db"):
        self.root = root
        self.db_path = db_path
        self.treeview = None
        self.country_entry = None
        self.province_entry = None
        self.date_entry = None
        self.init_ui()  # initialize the user interface components

    def init_ui(self):
        # create a frame to hold the treeview and its scrollbar
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True)

        # create a vertical scrollbar for the treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # create the treeview widget to display data
        self.treeview = ttk.Treeview(
            tree_frame,
            columns=("Country/Region", "State/Province", "Date", "Type", "Reference"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        for col in self.treeview["columns"]:
            # set column headings and allow sorting by clicking on them
            self.treeview.heading(col, text=col, command=lambda _col=col: self.sort_treeview(_col, False))
            self.treeview.column(col, width=150, anchor="center")
        self.treeview.pack(fill="both", expand=True)

        # connect the scrollbar to the treeview
        scrollbar.config(command=self.treeview.yview)

        # bind double-click events for opening links
        self.treeview.bind("<Double-1>", self.on_double_click)
        # bind the return key to trigger a search
        self.root.bind("<Return>", lambda event=None: self.search_data_threaded())

        # create a filter frame for user inputs
        filter_frame = ttk.LabelFrame(self.root, text="Filters")
        filter_frame.pack(pady=10, padx=10, fill="x")

        # create a filter input for country
        ttk.Label(filter_frame, text="Country:").grid(row=0, column=0, padx=5, pady=5)
        self.country_entry = ttk.Entry(filter_frame)
        self.country_entry.grid(row=0, column=1, padx=5, pady=5)

        # create a filter input for province
        ttk.Label(filter_frame, text="Province:").grid(row=1, column=0, padx=5, pady=5)
        self.province_entry = ttk.Entry(filter_frame)
        self.province_entry.grid(row=1, column=1, padx=5, pady=5)

        # create a filter input for date
        ttk.Label(filter_frame, text="Date (yyyy-mm-dd):").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(filter_frame)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # create a button to trigger search functionality
        search_button = ttk.Button(filter_frame, text="Search", command=self.search_data_threaded)
        search_button.grid(row=3, column=0, pady=10)

        # create a button to reset filters and reload data
        reset_button = ttk.Button(filter_frame, text="Reset", command=self.reset_data)
        reset_button.grid(row=3, column=1, pady=10)

        # load the data when the application starts
        self.load_data_threaded()

    def sort_treeview(self, col, reverse):
        # sort the treeview by a specific column
        items = [(self.treeview.set(k, col), k) for k in self.treeview.get_children("")]
        items.sort(reverse=reverse, key=lambda t: t[0].lower() if isinstance(t[0], str) else t[0])

        # rearrange the items in sorted order
        for index, (_, k) in enumerate(items):
            self.treeview.move(k, "", index)

        # toggle sorting direction for the next click
        self.treeview.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def search_data_threaded(self):
        # run the search functionality in a separate thread
        threading.Thread(target=self.search_data, daemon=True).start()

    def search_data(self):
        # get filter inputs
        country = self.country_entry.get().strip()
        province = self.province_entry.get().strip()
        date = self.date_entry.get().strip()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # dynamically build the SQL query
        query = "SELECT rowid, * FROM countries WHERE 1=1"
        params = []

        # add full-text search conditions for country and province
        if country:
            query += " AND Country_Region MATCH ?"
            params.append(country)
        if province:
            query += " AND Province MATCH ?"
            params.append(province)

        # query auxiliary table for date filtering
        if date:
            date_query = """
                SELECT id FROM countries_aux WHERE Date = ?
            """
            cursor.execute(date_query, [date])
            date_ids = cursor.fetchall()
            if date_ids:
                query += f" AND rowid IN ({','.join(str(id[0]) for id in date_ids)})"
            else:
                query += " AND 1=0"  # no matches found

        # execute the final query
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        # update the treeview with the results
        self.treeview.delete(*self.treeview.get_children())
        for row in results:
            item_id = self.treeview.insert("", "end", values=row[1:])  # skip the rowid
            self.treeview.item(item_id, tags="highlight")

        # highlight matching rows
        self.treeview.tag_configure("highlight", background="#FFFF99")

    def reset_data(self):
        # clear all filter inputs and reload data
        self.country_entry.delete(0, tk.END)
        self.province_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.load_data_threaded()

    def load_data_threaded(self):
        # run the load_data function in a separate thread
        threading.Thread(target=self.load_data, daemon=True).start()

    def load_data(self):
        # load all data from the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM countries")
        results = cursor.fetchall()
        conn.close()

        # populate the treeview with the data
        self.treeview.delete(*self.treeview.get_children())
        for row in results:
            self.treeview.insert("", "end", values=row)

    def on_double_click(self, event):
        # handle double-click events to open a reference link
        item_id = self.treeview.selection()
        if not item_id:
            return

        # get the selected item's data
        item = self.treeview.item(item_id[0])
        values = item.get("values", [])
        if len(values) > 4:
            url = values[4]
            # open the URL if it's valid
            if url.startswith("http"):
                webbrowser.open(url)
            else:
                messagebox.showerror("Invalid URL", "The selected reference is not a valid URL.")
        else:
            messagebox.showerror("Error", "No valid reference link found.")

# run the application
create_database()
root = tk.Tk()
root.title("Data Viewer with SQLite")
app = App(root)
root.mainloop()
