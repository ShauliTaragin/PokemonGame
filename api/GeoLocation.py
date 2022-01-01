import math


class GeoLocation:
    def __init__(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

    def rang_to_other(self, other_location: tuple):
        return math.sqrt((self.x - other_location[0]) ** 2 + (self.y - other_location[1]) ** 2)

    def get_has_tuple(self) -> tuple:
        return self.x, self.y, self.z
