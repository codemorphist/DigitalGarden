import tkinter as tk
from tkinter import ttk


class DrawPlantFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.canvas_width = 600
        self.canvas_heigth = 600

        self.canvas = tk.Canvas(self, 
                                width=self.canvas_width,
                                height=self.canvas_heigth,
                                bg="white")
        self.start_button = tk.Button(self,
                                      text="Start", height=2,
                                      command=self.start_drawing)

        self.canvas.grid(row=0, column=0)
        self.start_button.grid(row=1, column=0, sticky="ew")

    def start_drawing(self):
        pass


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_window()
        self.setup_widgets()

    def setup_window(self):
        """
        Set title ans size of window
        """
        self.title("Async Drawing")

        self.geometry("1280x800")

    def setup_widgets(self):
        """
        Setup frames with plants 
        """
        self.plant1 = DrawPlantFrame(self) 
        self.plant2 = DrawPlantFrame(self)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.plant1.grid(row=0, column=0, padx=10, pady=10)
        self.plant2.grid(row=0, column=1, padx=10, pady=10)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
