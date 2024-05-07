from __future__ import annotations
from random import uniform
from plant_generator.genom import AgentGenom, PlantGenom
from tools import Vec2, Circle, Color
from math import pi
from copy import deepcopy


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

        if self.generation > 1:
            rangle = self.agent_genom.random_angle
            turn = self.agent_genom.turn
            self.agent_genom.turn = turn.rotate(uniform(-rangle, rangle))

    def get_circle(self) -> Circle:
        r = self.agent_genom.red
        g = self.agent_genom.green
        b = self.agent_genom.blue

        rc = self.agent_genom.red_changes/255
        gc = self.agent_genom.green_changes/255
        bc = self.agent_genom.blue_changes/255

        c1 = Color(r, g, b)
        c2 = Color(rc, gc, bc)

        circle = Circle(self.pos, self.agent_genom.size, c1)

        c1 += c2
        self.agent_genom.red = c1.r
        self.agent_genom.green = c1.g
        self.agent_genom.blue = c1.b

        self.agent_genom.size += self.agent_genom.size_changes 
        self.pos += self.agent_genom.turn
        self.agent_genom.length -= 1

        return circle

    @property
    def is_live(self) -> bool:
        return self.agent_genom.length > 0

    def get_heirs(self) -> list[Agent]:
        heirs = []
        heirs_genom = self.plant_genom.evolve(
            self.generation, self.agent_genom)

        n = self.agent_genom.number_branches
        for i in range(n):
            heir_genom = deepcopy(heirs_genom)

            a = self.agent_genom.angle_branches * pi / 180
            heir_genom.turn = heir_genom.turn.rotate(n//2 * a + i * a)

            heir = Agent(agent_genom=heir_genom,
                         plant_genom=self.plant_genom, 
                         generation=self.generation+1, 
                         start_pos=self.pos)
            heirs.append(heir)

        return heirs

    def __repr__(self) -> str:
        return f"Agent(pos={self.pos}, agent_genom={self.agent_genom})"


class EmptyAgent(Agent):
    def __init__(self, plant_genom: PlantGenom, 
                 start_pos: Vec2):
        empty_agent_genom = AgentGenom(
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, Vec2(0, 0), 0
        )
        super().__init__(
            agent_genom=empty_agent_genom,
            plant_genom=plant_genom,
            generation=0,
            start_pos=start_pos 
        )

