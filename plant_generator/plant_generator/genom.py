from dataclasses import dataclass
from tools import Vec2


@dataclass
class AgentGenom:
    length: int
    length_deviation: int

    size: float
    size_from_ancestor: float
    size_from_level: float
    size_changes: float

    # red: int
    # green: int
    # blue: int
    # red_changes: int
    # green_changes: int
    # blue_changes: int
    # color_from_ancestor: float
    # color_deviation: float

    number_branches: int
    angle_branches: float
    angle_deviation: float

    turn: Vec2
    random_turn: Vec2
    random_angle: float


class PlantGenom:
    def __init__(self, genom: list[AgentGenom]):
        self._genom = genom

    def evolve(generation: int, 
               agent_genom: AgentGenom) -> AgentGenom:
        pass
