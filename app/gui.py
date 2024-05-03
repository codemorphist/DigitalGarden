import tkinter as tk
from tkinter import ttk

from plant_generator import Plant, TestPlant
from tools import Color, Vec2, Circle


class PlantGeneratorFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

    def draw(self):
        pass            


class App(tk.Tk):
    def __init__(self):
        super().__init__()

