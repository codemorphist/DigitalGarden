import tkinter as tk
from tkinter import ttk


class SmashPlant(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.controller = controller

         # Back button 
        self.back_button = ttk.Button(self, text="Back",
            command=lambda: self.controller.show_frame("Menu"))

        self.configure_widgets()

    def configure_widgets(self):
        self.back_button.grid(row=0, column=0, pady=10, padx=10)

