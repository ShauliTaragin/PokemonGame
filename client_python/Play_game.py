import math as mh
import sys
import time as tm
from typing import Any

from api.GeoLocation import GeoLocation
from client_python.client import Client
import json
from pygame import gfxdraw
import pygame
import itertools
from pygame import *
import threading
import multiprocessing
from client_python.Agent import Agent
from client_python.Arena import Arena
from client_python.Pokemon import Pokemon
from client_python.Window import Window


def calculate_time_of_path(arena: Arena, list_of_stops: list) -> (float, list):
    the_weight_of_path: float
    the_weight_of_path = arena.dijkstra_list[list_of_stops[0]][list_of_stops[1].curr_edge.src]
    the_weight_of_path += list_of_stops[1].curr_edge.weight
    for i in range(1, len(list_of_stops) - 1):
        current_weight = arena.dijkstra_list[list_of_stops[i].curr_edge.dst][list_of_stops[i + 1].curr_edge.src]
        current_weight += list_of_stops[i + 1].curr_edge.weight
        the_weight_of_path += current_weight
    return the_weight_of_path


def get_all_permutations(pokemon_list) -> list:
    return list(itertools.permutations(pokemon_list))


def AllocateAgent(agents_list, pokemon: Pokemon, arena: Arena) -> int:  # return agents id
    min_weight = sys.maxsize  # hold the min weight if an agent would pick up the pokemon
    min_agent = sys.maxsize  # hold the agent for which we find will pick up the pokemon quickest
    min_permutation = []
    the_path = []
    temp_dist: float
    for agent in agents_list:
        agent.permutaion.append(pokemon)
        agent.permutaion.extend(agent.pokemons_to_eat)
        permutations_of_all_pokemons = get_all_permutations(agent.permutaion)
        for i in permutations_of_all_pokemons:
            if agent.dest == -1:  # if the agent is on a node we add the node to the path
                # im worried agent is not updated here and dest wont be -1 even tho it needs to
                i = list(i)
                i.insert(0, agent.src)
            else:
                i = list(i)
                i.insert(0, agent.dest)
            temp_dist = calculate_time_of_path(arena, i)

            if temp_dist < min_weight:
                min_permutation = i
                min_weight = temp_dist
                min_agent = agent.id

    tuple_of_dijkstra_ans = arena.graph_algo.shortest_path(min_permutation[0], min_permutation[1].curr_edge.src)
    the_weight_of_path, check_if_src_agent_equal_pokemon_src = tuple_of_dijkstra_ans[0], tuple_of_dijkstra_ans[1]
    if the_weight_of_path != 0:
        the_path.extend(check_if_src_agent_equal_pokemon_src)
    else:
        the_path.append(min_permutation[0])
    the_weight_of_path += min_permutation[1].curr_edge.weight
    if len(min_permutation) == 2:
        the_path.append(min_permutation[1].curr_edge.dst)
    for i in range(1, len(min_permutation) - 1):
        # if min_permutation[i].curr_edge.src != min_permutation[i + 1].curr_edge.src:
        current_weight, temp_path = arena.graph_algo.shortest_path(min_permutation[i].curr_edge.dst
                                                                   , min_permutation[i + 1].curr_edge.src)
        temp_path.append(min_permutation[i + 1].curr_edge.dst)
        current_weight += min_permutation[i + 1].curr_edge.weight
        the_path.extend(temp_path)
        the_weight_of_path += current_weight
    arena.agents_lst[min_agent].agents_path = the_path
    arena.agents_lst[min_agent].pokemons_to_eat.append(pokemon)
    for agent in agents_list:
        agent.permutaion.clear()
    return min_agent


class Play_game:
    # dont forget to add threads
    def __init__(self):
        self.moves = 0
        self.grade = 0
        self.id: int
        self.scanerio_num: int

    def dist_between_points(self, point1: GeoLocation, point2: GeoLocation) -> float:
        return mh.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    def thread_paint(self, graph_algo, agents_lst, pokemons_lst, pygame, screen, clock):
        try:
            Window(graph_algo, agents_lst, pokemons_lst, pygame, screen, clock)
        except Exception:
            return

    def thread_function(self, client_of_thread, time_to_sleep):
        try:
            tm.sleep(time_to_sleep*0.9)
            client_of_thread.move()
            sys.exit()
        except Exception:
            return

    def run_game(self):
        # try:
        threads = []
        HOST = '127.0.0.1'
        PORT = 6666
        WIDTH, HEIGHT = 1080, 720
        start_time = tm.time()
        client = Client()
        client.start_connection(HOST, PORT)
        arena = Arena(client.get_info(), client)
        first_pokemons = arena.update_pokemons_lst(client.get_pokemons(), True)
        agents_list = arena.place_agents_at_beginning(first_pokemons)
        for i in agents_list:
            client.add_agent(agents_list[i])
        arena.update_agent_lst(client.get_agents(), True)
        pygame.init()
        screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        clock = pygame.time.Clock()
        pygame.font.init()
        client.start()
        while client.is_running() == 'true':
            arena.update_game_info(client.get_info())
            for agent in arena.agents_lst:
                agent.agents_path.clear()
                agent.pokemons_to_eat.clear()
            arena.update_pokemons_lst(client.get_pokemons(), False)
            arena.update_agent_lst(client.get_agents(), False)
            print(arena.info_dict)
            Window(arena, pygame, screen , client.time_to_end())
            # here need to put update game info
            # y = threading.Thread(target=self.thread_paint, args=(arena.graph_algo, arena.agents_lst,
            #                                                      arena.pokemons_lst, pygame, screen, clock))
            # y.start()
            # y.join()
            # for events in pygame.event.get():
            #     if events.type == pygame.QUIT:
            #         pygame.quit()
            #         exit(0)
            # find which agent goes to which pokemon
            for pokemon in arena.pokemons_lst:
                # need to allocate only for a pokemon which is new
                agents_id_allocated = AllocateAgent(arena.agents_lst, pokemon, arena)
            for agent in arena.agents_lst:
                if agent.dest == -1:
                    # change this to our algorithm of move and choose next edge
                    if len(agent.agents_path) > 0:
                        if agent.agents_path[0] != agent.src:
                            next_node = agent.agents_path[0]
                        else:
                            agent.agents_path.pop(0)
                            if len(agent.agents_path) > 0:
                                next_node = agent.agents_path[0]
                            else:
                                continue
                        client.choose_next_edge(
                            '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                        ttl = client.time_to_end()
                        print(ttl, client.get_info())
                    arena.update_agent_lst(client.get_agents(), False)
                for pokemon_close_enough in agent.pokemons_to_eat:
                    if agent.src == pokemon_close_enough.curr_edge.src \
                            and agent.dest == pokemon_close_enough.curr_edge.dst:  # if close enough to pokemon
                        dist_from_src_to_dst = self.dist_between_points(pokemon_close_enough.curr_edge.src_location,
                                                                        pokemon_close_enough.curr_edge.dst_location)
                        dist_from_src_to_pokemon = self.dist_between_points(pokemon_close_enough.curr_edge.src_location,
                                                                            pokemon_close_enough.pos)

                        weight_of_edge = pokemon_close_enough.curr_edge.weight
                        speed_of_agent = agent.speed
                        the_part_of_the_edge = dist_from_src_to_pokemon / dist_from_src_to_dst
                        the_part_weight = weight_of_edge * the_part_of_the_edge
                        time_to_run_on_edge = the_part_weight / speed_of_agent
                        x = threading.Thread(target=self.thread_function, args=(client, time_to_run_on_edge))
                        threads.append(x)
                        x.start()
                        # x.join()
                        self.moves += 1
                        arena.pokemons_lst.remove(pokemon_close_enough)  # note that if it work
                        agent.pokemons_to_eat.remove(pokemon_close_enough)
                curr_time = tm.time()
                dif_in_times = (curr_time - start_time)
                if (dif_in_times / self.moves) < 10:
                    if int(10 - (dif_in_times / self.moves)) - 1 > 0:
                        clock.tick(int(10 - (dif_in_times / self.moves) - 1))
                        client.move()
                    else:
                        clock.tick(int(10 - (dif_in_times / self.moves)))
                        client.move()
                    self.moves += 1
                for index, thread in enumerate(threads):
                    if not thread.is_alive():
                        threads.remove(thread)
                    else:
                        thread.join()
            # need to add methods for when we call the move

            # client.stop()
            # client.stop_connection()
        # except Exception:
        #     pygame.quit()
        #     return print("game ended")
        pygame.quit()


if __name__ == '__main__':
    print("at main")
    pf = Play_game()
    print(pf)
    pf.run_game()
