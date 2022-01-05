from api.Edge import Edge
from api.GeoLocation import GeoLocation


class Pokemon:
    """
     @:param: Receiving all the arguments which we get for each agent from the server. Very basic constructor
    """

    def __init__(self, value: float, type: int, pos: GeoLocation, edge: Edge):
        self.value = value
        self.type = type
        self.pos = pos
        self.curr_edge = edge

    def __repr__(self):
        return "Pokemons src is :  {} , Pokemons dest is: {}".format(self.curr_edge.src, self.curr_edge.dst)