import logging
import sys

FORMAT = "[%(asctime)s] <%(levelname)-8s> %(filename)s:" \
         "%(lineno)d (%(name)s) : %(message)s" 

logging.basicConfig(
    level=logging.DEBUG,
    filename="digital_garden.log",
    format=FORMAT,
    encoding="utf-8",
    filemode="a"
)

formatter = logging.Formatter(FORMAT)

logger = logging.getLogger(__name__)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

import tkinter as tk
from tkinter import ttk
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

        self.setup_log()
        logger.info("Starting window...")
        self.setup_window()
        
        # Creating a container
        container = tk.Frame(self)  
        container.pack(side="top", fill="both", expand=True) 
  
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
  
        # Setup all frames
        logger.info("Initializing frames...")
        self.frames = {}  
        for F in (Menu, PlantGenerator, SmashPlant, MassSmash):
            frame = F(container, self)
            self.frames[F.__name__] = frame 
            frame.grid(row=0, column=0, sticky="nsew")
        logger.info("Frames initialized!")
  
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

    def setup_log(self):
        self.log_window = LogWindow(self, self)
        self.bind("<F12>", lambda _: self.log_window.state_switch())
        self.log_window.withdraw()

    def quit(self):
        logger.info("Exit from program!")
        self.destroy()


class TextHandler(logging.Handler):
    def __init__(self, text):
        logging.Handler.__init__(self)
        self.setFormatter(formatter)
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state="normal")
            self.text.insert(tk.END, msg + "\n")
            self.text.configure(state="disabled")
            self.text.yview(tk.END)
        self.text.after(0, append)


class LogWindow(tk.Toplevel):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        self.geometry("700x400")
        self.minsize(700, 400)
        self.title("Garden Log")

        self.log_field = tk.Text(self,
                                 state="disabled",
                                 background="black",
                                 foreground="white",
                                 highlightthickness=0)
        self.text_handler = TextHandler(self.log_field)
        logger.addHandler(self.text_handler)

        self.clear_button = ttk.Button(self, text="Clear Log", command=self.clear_log)

        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        self.transient(controller)
        self.configure_widgets()

        self.bind("<F12>", lambda _: self.state_switch())

    def configure_widgets(self):
        self.log_field.pack(fill="both", expand=True, padx=2, pady=2)
        self.clear_button.pack(pady=(0, 5))

    def state_switch(self):
        if self.state() == "normal":
            self.withdraw()
        elif self.state() == "withdrawn":
            self.deiconify()

    def add_message_line(self, message: str):
        self.log_field.configure(state="normal")
        self.log_field.insert("end", message)
        self.log_field.configure(state="disabled")

    def clear_log(self):
        self.log_field.configure(state="normal")
        self.log_field.delete(1.0, "end")
        self.log_field.configure(state="disabled")