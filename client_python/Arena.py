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
        # self.actual_pokemons_in_graph : [Pokemon] = []
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

    def update_pokemons_lst(self, json_file, first_iter: bool)-> list:
        # self.pokemons_lst.clear()
        try:
            # self.pokemons_lst.clear()
            pokemons_to_allocate: list = []
            pokemons = json.loads(json_file,
                                  object_hook=lambda d: SimpleNamespace(**d)).Pokemons
            pokemons = [p.Pokemon for p in pokemons]
            for i in pokemons:
                d: str = i.pos
                x, y, z = d.split(',')
                edge = self.graph_algo.get_edge_on_point((float(x), float(y), float(z)), i.type)
                location = GeoLocation((float(x), float(y), float(z)))
                found_pokemon_exists = False
                for exiting_pokemon in self.pokemons_lst:
                    if exiting_pokemon.pos.x == location.x and exiting_pokemon.pos.y == location.y:
                        found_pokemon_exists = True
                        break
                if not found_pokemon_exists:
                    poki = Pokemon(i.value, i.type, location, edge)
                    if poki.curr_edge.src not in self.dijkstra_list:
                        g_algo = GraphAlgo(self.graph_algo.graph)
                        # init the dijkstra class
                        dijkstra = MinHeapDijkstra.DijkstraUsingMinHeap.Graph(g_algo)
                        dijkstra.dijkstra_Getmin_distances(poki.curr_edge.src)
                        self.dijkstra_list[poki.curr_edge.src] = list(dijkstra.heap_nodes)
                    # already_in_list=-1
                    # for current_pokes in self.actual_pokemons_in_graph:
                    #     if(current_pokes.pos.x == poki.pos.x and current_pokes.pos.y == poki.pos.y
                    #             and poki.curr_edge == current_pokes.curr_edge and poki.value == current_pokes.value):
                    #         already_in_list = 0
                    # if already_in_list == -1:
                    self.pokemons_lst.append(poki)
                    if first_iter:
                        self.pokemons_lst.clear()
                    pokemons_to_allocate.append(poki)
            return pokemons_to_allocate
        except Exception:
            print("problem with json load pokemon")

    """
    @:param json_file
    need to see in which way the server sends the json of the pokems/agent(if its json object ,string, etc..) 
    """

    def update_agent_lst(self, json_file , already_exists:bool):
        try:
            agents = json.loads(json_file,
                                object_hook=lambda d: SimpleNamespace(**d)).Agents
            agents = [agent.Agent for agent in agents]
            for i in agents:
                d: str = i.pos
                x, y, z = d.split(',')
                location = GeoLocation((float(x), float(y), float(z)))
                if already_exists is True:
                    double007 = Agent(i.id, location, i.value, i.src, i.dest, i.speed)
                    if double007.src not in self.dijkstra_list:
                        g_algo = GraphAlgo(self.graph_algo.graph)
                        # init the dijkstra class
                        dijkstra = MinHeapDijkstra.DijkstraUsingMinHeap.Graph(g_algo)
                        dijkstra.dijkstra_Getmin_distances(double007.src)
                        self.dijkstra_list[double007.src] = list(dijkstra.heap_nodes)
                    self.agents_lst.append(double007)
                else:
                    for existing_agent in self.agents_lst:
                        if existing_agent.id == i.id:
                            existing_agent.update_from_given_values(location, i.speed, i.dest, i.src, i.value)
                            break
        except Exception:
            print("problem with json load pokemon")

    def place_agents_at_beginning(self, first_pkoemons: list)-> dict:
        i = 0
        list_of_agent = {}
        while i < self.info_dict["agents"] and i < self.info_dict["pokemons"]:
            pokemon_src = first_pkoemons[i].curr_edge.src
            string_of_src="{}".format(pokemon_src)
            json_to_agent = "{\"id\":"+string_of_src+"}"
            list_of_agent[i]=json_to_agent
            i += 1
        return list_of_agent