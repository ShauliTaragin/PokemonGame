from api.Node import Node


class Agent:
    def __init__(self , id:int):
        self.id = id
        self.value = 0
        self.src = 0
        self.dest = 0
        self. speed = 0.0
        self.pos = 0 #this is position in geo location
        self.curr_node: Node

    """
    if we want to change agent according to json file we read we can do that here.
    """
    def update_from_json(self, json_file:str):
        pass

    def onNOde(self)->bool:
        pass
