from api.GeoLocation import GeoLocation


class Edge:
    def __init__(self, src: int, dst: int, weight: int, src_location: GeoLocation, dst_location: GeoLocation):
        self.src = src
        self.dst = dst
        self.weight = weight
        self.edge_type = src - dst
        self.src_location = src_location
        self.dst_location = dst_location
        self.m, self.b = self.line_equation()[0], self.line_equation()[1]

    def line_equation(self) -> tuple:
        line_m = (self.src_location.x - self.dst_location.x) / (self.src_location.y - self.dst_location.y)
        line_b = (self.src_location.y - line_m * self.src_location.x)
        return line_m, line_b

    def get_point_on_edge(self, x: float) -> float:
        return self.m * x + self.b
