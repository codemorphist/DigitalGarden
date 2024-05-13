import tkinter as tk
from tkinter import ttk
from generator_frame import PlantGenerator


class Menu(ttk.Frame):
    def __init__(self, containter, controller):
        super().__init__(containter)
         
        self.generate_btn = ttk.Button(self, text="Generate Plant",
        command = lambda: controller.show_frame(PlantGenerator))

        self.configure_widgets()
     
    def configure_widgets(self):
        """
        Self-explanatory
        """
        self.generate_btn.grid(row=1, column=1, padx=10, pady=10)
  
