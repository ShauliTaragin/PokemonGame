from api.GraphAlgo import GraphAlgo
from client_python.Agent import Agent
from client_python.Pokemon import Pokemon


class Arena:
    Eps = 0.001

    def __init__(self):
        self.pokemons_lst: [Pokemon]
        self.agents_lst: [Agent]
        self.algorithm: GraphAlgo
        self.info_lst: [str]

    """
    need to see in which way the server sends the json of the pokems/agent(if its json object ,string, etc..) 
    """
    def update_pokemons_lst(self, json_file):
        pass

    """
    @:param json_file
    need to see in which way the server sends the json of the pokems/agent(if its json object ,string, etc..) 
    """
    def update_agent_lst(self, json_file):
        pass
