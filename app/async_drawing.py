import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk

from tools import Color, Circle, Vec2
from plant_generator import Plant

class DrawPlantFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.canvas_width = 600
        self.canvas_height = 600

        self.canvas = tk.Canvas(self, 
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg="white")
        self.start_button = tk.Button(self,
                                      text="Start", height=2,
                                      command=self.start_drawing)

        self.background = (250, 250, 250)
        self.plant_image = Image.new("RGBA",
                                     (self.canvas_width, self.canvas_height),
                                     self.background)
        self.plant_draw = ImageDraw.Draw(self.plant_image)
        self.current_drawing = None

        self.canvas.grid(row=0, column=0)
        self.start_button.grid(row=1, column=0, sticky="ew")

    def update_canvas(self):
        """
        Show image on canvas
        """
        self.canvas.image = ImageTk.PhotoImage(self.plant_image)
        self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2,
                                 anchor=tk.CENTER, image=self.canvas.image)

    def clear_canvas(self):
        """
        Clear image with plant and update canvas
        """
        self.plant_image = Image.new("RGB",
                                     (self.canvas_width, self.canvas_height),
                                     self.background)
        self.plant_draw = ImageDraw.Draw(self.plant_image)
        self.update_canvas()

    def draw_circle(self, circle: Circle):
        """
        Draw circle on image

        Draw 3 circles, main, darker and lighter
        for 3d effect
        """
        width = self.canvas_width
        height = self.canvas_height

        x, y = circle.pos + Vec2(width // 2, height // 2)
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
        self.plant_draw.ellipse((x0 - 1, y0 - 1, x1 - 1, y1 - 1),
                                fill=default_color.rgb)
        self.plant_draw.ellipse((x0 + 1, y0 + 1, x1 + 1, y1 + 1),
                                fill=dark_color.rgb)

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
        plant = Plant.random()
        self.current_drawing = self.after(1, self.draw, plant)

    def draw(self, plant: Plant):
        """
        Draw plant while it is growing
        """
        for circle in plant.get_circles():
            self.draw_circle(circle)
        self.update_canvas()

        if plant.is_growing():
            self.current_drawing = self.after(1, self.draw, plant)
        else:
            self.current_drawing = None


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
