import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import time
from threading import Thread, Event
from random import uniform

from tools import Color, Circle, Vec2
from plant_generator import Plant


class StoppableThread(Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class AsyncPainter(StoppableThread):
    def __init__(self, canvas, image, draw, plant):
        super().__init__()
        self.canvas = canvas
        self.image_id = None
        self.image = image
        self.draw = draw
        self.plant = plant
        self.delay = 0.01

    def clear_canvas(self):
        """
        Clear image with plant and update canvas
        """
        self.image = Image.new("RGB",
                               (600, 600),
                               (255, 255, 255)) 
        self.draw = ImageDraw.Draw(self.image)
        self.update_canvas()

    def update_canvas(self):
        """
        Show image on canvas
        """
        self.canvas.image = ImageTk.PhotoImage(self.image)
        if self.image_id is None:
            self.image_id = self.canvas.create_image(600 // 2, 600 // 2,
                                 anchor=tk.CENTER, image=self.canvas.image)
        else:
            self.canvas.itemconfig(self.image_id, image=self.canvas.image)

    def draw_circle(self, circle: Circle):
        """
        Draw circle on image

        Draw 3 circles, main, darker and lighter
        for 3D effect
        """
        width = 600
        height = 600
        x, y = circle.pos + Vec2(width // 2, height // 2)
        if x < 0 or x > width or y < 0 or y > height:
            return
        r = abs(circle.radius) + 1

        x0, y0 = x - r, y - r
        x1, y1 = x + r, y + r

        default_color = circle.color
        dark_color = circle.color + Color(20, 20, 20)
        light_color = circle.color - Color(20, 20, 20)
        self.draw.ellipse((x0, y0, x1, y1),
                                fill=light_color.rgb)
        self.draw.ellipse((x0 - 1, y0 - 1, x1 - 1, y1 - 1),
                                fill=default_color.rgb)
        self.draw.ellipse((x0 + 1, y0 + 1, x1 + 1, y1 + 1),
                                fill=dark_color.rgb)

    def run(self):
        self.clear_canvas()
        while self.plant.is_growing() and not self.stopped():
            for circle in self.plant.get_circles():
                self.draw_circle(circle)
            time.sleep(self.delay) 
            self.canvas.after(1, self.update_canvas)


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
    
    def start_drawing(self):
        if self.current_drawing:
            self.current_drawing.stop()

        self.current_drawing = AsyncPainter(self.canvas,
                                            self.plant_image,
                                            self.plant_draw,
                                            Plant.random())
        self.current_drawing.start()


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
