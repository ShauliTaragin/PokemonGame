from api.GeoLocation import GeoLocation
from api.Node import Node


class Agent:
    def __init__(self , id:int, location: GeoLocation , value , src , dest ,speed):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = location #this is position in geo location
        self.curr_node: Node
        self.agents_path = []
        self.pokemons_to_eat = []
        self.permutaion = []
    """
    if we want to change agent according to json file we read we can do that here.
    """
    def update_from_given_values(self, pos: GeoLocation, speed: float, dest: int, src: int, value: int):
        self.pos = pos
        self.speed = speed
        self.dest = dest
        self.src = src
        self.value = value

    def onNOde(self)->bool:
        pass
