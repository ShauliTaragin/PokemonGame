from api.GeoLocation import GeoLocation
from api.Node import Node


class Agent:
    """
    @:param: Receiving all the arguments which we get for each agent from the server. Very basic constructor
    """

    def __init__(self, id: int, location: GeoLocation, value, src, dest, speed):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = location  # this is position in geo location
        self.curr_node: Node
        # these following class fields will help us with computing our main algorithm meaning which pokemon is allocated to
        # which agent and the path each agent will have to take
        self.current_time_of_path = 0
        self.agents_path = []
        self.pokemons_to_eat = []
        self.permutaion = []


    """
    A function which is the same as the constructor however here we only update the parameters which change every move we make
    """
    def update_from_given_values(self, pos: GeoLocation, speed: float, dest: int, src: int, value: int):
        self.pos = pos
        self.speed = speed
        self.dest = dest
        self.src = src
        self.value = value

