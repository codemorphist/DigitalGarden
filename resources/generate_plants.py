import os
from plant_generator import PlantGenom
from tools.planticus import random_name


def generate_random_genomes(folder_path: str, count: int):
    for _ in range(count):
        try:
            name = random_name()
            path = os.path.join(folder_path, name) + ".txt"
            while os.path.exists(path):
                name = random_name()
                path = os.path.join(folder_path, name + ".txt")
            genom = PlantGenom.random()
            with open(path, "w") as file:
                file.write(PlantGenom.export_genom(genom))
            print(f"Generated: {name}")
        except:
            print("Opps, some error!")

generate_random_genomes("./orangery", 101)
