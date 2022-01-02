import json
from types import SimpleNamespace

from api import MinHeapDijkstra
from api.DiGraph import DiGraph
from api.GeoLocation import GeoLocation
from api.GraphAlgo import GraphAlgo
from api.Edge import Edge
from client_python.Agent import Agent
from client_python.Pokemon import Pokemon
from client import Client


class Arena:
    Eps = 0.001

    def __init__(self, game_info: str, client: Client):
        self.pokemons_lst: [Pokemon] = []
        self.agents_lst: [Agent] = []
        self.graph_algo: GraphAlgo = GraphAlgo()
        self.info_dict = {}
        self.dijkstra_list = {}
        self.client = Client
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
            self.graph_algo.load_from_json(self.info_dict["graph"])
        else:
            self.info_dict = {}

    """
    need to see in which way the server sends the json of the pokems/agent(if its json object ,string, etc..) 
    """

    def update_pokemons_lst(self, json_file):
        self.pokemons_lst.clear()
        try:
            self.pokemons_lst.clear()
            pokemons = json.loads(json_file,
                                  object_hook=lambda d: SimpleNamespace(**d)).Pokemons
            pokemons = [p.Pokemon for p in pokemons]
            for i in pokemons:
                d: str = i.pos
                x, y, z = d.split(',')
                edge = self.graph_algo.get_edge_on_point((float(x), float(y), float(z)), i.type)
                location = GeoLocation((float(x), float(y), float(z)))
                poki = Pokemon(i.value, i.type, location, edge)
                if poki.curr_edge.src not in self.dijkstra_list:
                    g_algo = GraphAlgo(self.graph_algo.graph)
                    # init the dijkstra class
                    dijkstra = MinHeapDijkstra.DijkstraUsingMinHeap.Graph(g_algo)
                    dijkstra.dijkstra_Getmin_distances(poki.curr_edge.src)
                    self.dijkstra_list[poki.curr_edge.src] = list(dijkstra.heap_nodes)
                self.pokemons_lst.append(poki)

        except Exception:
            print("problem with json load pokemon")

    """
    @:param json_file
    need to see in which way the server sends the json of the pokems/agent(if its json object ,string, etc..) 
    """

    def update_agent_lst(self, json_file):
        self.agents_lst.clear()
        try:
            agents = json.loads(json_file,
                                object_hook=lambda d: SimpleNamespace(**d)).Agents
            agents = [agent.Agent for agent in agents]
            for i in agents:
                d: str = i.pos
                x, y, z = d.split(',')
                location = GeoLocation((float(x), float(y), float(z)))
                double007 = Agent(i.id, location, i.value, i.src, i.dest, i.speed)
                if double007.src not in self.dijkstra_list:
                    g_algo = GraphAlgo(self.graph_algo.graph)
                    # init the dijkstra class
                    dijkstra = MinHeapDijkstra.DijkstraUsingMinHeap.Graph(g_algo)
                    dijkstra.dijkstra_Getmin_distances(double007.src)
                    self.dijkstra_list[double007.src] = list(dijkstra.heap_nodes)
                self.agents_lst.append(double007)
        except Exception:
            print("problem with json load pokemon")

    def place_agents_at_beginning(self)-> dict:
        i = 0
        list_of_agent = {}
        while i < self.info_dict["agents"] and i < self.info_dict["pokemons"]:
            pokemon_src = self.pokemons_lst[i].curr_edge.src
            string_of_src="{}".format(pokemon_src)
            json_to_agent = "{\"id\":"+string_of_src+"}"
            list_of_agent[i]=json_to_agent
            i += 1
        return list_of_agent
