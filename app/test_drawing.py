from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import random

# Function to draw a circle on the image
def draw_circle(image_draw, center, radius):
    x, y = center
    image_draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(255, 0, 0))

# Function to update the Tkinter canvas with the image
def update_canvas(canvas, image):
    canvas.image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=NW, image=canvas.image)

# Function to draw circles one by one and update canvas
def draw_and_update(canvas, image_draw, width, height, circles):
    if circles > 0:
        # Draw one circle
        center = (random.randint(0, width), random.randint(0, height))
        radius = random.randint(10, 50)
        draw_circle(image_draw, center, radius)

        # Update canvas
        update_canvas(canvas, image)
        
        # Call the function again after a delay
        canvas.after(1, draw_and_update, canvas, image_draw, width, height, circles - 1)

# Create a Tkinter window
root = Tk()
root.title("Drawing Circles on Image")

# Create a blank image using Pillow
width, height = 800, 600
image = Image.new("RGB", (width, height), (255, 255, 255))

# Create a Tkinter canvas to display the image
canvas = Canvas(root, width=width, height=height)
canvas.pack()

# Create a drawing object
image_draw = ImageDraw.Draw(image)

# Draw circles one by one and update canvas
draw_and_update(canvas, image_draw, width, height, 3**9)  # Change 5 to the number of circles you want to draw

root.mainloop()

