import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import my_database as db
import headerBar as hb

database = "personal.db"
table = "personal"

class Personal(ctk.CTkFrame):
    def __init__(self, master, columns, **kwargs):
        super().__init__(master, **kwargs)

        self.header = hb.HeaderBar(self)
        self.header.pack(side="top", fill="x", pady=20)

        self.columns = columns

        # Frame for Treeview and Scrollbars
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(expand=True, anchor="nw")
        self.tree_frame.configure(height=0.9, width=0.6 )

        # Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_by(_col, False))
        self.tree.pack(side="left", fill="both", expand=True)

        # Vertical Scrollbar
        self.v_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.v_scrollbar.set)
        self.v_scrollbar.pack(side="right", fill="y")

        # Horizontal Scrollbar
        self.h_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscroll=self.h_scrollbar.set)
        self.h_scrollbar.pack(side="bottom", fill="x")

        self.load_data()
        self.adjust_column_widths()

        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_double_click)

    def load_data(self):
        query = f"SELECT {', '.join(self.columns)} FROM {table}"
        rows = db.execute_query(database, query)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def adjust_column_widths(self):
        max_width = 150  
        min_integer_width = 30  

        for col in self.columns:
            content = [self.tree.heading(col, "text")] + [str(item) for item in self.tree.set("", col)]
            width = max(len(item) for item in content) * 10 + 10  

            is_integer_column = db.get_column_type(database, table, col) == "INTEGER"

            if is_integer_column:
                width = max(width, min_integer_width)
            
            width = min(width, max_width)
            
            self.tree.column(col, width=width)

    def on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if item_id and column:
            current_value = self.tree.item(item_id, "values")[int(column[1:]) - 1]

            entry = ctk.CTkEntry(self.tree)
            entry.place(x=event.x, y=event.y)
            entry.insert(0, current_value)
            entry.focus()

            def save_edit(event):
                new_value = entry.get()
                column_name = self.columns[int(column[1:]) - 1]
                entry_id = self.tree.item(item_id, "values")[0]

                if not self.validate_input(column_name, new_value):
                    messagebox.showerror("Invalid Input", f"Invalid input for column '{column_name}'. Please enter a valid value.")
                    entry.destroy()
                    return

                self.tree.set(item_id, column=column, value=new_value)
                entry.destroy()

                data = {column_name: new_value}
                db.update_entry(database, table, data, entry_id)

            entry.bind("<Return>", save_edit)

            def cancel_edit(event):
                entry.destroy()

            entry.bind("<Escape>", cancel_edit)

    def validate_input(self, column_name, value):
        column_type = db.get_column_type(database, table, column_name)

        if column_type == "INTEGER":
            if value.isdigit() or value == '':
                return True
            else:
                return False
        
        return True

    def sort_by(self, col, reverse):
        
        data = [(self.tree.item(child)["values"], child) for child in self.tree.get_children()]
        
        data.sort(key=lambda x: x[0][self.columns.index(col)], reverse=reverse)
        
        for index, (values, child) in enumerate(data):
            self.tree.move(child, '', index)

        for c in self.columns:
            self.tree.heading(c, command=lambda c=c: self.sort_by(c, not reverse))
        self.tree.heading(col, text=f"{col} {'▲' if reverse else '▼'}", command=lambda: self.sort_by(col, not reverse))
