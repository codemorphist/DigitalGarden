from plant_generator import Plant


plant = Plant.random()

__import__('pprint').pprint(plant.agents)

while plant.is_growing():
    print("plant is growing")
    for circle in plant:
        print(circle)
        input()
