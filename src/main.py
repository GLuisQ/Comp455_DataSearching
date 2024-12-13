import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser

# Load CSV data into SQLite
def create_database():
    conn = sqlite3.connect("countries.db")
    cursor = conn.cursor()

    # Create FTS5 virtual table
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS countries USING fts5(
            Country_Region, Province, Date, Type, Reference
        )
    """)
    conn.commit()

    # Insert data into FTS table if empty
    cursor.execute("SELECT COUNT(*) FROM countries")
    if cursor.fetchone()[0] == 0:
        df = pd.read_csv("countries.csv")
        df.columns = df.columns.str.strip().str.replace("/", "_")
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce").dt.strftime('%Y-%m-%d')
        df.to_sql("countries", conn, if_exists="append", index=False)
        print("Data successfully loaded into the FTS table.")
    else:
        print("FTS table already initialized.")

    # Create auxiliary table for indexing Date column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries_aux AS
        SELECT rowid AS id, Date FROM countries
    """)
    conn.commit()

    # Create an index on the Date column in the auxiliary table
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date_aux ON countries_aux(Date)")
    conn.commit()
    print("Index on 'Date' column created in auxiliary table (if it didn't already exist).")
    conn.close()

# GUI Application
class App:
    def __init__(self, root, db_path="countries.db"):
        self.root = root
        self.db_path = db_path
        self.treeview = None
        self.country_entry = None
        self.province_entry = None
        self.date_entry = None
        self.init_ui()

    def init_ui(self):
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.treeview = ttk.Treeview(
            tree_frame,
            columns=("Country/Region", "State/Province", "Date", "Type", "Reference"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col, command=lambda _col=col: self.sort_treeview(_col, False))
            self.treeview.column(col, width=150, anchor="center")
        self.treeview.pack(fill="both", expand=True)

        scrollbar.config(command=self.treeview.yview)
        self.treeview.bind("<Double-1>", self.on_double_click)
        self.root.bind("<Return>", lambda event=None: self.search_data_threaded())

        filter_frame = ttk.LabelFrame(self.root, text="Filters")
        filter_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(filter_frame, text="Country:").grid(row=0, column=0, padx=5, pady=5)
        self.country_entry = ttk.Entry(filter_frame)
        self.country_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Province:").grid(row=1, column=0, padx=5, pady=5)
        self.province_entry = ttk.Entry(filter_frame)
        self.province_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Date (yyyy-mm-dd):").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(filter_frame)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        search_button = ttk.Button(filter_frame, text="Search", command=self.search_data_threaded)
        search_button.grid(row=3, column=0, pady=10)

        reset_button = ttk.Button(filter_frame, text="Reset", command=self.reset_data)
        reset_button.grid(row=3, column=1, pady=10)

        self.load_data_threaded()

    def sort_treeview(self, col, reverse):
        items = [(self.treeview.set(k, col), k) for k in self.treeview.get_children("")]
        items.sort(reverse=reverse, key=lambda t: t[0].lower() if isinstance(t[0], str) else t[0])

        for index, (_, k) in enumerate(items):
            self.treeview.move(k, "", index)

        self.treeview.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def search_data_threaded(self):
        threading.Thread(target=self.search_data, daemon=True).start()

    def search_data(self):
        country = self.country_entry.get().strip()
        province = self.province_entry.get().strip()
        date = self.date_entry.get().strip()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build SQL query dynamically
        query = "SELECT rowid, * FROM countries WHERE 1=1"
        params = []

        # Full-text search for country and province
        if country:
            query += " AND Country_Region MATCH ?"
            params.append(country)
        if province:
            query += " AND Province MATCH ?"
            params.append(province)

        # Auxiliary table query for Date
        if date:
            date_query = """
                SELECT id FROM countries_aux WHERE Date = ?
            """
            cursor.execute(date_query, [date])
            date_ids = cursor.fetchall()
            if date_ids:
                query += f" AND rowid IN ({','.join(str(id[0]) for id in date_ids)})"
            else:
                query += " AND 1=0"  # No match found

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        self.treeview.delete(*self.treeview.get_children())
        for row in results:
            item_id = self.treeview.insert("", "end", values=row[1:])  # Skip the rowid
            self.treeview.item(item_id, tags="highlight")

        self.treeview.tag_configure("highlight", background="#FFFF99")

    def reset_data(self):
        self.country_entry.delete(0, tk.END)
        self.province_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.load_data_threaded()

    def load_data_threaded(self):
        threading.Thread(target=self.load_data, daemon=True).start()

    def load_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM countries")
        results = cursor.fetchall()
        conn.close()

        self.treeview.delete(*self.treeview.get_children())
        for row in results:
            self.treeview.insert("", "end", values=row)

    def on_double_click(self, event):
        item_id = self.treeview.selection()
        if not item_id:
            return

        item = self.treeview.item(item_id[0])
        values = item.get("values", [])
        if len(values) > 4:
            url = values[4]
            if url.startswith("http"):
                webbrowser.open(url)
            else:
                messagebox.showerror("Invalid URL", "The selected reference is not a valid URL.")
        else:
            messagebox.showerror("Error", "No valid reference link found.")

# Run the application
create_database()
root = tk.Tk()
root.title("Data Viewer with SQLite")
app = App(root)
root.mainloop()
