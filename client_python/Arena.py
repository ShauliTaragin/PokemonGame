import json
from types import SimpleNamespace

from api import MinHeapDijkstra
from api.GeoLocation import GeoLocation
from api.GraphAlgo import GraphAlgo
from client_python.Agent import Agent
from client_python.Pokemon import Pokemon
from client_python.client import Client


class Arena:
    Eps = 0.001

    def __init__(self, game_info: str):
        # create the arena variables
        self.pokemons_lst: [Pokemon] = []
        self.agents_lst: [Agent] = []
        self.graph_algo: GraphAlgo = GraphAlgo()
        self.info_dict = {}
        self.dijkstra_list = {}
        self.client = Client
        # reading the json of the game information from the client
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
    this function will get the pokemons from the server and the it will create for each pokemon object with his values
    and will add him to the arena pokemon list
    """

    def update_pokemons_lst(self, json_file, first_iter: bool) -> list:
        try:
            # first clear the current list of available pokemons
            self.pokemons_lst.clear()
            pokemons_to_allocate: list = []
            pokemons = json.loads(json_file,
                                  object_hook=lambda d: SimpleNamespace(**d)).Pokemons
            pokemons = [p.Pokemon for p in pokemons]
            # iterate over every given pokemon and make it object from json of the client
            for i in pokemons:
                d: str = i.pos
                x, y, z = d.split(',')
                edge = self.graph_algo.get_edge_on_point((float(x), float(y), float(z)), i.type)
                location = GeoLocation((float(x), float(y), float(z)))
                found_pokemon_exists = False
                # check if the pokemon is somehow in the list
                for exiting_pokemon in self.pokemons_lst:
                    # we will say that it is the same pokemon if the locations are the same
                    if exiting_pokemon.pos.x == location.x and exiting_pokemon.pos.y == location.y:
                        found_pokemon_exists = True
                        break
                # if the pokemon is not in the arena pokemon list then create pokemon object
                # and add it to the arena pokemon list
                if not found_pokemon_exists:
                    poki = Pokemon(i.value, i.type, location, edge)
                    self.pokemons_lst.append(poki)
                    if first_iter:
                        self.pokemons_lst.clear()
                    pokemons_to_allocate.append(poki)
            return pokemons_to_allocate
        except Exception:
            print("problem with json load pokemon")

    """
    @:param json_file
    get the agents information from the server and only update the data of the agents
    """

    def update_agent_lst(self, json_file, already_exists: bool):
        try:
            agents = json.loads(json_file,
                                object_hook=lambda d: SimpleNamespace(**d)).Agents
            agents = [agent.Agent for agent in agents]
            # iterate over all of the agents data
            for i in agents:
                d: str = i.pos
                x, y, z = d.split(',')
                location = GeoLocation((float(x), float(y), float(z)))
                # if there is no agent with this id then create new agent and add him to the agents list
                if already_exists is True:
                    double007 = Agent(i.id, location, i.value, i.src, i.dest, i.speed)
                    self.agents_lst.append(double007)
                else:
                    # if there is such agent then update his values from the data
                    for existing_agent in self.agents_lst:
                        if existing_agent.id == i.id:
                            existing_agent.update_from_given_values(location, i.speed, i.dest, i.src, i.value)
                            break
        except Exception:
            print("problem with json load pokemon")
    """
    This function will be called before the start of the client run.
    At first it will iterate over every node of the graph and activate the dijkstra algorithm on it in order to save 
    the values of the shortest paths from every node to all the other nodes to later use.
    Then it will count the appearance of the edges that have pokemons on them, then it will sort the appearances
    from biggest to smallest and place agents at the edges with the most appearances.
    """
    def place_agents_at_beginning(self, first_pokemons: list) -> dict:
        g_algo = GraphAlgo(self.graph_algo.graph)

        for node in self.graph_algo.graph.nodes.values():
            # init the dijkstra class
            dijkstra = MinHeapDijkstra.DijkstraUsingMinHeap.Graph(g_algo)
            # run the dijkstra algorithm on every node
            dijkstra.dijkstra_Getmin_distances(node.key)
            self.dijkstra_list[node.key] = list(dijkstra.heap_nodes)
        i = 0
        list_of_agent = {}
        counter_of_edges = {}
        # iterate over the pokemons and count the appearance of every pokemon edge.src
        while i < self.info_dict["pokemons"]:
            if first_pokemons[i].curr_edge.src in counter_of_edges.keys():
                counter_of_edges[first_pokemons[i].curr_edge.src] += 1
            else:
                counter_of_edges[first_pokemons[i].curr_edge.src] = 1
            i += 1
        # sort the dict of the counted appearances by the appearance value
        var = {k: v for k, v in sorted(counter_of_edges.items(), key=lambda item: item[1], reverse=True)}
        i = 0
        # run on the sorted dict of appearances and add agents near the most frequently appearing edges
        for counter in var:
            pokemon_src = counter
            string_of_src = "{}".format(pokemon_src)
            # add agent
            json_to_agent = "{\"id\":" + string_of_src + "}"
            list_of_agent[i] = json_to_agent
            i += 1
        return list_of_agent
    """
    update the game information from given json
    """
    def update_game_info(self, game_info):
        self.info_dict = {}
        # parse the json info and change the values at the correct places
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
