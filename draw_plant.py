import os
import time

from plant_generator import Plant, PlantGenom
from tools import Vec2, Color

from PIL import Image, ImageDraw
from PIL import ImageEnhance
from tools.circle import Circle


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POT_IMAGE_PATH = os.path.join(SCRIPT_DIR, "resources", "pot_mmf_logo.png")
BACKGROUND_IMAGE_PATH = os.path.join(SCRIPT_DIR, "resources", "background.png")


def draw_circle(draw, 
                image_size: tuple[int, int], 
                circle: Circle):
    width, height = image_size
    x, y = circle.pos + Vec2(width // 2, height // 2)
    if x < 0 or x > width or y < 0 or y > height:
        return
    r = abs(circle.radius) + 1

    x0, y0 = x - r, y - r
    x1, y1 = x + r, y + r

    default_color = circle.color
    dark_color = circle.color + Color(20, 20, 20)
    light_color = circle.color - Color(20, 20, 20)

    draw.ellipse((x0 - 2, y0 - 2, x1 - 2, y1 - 2),
                                fill=dark_color.rgb)
    draw.ellipse((x0 + 2, y0 + 2, x1 + 2, y1 + 2),
                                fill=light_color.rgb)
    draw.ellipse((x0, y0, x1, y1),
                                fill=default_color.rgb)


def draw_plant_from_file(path_to_plant: str, path_to_save: str):
    genome = None
    with open(path_to_plant, "r") as file:
        genome = PlantGenom.import_genom(file.read())
    plant = Plant(genome, Vec2(0, 220))

    image_size = (1024, 1024)
    plant_image = Image.new("RGBA", image_size, (255, 255, 255, 0)) 
    draw = ImageDraw.Draw(plant_image)

    while plant.is_growing():
        for circle in plant.get_circles():
            draw_circle(draw, image_size, circle)

    enh = ImageEnhance.Color(plant_image)
    plant_image = enh.enhance(2.0)

    w, h = image_size
    image = Image.open(BACKGROUND_IMAGE_PATH)
    pot_image = Image.open(POT_IMAGE_PATH)
    pot_image = pot_image.resize((w//4, h//4), Image.LANCZOS)
    pot_pos = (w//2 - w//8, w//2 + plant.start_pos.y - 48)
    image.paste(pot_image, pot_pos, pot_image)
    image.paste(plant_image, (0, 0), plant_image)

    image.save(path_to_save)


def draw_all_plants(path_to_plants: str, path_to_save: str):
    for i, filename in enumerate(os.listdir(path_to_plants)):
        filepath = os.path.join(path_to_plants, filename)
        name = filename.split(".txt")[0] + ".png"
        savepath = os.path.join(path_to_save, name)
        if os.path.isfile(filepath) and filename.endswith(".txt"):
            try:
                draw_plant_from_file(filepath, savepath)
                print(f"- [{i}] Successfully drawed: {filepath} and saved to {savepath}\n")
            except:
                print(f"Invalid plant: {filepath}")


if __name__ == "__main__":
    start = time.time()
    draw_all_plants("./orangery/", "./gallery/")
    print(f"Time ellapsed: {time.time() - start}")
