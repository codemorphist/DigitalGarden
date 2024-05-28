import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
from idlelib.tooltip import Hovertip
from dataclasses import astuple
from colorsys import hsv_to_rgb
from copy import deepcopy

from PIL import Image, ImageDraw, ImageTk

from plant_generator import Plant, PlantGenom
from tools import Circle, Color, Vec2
from generator_frame import PlantFrame

from fsm import MethodConfig


Config = MethodConfig()


class ParentUserFrame(ttk.Frame):
    """
    This frame realises the functionality for the import and
    showing of the parent plants (i.e. the left-most and the
    right-most frames respectively); contains the "Import"
    and "Show" buttons
    """
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self.import_button = ttk.Button(self, text="Import",
                                        command=self.genome_unpack)
        self.show_button = ttk.Button(self, text="Show",
                                      command=controller.plant_frame.start_drawing)

        self.plant_genome = PlantGenom.empty()
        self.configure_widgets()

    def configure_widgets(self):
        self.import_button.pack(padx=10, pady=5)
        self.import_tip = Hovertip(self.import_button, text=f"Import the genome (.txt) \n"
                                                            f"of parent {self.controller.parent_number}")

        self.show_button.pack(padx=10, pady=5)
        self.show_tip = Hovertip(self.show_button, text=f"Generate parent {self.controller.parent_number}")
    
    def genome_unpack(self):
        """
        The function that realises the "Import" function through
        the file dialogue opener
        """
        try:
            filename = askopenfilename()
            if not filename:  # Exception when user has not chosen any file
                return
            with open(filename) as file:
                self.plant_genome = PlantGenom.import_genom(file.read())

            messagebox.showinfo("Message", "Genome imported successfully!")
        except:
            messagebox.showerror("Error", "Import attempted with an invalid genome:\n"
                                          "The genome has to be a .txt file with a 20x9 table of \n"
                                          "integer inputs separated by spaces")
    def get_plant(self) -> Plant:
        start_pos = Vec2(0, 180)
        plant = Plant(self.plant_genome, start_pos)
        return plant


class HeirUserFrame(ttk.Frame):
    """
    This frame contains all the buttons that control what will be
    drawn on the middle canvas; contains the "Method", "Generate",
    "Export" and "Save" buttons
    """
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        """
        This identifier can be changed by the User through
        the "Method" dialogue window; this sets the way
        in which the parent genomes are to be smashed
        """
        self.plant_genome = PlantGenom.empty()

        self.method_button = ttk.Button(self,
                                        text="Method",
                                        command=self.open_method_settings)
        self.generate_button = ttk.Button(self,
                                          text="Generate",
                                          command=self.controller.plant_frame.start_drawing)
        self.export_button = ttk.Button(self,
                                        text="Export",
                                        command=self.genome_pack)
        self.save_button = ttk.Button(self,
                                      text="Save",
                                      command=self.save_plant_as)

        self.configure_widgets()

    def set_smashed_genome(self):
        parent_1 = self.controller.controller.parent_frame_1.user_frame.plant_genome
        parent_2 = self.controller.controller.parent_frame_2.user_frame.plant_genome
        self.plant_genome = Config.smash(parent_1, parent_2)

    def genome_pack(self):
        """
        The function that realises the "Export" function through
        the file dialogue opener
        """
        try:
            host_file = asksaveasfilename(filetypes=[("Text file", "*.txt")],
                                          defaultextension=".txt")
            if not host_file:
                return

            genom_str = PlantGenom.export_genom(self.plant_genome)
            with open(host_file, "w") as file:
                file.write(genom_str)
            messagebox.showinfo("Message", "Genome exported successfully!")
        except:
            messagebox.showerror("Error", "Please enter a valid genome to enable export:\n"
                                          "All the entries have to be filled out with integers")

    def save_plant_as(self):
        """
        This method realises the "Save" button functionality;
        it saves the current canvas picture (including during
        generation) in the .png format
        """
        host_file = asksaveasfilename(filetypes=[("Image", "*.png")],
                                      defaultextension=".png")
        if not host_file:
            return

        plant_image = self.controller.plant_frame.get_image()
        plant_image.save(host_file, "PNG")
        messagebox.showinfo("Message", "Image saved successfully!")

    def configure_widgets(self):
        self.method_button.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        self.method_tip = Hovertip(self.method_button, text="Set the method of genome-smashing")

        self.generate_button.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        self.generate_tip = Hovertip(self.generate_button, text="See what happens!")

        self.export_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.export_tip = Hovertip(self.export_button, "Export the genome of \n"
                                                       "the plant last generated \n"
                                                       "in the .txt format (tip: share!)")

        self.save_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
        self.save_tip = Hovertip(self.save_button, "Save a picture of your gorgeous plant!")

    def open_method_settings(self):
        self.method_settings = MethodSettingsWindow(self.controller.controller, self.controller.controller)

    def get_plant(self) -> Plant:
        self.set_smashed_genome()
        start_pos = Vec2(0, 250)
        plant = Plant(self.plant_genome, start_pos)
        return plant


class ParentGeneratorFrame(ttk.Frame):
    """
    This frame consists of a PlantFrame and a ParentUserFrame,
    as well as a progressbar; the parent plants are controlled
    and drawn here
    """
    def __init__(self, container, controller, parent_number: int):
        super().__init__(container)
        self.controller = controller
        self.parent_number = parent_number

        self.plant_frame = PlantFrame(self, self, 450, 450)
        self.user_frame = ParentUserFrame(self, self)

        self.configure_widgets()

    def configure_widgets(self):
        self.plant_frame.pack()
        self.user_frame.pack()


class HeirGeneratorFrame(ttk.Frame):
    """
    This frame consists of a PlantFrame and an HeirUserFrame,
    as well as a progressbar; the heir plant is controlled
    and drawn here
    """
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self.plant_frame = PlantFrame(self, self, 450, 450)
        self.user_frame = HeirUserFrame(self, self)

        self.configure_widgets()

    def configure_widgets(self):
        self.plant_frame.pack()
        self.user_frame.pack()


class MethodSettingsWindow(tk.Toplevel):
    """
    This is a pop-up window where the User can regulate
    the parameters of the genome smashing method
    """
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        self.geometry("500x230")
        self.title("Method")

        self.settings_frame = ttk.Frame(self)

        self.methods = Config.METHODS
        self.method_name_var = tk.StringVar(value=Config.method_name)
        self.method_box = ttk.Combobox(self.settings_frame,
                                       values=self.methods,
                                       textvariable=self.method_name_var,
                                       state="readonly")
        self.method_label = ttk.Label(self.settings_frame, text="Method: ")

        self.lean_var = tk.IntVar(value=Config.proportion)
        self.lean_slider = tk.Scale(self.settings_frame,
                                    from_=0,
                                    to=100,
                                    variable=self.lean_var,
                                    orient=tk.HORIZONTAL,
                                    tickinterval=25,
                                    showvalue=True,
                                    length=300)
        self.lean_label = ttk.Label(self.settings_frame, text="Parent 1 / Parent 2\n"
                                                              "proportion (%):")

        self.mutations_var = tk.IntVar(value=Config.mutations)
        self.mutation_count_box = ttk.Spinbox(self.settings_frame,
                                              state="readonly",
                                              from_=0,
                                              to=180,
                                              increment=1,
                                              textvariable=self.mutations_var)
        self.mutation_label = ttk.Label(self.settings_frame, text="Mutations: ")

        self.apply_button = ttk.Button(self, text="Apply", command=self.communicate_method)

        self.resizable(False, False)
        self.transient(controller)
        self.grab_set()
        self.configure_widgets()

    def configure_widgets(self):
        self.method_label.grid(row=0, column=0, pady=5, sticky="nse")
        self.method_box.grid(row=0, column=1, padx=20, pady=5, sticky="nsew")

        self.lean_label.grid(row=1, column=0, pady=5, sticky="nse")
        self.lean_slider.grid(row=1, column=1, padx=20, pady=5, sticky="nsew")

        self.mutation_label.grid(row=2, column=0, pady=5, sticky="nse")
        self.mutation_count_box.grid(row=2, column=1, padx=20, pady=5, sticky="nsew")

        self.settings_frame.pack(padx=15, pady=10)
        self.apply_button.pack(padx=15, pady=10)

    def set_method(self):
        """
        Obtains the values of the tkinter variables and updates the method
        identifier accordingly
        """
        Config.method = self.method_name_var.get()
        Config.proportion = self.lean_var.get()
        Config.mutations = self.mutations_var.get()

    def communicate_method(self):
        """
        Sets the method identifier of parent frames to that dictated
        by the variable values configured by the User; the pop-up window
        is then destroyed
        """
        self.set_method()
        self.destroy()


class SmashPlant(ttk.Frame):
    """
    The main frame of the feature
    """
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self.parent_frame_1 = ParentGeneratorFrame(self, self, 1)
        self.heir_frame = HeirGeneratorFrame(self, self)
        self.parent_frame_2 = ParentGeneratorFrame(self, self, 2)

        self.back_button = ttk.Button(self, text="Back",
            command=lambda: self.controller.show_frame("Menu"))

        self.configure_widgets()

    def configure_widgets(self):
        self.back_button.place(x=10, y=10)
        self.parent_frame_1.pack(side="left", padx=5)
        self.heir_frame.pack(side="left")
        self.parent_frame_2.pack(side="left", padx=5)
