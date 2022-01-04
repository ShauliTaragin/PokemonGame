from unittest import TestCase

from api.GeoLocation import GeoLocation
from client_python.Agent import Agent
from client_python.Arena import Arena
from client_python.Play_game import Play_game
import time as tm


class ClientTest(TestCase):

    def creat_agent(self):
        {"GameServer": {"pokemons": 1, "is_logged_in": False, "moves": 0, "grade": 0, "game_level": 0,
                        "max_user_level": -1, "id": 0, "graph": "data/A0", "agents": 1}}
        json_of_arena = str({"GameServer": {"pokemons": 4, "is_logged_in": False, "moves": 0, "grade": 0,
                                            "game_level": 9, "max_user_level": -1, "id": 0, "graph": "data/A2",
                                            "agents": 1}})
        print(type(json_of_arena))
        location = GeoLocation((35.20260156093624, 32.10476360672269, 0.0))
        id_of_agent = 0
        value = 0
        src = 9
        dest = 8
        speed = 1.0
        agent = Agent(id_of_agent, location, value, src, dest, speed)
        self.assertIsNotNone(agent)
        self.assertEqual(agent.pos, location)
        self.assertEqual(agent.id, 0)
        self.assertEqual(agent.src, 9)
        self.assertEqual(agent.dest, 8)
        self.assertEqual(agent.speed, 1.0)
        print("finish")
