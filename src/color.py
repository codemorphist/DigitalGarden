from vector import Vector


class Color(Vector):
    def __init__(self, r: int, g: int, b: int, alpha: int = 1):
        """
        :param r: red   color value (from 0 to 255)
        :param g: green color value (from 0 to 255)
        :param b: blue  color value (from 0 to 255)
        """
        super().__init__(r, g, b)

    @property
    def rgb(self):
        return self.values

    @property
    def r(self):
        return self.value[0]

    @property
    def g(self):
        return self.value[1]

    @property
    def b(self):
        return self.value[2]

    def __str__(self) -> str:
        return str(self._rgb)
    
    def __repr__(self) -> str:
        return f"Color{self._rgb}"

    
