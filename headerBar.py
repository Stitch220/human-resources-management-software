import customtkinter as ctk

class HeaderBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(height=master.winfo_screenheight() * 0.04, fg_color="grey")

        self.pack(fill="x")