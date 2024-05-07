from __future__ import annotations
from plant_generator.genom import AgentGenom, PlantGenom
from tools import Vec2, Circle


class Agent:
    def __init__(self, 
                 agent_genom: AgentGenom, 
                 plant_genom: PlantGenom,
                 generation: int,
                 start_pos: Vec2):
        self.agent_genom = agent_genom
        self.plant_genom = plant_genom
        self.generation = generation
        self.pos = start_pos

    def get_circle(self) -> Circle:
        pass

    @property
    def is_live(self) -> bool:
        pass

    def get_heirs(self) -> list[Agent]:
        pass


class EmptyAgent(Agent):
    def __init__(self, plant_genom: PlantGenom, 
                 start_pos: Vec2):
        empty_agent_genom = AgentGenom(
            0, 0, 0, 0, 0, 0, 0, 0, 0, Vec2(0, 0), 0, 0
        )
        super().__init__(
            agent_genom=empty_agent_genom,
            plant_genom=plant_genom,
            generation=0,
            start_pos=start_pos 
        )

