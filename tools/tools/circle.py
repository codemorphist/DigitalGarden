from __future__ import annotations


from tools.vector import Vec2
from tools.color import Color
from random import randint
from dataclasses import dataclass


@dataclass
class Circle:
    pos: Vec2
    radius: float
    color: Color

    @staticmethod
    def random() -> Circle:
        return Circle(
            Vec2.random(),
            randint(10, 20),
            Color.random()
        )

    def __repr__(self) -> str:
        return f"Circle(position={self.pos}, radius={self.radius}, color={self.color})"

