import customtkinter as ctk
import my_database as db
import personal as p
import tkinter as tk
import headerBar as hb

data = "name"

db.initialize_database("personal.db", "personal", data)

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Header Bar hinzufügen
        self.header = hb.HeaderBar(self)
        self.header.pack(side="top", fill="x", pady = 20)

        # Button hinzufügen
        self.new_entry_btn = ctk.CTkButton(
            self,
            text="New Entry",
            fg_color="green",
            width=250,
            font=self.winfo_toplevel().button_font,
            command=self.close_and_show_personal
        )
        self.new_entry_btn.pack(pady=10)


    def close_and_show_personal(self):
        self.destroy()  # Schließt das MainWindow

        columns = ["id", "first_name", "last_name", "age", "street", "house", "pzl", "city", "country"]
        self.master.personal_frame = p.Personal(self.master, columns, fg_color="transparent")
        self.master.personal_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Appearance
        ctk.set_appearance_mode('dark')
        self.title('Human-Resource-Management')
        self.geometry('1000x600')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Fonts
        self.button_font = ctk.CTkFont(
            family="Helvetica",
            size=13
        )

        # MainWindow
        self.main_window = MainWindow(self, fg_color="transparent")
        self.main_window.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        # Placeholder for Personal frame
        self.personal_frame = None

app = App()
app.mainloop()
