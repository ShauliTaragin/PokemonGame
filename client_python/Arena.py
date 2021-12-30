import json
from types import SimpleNamespace

from api.GeoLocation import GeoLocation
from api.GraphAlgo import GraphAlgo
from client_python.Agent import Agent
from client_python.Pokemon import Pokemon
from client import Client


class Arena:
    Eps = 0.001

    def __init__(self, game_info: str):
        self.pokemons_lst: [Pokemon]=[]
        self.agents_lst:[Agent] = []
        self.algorithm: GraphAlgo
        self.info_dict = {}
        if game_info is not None:
            namespace = json.loads(game_info,
                                   object_hook=lambda d: SimpleNamespace(**d)).GameServer
            self.info_dict["moves"] = namespace.moves
            self.info_dict["pokemons"] = namespace.pokemons
            self.info_dict["is_logged_in"] = namespace.is_logged_in
            self.info_dict["grade"] = namespace.grade
            self.info_dict["game_level"] = namespace.game_level
            self.info_dict["max_user_level"] = namespace.max_user_level
            self.info_dict["id"] = namespace.id
            self.info_dict["graph"] = namespace.graph
            self.info_dict["agents"] = namespace.agents
        else:
            self.info_dict = {}

    """
    need to see in which way the server sends the json of the pokems/agent(if its json object ,string, etc..) 
    """

    def update_pokemons_lst(self, json_file):
        try:
            pokemons = json.loads(json_file,
                                  object_hook=lambda d: SimpleNamespace(**d)).Pokemons
            pokemons = [p.Pokemon for p in pokemons]
            for i in pokemons:
                d:str = i.pos
                x,y,z = d.split(',')
                location = GeoLocation(float(x) , float(y) , float(z))
                poki = Pokemon(i.value , i.type , location)
                self.pokemons_lst.append(poki)
        except Exception:
            print("problem with json load pokemon")

    """
    @:param json_file
    need to see in which way the server sends the json of the pokems/agent(if its json object ,string, etc..) 
    """

    def update_agent_lst(self, json_file):
        try:
            agents = json.loads(json_file,
                                  object_hook=lambda d: SimpleNamespace(**d)).Agents
            agents = [agent.Agent for agent in agents]
            for i in agents:
                d: str = i.pos
                x, y, z = d.split(',')
                location = GeoLocation(float(x), float(y), float(z))
                double007 = Agent(i.id, location , i.value , i.src , i.dest , i.speed)
                self.agents_lst.append(double007)
        except Exception:
            print("problem with json load pokemon")
