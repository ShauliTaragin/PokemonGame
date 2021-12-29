from api.Edge import Edge


class Pokemon:
    def __init__(self , value:float , type:int , pos:tuple):
        self.value = value
        self.type = type
        self.pos = pos
        self.curr_edge: Edge

