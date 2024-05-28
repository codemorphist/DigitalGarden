from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from tools import Color
from random import randint, uniform
from copy import deepcopy


@dataclass
class AgentGenom:
    length: int
    length_deviation: int

    size: int
    size_from_ancestor: int
    size_from_level: int
    size_changes: int

    red: int
    green: int
    blue: int
    red_changes: int
    green_changes: int
    blue_changes: int
    color_from_ancestor: int
    color_deviation: int

    number_branches: int
    angle_branches: int
    angle_deviation: int

    turn: int
    random_turn: int
    down: int

    @staticmethod
    def random() -> AgentGenom:
        r, g, b = Color.random()
        rc, gc, bc = Color.random()

        return AgentGenom(
            length=randint(20, 150),
            length_deviation=randint(0, 30),
            size=randint(5, 80),
            size_from_ancestor=randint(10, 90),
            size_from_level=randint(5, 100),
            size_changes=randint(-30, 30),
            red=r, green=g, blue=b,
            red_changes=rc, green_changes=gc, blue_changes=bc,
            color_deviation=randint(-20, 20),
            color_from_ancestor=randint(0, 80),
            number_branches=randint(1, 3),
            angle_branches=randint(0, 120),
            angle_deviation=randint(10, 30),
            turn=randint(-120, 120),
            random_turn=randint(0, 80),
            down=randint(-30, 30)
        )

    @classmethod
    def attr_list(cls) -> list:
        class_attributes = [attr for attr in AgentGenom.__annotations__]
        return class_attributes

    @staticmethod
    def empty() -> AgentGenom:
        """
        Return empty AgentGenom
        """
        return AgentGenom(*[0  for _ in AgentGenom.attr_list()])

    def __iter__(self):
        for attr in self.attr_list():
            yield attr, getattr(self, attr)


class PlantGenom:
    def __init__(self, genom: list[AgentGenom]):
        self.genom = genom

    def evolve(self,
               generation: int,
               agent_genom: AgentGenom) -> Optional[AgentGenom]:
        """
        Evolute genom of Agent to new generation
        """
        if generation >= len(self.genom):
            return None

        evolved_genom = deepcopy(self.genom[generation])

        size_percent = evolved_genom.size_from_ancestor / 100
        evolved_genom.size = (evolved_genom.size_from_level + evolved_genom.size) / 2
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

        r, g, b = ((acolor + scolor) * (evolved_genom.color_from_ancestor / 100)).rgb

        evolved_genom.red = r
        evolved_genom.green = g
        evolved_genom.blue = b

        return evolved_genom

    def __iter__(self):
        """
        Convert genom to dict in next format

        'Agent 1': { ... },
        'Agent 2': { ... },
                     ...
        """
        for i, agent in enumerate(self.genom):
            yield f"Agent{i}", dict(agent)

    @staticmethod
    def random(generations: int = 9) -> PlantGenom:
        return PlantGenom([
            AgentGenom.random() for _ in range(generations)
        ])

    @staticmethod
    def dict_is_genome(entries_dict: dict) -> bool:
        """
        This static method echoes that of the UserFrame class, but is instead
        used for the case when the variables are ordinary strings; that is to say,
        it is a simple check for being capable of being seen as a genome
        """
        try:
            for _, val in entries_dict.items():
                int(val)
            return True
        except:
            return False

    @staticmethod
    def export_genom(genom: PlantGenom) -> str:
        """
        Impoort genom to string

        Output format
                A1  A2  A3  ..
            G1
            G2
            G3
            ..
        """
        transposed = list(zip(*genom.table()))
        agents_str = [" ".join(map(str, map(int, agent))) for agent in transposed]
        return "\n".join(agents_str)

    @staticmethod
    def import_genom(genom: str) -> PlantGenom:
        """
        Export genom from string

        Imput format
                A1  A2  A3  ..
            G1
            G2
            G3
            ..
        """
        values = []
        for row in genom.rstrip().split("\n"):
            val_row = []
            for val in row.rstrip().split():
                val_row.append(int(val))
            values.append(val_row)

        agents = []
        for c in range(len(values[0])):
            gens = []
            for v in range(len(values)):
                gens.append(values[v][c])
            agents.append(AgentGenom(*gens))
        return PlantGenom(agents)

    @staticmethod
    def empty(agents: int = 9) -> PlantGenom:
        genom = []
        for _ in range(agents):
            genom.append(AgentGenom.empty())
        return PlantGenom(genom)

    def table(self) -> list[list]:
        genom_table = []

        for _, agent in self:
            a = []
            for gen in agent.values():
                a.append(gen)
            genom_table.append(a)

        return genom_table

    def __repr__(self) -> str:
        return f"PlantGenom({self.genom})" 
