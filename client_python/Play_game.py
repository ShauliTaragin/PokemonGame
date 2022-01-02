from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

from client_python.Arena import Arena
from client_python.Window import Window


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
        WIDTH, HEIGHT = 1080, 720
        client = Client()
        client.start_connection(HOST, PORT)
        arena = Arena(client.get_info(), client)
        arena.update_pokemons_lst(client.get_pokemons())
        agents_list = arena.place_agents_at_beginning()
        for i in agents_list:
            client.add_agent(agents_list[i])
        arena.update_agent_lst(client.get_agents())
        pygame.init()
        screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        clock = pygame.time.Clock()
        pygame.font.init()
        client.start()
        while client.is_running() == 'true':
            arena.update_pokemons_lst(client.get_pokemons())
            arena.update_agent_lst(client.get_agents())
            # here need to put update game info
            Window(arena.graph_algo, arena.agents_lst, arena.pokemons_lst , pygame , screen, clock )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
            for agent in arena.agents_lst:
                if agent.dest == -1:
                    #change this to our algorithm of move and choose next edge
                    next_node = (agent.src - 1) % len(arena.graph_algo.graph.nodes)
                    client.choose_next_edge(
                        '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                    ttl = client.time_to_end()
                    print(ttl, client.get_info())

            client.move()
        pygame.quit()

if __name__ == '__main__':
    print("at main")
    pf = Play_game()
    print(pf)
    pf.run_game()
