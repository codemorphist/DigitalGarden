class Vector:
    def __init__(self, *values):
        for value in values:
            if not isinstance(value, (int, float, complex)):
                raise ValueError(f"Invalid type for Vector value: {type(value).__name__}")

        self._values: tuple = tuple(values)
        self._size: int = len(values)

    @property
    def size(self):
        return self._size

    @property
    def values(self):
        return self._values

    def __iter__(self):
        for val in self._values:
            yield val

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError(f"Can't add {type(other).__name__} to {type(self).__name__}")

        if self.size != other.size:
            raise TypeError("Can't add Vectors with different size")

        new_values = []
        for self_val, other_val in zip(self.values, other.values):
            new_values.append(self_val + other_val)

        return type(self)(*new_values)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError(f"Can't sub {type(other).__name__} from {type(self).__name__}")

        if self.size != other.size:
            raise TypeError("Can't sub Vectors with different size")

        return self + -1 * other

    def __mul__(self, other: int | float | complex):
        if not isinstance(other, (int, float, complex)):
            raise TypeError(f"Can't multiply Vector by {other}")

        new_values = []
        for val in self.values:
            new_values.append(val * other)

        return type(self)(*new_values)
        
    def __truediv__(self, other: int | float | complex):
        if not isinstance(other, (int, float, complex)):
            raise Exception(f"Can't divide Vector by {other}")
    
        if other == 0:
            raise ZerroDivisionError("Can't divide Vector by Zero")

        return self * (1/other)

    def __rmul__(self, other):
        return self * other

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector):
            return False
        return self.values == other.values

    def __str__(self) -> str:
        return str(self.values)

    def __repr__(self) -> str:
        return f"Vector{self.values}"
    

class Vec2(Vector):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    @property 
    def x(self) -> float:
        return self._values[0]

    @property 
    def y(self) -> float:
        return self._values[1]


class Vec3(Vector):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)

    @property 
    def x(self) -> float:
        return self._values[0]

    @property 
    def y(self) -> float:
        return self._values[1]

    @property
    def z(self):
        return self._z



