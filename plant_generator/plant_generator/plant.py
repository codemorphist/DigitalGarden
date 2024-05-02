from .genom import AgentGenom, PlantGenom
from .agent import Agent, EmptyAgent
from tools import Vec2, Circle, Color

from random import randint


class TestPlant():
    def __init__(self, lenght: int):
        self.lenght = lenght

    def __iter__(self):
        return self.get_circles()

    def get_circles(self):
        return Circle(
            pos=Vec2.random(),
            radius=randint(1, 10),
            color=Color.random()
        )
        


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

    def __iter__(self):
        return self.get_circles()  

    def get_circles(self):
        for agent in self.agents:
            yield agent.get_circle()
        
        new_agents = []
        for agent in self.agents:
            if agent.is_live:
                new_agents.append(agent)
            else:
                new_agents += agent.get_heirs()
        self.agents = new_agents
    
