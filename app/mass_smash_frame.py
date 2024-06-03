import logging
logger = logging.getLogger(__name__)


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename, askopenfilenames, test
from idlelib.tooltip import Hovertip
from dataclasses import astuple
from colorsys import hsv_to_rgb
from pathlib import Path

from PIL import Image, ImageDraw, ImageTk

from plant_generator import Plant, PlantGenom, SmashGenom
from generator_frame import PlantFrame
from tools import Circle, Color, Vec2

from method_config import MethodConfig
from smash_plant import MethodSettingsWindow


Config = MethodConfig()


class GenomeViewFrame(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.controller = controller
        self.genomes_dict = {}

        self.genome_view = ttk.Treeview(self, columns=("genomes",), show="headings", height=31)
        self.genome_view.heading("genomes", text="Genomes")

        self.up_button = ttk.Button(self, text="Up", command=self.move_up)
        self.down_button = ttk.Button(self, text="Down", command=self.move_down)

        self.add_button = ttk.Button(self, text="Add", command=self.add_genomes)
        self.remove_button = ttk.Button(self, text="Remove", command=self.remove_genomes)

        self.configure_widgets()

    def configure_widgets(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.genome_view.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.up_button.grid(row=1, column=0, sticky="new")
        self.up_tip = Hovertip(self.up_button, text="Move genomes to higher in the list")

        self.down_button.grid(row=1, column=1, sticky="new")
        self.down_tip = Hovertip(self.down_button, text="Move genomes to lower in the list")

        self.add_button.grid(row=2, column=0, sticky="new")
        self.add_tip = Hovertip(self.add_button, text="Add parent genomes to the pool")

        self.remove_button.grid(row=2, column=1, sticky="new")
        self.remove_tip = Hovertip(self.remove_button, text="Remove selected parent genomes \n"
                                                            "from the pool")

    def add_genomes(self):
        genome_files = askopenfilenames()
        if not genome_files:
            return
        for genome_file_name in genome_files:
            try:
                genome = self.genome_unpack(genome_file_name)
                assert genome
                self.genome_view.insert(parent="", index = "end", iid=genome_file_name, values=(Path(genome_file_name).stem,))
                self.genomes_dict[genome_file_name] = genome
                logger.info(f"Genome {genome_file_name} imported and added to pool")
            except AssertionError:
                messagebox.showerror("Error", "Import attempted with an invalid genome:\n"
                                              "The genome has to be a .txt file with a 20x9 table of \n"
                                              "integer inputs separated by spaces")

    def genome_unpack(self, file_name) -> PlantGenom:
        """
        This function returns a plant genome from a read file as a PlantGenome
        """
        try:
            with open(file_name) as file:
                plant_genome = PlantGenom.import_genom(file.read())
                return plant_genome
        except Exception as e:
            logger.exception(e)

    def remove_genomes(self):
        selection = self.genome_view.selection()
        for path in selection:
            self.genome_view.delete(path)
            logger.info(f"Genome {path} removed from pool")
            del self.genomes_dict[path]

    def move_up(self):
        selected_item = self.genome_view.selection()
        if not selected_item:
            return

        for item in selected_item:
            prev_item = self.genome_view.prev(item)
            if prev_item:
                self.genome_view.move(item, 
                                      self.genome_view.parent(item), 
                                      self.genome_view.index(prev_item))

    def move_down(self):
        selected_item = self.genome_view.selection()
        if not selected_item:
            return

        for item in reversed(selected_item):
            next_item = self.genome_view.next(item)
            if next_item:
                self.genome_view.move(item, 
                                      self.genome_view.parent(item), 
                                      self.genome_view.index(next_item))

    def get_genomes(self):
        for genome in self.genome_view.get_children():
            yield self.genomes_dict[genome]


class MassSmashUserFrame(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self.plant_genome = PlantGenom.empty()

        self.genome_view = GenomeViewFrame(self, self)

        self.method_button = ttk.Button(self, text="Method", command=self.open_method_settings)
        self.generate_button = ttk.Button(self,
                                          text="Generate Plant",
                                          command=lambda: self.controller.plant_frame.start_drawing(False))
        self.fgenerate_button = ttk.Button(self,
                                           text="Fast",
                                           command=lambda: self.controller.plant_frame.start_drawing(True))
        self.export_button = ttk.Button(self, text="Export", command=self.genome_pack)
        self.save_button = ttk.Button(self, text="Save", command=self.save_plant_as)

        button_style = ttk.Style()
        button_style.configure("TButton", font=("Times New Roman", 17))

        self.configure_widgets()

    def configure_widgets(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.genome_view.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.method_button.grid(row=1, column=0, columnspan=2, pady=(20, 0), sticky="nsew")
        self.method_tip = Hovertip(self.method_button, text="Set the method of genome-smashing")

        self.generate_button.grid(row=2, column=0, sticky="nsew")
        self.generate_tip = Hovertip(self.generate_button, text="See what happens!")

        self.fgenerate_button.grid(row=2, column=1, sticky="nsew")
        self.fgenerate_tip = Hovertip(self.fgenerate_button, "Click for a quick generation")

        self.export_button.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.export_tip = Hovertip(self.export_button, "Export the genome of \n"
                                                       "the plant last generated \n"
                                                       "in the .txt format (tip: share!)")

        self.save_button.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.save_tip = Hovertip(self.save_button, "Save a picture of your gorgeous plant!")

    def set_smashed_genome(self):
        self.plant_genome = SmashGenom.mass_smash(self.parents_list,
                                                  Config.method,
                                                  Config.proportion / 100,
                                                  Config.mutations)
        logger.info(f"Genome smashed from pool with parameters "
                    f"{(Config.method, Config.proportion / 100, Config.mutations)}")

    @property
    def parents_list(self) -> list[PlantGenom]:
        return list(self.genome_view.get_genomes())

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
        logger.info(f"Exported genome to: {host_file}")
        messagebox.showinfo("Message", "Genome exported successfully!")

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

        try:
            plant_image = self.controller.plant_frame.get_image()
            
            if plant_image is None:
                raise Exception("You haven't generated any plant!")

            plant_image.save(host_file, "PNG")
            logger.info(f"Saved plant to: {host_file}")
            messagebox.showinfo("Message", "Image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", "You haven't generated any plant!")
            logger.exception(e)

    def open_method_settings(self):
        self.method_settings = MethodSettingsWindow(self, self, Config)

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
                                      command=lambda: self.back())

        self.configure_widgets()

    def configure_widgets(self):
        """
        Configure place and style of widgets and frames
        """
        self.plant_frame.pack(side="left", padx=20, pady=20)
        self.user_frame.pack(side="left", padx=20, pady=30, expand=True, fill="x")
        self.back_button.place(x=10, y=10)

    def back(self):
        self.controller.show_frame("Menu")
        self.plant_frame.pause_drawing()

    def resume(self):
        self.plant_frame.resume_drawing()


