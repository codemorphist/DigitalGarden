import tkinter as tk
from generator_frame import PlantGenerator
from menu_frame import Menu
from smash_plant import SmashPlant
from mass_smash_frame import MassSmash


class RootWindow(tk.Tk):
    """
    Root window of application
    """
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        self.setup_window()
         
        # Creating a container
        container = tk.Frame(self)  
        container.pack(side="top", fill="both", expand=True) 
  
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
  
        # Setup all frames
        self.frames = {}  
        for F in (Menu, PlantGenerator, SmashPlant, MassSmash):
            frame = F(container, self)
            self.frames[F.__name__] = frame 
            frame.grid(row=0, column=0, sticky="nsew")
  
        # Show Menu Frame
        self.show_frame("Menu")

    def setup_window(self):
        """
        Set title ans size of window
        """
        self.title("Digital Garden")

        self.geometry("1420x1000")
        self.minsize(1024, 512)
  
    def show_frame(self, frame_name: str):
        """
        Display frame passed by parameter
        """
        frame = self.frames[frame_name]
        frame.tkraise()

    def quit(self):
        self.destroy()
