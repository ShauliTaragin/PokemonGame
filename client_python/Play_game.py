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

"""
@:param -> arena : we recieve our arena for which we are working on
@:param -> list_of_stops : the list of stops which we need to calculate
@:returns -> float : the sum of the edges weights for which we will have to travel to inorder to visit all stops 
Our function works in the following manner-
    our arena holds a list of dijkstra for each node in the graph. we traverse over the list of stops and calculate
    only how long it will take to travel the graph. How long being the sum of weights of nodes we traveled
"""


def calculate_time_of_path(arena: Arena, list_of_stops: list) -> float:
    the_weight_of_path: float
    the_weight_of_path = arena.dijkstra_list[list_of_stops[0]][list_of_stops[1].curr_edge.src]
    the_weight_of_path += list_of_stops[1].curr_edge.weight
    for i in range(1, len(list_of_stops) - 1):
        current_weight = arena.dijkstra_list[list_of_stops[i].curr_edge.dst][list_of_stops[i + 1].curr_edge.src]
        current_weight += list_of_stops[i + 1].curr_edge.weight
        the_weight_of_path += current_weight
    return the_weight_of_path


"""
:@param -> pokemon_list - the list of pokemons our current agent needs to eat. e.g that have been allocated to him
:@return -> a list of tuples where each tuple holds a possible permutation for the list of pokemons the agent needs to eat
"""


def get_all_permutations(pokemon_list) -> list:
    return list(itertools.permutations(pokemon_list))


"""
This is our main algorithm

:@param -> agents_list - the list of agents which we have in this scenario and can potentially eat pokemons
:@param -> pokemon - the list of Pokemon's which we need to allocate 
:@param -> arena - our arena
:@return -> the allocated agent

Our algorithm iterates over all our agents and then iterates over all our permutations for catching the pokemons
for each permutation we calculate with our previous function how long will it take to travel over the whole path
The permutation for the agent that will catch that pokemon the quickest will be the agent allocated
Once we found the allocated agent we update his path he will now have to travel and update his pokemon list  
"""


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
                i = list(i)
                i.insert(0, agent.src)
            else:  # otherwise we add his destination to the path
                i = list(i)
                i.insert(0, agent.dest)
            temp_dist = calculate_time_of_path(arena, i)
            # if we found the current shortest path update the min path to be that one
            if temp_dist < min_weight:
                min_permutation = i
                min_weight = temp_dist
                min_agent = agent.id
    # now we have found the minimal agent and we just need to update his path.
    # Updating the agents path using the dijkstra list for each stop on his way
    tuple_of_dijkstra_ans = arena.graph_algo.shortest_path(min_permutation[0], min_permutation[1].curr_edge.src)
    the_weight_of_path, check_if_src_agent_equal_pokemon_src = tuple_of_dijkstra_ans[0], tuple_of_dijkstra_ans[1]
    # if the agent is currently on the src of the pokemon he needs to eat then dont add that node twice to his path
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
    min_permutation.pop(0)
    arena.agents_lst[min_agent].pokemons_to_eat = min_permutation
    for agent in agents_list:
        agent.permutaion.clear()
    return min_agent


# the actual "main" class
class Play_game:

    def __init__(self):
        self.moves = 0
        self.grade = 0
        self.id: int
        self.scanerio_num: int

    """
    Function to calculate distance on a graph between 2 points. A simple calculation
    """

    def dist_between_points(self, point1: GeoLocation, point2: GeoLocation) -> float:
        return mh.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    # currently not in use
    def thread_paint(self, graph_algo, agents_lst, pokemons_lst, pygame, screen, clock):
        try:
            Window(graph_algo, agents_lst, pokemons_lst, pygame, screen, clock)
        except Exception:
            return

    """
    our thread ,  for each agent that is about to eat A pokemon we reieve the time it will take him to eat that pokemon
    and make the thread sleep till that time. when the time comes we move the server thus catching the pokemon
    """

    def thread_function(self, client_of_thread, time_to_sleep):
        try:
            tm.sleep(time_to_sleep)
            client_of_thread.move()
            sys.exit()
        except Exception:
            return

    # our main function
    def run_game(self):
        # Simply initializing all our arena with the initial information from the server
        threads = []
        threads_of_nodes = []
        HOST = '127.0.0.1'
        PORT = 6666
        WIDTH, HEIGHT = 1080, 720
        start_time = tm.time()
        client = Client()
        client.start_connection(HOST, PORT)
        arena = Arena(client.get_info())
        first_pokemons = arena.update_pokemons_lst(client.get_pokemons(), True)
       # print(client.get_pokemons())
        agents_list = arena.place_agents_at_beginning(first_pokemons)
        for i in agents_list:
            client.add_agent(agents_list[i])
        arena.update_agent_lst(client.get_agents(), True)
        pygame.init()
        screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        clock = pygame.time.Clock()
        pygame.font.init()
        client.start()
        # starting our game
        while client.is_running() == 'true':
            # every iteratiion we update our information i.e the pokemons the agent the game info and we redraw our gui
            arena.update_game_info(client.get_info())
            for agent in arena.agents_lst:
                agent.agents_path.clear()
                agent.pokemons_to_eat.clear()
            arena.update_pokemons_lst(client.get_pokemons(), False)
            arena.update_agent_lst(client.get_agents(), False)
           # print(arena.info_dict)
            # calling our gui
            time_to_end = client.time_to_end()
            Window(arena, pygame, screen, client.time_to_end())
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

            for pokemon in arena.pokemons_lst:  # allocating our pokemons
                # need to allocate only for a pokemon which is new
                agents_id_allocated = AllocateAgent(arena.agents_lst, pokemon, arena)
            for agent in arena.agents_lst:
                if agent.dest == -1:
                    # if agent is on node the move to our next node in that agents path
                    if len(agent.agents_path) > 0:
                        if agent.agents_path[0] != agent.src:
                            # only if the agent needs to move to a different node then the one he is on now
                            next_node = agent.agents_path[0]
                        else:
                            agent.agents_path.pop(0)
                            if len(agent.agents_path) > 0:
                                next_node = agent.agents_path[0]
                            else:
                                continue
                        # we simply choose the next edge to be the next node in our agents path
                        client.choose_next_edge(
                            '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                        weight_of_edge = arena.graph_algo.graph.nodes[agent.src].outEdges[next_node].weight
                        speed_of_agent = agent.speed
                        the_time_of_path = weight_of_edge / speed_of_agent
                        y = threading.Thread(target=self.thread_function, args=(client, the_time_of_path))
                        threads_of_nodes.append(y)
                        y.start()
                        self.moves += 1
                        ttl = client.time_to_end()
                       # print(ttl, client.get_info())

                    # updating our agents list so our main algorithm will always be updated
                    arena.update_agent_lst(client.get_agents(), False)
                counter = 0
                pos_of_pokemon_on_same_edge = 0
                the_part_weight = 0
                weight_of_new_edge = 0
                time_to_run_on_edge = 0
                for pokemon_close_enough in agent.pokemons_to_eat:
                    if agent.src == pokemon_close_enough.curr_edge.src \
                            and agent.dest == pokemon_close_enough.curr_edge.dst:  # if close enough to pokemon
                        print("Time to end is : {}   ,  Pokemons to eat list is {}".format(int(time_to_end)/1000 , agent.pokemons_to_eat))
                        print("Agents src is : {}  . Agents dest is : {}".format(agent.src , agent.dest))
                        if counter == 0:
                            dist_from_src_to_dst = self.dist_between_points(agent.pos,
                                                                            pokemon_close_enough.curr_edge.dst_location)
                            dist_from_src_to_pokemon = self.dist_between_points(agent.pos,
                                                                                pokemon_close_enough.pos)
                            # We check weather any agent is on the same node as the src of any pokemon and going to the same dest
                            # if so we calculate the time it will take for that agent to catch that pokemon and send that agent to the
                            # thread function above making sure he will catch the pokemon on time
                            weight_of_edge = pokemon_close_enough.curr_edge.weight
                            speed_of_agent = agent.speed
                            pos_of_pokemon_on_same_edge = pokemon_close_enough.pos
                            the_part_of_the_edge = dist_from_src_to_pokemon / dist_from_src_to_dst
                            the_part_weight = weight_of_edge * the_part_of_the_edge
                            weight_of_new_edge = pokemon_close_enough.curr_edge.weight - the_part_weight
                            time_to_run_on_edge = the_part_weight / speed_of_agent
                            x = threading.Thread(target=self.thread_function, args=(client, time_to_run_on_edge))
                            threads.append(x)
                            x.start()
                            counter += 1
                        else:
                            dist_from_poke_to_dest = self.dist_between_points(pos_of_pokemon_on_same_edge,
                                                                            pokemon_close_enough.curr_edge.dst_location)
                            dest_from_poke_to_poke = self.dist_between_points(pos_of_pokemon_on_same_edge,
                                                                              pokemon_close_enough.pos)
                            the_part_of_the_edge = dest_from_poke_to_poke / dist_from_poke_to_dest

                            the_part_weight = weight_of_new_edge * the_part_of_the_edge
                            weight_of_new_edge = weight_of_new_edge - the_part_weight
                            time_to_run_on_edge = the_part_weight / agent.speed
                            pos_of_pokemon_on_same_edge = pokemon_close_enough.pos
                            x = threading.Thread(target=self.thread_function, args=(client, time_to_run_on_edge))
                            threads.append(x)
                            x.start()

                        # x.join()
                        self.moves += 1
                        arena.pokemons_lst.remove(pokemon_close_enough)  # note that if it work
                        agent.pokemons_to_eat.remove(pokemon_close_enough)

            for index, thread in enumerate(threads_of_nodes):
                if not thread.is_alive():
                    threads_of_nodes.remove(thread)
                else:
                    # thread.start()
                    thread.join()
            for index, thread in enumerate(threads):
                if not thread.is_alive():
                    threads.remove(thread)
                else:
                    thread.join()
            curr_time = tm.time()
            dif_in_times = (curr_time - start_time)
            # we want to make sure we dont excess the amount of permitted moves therefore we will only move if our
            # pace of move calling permits it
            # if (dif_in_times / self.moves) < 10:
            #     if int(10 - (dif_in_times / self.moves)) - 1 > 0:
            #         clock.tick(int(10 - (dif_in_times / self.moves) - 1))
            #         client.move()
            #     else:
            #         clock.tick(int(10 - (dif_in_times / self.moves)))
            #         client.move()
            #     self.moves += 1

            clock.tick(30)
        pygame.quit()


if __name__ == '__main__':
    pf = Play_game()
   # print(pf)
    pf.run_game()
