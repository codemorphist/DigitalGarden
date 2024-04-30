from dataclasses import dataclass
from vector import Vec2


@dataclass
class AgentGenom:
    length:             int
    length_deviation:   int

    size:               int
    size_changes:       float

    number_branches:    int
    angle_branches:     float
    angle_changes:      float

    turn:               Vec2
    random_turn:        Vec2
    random_angle:       float



# TODO :
class PlantGenom:
    pass
