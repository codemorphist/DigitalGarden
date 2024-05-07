from __future__ import annotations
from dataclasses import dataclass
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
    # color_from_ancestor: float
    # color_deviation: float

    number_branches: int
    angle_branches: float
    angle_deviation: float

    turn: Vec2
    # random_turn: Vec2
    random_angle: float
    down: float

    @staticmethod
    def random() -> AgentGenom:
        r, g, b = Color.random()
        rc, gc, bc = Color.random()

        return AgentGenom(
            randint(20, 150),
            0,
            randint(1, 3),
            randint(20, 60),
            randint(0, 3), 
            uniform(-0.05, 0.05),
            r, g, b, 
            rc, gc, bc,
            randint(1, 2),
            randint(45, 270),
            randint(20, 90),
            Vec2(0, -1),
            uniform(0, 20 * pi / 180),
            randint(-20, 20)
        )


class PlantGenom:
    def __init__(self, genom: list[AgentGenom]):
        self._genom = genom

    def evolve(self,
               generation: int, 
               agent_genom: AgentGenom) -> AgentGenom:
        evolved_genom = self._genom[generation-1]

        size_percent = evolved_genom.size_from_ancestor / 100 
        evolved_genom.size = (evolved_genom.size_from_level + evolved_genom.size) / 2
        evolved_genom.size = size_percent * (agent_genom.size + evolved_genom.size)

        evolved_genom.length += randint(0, agent_genom.length_deviation)
        evolved_genom.angle_branches += agent_genom.angle_deviation

        return evolved_genom

    @staticmethod
    def random() -> PlantGenom:
        return PlantGenom([
            AgentGenom.random() for _ in range(9)
        ])
