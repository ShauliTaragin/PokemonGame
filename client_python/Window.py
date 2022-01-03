from api.GraphAlgo import GraphAlgo
from pygame import gfxdraw
import pygame
from pygame import *
import math
import sys
from math import inf


def draw_arrow_lines(scr: pygame.Surface, x1, y1, x2, y2, d, h):
    dx = x2 - x1
    dy = y2 - y1
    D = math.sqrt(dx * dx + dy * dy)
    xm = D - 3.5
    xn = xm
    ym = h
    yn = (0 - h)
    sin = dy / D
    cos = dx / D
    x = xm * cos - ym * sin + x1
    ym = xm * sin + ym * cos + y1
    xm = x
    x = xn * cos - yn * sin + x1
    yn = xn * sin + yn * cos + y1
    xn = x
    newX2 = (xm + xn) / 2
    newY2 = (ym + yn) / 2
    dx1 = newX2 - x1
    dy1 = newY2 - y1
    D1 = math.sqrt(dx1 * dx1 + dy1 * dy1)
    xm1 = D1 - d
    xn1 = xm1
    ym1 = h
    yn1 = 0 - h
    sin1 = dy1 / D1
    cos1 = dx1 / D1
    nx = xm1 * cos1 - ym1 * sin1 + x1
    ym1 = xm1 * sin1 + ym1 * cos1 + y1
    xm1 = nx
    nx = xn1 * cos1 - yn1 * sin1 + x1
    yn1 = xn1 * sin1 + yn1 * cos1 + y1
    xn1 = nx
    points = [(newX2, newY2), (xm1, ym1), (xn1, yn1)]
    pygame.draw.polygon(scr, (200, 30, 70), points)


class Window:
    def __init__(self ,graph_algo: GraphAlgo ,agents: list , pokemons:list , pygame , screen, clock):
        self.graph_algo = graph_algo
        self.agents = agents
        self.pokemons = pokemons
        self.pygame = pygame
        self.screen = screen
        self.clock = self.pygame.time.Clock()
        self.draw_game()

    def draw_game(self):
        radius = 15
        FONT = pygame.font.SysFont('Arial', 20, bold=True)
        # refresh surface
        self.screen.fill(Color(0, 0, 0))

        min_x = min(list(self.graph_algo.graph.nodes.values()), key=lambda n: n.geolocation[0]).geolocation[0]
        min_y = min(list(self.graph_algo.graph.nodes.values()), key=lambda n: n.geolocation[1]).geolocation[1]
        max_x = max(list(self.graph_algo.graph.nodes.values()), key=lambda n: n.geolocation[0]).geolocation[0]
        max_y = max(list(self.graph_algo.graph.nodes.values()), key=lambda n: n.geolocation[1]).geolocation[1]

        def scale(data, min_screen, max_screen, min_data, max_data):
            """
            get the scaled data with proportions min_data, max_data
            relative to min and max screen dimentions
            """
            return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

        # decorate scale with the correct values

        def my_scale(data, x=False, y=False):
            if x:
                return scale(data, 50, self.screen.get_width() - 50, min_x, max_x)
            if y:
                return scale(data, 50, self.screen.get_height() - 50, min_y, max_y)

        # draw nodes
        for n in self.graph_algo.graph.nodes.values():
            x = my_scale(n.geolocation[0], x=True)
            y = my_scale(n.geolocation[1], y=True)

            # its just to get a nice Intialiased circle
            gfxdraw.filled_circle(self.screen, int(x), int(y),
                                  radius, Color(64, 80, 174))
            gfxdraw.aacircle(self.screen, int(x), int(y),
                             radius, Color(255, 255, 255))

            # draw the node id
            id_srf = FONT.render(str(n.key), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            self.screen.blit(id_srf, rect)
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
                self.pygame.draw.line(self.screen, Color(61, 72, 126),
                                 (src_x, src_y), (dest_x, dest_y))
                draw_arrow_lines(self.screen, src_x, src_y, dest_x, dest_y, 6, 5)



        # draw agents
        for agent in self.agents:
            x = my_scale(agent.pos.x, x=True)
            y = my_scale(agent.pos.y, y=True)
            self.pygame.draw.circle(self.screen, Color(122, 61, 23),
                               (int(x), int(y)), radius*0.6666)
        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
        for p in self.pokemons:
            x = my_scale(p.pos.x, x=True)
            y = my_scale(p.pos.y, y=True)
            self.pygame.draw.circle(self.screen, Color(0, 255, 255), (int(x), int(y)), radius*0.6666)

        # update screen changes
        self.pygame.display.update()
        self.clock.tick(60)
        # refresh rate

