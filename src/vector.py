"""
Vector2D class optimized for calculation efficiency
"""

import numpy as np

class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self.vector = np.array([x, y], dtype=np.float64)

    def copy(self):
        return Vector2D(*self.vector.copy())

    @property
    def x(self):
        return self.vector[0]

    @property
    def y(self):
        return self.vector[1]

    @property
    def Args(self):
        return tuple(self.vector)

    @property
    def magnitude(self):
        return np.linalg.norm(self.vector)

    def dot(self, other):
        return np.dot(self.vector, other.vector)

    def __add__(self, other):
        return Vector2D(*(self.vector + other.vector))

    def __sub__(self, other):
        return Vector2D(*(self.vector - other.vector))

    def __mul__(self, scalar):
        return Vector2D(*(self.vector * scalar))

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Vector2D(*(self.vector / scalar))

    def __str__(self):
        return f"(x={self.vector[0]}, y={self.vector[1]})"
