from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from tools import Vec2, Color
from random import randint
from copy import deepcopy


@dataclass
class AgentGenom:
    length: int
    length_deviation: int

    size: float
    size_from_ancestor: float
    size_from_level: float
    size_changes: float

    red: int
    green: int
    blue: int
    red_changes: int
    green_changes: int
    blue_changes: int
    color_from_ancestor: float
    color_deviation: float

    number_branches: int
    angle_branches: float
    angle_deviation: float

    turn: Vec2
    random_turn: int
    down: float

    @staticmethod
    def random() -> AgentGenom:
        r, g, b = Color.random()
        rc, gc, bc = Color.random()

        return AgentGenom(
            length=50,
            length_deviation=0,
            size=randint(1, 6),
            size_from_ancestor=randint(30, 80),
            size_from_level=randint(2, 6), 
            size_changes=randint(-5, 5),
            red=r, green=g, blue=b, 
            red_changes=rc, green_changes=gc, blue_changes=bc,
            color_deviation=randint(-10, 10),
            color_from_ancestor=randint(0, 80),
            number_branches=2,
            angle_branches=45,
            angle_deviation=0,
            turn=0,
            random_turn=20,
            down=0
        )


class PlantGenom:
    def __init__(self, genom: list[AgentGenom]):
        self._genom = genom

    def evolve(self,
               generation: int, 
               agent_genom: AgentGenom) -> Optional[AgentGenom]:
        """
        Evolute genom of Agent to new generation
        """
        if generation >= len(self._genom):
            return None


        evolved_genom = deepcopy(self._genom[generation])

        size_percent = evolved_genom.size_from_ancestor / 100 
        # evolved_genom.size = (evolved_genom.size_from_level + evolved_genom.size) / 2
        evolved_genom.size = size_percent * (agent_genom.size + evolved_genom.size)

        len_deviation = agent_genom.length_deviation
        evolved_genom.length += randint(-len_deviation, len_deviation)
        evolved_genom.angle_branches += agent_genom.angle_deviation
    
        ar = agent_genom.red + evolved_genom.color_deviation
        ag = agent_genom.green + evolved_genom.color_deviation
        ab = agent_genom.blue + evolved_genom.color_deviation


        sr = evolved_genom.red
        sg = evolved_genom.green
        sb = evolved_genom.blue

        acolor = Color(ar, ag, ab)
        scolor = Color(sr, sg, sb)
    
        r, g, b = ((acolor + scolor)*(evolved_genom.color_from_ancestor/100)).rgb

        evolved_genom.red = r
        evolved_genom.green = g
        evolved_genom.blue = b

        return evolved_genom

    @staticmethod
    def random(generations: int = 9) -> PlantGenom:
        return PlantGenom([
            AgentGenom.random() for _ in range(generations)
        ])
