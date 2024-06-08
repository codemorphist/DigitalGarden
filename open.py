from PIL import Image
from plant_generator import PlantGenom

# Load the image with metadata
image = Image.open("./fdasfda.png")

# Retrieve the metadata
metadata = image.info

print(metadata)
print(PlantGenom.import_genom(metadata["Genom"]))
