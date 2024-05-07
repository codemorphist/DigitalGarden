from __future__ import annotations
from plant_generator.genom import PlantGenom
from plant_generator.agent import EmptyAgent
from tools import Vec2, Circle, Color


class TestPlant:
    """
    Plant which generates random circles
    Usage example:

        from plant_generator import TestPlant

        plant = TestPlant(10)

        while plant.is_growing():
            for circle in plant.get_circles():
                print(circle)
    """
    def __init__(self, length: int):
        self.length = length
        self.circle_count = 10

    def is_growing(self) -> bool:
        return self.length > 0

    def __iter__(self):
        return self.get_circles()
   
    def get_circles(self):
        for _ in range(self.circle_count):
            yield Circle.random()       
            self.length -= 1


class Plant:
    def __init__(self, 
                 plant_genom: PlantGenom,
                 start_pos: Vec2):
        self.plant_genom = plant_genom
        self.agents = []
        self.init_agents(start_pos)

    def init_agents(self, start_pos: Vec2):
        zero_agent = EmptyAgent(self.plant_genom, start_pos) 
        self.agents = zero_agent.get_heirs()

    def is_growing(self) -> bool:
        return len(self.agents) > 0

    def __iter__(self):
        return self.get_circles()  

    def get_circles(self):
        for agent in self.agents:
            circle = agent.get_circle()
            yield circle
        
        new_agents = []
        for agent in self.agents:
            if agent.is_live:
                new_agents.append(agent)
            else:
                new_agents += agent.get_heirs()
        self.agents = new_agents

    @staticmethod
    def random() -> Plant:
        return Plant(
            PlantGenom.random(),
            Vec2(0, 200)
        )
    
