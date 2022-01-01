from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

from client_python.Arena import Arena


class Play_game:
    # dont forget to add threads
    def __init__(self):
        self.grade = 0
        self.id: int
        self.scanerio_num: int

    def run_game(self):
        print("here")
        HOST = '127.0.0.1'
        PORT = 6666
        client = Client()
        client.start_connection(HOST, PORT)
        arena = Arena(client.get_info(),client)
        arena.update_pokemons_lst(client.get_pokemons())
        agents_list = arena.place_agents_at_beginning()
        for i in agents_list:
            client.add_agent(agents_list[i])
        arena.update_agent_lst(client.get_agents())
        a=5
if __name__ == '__main__':
    print("at main")
    pf = Play_game()
    print(pf)
    pf.run_game()
