from PIL import Image
import hashlib
from plant_generator import PlantGenom

# Load the image with metadata
image = Image.open("./fdasfda.png")

# Retrieve the metadata
metadata = image.info
name = metadata["Plant"]
genom = metadata["Genom"]

hash_string = name + genom.replace(" ", "/").replace("\n","|")
print(hash_string)
hash = hashlib.sha256(hash_string.encode("utf-8")).hexdigest()
print(hash == metadata["PlantHash"]) 

print(metadata)
print(PlantGenom.import_genom(metadata["Genom"]))
