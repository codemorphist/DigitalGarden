from __future__ import annotations

import turtle

from tools.vector import Vec2
from tools.color import Color
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
            randint(10, 20),
            Color.random()
        )

    def __repr__(self) -> str:
        return f"Circle(position={self.pos}, radius={self.radius}, color={self.color})"
             
    def canvas_turtle_draw(self, canvas_turtle):
        """

        This Circle method draws a given circle with a given turtle,
        which is thought as tied to a specific canvas; the parameters of
        the drawn circle match those of the Object.

        """
        canvas_turtle.speed(0)
        # turtle.colormode(255)
        canvas_turtle.penup()
        canvas_turtle.goto(self.pos.x, self.pos.y)
        canvas_turtle.forward(self.radius)
        canvas_turtle.left(90)
        canvas_turtle.pendown()
        # canvas_turtle.pencolor(self.color.rgb)
        canvas_turtle.circle(self.radius)
        canvas_turtle.penup()
        canvas_turtle.goto(self.pos.x, self.pos.y)
