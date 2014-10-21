from __future__ import division
import math

# handles vector math
class Vector:
    # set initial values
    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def angle(self):
        if self.y >= 0:
            return -math.acos(self*Vector(1, 0) / self.mag())
        else:
            return math.acos(self*Vector(1, 0) / self.mag())

    # return the magnitude
    def mag (self):
        return self.magSquared () ** 0.5

    # returns the magnitude squared (faster, no square root operation)
    def magSquared (self):
        return sum ([self.x**2, self.y**2])

    # return vector of magnitude m in same direction
    def setMag (self, m):
        return self * (1.0 * m / self.mag ())

    def rotate(self, t):
        return Vector(self.x*math.cos(t) - self.y*math.sin(t), self.y*math.cos(t) + self.x*math.sin(t))

    # return normal vector
    def normal (self):
        return self.setMag (1)

    # return vector as a list
    def toList (self):
        return [self.x, self.y]

    # adds two vectors/ adds vector with scalar
    def __add__ (self, other):
        if isinstance (other, Vector):
            return Vector (self.x+other.x, self.y+other.y)
        elif isinstance (other, int) or isinstance (other, float):
            return Vector (self.x+other, self.y+other)
        else:
            return NotImplemented

    def __radd__ (self, other):
        return self + other

    def __iadd__ (self, other):
        return self + other

    def __sub__ (self, other):
        return self + -1*other

    def __rsub__ (self, other):
        return self - other

    def __isub__ (self, other):
        return self - other

    def __neg__ (self):
        return self * -1

    # returns dot product if two vectors / scalar multiplication if scalar
    def __mul__ (self, other):
        if isinstance (other, Vector):
            return self.x*other.x + self.y*other.y
        elif isinstance (other, int) or isinstance (other, float):
            return Vector (self.x*other, self.y*other)
        else:
            return NotImplemented

    def __rmul__ (self, other):
        return self * other

    def __imul__ (self, other):
        return self * other

    # returns true if dimension and coordinates of both vectors are equal
    def __eq__ (self, other):
        if self.x != other.x or self.y != other.y:
            return False
        return True
