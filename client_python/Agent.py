from api.GeoLocation import GeoLocation
from api.Node import Node


class Agent:
    def __init__(self , id:int, location: GeoLocation , value , src , dest ,speed):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self. speed = speed
        self.pos = location #this is position in geo location
        self.curr_node: Node

    """
    if we want to change agent according to json file we read we can do that here.
    """
    def update_from_json(self, json_file:str):
        pass

    def onNOde(self)->bool:
        pass
