from __future__ import annotations


from tools.vector import Vec2
from tools.color import Color
from random import randint


class Circle:
    def __init__(self, pos: Vec2, radius: float, color: Color = Color(0, 0, 0)):
        self.pos = pos             
        self.radius = radius
        self.color = color

    @staticmethod
    def random() -> Circle:
        return Circle(
            Vec2.random(),
            randint(10, 20),
            Color.random()
        )

    def __repr__(self) -> str:
        return f"Circle(position={self.pos}, radius={self.radius}, color={self.color})"

