import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import sqlite3
import my_database as db


class Personal(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
    
        self.title("Personal")
        self.geometry("600x400")

        # Treeview
        self.tree = ttk.Treeview(self, columns=("id", "name", "position"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("position", text="Position")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_data()

        def load_data(self):
            query = "SELECT * FROM personal"
            rows = db.execute_query('personal.db', query)

            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in rows:
                self.tree.insert("", tk.END, values=row)
