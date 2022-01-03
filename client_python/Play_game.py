import math as mh
import sys

from client import Client
import json
from pygame import gfxdraw
import pygame
import itertools
from pygame import *

from client_python.Agent import Agent
from client_python.Arena import Arena
from client_python.Pokemon import Pokemon
from client_python.Window import Window


class Play_game:
    # dont forget to add threads
    def __init__(self):
        self.grade = 0
        self.id: int
        self.scanerio_num: int
        self.EPS = 0.001
        self.move_count = 0;

    def distance_between_agent2Pokemon(self, agent: Agent, pokemon: Pokemon) -> float:
        return mh.sqrt(((agent.pos.x - pokemon.pos.x) ** 2) + ((agent.pos.y - pokemon.pos.y) ** 2))

    def calculate_time_of_path(self, arena: Arena, list_of_stops: list) -> (float, list):
        the_path: list
        the_weight_of_path: float
        the_weight_of_path, the_path = arena.graph_algo.shortest_path(list_of_stops[0], list_of_stops[1].curr_edge.src)
        the_weight_of_path += list_of_stops[1].curr_edge.weight
        the_path.append(list_of_stops[1].curr_edge.dst)
        for i in range(1, len(list_of_stops) - 1):
            current_weight, temp_path = arena.graph_algo.shortest_path(list_of_stops[i].curr_edge.dst
                                                                       , list_of_stops[i + 1].curr_edge.src)
            temp_path.append(list_of_stops[i + 1].curr_edge.dst)
            current_weight += list_of_stops[i + 1].curr_edge.weight
            the_path.extend(temp_path)
            the_weight_of_path += current_weight
        return the_weight_of_path, the_path

    def get_all_permutations(self, pokemon_list) -> list:
        return list(itertools.permutations(pokemon_list))

    def AllocateAgent(self, agents_list, pokemon: Pokemon, arena: Arena) -> Agent:  # return agents id
        min_weight = sys.maxsize  # hold the min weight if an agent would pick up the pokemon
        min_agent: Agent  # hold the agent for which we find will pick up the pokemon quickest
        min_path = []
        temp_path = []
        temp_dist: float
        for agent in agents_list:
            agent.permutaion.append(pokemon)
            agent.permutaion.extend(agent.pokemons_to_eat)
            permutations_of_all_pokemons = self.get_all_permutations(agent.permutaion)
            for i in permutations_of_all_pokemons:
                if agent.dest == -1:  # if the agent is on a node we add the node to the path
                    i = list(i)
                    i.insert(0, agent.src)
                else:
                    i = list(i)
                    i.insert(0, agent.dest)
                temp_tuple = self.calculate_time_of_path(arena, i)
                temp_dist, temp_path = temp_tuple[0], temp_tuple[1]
                if temp_dist / agent.speed < min_weight:
                    min_path = temp_path
                    min_weight = temp_dist / agent.speed
                    min_agent = agent
        arena.agents_lst[min_agent.id].agents_path = min_path
        arena.agents_lst[min_agent.id].pokemons_to_eat.append(pokemon)
        for agent in agents_list:
            agent.permutaion.clear()
        return min_agent

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
        arena.create_agents(client.get_agents())
        pygame.init()
        screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        clock = pygame.time.Clock()
        pygame.font.init()
        client.start()
        while client.is_running() == 'true':
            arena.update_pokemons_lst(client.get_pokemons())
            arena.update_agent_lst(client.get_agents())
            # here need to put update game info
            Window(arena.graph_algo, arena.agents_lst, arena.actual_pokemons_in_graph, pygame, screen, clock)
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
            # find which agent goes to which pokemon
            for pokemon in arena.pokemons_lst:
                # need to allocate only for a pokemon which is new
                # if not pokemon in arena.actual_pokemons_in_graph:
                agents_id_allocated = self.AllocateAgent(arena.agents_lst, pokemon, arena)
                arena.actual_pokemons_in_graph.append(pokemon)
            for agent in arena.agents_lst:
                if agent.dest == -1:
                    # change this to our algorithm of move and choose next edge
                    if len(agent.agents_path) > 0:
                        if agent.agents_path[0] != agent.src:
                            next_node = agent.agents_path[0]
                        else:
                            agent.agents_path.remove(agent.agents_path[0])
                            next_node = agent.agents_path[0]
                        client.choose_next_edge(
                            '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                        ttl = client.time_to_end()
                        print(ttl, client.get_info())
                        client.move()
                        self.move_count += 1
                for poke in agent.pokemons_to_eat:
                    if self.distance_between_agent2Pokemon(agent, poke) < self.EPS:
                        client.move()
                        self.move_count += 1
                        self.grade += agent.value

            # need to add methods for when we call the move
        pygame.quit()


if __name__ == '__main__':
    print("at main")
    pf = Play_game()
    print(pf)
    pf.run_game()
