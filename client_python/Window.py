from api.GraphAlgo import GraphAlgo
from pygame import gfxdraw
import pygame
from pygame import *


class Window:
    def __init__(self ,graph_algo: GraphAlgo ,agents: list , pokemons:list , pygame , screen, clock):
        self.graph_algo = graph_algo
        self.agents = agents
        self.pokemons = pokemons

        radius = 15
        FONT = pygame.font.SysFont('Arial', 20, bold=True)
        # refresh surface
        screen.fill(Color(0, 0, 0))

        min_x = min(list(graph_algo.graph.nodes.values()), key=lambda n: n.geolocation[0]).geolocation[0]
        min_y = min(list(graph_algo.graph.nodes.values()), key=lambda n: n.geolocation[1]).geolocation[1]
        max_x = max(list(graph_algo.graph.nodes.values()), key=lambda n: n.geolocation[0]).geolocation[0]
        max_y = max(list(graph_algo.graph.nodes.values()), key=lambda n: n.geolocation[1]).geolocation[1]

        def scale(data, min_screen, max_screen, min_data, max_data):
            """
            get the scaled data with proportions min_data, max_data
            relative to min and max screen dimentions
            """
            return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

        # decorate scale with the correct values

        def my_scale(data, x=False, y=False):
            if x:
                return scale(data, 50, screen.get_width() - 50, min_x, max_x)
            if y:
                return scale(data, 50, screen.get_height() - 50, min_y, max_y)

        # draw nodes
        for n in graph_algo.graph.nodes.values():
            x = my_scale(n.geolocation[0], x=True)
            y = my_scale(n.geolocation[1], y=True)

            # its just to get a nice Intialiased circle
            gfxdraw.filled_circle(screen, int(x), int(y),
                                  radius, Color(64, 80, 174))
            gfxdraw.aacircle(screen, int(x), int(y),
                             radius, Color(255, 255, 255))

            # draw the node id
            id_srf = FONT.render(str(n.key), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)
            # draw edges
            for e in n.outEdges.values():
                # find the edge nodes
                src = e.src_location
                dest = e.dst_location

                # scaled positions
                src_x = my_scale(src.x, x=True)
                src_y = my_scale(src.y, y=True)
                dest_x = my_scale(dest.x, x=True)
                dest_y = my_scale(dest.y, y=True)

                # draw the line
                pygame.draw.line(screen, Color(61, 72, 126),
                                 (src_x, src_y), (dest_x, dest_y))



        # draw agents
        for agent in agents:
            x = my_scale(agent.pos.x, x=True)
            y = my_scale(agent.pos.y, y=True)
            pygame.draw.circle(screen, Color(122, 61, 23),
                               (int(x), int(y)), radius*0.6666)
        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
        for p in pokemons:
            x = my_scale(p.pos.x, x=True)
            y = my_scale(p.pos.y, y=True)
            pygame.draw.circle(screen, Color(0, 255, 255), (int(x), int(y)), radius*0.6666)

        # update screen changes
        display.update()

        # refresh rate
        clock.tick(60)

        # choose next edge