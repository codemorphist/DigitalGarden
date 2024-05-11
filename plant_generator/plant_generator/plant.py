from __future__ import annotations
from plant_generator.genom import PlantGenom
from plant_generator.agent import Agent
from tools import Vec2


class Plant:
    def __init__(self, 
                 plant_genom: PlantGenom,
                 start_pos: Vec2):
        """
        :param plant_genom: Genom of Plant
        :param start_pos: Start postion of Plant
        """
        self.plant_genom = plant_genom
        self.agents = []

        # Total count of agents
        self.total = 1
        for agent in self.plant_genom.genom[::-1]:
            self.total *= agent.number_branches 
            self.total += agent.length
        self.total += 1

        # Conut of dead agents
        self.drawed = 0

        self.init_agents(start_pos)

    def init_agents(self, start_pos: Vec2):
        """
        Init first Agent of Plant
        """
        self.agents.append(Agent(
            agent_genom=self.plant_genom.genom[0],
            plant_genom=self.plant_genom,
            generation=0,
            start_pos=start_pos
        ))

    def is_growing(self) -> bool:
        """
        Return life status of Plant
        """
        return len(self.agents) > 0

    def __iter__(self):
        return self.get_circles()  

    def get_circles(self):
        """
        Get circles from all Agents of Plant
        """
        for agent in self.agents:
            circle = agent.get_circle()
            self.drawed += 1
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
            Vec2(0, 300)
        )

    def __del__(self):
        del self.plant_genom
        del self
    
