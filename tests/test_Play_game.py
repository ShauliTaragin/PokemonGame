import json
from unittest import TestCase

from api.GeoLocation import GeoLocation
from client_python.Agent import Agent
from client_python.Arena import Arena
from client_python.Play_game import Play_game, get_all_permutations, calculate_time_of_path, AllocateAgent


class Test(TestCase):
    def test_calculate_time_of_path(self):
        arena = Arena(json.dumps({"GameServer": {"pokemons": 1, "is_logged_in": False, "moves": 0, "grade": 0, "game_level": 0,
                        "max_user_level": -1, "id": 0, "graph": "data/A0", "agents": 1}}))
        self.assertEqual(arena.dijkstra_list, {})
        self.assertIsNotNone(arena.graph_algo)
        first_pokemons= arena.update_pokemons_lst(json.dumps({"Pokemons":[{"Pokemon":{"value":5.0,"type":-1,
                                                                "pos":"35.197656770719604,32.10191878639921,0.0"}}]}),
                                                  True)
        agents_list=arena.place_agents_at_beginning(first_pokemons)
        self.assertEqual(len(agents_list), 1)
        self.assertEqual(len(first_pokemons), 1)
        self.assertEqual(arena.pokemons_lst, [])
        self.assertIsNotNone(arena.graph_algo)
        self.assertIsNotNone(arena.dijkstra_list, {})
        list_to_calculate= [9, first_pokemons[0]]
        time_of_path=calculate_time_of_path(arena, list_to_calculate)
        self.assertEqual(1.4575484853801393, time_of_path)
        self.assertEqual(arena.dijkstra_list[9][8], 1.4575484853801393)

    def test_get_all_permutations(self):
        self.assertEqual([(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)],
                         get_all_permutations([1,2,3]))
    def test_allocate_agent(self):
        location = GeoLocation((35.20260156093624, 32.10476360672269, 0.0))
        id_of_agent = 0
        value = 0
        src = 9
        dest = 8
        speed = 1.0
        agent = Agent(id_of_agent, location, value, src, dest, speed)
        list_of_agents = [agent]
        arena = Arena(
            json.dumps({"GameServer": {"pokemons": 1, "is_logged_in": False, "moves": 0, "grade": 0, "game_level": 0,
                                       "max_user_level": -1, "id": 0, "graph": "data/A0", "agents": 1}}))
        self.assertEqual(arena.dijkstra_list, {})
        self.assertIsNotNone(arena.graph_algo)
        first_pokemons = arena.update_pokemons_lst(json.dumps({"Pokemons": [{"Pokemon": {"value": 5.0, "type": -1,
                                                                                         "pos": "35.197656770719604,32.10191878639921,0.0"}}]}),
                                                   True)
        arena.agents_lst.append(agent)
        agents_list = arena.place_agents_at_beginning(first_pokemons)
        agent_to_choose = AllocateAgent(list_of_agents, first_pokemons[0], arena)
        self.assertEqual(0, agent_to_choose)
