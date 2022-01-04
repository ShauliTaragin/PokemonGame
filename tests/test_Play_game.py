import json
from unittest import TestCase

from client_python.Arena import Arena
from client_python.Play_game import Play_game, get_all_permutations


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
    def test_get_all_permutations(self):
        self.assertEqual([(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)],
                         get_all_permutations([1,2,3]))
    def test_allocate_agent(self):
        self.fail()
