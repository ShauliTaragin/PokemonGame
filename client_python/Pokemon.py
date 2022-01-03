from api.Edge import Edge
from api.GeoLocation import GeoLocation


class Pokemon:
    def __init__(self, value: float, type: int, pos: GeoLocation, edge: Edge):
        self.value = value
        self.type = type
        self.pos = pos
        self.curr_edge = edge