from api.Edge import Edge
from api.GeoLocation import GeoLocation


class Node:
    def __init__(self, key: int, geolocation: GeoLocation):
        self.key = key
        self.weight = 0
        self.geolocation = geolocation
        self.tag = 0
        self.outEdges = {}
        self.inEdges = {}

    # print the node as we want
    def __repr__(self):
        return "{}: |edges out| {} |edges in| {}".format(self.key, len(self.outEdges), len(self.inEdges))

    def __str__(self):
        return "{}: |edges out| {} |edges in| {}".format(self.key, self.outEdges, self.inEdges)

    # add out edge
    def add_out_edge(self, edge: Edge):
        self.outEdges[edge.dst] = edge
        self.outEdges.values()

    # add in edge
    def add_in_edge(self, weight: float, src: int):
        self.inEdges[src] = weight

