import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
from idlelib.tooltip import Hovertip
from dataclasses import astuple
from colorsys import hsv_to_rgb

from PIL import Image, ImageDraw, ImageTk

from plant_generator import Plant, PlantGenom, AgentGenom
from tools import Color, Vec2, Circle


class UserFrame(ttk.Frame):
    """
    Contains the User side of the interface, i.e.
    the buttons and the genome input table
    """

    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

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
        self.entry_tips = {}

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
                self.entry_tips[(row, column)] = Hovertip(self.genom_entry_fields[(row, column)],
                                                          f"Agent generation: {column + 1} "
                                                           f"\nGene: {AgentGenom.attr_list()[row]}",
                                                          hover_delay=0)

        button_style = ttk.Style()
        button_style.configure("TButton", font=("Times New Roman", 18))

        self.import_button = ttk.Button(self, text="Import", command=self.genome_unpack)
        self.export_button = ttk.Button(self, text="Export", command=self.genome_pack)
        self.random_button = ttk.Button(self, text="Random", command=self.set_random)
        self.generate_button = ttk.Button(self, text="Generate Plant", 
                                          command=self.controller.plant_frame.start_drawing)

        self.import_button.grid(row=self.table_height,
                                column=0,
                                columnspan=3,
                                sticky="nsew",
                                padx=5,
                                pady=10)
        self.import_tip = Hovertip(self.import_button, "Import a genome (.txt) \nto fill out the table")

        self.random_button.grid(row=self.table_height,
                                column=3,
                                columnspan=3,
                                sticky="nsew",
                                padx=5,
                                pady=10)
        self.random_tip = Hovertip(self.random_button, "Fill out a random gene \n(you could get lucky!)")

        self.export_button.grid(row=self.table_height,
                                column=6,
                                columnspan=3,
                                sticky="nsew",
                                padx=5,
                                pady=10)
        self.export_tip = Hovertip(self.export_button, "Export a genome you find the best \nin the .txt "
                                                  "format (tip: share!)")

        self.generate_button.grid(row=self.table_height + 1,
                                  column=0,
                                  columnspan=9,
                                  sticky="nsew",
                                  padx=5)
        self.generate_tip = Hovertip(self.generate_button, "See what happens!")

    def get_agent_genome(self, column: int) -> AgentGenom:
        """
        Returns an agent genome based upon the entries from
        a column of the entry table
        """
        agent_genome_entries = []
        for row in range(self.table_height):
            value = self.genom_entries_tkvar[(row, column)].get()
            agent_genome_entries.append(value)
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
            try:
                agent_genomes.append(self.get_agent_genome(column))
            except tk.TclError:
                messagebox.showerror("showerror", f"Неправильне значення геному")
                return
        plant_genome = PlantGenom(agent_genomes)
        return plant_genome

    def get_plant(self) -> Plant:
        plant_genome = self.get_plant_genome()
        start_pos = Vec2(0, 250)
        plant = Plant(plant_genome, start_pos)
        return plant

    def set_random(self):
        """
        Sets random table entry values; bound to the "Random" button
        """
        random_genome = PlantGenom.random()
        for column in range(self.table_width):
            agent_genome = random_genome.genom[column]
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

        if not file: # Exception when user was not chosen any file
            return 

        try:
            with open(file) as f:
                lines = f.readlines()
                for row in range(len(lines)):
                    entries = list(map(int, lines[row].split()))
                    for column in range(self.table_width):
                        self.genom_entries_tkvar[(row, column)].set(entries[column])
        except:
            messagebox.showerror("showerror", "Неправильний формат геному!")


class PlantFrame(ttk.Frame):
    """
    Contains the canvas where the plant is drawn
    """

    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        # Style of program
        self.style = ttk.Style()
        self.style.configure("Custom.Vertical.TProgressbar", 
                             troughcolor='gray')

        # Canvas with plant
        self.canvas_width = 800
        self.canvas_height = 800

        self.canvas = tk.Canvas(master=self,
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg="lightgray")
        self.canvas.grid(padx=0, 
                         pady=10, 
                         row=0, 
                         column=1, 
                         rowspan=10, 
                         columnspan=10)

        # Image on which draw plant
        self.background = Color(250, 250, 250)
        self.plant_image = Image.new("RGBA",
                                     (self.canvas_width, self.canvas_height),
                                     self.background.rgb)
        self.plant_draw = ImageDraw.Draw(self.plant_image)

        # Progress bar 
        self.progress_var = tk.DoubleVar()
        self.plant_progress = ttk.Progressbar(self, 
                                              style="Custom.Vertical.TProgressbar",
                                              orient=tk.VERTICAL,
                                              length=800,
                                              variable=self.progress_var,
                                              maximum=100)
        self.plant_progress.grid(row=0, column=0, pady=10)

        # Plant generation process
        self.current_drawing = None

    def update_canvas(self):
        """
        Show image on canvas
        """
        self.canvas.image = ImageTk.PhotoImage(self.plant_image)
        self.canvas.create_image(self.canvas_width//2, self.canvas_height//2,
                                 anchor=tk.CENTER, image=self.canvas.image)

    def clear_canvas(self):
        """
        Clear image with plant and update canvas
        """
        self.plant_image = Image.new("RGB",
                                     (self.canvas_width, self.canvas_height),
                                     self.background.rgb)
        self.plant_draw = ImageDraw.Draw(self.plant_image)
        self.update_canvas()

    def draw_circle(self, circle: Circle):
        """
        Draw circle on image

        Draw 3 circles, main, darker and ligher 
        for 3d effect
        """
        width = self.canvas_width
        height = self.canvas_height

        x, y = circle.pos + Vec2(width//2, height//2)
        if x < 0 or x > width or y < 0 or y > height:
            return
        r = abs(circle.radius) + 1

        x0, y0 = x - r, y - r
        x1, y1 = x + r, y + r
         
        default_color = circle.color
        dark_color = circle.color + Color(20, 20, 20)
        light_color = circle.color - Color(20, 20, 20)
        self.plant_draw.ellipse((x0, y0, x1, y1),
                                fill=light_color.rgb)
        self.plant_draw.ellipse((x0-1, y0-1, x1-1, y1-1),
                                fill=default_color.rgb)
        self.plant_draw.ellipse((x0+1, y0+1, x1+1, y1+1),
                                fill=dark_color.rgb)

    def update_progress(self, value: float):
        """
        Update status and color of progressbar 
        by given value
        """
        self.progress_var.set(value)
        current_value = self.plant_progress["value"]
        
        hue = (current_value / 100.0) * 0.3
        r, g, b = hsv_to_rgb(hue, 1, 1)
        color = '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

        self.style.configure("Custom.Vertical.TProgressbar", 
                             foreground=color, background=color)
        self.plant_progress.config(style="Custom.Vertical.TProgressbar")

    def start_drawing(self):
        """
        Start drawing and generation of plant

        1. Stop all previous drawing (if exist)
        2. Get new plant
        3. Start drawing and generating new plant
        """
        if self.current_drawing:
            self.after_cancel(self.current_drawing)
        self.clear_canvas()
        self.progress_var.set(0)
        plant = self.controller.user_frame.get_plant()
        self.current_drawing = self.after(1, self.draw, plant)
        
    def draw(self, plant: Plant):
        """
        Draw plant while it is growing
        """
        for circle in plant.get_circles():
            self.draw_circle(circle)
        self.update_progress(plant.drawed/plant.total*100) 
        self.update_canvas()

        if plant.is_growing():
            self.current_drawing = self.after(1, self.draw, plant)
        else:
            self.update_progress(100.0)
            self.current_drawing = None


class PlantGenerator(ttk.Frame):
    """
    Main application window
    """

    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """
        Self-explanatory
        """
        self.plant_frame = PlantFrame(self, self)
        self.user_frame = UserFrame(self, self)


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.plant_frame.grid(column=0, row=0, padx=20, pady=20)
        self.user_frame.grid(column=1, row=0, padx=20, pady=20)
