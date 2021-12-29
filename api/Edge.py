class Edge:
    def __init__(self , src: int, dst: int , weight:int ):
        self.src = src
        self.dst = dst
        self.weight = weight
        self.edge_type = src - dst

