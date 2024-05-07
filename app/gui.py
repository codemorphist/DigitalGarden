import tkinter as tk
from tkinter import ttk
import turtle

from plant_generator import Plant, TestPlant
from tools import Color, Vec2, Circle


class UserFrame(ttk.Frame):
    """
    Contains the User side of the interface, i.e.
    the buttons and the genome input table
    """
    def __init__(self, container):
        super().__init__(container)

        self.table_height = 9
        self.table_width = 9

        for row in range(self.table_height):
            self.rowconfigure(row, weight = 1)
        for column in range(self.table_width):
            self.columnconfigure(column, weight = 1)

        self.rowconfigure(self.table_height, weight = 5)
        self.rowconfigure(self.table_height + 1, weight = 5)

        """
        In the above, the "weight" parameter seems 
        to have no impact on the size of the buttons.
        Leave as it is, but fix later with styling.
        """

        self.genom_entries = {}
        counter = 0

        for row in range(self.table_height):
            for column in range(self.table_width):
                self.genom_entries[counter] = ttk.Entry(self, width=5)
                self.genom_entries[counter].grid(row = row,
                                                 column = column,
                                                 padx = 5,
                                                 pady = 5)
                counter += 1

        self.import_button = ttk.Button(self, text = "Import")
        self.export_button = ttk.Button(self, text = "Export")
        self.random_button = ttk.Button(self, text = "Random")
        self.generate_button = ttk.Button(self, text = "Generate Plant")

        self.import_button.grid(row = self.table_height,
                                column = 0,
                                columnspan = 3,
                                sticky = "nsew",
                                padx = 5,
                                pady = 10)
        self.random_button.grid(row = self.table_height,
                                column = 3,
                                columnspan = 3,
                                sticky = "nsew",
                                padx = 5,
                                pady = 10)
        self.export_button.grid(row = self.table_height,
                                column = 6,
                                columnspan = 3,
                                sticky = "nsew",
                                padx = 5,
                                pady = 10)
        self.generate_button.grid(row = self.table_height + 1,
                                column = 0,
                                columnspan = 9,
                                sticky = "nsew",
                                padx = 5)

    def get_plant(self):
        return TestPlant(10)

class PlantFrame(ttk.Frame):
    """
    Contains the canvas where the plant is drawn
    """
    def __init__(self, container):
        super().__init__(container)

        self.canvas = tk.Canvas(master=self, width=800, height=800)
        self.canvas.grid(padx=10, pady=10, row=0, column=0, rowspan=10, columnspan=10)
        self.canvas_turtle = turtle.RawTurtle(self.canvas)

        # self.genom_input = self.master.user_frame
        self.genom_input = None

    def draw_circle(self, circle: Circle):
        """
        This Circle method draws a given circle using the turtle
        defined herein
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
    """
    Main application window
    """
    def __init__(self):
        super().__init__()

        self.title("Digital Garden")
        self.geometry("1280x900")
        self.minsize(1024, 512)

        self.__create_widgets__()


    def __create_widgets__(self):
        """
        Self-explanatory
        """
        self.plant_frame = PlantFrame(self)
        self.user_frame = UserFrame(self)

        self.plant_frame.genom_input = self.user_frame
        self.user_frame.generate_button.configure(command = self.plant_frame.draw)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 1)

        self.plant_frame.grid(column = 0, row = 0, padx = 20, pady = 20)
        self.user_frame.grid(column = 1, row = 0, padx = 20, pady = 20)


