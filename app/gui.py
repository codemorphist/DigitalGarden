import tkinter as tk
from tkinter import ttk
import turtle

from plant_generator import Plant, TestPlant
from tools import Color, Vec2, Circle


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

    def get_plant(self):
        return TestPlant(10)


class PlantGeneratorFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.canvas = tk.Canvas(master=self, width=800, height=800)
        self.canvas.grid(padx=10, pady=10, row=0, column=0, rowspan=10, columnspan=10)
        self.canvas_turtle = turtle.RawTurtle(self.canvas)

        self.generate_button = tk.Button(master=self,
                                         text="Generate",
                                         command=self.draw)
        self.generate_button.grid(padx=2,
                                  pady=2,
                                  row=1,
                                  column=11,
                                  sticky='nsew')

        self.genom_input = GenomTableFrame(self)
        self.genom_input.grid(row=0, column=11)

    def draw_circle(self, circle: Circle):
        """

        This Circle method draws a given circle with a given turtle,
        which is thought as tied to a specific canvas; the parameters of
        the drawn circle match those of the Object.

        """
        self.canvas_turtle.speed(0)
        # turtle.colormode(255)
        self.canvas_turtle.penup()
        self.canvas_turtle.goto(*circle.pos)
        self.canvas_turtle.forward(circle.radius)
        self.canvas_turtle.left(90)
        self.canvas_turtle.pendown()
        # canvas_turtle.pencolor(self.color.rgb)
        self.canvas_turtle.circle(circle.radius)
        self.canvas_turtle.penup()
        self.canvas_turtle.goto(*circle.pos)

    def draw(self):
        """
        Draws the TestPlant circles
        """
        test_plant = self.genom_input.get_plant()
        while test_plant.is_growing():
            for circle in test_plant.get_circles():
                self.draw_circle(circle)



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Digital Garden")
        self.geometry("1280x900")

        self.__create_widgets__()

    def __create_widgets__(self):
        generate_frame = PlantGeneratorFrame(self)
        generate_frame.grid(column=0, row=0)
