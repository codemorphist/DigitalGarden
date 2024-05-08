import tkinter as tk
from tkinter import ttk

from plant_generator import Plant
from tools import Color


class GenomTableFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.genom_entries = {}

        self.table_height = 9
        self.table_width = 9
        counter = 0
        for row in range(self.table_height):
            for column in range(self.table_width):
                self.genom_entries[counter] = ttk.Entry(self, width=5)
                self.genom_entries[counter].grid(padx=1, pady=1,
                                                 row=row, column=column)
                counter += 1

        self.import_button = ttk.Button(self, text="Import")
        self.export_button = ttk.Button(self, text="Export")

        self.import_button.grid(row=self.table_height + 5, column=2)
        self.export_button.grid(row=self.table_height + 5, column=6)

        self.plant = None

    def get_plant(self):
        # return TestPlant(10)
        return Plant.random()


class PlantGeneratorFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.canvas_width = 800
        self.canvas_height = 800

        self.canvas = tk.Canvas(master=self, 
                                width=self.canvas_width, 
                                height=self.canvas_height, 
                                bg="lightgray")
        self.canvas.grid(padx=10, pady=10, row=0, column=0, rowspan=10, columnspan=10)

        self.generate_button = tk.Button(master=self, text="Generate", command=self.start_drawing)
        self.generate_button.grid(padx=2, pady=2, row=1, column=11, sticky='nsew')

        self.genom_input = GenomTableFrame(self)
        self.genom_input.grid(row=0, column=11)

    def draw_circle(self, circle):
        x, y, radius = *circle.pos, circle.radius
        color = circle.color.hex
        canvas_center_x = self.canvas_width // 2
        canvas_center_y = self.canvas_height // 2
        x0 = canvas_center_x + x - radius
        y0 = canvas_center_y + y - radius
        x1 = canvas_center_x + x + radius
        y1 = canvas_center_y + y + radius        
        dark = (circle.color + Color(10, 10, 10)).hex
        light= (circle.color - Color(10, 10, 10)).hex
        self.canvas.create_oval(x0, y0, x1, y1, outline=color, fill=color)
        self.canvas.create_oval(x0-1, y0-1, x1-1, y1-1, outline=dark, fill=dark)
        self.canvas.create_oval(x0+1, y0+1, x1+1, y1+1, outline=light, fill=light)

    def start_drawing(self):
        self.canvas.delete("all")
        self.plant = self.genom_input.get_plant()
        self.draw()

    def get_delay(self, agents_count: int) -> int:
        # return 0 
        if agents_count <= 2:
            return 10
        elif agents_count <= 10:
            return 5
        elif agents_count <= 100:
            return 1
        else:
            return 1

    def draw(self):
        if self.plant is None:
            return

        for circle in self.plant.get_circles():
            self.draw_circle(circle)
        if self.plant.is_growing():
            self.after(self.get_delay(len(self.plant.agents)), self.draw)
        else:
            del self.plant
            self.plant = None


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Digital Garden")
        self.geometry("1280x1000")

        self.__create_widgets__()

    def __create_widgets__(self):
        generate_frame = PlantGeneratorFrame(self)
        generate_frame.grid(column=0, row=0)
