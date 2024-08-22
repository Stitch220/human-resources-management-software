import customtkinter as ctk
import my_database as db
import personal as p

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        self.new_entry_btn = ctk.CTkButton(self, text="New Entry", fg_color="green", width=250, font=self.winfo_toplevel().button_font, command=self.winfo_toplevel().new_entry)
        self.new_entry_btn.grid(column=0, row=0, padx=10, pady=10)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Appearance
        ctk.set_appearance_mode('dark')
        self.title('Human-Resource-Management')
        self.geometry('1000x600')
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Fonts
        self.button_font = ctk.CTkFont(
            family="Helvetica",
            size=13
        )

        # MainWindow
        self.main_window = MainWindow(self, fg_color="transparent")
        self.main_window.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")


    def new_entry(self):
        p.Personal()


app = App()
app.mainloop()
