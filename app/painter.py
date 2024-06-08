import logging
logger = logging.getLogger(__name__)

from abc import ABC, abstractmethod

import os
import hashlib
import time
from threading import Thread, Event, Condition
import tkinter as tk

from PIL import Image, ImageDraw, ImageTk
from PIL import ImageEnhance, PngImagePlugin

from plant_generator import Plant, PlantGenom
from tools import Circle, Color, Vec2


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POT_IMAGE_PATH = os.path.join(SCRIPT_DIR, "..", "resources", "pot_mmf_logo.png")
BACKGROUND_IMAGE_PATH = os.path.join(SCRIPT_DIR, "..", "resources", "background.png")


class Painter(ABC):
    def __init__(self, 
                 plant: Plant, 
                 canvas: tk.Canvas,
                 image_size: tuple[int, int] = (1024, 1024)):
        self.plant = plant

        self.canvas = canvas
        self.width = canvas.winfo_width()
        self.height = canvas.winfo_height()

        self.image_size = image_size

        self.plant_image = Image.new("RGBA", self.image_size, (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.plant_image, "RGBA")

        self.image = Image.new("RGBA", self.image_size, (0, 0, 0, 0))
        self.setup_image()

    @abstractmethod
    def draw_plant(self):
        """
        Draw plant
        """
        pass

    def setup_image(self):
        """
        Setup basic image
        """
        w, h = self.image_size
        background = Image.open(BACKGROUND_IMAGE_PATH) 
        background.resize(self.image_size, Image.LANCZOS)
        pot_image = Image.open(POT_IMAGE_PATH)
        pot_image = pot_image.resize((w//4, h//4), Image.LANCZOS)
        pot_pos = (w//2 - w//8,
                        w//2 + self.plant.start_pos.y - 48)
        self.image.paste(background, (0, 0))
        self.image.paste(pot_image, pot_pos, pot_image)

    def draw_circle(self, circle: Circle):
        """
        Draw circle on plant image
        """
        width, height = self.image_size
        x, y = circle.pos + Vec2(width // 2, height // 2)
        if x < 0 or x > width or y < 0 or y > height:
            return
        r = abs(circle.radius) + 1

        x0, y0 = x - r, y - r
        x1, y1 = x + r, y + r

        default_color = circle.color
        dark_color = circle.color + Color(20, 20, 20)
        light_color = circle.color - Color(20, 20, 20)

        self.draw.ellipse((x0 - 2, y0 - 2, x1 - 2, y1 - 2),
                                    fill=dark_color.rgb)
        self.draw.ellipse((x0 + 2, y0 + 2, x1 + 2, y1 + 2),
                                    fill=light_color.rgb)
        self.draw.ellipse((x0, y0, x1, y1),
                                    fill=default_color.rgb)

    def draw_current_layer(self):
        """
        Draw current layer of agents
        """
        for circle in self.plant.get_circles():
            self.draw_circle(circle)

    def get_image(self):
        """
        Enhance and return drawn plant
        """
        enh = ImageEnhance.Color(self.plant_image)
        plant_image = enh.enhance(2.0)
        image = self.image.copy()
        image.paste(plant_image, (0, 0), plant_image)
        return image

    def update_canvas(self):
        """
        Show image on canvas
        """
        canvas_image = self.get_image()
        canvas_image = canvas_image.resize((self.width, self.height), Image.LANCZOS)
        self.canvas.image = ImageTk.PhotoImage(canvas_image)
        self.canvas.create_image(self.width // 2, self.height // 2,
                                 anchor=tk.CENTER, image=self.canvas.image)

    def save(self, path: str):
        filename = os.path.basename(path)
        name = os.path.splitext(filename)[0]
        genom = PlantGenom.export_genom(self.plant.plant_genom)
        hash_string = name + genom.replace(" ", "/").replace("\n","|")
        hash = hashlib.sha256(hash_string.encode("utf-8")).hexdigest()

        image = self.get_image() 

        meta = PngImagePlugin.PngInfo()
        meta.add_text("Plant", name)
        meta.add_text("Genom", genom)
        meta.add_text("PlantHash", hash)

        image.save(path, format="PNG", pnginfo=meta)


class CustomThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.paused = False
        self.state = Condition()
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def pause(self):
        with self.state:
            self.paused = True  

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify() 


class ThreadPainter(Painter, CustomThread):
    def __init__(self, plant, canvas, progress, fast_draw):
        Painter.__init__(self, plant, canvas)
        CustomThread.__init__(self)

        self.fast_draw = fast_draw

        self.update = None
        self.delay = 0.01
        
        self.progress = progress

        logger.info(f"Initialized{' Fast ' if self.fast_draw else ' '}ThreadPainter: {id(self)} ")

    def draw_plant(self):
        logger.info(f"Started generation: {id(self)}")
        self.start()

    def update_progress(self, value: float):
        """
        Update status and color of progressbar
        by given value
        """
        if self.progress:
           self.progress.set(value)

    def run(self):
        logger.info(f"Running generation: {id(self)}")
        self.update_canvas()

        while self.plant.is_growing():
            with self.state:
                if self.paused:
                    self.state.wait()

            if self.stopped():
                return

            self.draw_current_layer()
            self.update_progress(self.plant.drawed / self.plant.total * 100)

            if not self.fast_draw: # if not fast animate
                self.update = self.canvas.after(1, self.update_canvas)
                time.sleep(self.delay)

        self.update_progress(100)
        self.update_canvas()

        logger.info(f"Ended generation: {id(self)}")

    def cancel_update(self):
        """
        Cancel tkinter frame update
        """
        if self.update:
            self.canvas.after_cancel(self.update)
        self.update = None

    def stop(self):
        logger.info(f"Stopped generation: {id(self)}")
        self.cancel_update()
        return super().stop()

    def pause(self):
        logger.info(f"Paused generation: {id(self)}")
        self.cancel_update()
        return super().pause()




