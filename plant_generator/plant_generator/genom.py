from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from tools import Vec2, Color
from random import randint, uniform
from math import pi


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
    # color_deviation: float

    number_branches: int
    angle_branches: float
    angle_deviation: float

    turn: Vec2
    random_turn: int
    random_angle: float
    down: float

    @staticmethod
    def random() -> AgentGenom:
        r, g, b = Color.random()
        rc, gc, bc = Color.random()

        return AgentGenom(
            length=randint(20, 150),
            length_deviation=0,
            size=randint(1, 3),
            size_from_ancestor=randint(20, 60),
            size_from_level=randint(0, 3), 
            size_changes=uniform(-0.05, 0.05),
            red=r, green=g, blue=b, 
            red_changes=rc, green_changes=gc, blue_changes=bc,
            color_from_ancestor=randint(0, 80),
            number_branches=randint(1, 2),
            angle_branches=randint(45, 270),
            angle_deviation=randint(20, 90),
            turn=randint(-10, 10),
            random_turn=randint(0, 40),
            random_angle=uniform(0, 20 * pi / 180),
            down=randint(-2, 2)
        )


class PlantGenom:
    def __init__(self, genom: list[AgentGenom]):
        self._genom = genom

    def evolve(self,
               generation: int, 
               agent_genom: AgentGenom) -> Optional[AgentGenom]:
        if generation >= len(self._genom):
            return None

        evolved_genom = self._genom[generation]

        size_percent = evolved_genom.size_from_ancestor / 100 
        evolved_genom.size = (evolved_genom.size_from_level + evolved_genom.size) / 2
        evolved_genom.size = size_percent * (agent_genom.size + evolved_genom.size)

        evolved_genom.length += randint(0, agent_genom.length_deviation)
        evolved_genom.angle_branches += agent_genom.angle_deviation
    
        ar = agent_genom.red
        ag = agent_genom.green
        ab = agent_genom.blue

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
    def random() -> PlantGenom:
        return PlantGenom([
            AgentGenom.random() for _ in range(9)
        ])
