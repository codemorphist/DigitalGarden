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
        """
        :param agent_genom: Genom of Agent
        :param plant_genom: Genom of Plant
        :param generation: Generation of Agent
        :param start_pos: Start position of Agent
        """
        self.agent_genom = agent_genom
        self.plant_genom = plant_genom
        self.generation = generation
        self.pos = start_pos
        self.turn = Vec2(0, -1)

    def get_circle(self) -> Circle:
        """
        Return circle that draw Agent
        """

        # Get color values from genom
        r = self.agent_genom.red
        g = self.agent_genom.green
        b = self.agent_genom.blue

        color = Color(r, g, b)
        circle = Circle(self.pos, self.agent_genom.size, color)

        self.__grow_up__()

        return circle

    def __grow_up__(self):
        """
        Update genom and postion of Agent
        """
        r = self.agent_genom.red
        g = self.agent_genom.green
        b = self.agent_genom.blue

        rc = self.agent_genom.red_changes/255
        gc = self.agent_genom.green_changes/255
        bc = self.agent_genom.blue_changes/255

        c1 = Color(r, g, b)
        c2 = Color(rc, gc, bc)
        
        c1 += c2
        self.agent_genom.red = c1.r
        self.agent_genom.green = c1.g
        self.agent_genom.blue = c1.b

        self.agent_genom.size += self.agent_genom.size_changes / 100

        self.pos += self.turn.rotate(self.agent_genom.turn * pi / 180)
        self.turn = (self.turn + self.agent_genom.down / 100 * Vec2(0, 1)).ort
        rangle = self.agent_genom.random_turn * pi / 180
        self.turn = self.turn.rotate(uniform(-rangle, rangle))
        self.agent_genom.length -= 1

    @property
    def is_live(self) -> bool:
        """
        Return life status of Agent

        :return: True is Agent is live else False
        """
        return self.agent_genom.length > 0

    def get_heirs(self) -> list[Agent]:
        """
        Return heirs of Agent

        :return: list of new Agents (heirs of current Agent)
        """
        heirs = []
        heirs_genom = self.plant_genom.evolve(self.generation, self.agent_genom)

        if heirs_genom is None:
            return []

        n = self.agent_genom.number_branches
        for i in range(n):
            heir_genom = deepcopy(heirs_genom)

            a = self.agent_genom.angle_branches * pi / 180
            heir_genom.turn = heir_genom.turn + (n//2 * a + i * a)

            heir = Agent(agent_genom=heir_genom,
                         plant_genom=self.plant_genom, 
                         generation=self.generation+1, 
                         start_pos=self.pos)
            heirs.append(heir)

        return heirs

    def __repr__(self) -> str:
        return f"Agent(pos={self.pos}, agent_genom={self.agent_genom})"
