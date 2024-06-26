from __future__ import annotations
from random import randint


class Color:
    def __init__(self, r: float, g: float, b: float, alpha: float = 1):
        """
        :param r: red   color value (from 0 to 255)
        :param g: green color value (from 0 to 255)
        :param b: blue  color value (from 0 to 255)
        """
        self._rgb = (self.norm(r), self.norm(g), self.norm(b))

    def norm(self, value: float) -> float:
        if value > 255:
            return 255
        elif value < 0:
            return 0
        else:
            return value

    @staticmethod
    def random() -> Color:
        return Color(
            randint(0, 255),
            randint(0, 255),
            randint(0, 255)
        ) 

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b

    @property
    def rgb(self):
        return tuple([int(v) for v in self._rgb]) 

    @property
    def orgb(self):
        return tuple([v / 255 for v in self.rgb])

    @property
    def hex(self):
        return "#%02x%02x%02x" % self.rgb

    @property
    def r(self):
        return self._rgb[0]

    @property
    def g(self):
        return self._rgb[1]

    @property
    def b(self):
        return self._rgb[2]

    def __add__(self, other):
        if isinstance(other, Color):
            sr, sg, sb = self
            rr, gg, bb = other
            return Color(
                (sr + rr),
                (sg + gg),
                (sb + bb)
            )
        else:
            raise TypeError(f"Invalid type {type(other)} to add to Color")

    def __sub__(self, other):
        if isinstance(other, Color):
            sr, sg, sb = self
            rr, gg, bb = other
            return Color(
                (sr - rr),
                (sg - gg),
                (sb - bb)
            )
        else:
            raise TypeError(f"Invalid type {type(other)} to sub from Color")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            new_value = [int(v * other) for v in self._rgb] 
            return Color(*new_value)
        else:
            raise TypeError(f"Invalid type {type(other)} to mul on Color")

    def __eq__(self, other) -> bool:
        if isinstance(other, Color):
            return self.rgb == other.rgb
        elif isinstance(other, tuple):
            return self.rgb == other
        else:
            return False

    def __str__(self) -> str:
        return str(self._rgb)
    
    def __repr__(self) -> str:
        return f"Color{self._rgb}"

    

