from __future__ import annotations
from .vector import Vec2
from .color import Color
from random import randint


class Circle:
    def __init__(self, pos: Vec2, radius: float, color: Color):
        self.pos = pos             
        self.radius = radius
        self.color = color

    @staticmethod
    def random() -> Circle:
        return Circle(
            Vec2.random(),
            randint(1, 20),
            Color.random()
        )

             


