import general_checks as gc
import customtkinter as ctk
import my_database as db

class MainWindow(ctk.CTkFrame):
    def __intit__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Table and Database Name
        database = "personal.db"
        new_table = "Test"

        # Create the table with only the 'id' column
        db.create_table(database, new_table)

        # Add an entry with dynamic data
        entry_data = {
            "name": "conner",
            "age": "78"
        }
        db.add_entry(database, new_table, entry_data)

        # Read and print the entry
        entry = db.read_single_entry(database, new_table, 1)
        if entry:
            print(f"Entry data: {entry}")

        update_data = {
            "name": "Ottao",
            "street": "8a8"
        }
        db.update_entry(database,new_table,update_data,1)
        entry = db.read_single_entry(database, new_table, 1)
        if entry:
            print(f"Entry data: {entry}")


app = App()
app.mainloop()
