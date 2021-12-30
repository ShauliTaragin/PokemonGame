import math


class GeoLocation:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def rang_to_other(self, other_location: tuple):
        return math.sqrt((self.x - other_location[0]) ** 2 + (self.y - other_location[1]) ** 2)

    def get_has_tuple(self) -> tuple:
        return self.x, self.y, self.z
