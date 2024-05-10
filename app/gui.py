import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from plant_generator import Plant, PlantGenom, AgentGenom
from tools import Color, Vec2
from dataclasses import astuple

class UserFrame(ttk.Frame):
    """
    Contains the User side of the interface, i.e.
    the buttons and the genome input table
    """

    def __init__(self, container):
        super().__init__(container)

        self.table_height = 20
        self.table_width = 9

        for row in range(self.table_height):
            self.rowconfigure(row, weight=1)
        for column in range(self.table_width):
            self.columnconfigure(column, weight=1)

        self.rowconfigure(self.table_height, weight=3)
        self.rowconfigure(self.table_height + 1, weight=3)

        """
        In the above, the "weight" parameter seems 
        to have no impact on the size of the buttons.
        Leave as it is, but fix later with styling.
        """

        self.genom_entry_fields = {}
        self.genom_entries_tkvar = {}

        for row in range(self.table_height):
            for column in range(self.table_width):
                self.genom_entries_tkvar[(row, column)] = tk.IntVar(value=0)
                self.genom_entry_fields[(row, column)] = ttk.Entry(self,
                                                                   width=5,
                                                                   textvariable=self.genom_entries_tkvar[(row, column)])
                self.genom_entry_fields[(row, column)].grid(row=row,
                                                            column=column,
                                                            padx=5,
                                                            pady=5)

        button_style = ttk.Style()
        button_style.configure("TButton", font=("Charter", 14))

        self.import_button = ttk.Button(self, text="Import", command=self.genome_unpack)
        self.export_button = ttk.Button(self, text="Export", command=self.genome_pack)
        self.random_button = ttk.Button(self, text="Random", command=self.set_random)
        self.generate_button = ttk.Button(self, text="Generate Plant")

        self.import_button.grid(row=self.table_height,
                                column=0,
                                columnspan=3,
                                sticky="nsew",
                                padx=5,
                                pady=10)
        self.random_button.grid(row=self.table_height,
                                column=3,
                                columnspan=3,
                                sticky="nsew",
                                padx=5,
                                pady=10)
        self.export_button.grid(row=self.table_height,
                                column=6,
                                columnspan=3,
                                sticky="nsew",
                                padx=5,
                                pady=10)
        self.generate_button.grid(row=self.table_height + 1,
                                  column=0,
                                  columnspan=9,
                                  sticky="nsew",
                                  padx=5)

        self.plant = None

    def get_agent_genome(self, column: int) -> AgentGenom:
        """
        Returns an agent genome based upon the entries from
        a column of the entry table
        """
        agent_genome_entries = []
        for row in range(self.table_height):
            agent_genome_entries.append(self.genom_entries_tkvar[(row, column)].get())
        agent_genome_entries = tuple(agent_genome_entries)
        agent_genome = AgentGenom(*agent_genome_entries)
        return agent_genome

    def get_plant_genome(self) -> PlantGenom:
        """
        Returns a plant genome based upon the agent genomes
        to have been obtained by means of get_agent_genome() for
        all the columns of the entry table
        """
        agent_genomes = []
        for column in range(self.table_width):
            agent_genomes.append(self.get_agent_genome(column))
        plant_genome = PlantGenom(agent_genomes)
        return plant_genome

    def get_plant(self) -> Plant:
        plant_genome = self.get_plant_genome()
        start_pos = Vec2(0, 300)
        plant = Plant(plant_genome, start_pos)
        return plant

    def set_random(self):
        """
        Sets random table entry values; bound to the "Random" button
        """
        random_genome = PlantGenom.random()
        for column in range(self.table_width):
            agent_genome = random_genome._genom[column]
            for row in range(self.table_height):
                self.genom_entries_tkvar[(row, column)].set(astuple(agent_genome)[row])

    def genome_pack(self):
        """
        The function that realises the "Import" function through
        the file dialogue opener
        """
        host_file = asksaveasfilename(filetypes=[("Text File", "*.txt")],
                                      defaultextension=".txt")
        with open(host_file, "w") as file:
            for row in range(self.table_height):
                string = ""
                for column in range(self.table_width):
                    string += f"{self.genom_entries_tkvar[(row, column)].get()} "
                file.write(string + "\n")

    def genome_unpack(self):
        """
        The function that realises the "Export" function through
        the file dialogue opener
        """
        file = askopenfilename()
        with open(file) as f:
            lines = f.readlines()
            for row in range(len(lines)):
                entries = list(map(int, lines[row].split()))
                for column in range(self.table_width):
                    self.genom_entries_tkvar[(row, column)].set(entries[column])


class PlantFrame(ttk.Frame):
    """
    Contains the canvas where the plant is drawn
    """

    def __init__(self, container):
        super().__init__(container)

        self.canvas_width = 800
        self.canvas_height = 800

        self.canvas = tk.Canvas(master=self,
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg="lightgray")
        self.canvas.grid(padx=10, pady=10, row=0, column=0, rowspan=10, columnspan=10)

        self.genom_input = None

        self.plant = None

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
        light = (circle.color - Color(10, 10, 10)).hex
        self.canvas.create_oval(x0, y0, x1, y1, outline=color, fill=color)
        self.canvas.create_oval(x0 - 1, y0 - 1, x1 - 1, y1 - 1, outline=dark, fill=dark)
        self.canvas.create_oval(x0 + 1, y0 + 1, x1 + 1, y1 + 1, outline=light, fill=light)

    def start_drawing(self):
        self.canvas.delete("all")
        self.plant = self.genom_input.get_plant()
        self.draw()

    def get_delay(self, agents_count: int) -> int:
        return 1
        # if agents_count <= 2:
        #     return 10
        # elif agents_count <= 50:
        #     return 5
        # else:
        #     return 0

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
    """
    Main application window
    """

    def __init__(self):
        super().__init__()

        self.title("Digital Garden")

        self.geometry("1280x1000")
        self.minsize(1024, 512)

        self.__create_widgets__()

    def __create_widgets__(self):
        """
        Self-explanatory
        """
        self.plant_frame = PlantFrame(self)
        self.user_frame = UserFrame(self)

        self.plant_frame.genom_input = self.user_frame
        self.user_frame.generate_button.configure(command=self.plant_frame.start_drawing)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.plant_frame.grid(column=0, row=0, padx=20, pady=20)
        self.user_frame.grid(column=1, row=0, padx=20, pady=20)
