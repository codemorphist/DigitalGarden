import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename, askopenfilenames
from idlelib.tooltip import Hovertip
from dataclasses import astuple
from colorsys import hsv_to_rgb
from pathlib import Path

from PIL import Image, ImageDraw, ImageTk

from plant_generator import Plant, PlantGenom, SmashGenom
from generator_frame import PlantFrame
from tools import Circle, Color, Vec2

from fsm import MethodConfig
from smash_plant import MethodSettingsWindow


Config = MethodConfig()
Config.proportion = 50


class GenomeViewFrame(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.controller = controller
        self.genomes_dict = {}

        self.genome_view = ttk.Treeview(self, columns=("genomes",), show="headings", height=31)
        self.genome_view.heading("genomes", text="Genomes")

        self.add_button = ttk.Button(self, text="Add", command=self.add_genomes)
        self.remove_button = ttk.Button(self, text="Remove", command=self.remove_genomes)

        self.configure_widgets()

    def configure_widgets(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.genome_view.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.add_button.grid(row=1, column=0, sticky="new")
        self.add_tip = Hovertip(self.add_button, text="Add parent genomes to the pool")

        self.remove_button.grid(row=1, column=1, sticky="new")
        self.remove_tip = Hovertip(self.remove_button, text="Remove selected parent genomes \n"
                                                            "from the pool")

    def add_genomes(self):
        genome_files = askopenfilenames()
        if not genome_files:
            return
        for genome_file_name in genome_files:
            self.genome_view.insert(parent="", index = "end", iid=genome_file_name, values=(Path(genome_file_name).stem,))
            with open(genome_file_name) as file:
                genome = PlantGenom.import_genom(file.read())
                self.genomes_dict[genome_file_name] = genome

    def remove_genomes(self):
        selection = self.genome_view.selection()
        for path in selection:
            self.genome_view.delete(path)
            del self.genomes_dict[path]


class MassSmashUserFrame(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self.plant_genome = PlantGenom.empty()

        self.genome_view = GenomeViewFrame(self, self)

        self.method_button = ttk.Button(self, text="Method", command=self.open_method_settings)
        self.generate_button = ttk.Button(self, text="Generate Plant", command=self.controller.plant_frame.start_drawing)
        self.export_button = ttk.Button(self, text="Export", command=self.genome_pack)
        self.save_button = ttk.Button(self, text="Save", command=self.save_plant_as)

        button_style = ttk.Style()
        button_style.configure("TButton", font=("Times New Roman", 17))

        self.configure_widgets()

    def configure_widgets(self):
        self.genome_view.pack(fill="both", pady=15)

        self.method_button.pack(fill="both", pady=5)
        self.method_tip = Hovertip(self.method_button, text="Set the method of genome-smashing")

        self.generate_button.pack(fill="both", pady=5)
        self.generate_tip = Hovertip(self.generate_button, text="See what happens!")

        self.export_button.pack(fill="both", pady=5)
        self.export_tip = Hovertip(self.export_button, "Export the genome of \n"
                                                       "the plant last generated \n"
                                                       "in the .txt format (tip: share!)")

        self.save_button.pack(fill="both", pady=5)
        self.save_tip = Hovertip(self.save_button, "Save a picture of your gorgeous plant!")

    def set_smashed_genome(self):
        self.plant_genome = SmashGenom.mass_smash(self.parents_list,
                                                  Config.method,
                                                  Config.proportion / 100,
                                                  Config.mutations,)

    @property
    def parents_list(self) -> list[PlantGenom]:
        return [genome for genome in list(map(self.genome_unpack, [*self.genome_view.genomes_dict.keys()]))]

    def genome_pack(self):
        """
        The function that realises the "Export" function through
        the file dialogue opener
        """
        host_file = asksaveasfilename(filetypes=[("Text file", "*.txt")],
                                      defaultextension=".txt")
        if not host_file:
            return

        genome_str = PlantGenom.export_genom(self.plant_genome)
        with open(host_file, "w") as file:
            file.write(genome_str)
        messagebox.showinfo("Message", "Genome exported successfully!")

    def genome_unpack(self, file_name) -> PlantGenom:
        """
        This function returns a plant genome from a read file as a PlantGenome
        """
        try:
            with open(file_name) as file:
                plant_genome = PlantGenom.import_genom(file.read())
                return plant_genome
        except:
            messagebox.showerror("Error", "Import attempted with an invalid genome:\n"
                                          "The genome has to be a .txt file with a 20x9 table of \n"
                                          "integer inputs separated by spaces")

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

    def open_method_settings(self):
        self.method_settings = MethodSettingsWindow(self.controller, self.controller)

    def get_plant(self) -> Plant:
        self.set_smashed_genome()
        start_pos = Vec2(0, 250)
        plant = Plant(self.plant_genome, start_pos)
        return plant


class MassSmash(ttk.Frame):
    """
    The main frame of the feature
    """

    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self.plant_frame = PlantFrame(self, self)
        self.user_frame = MassSmashUserFrame(self, self)

        self.back_button = ttk.Button(self, text="Back",
                                      command=lambda: self.controller.show_frame("Menu"))

        self.configure_widgets()

    def configure_widgets(self):
        """
        Configure place and style of widgets and frames
        """
        self.plant_frame.pack(side="left", padx=20, pady=20)
        self.user_frame.pack(side="left", padx=20, pady=30, expand=True, fill="both")
        self.back_button.place(x=10, y=10)

