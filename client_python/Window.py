from tkinter import Button

from api.GraphAlgo import GraphAlgo
from pygame import gfxdraw
import pygame
from pygame import *
import math as mh
import os

from client_python.Arena import Arena


class Window:
    def __init__(self ,arena:Arena , pygame , screen , time_to_end):
        self.graph_algo = arena.graph_algo
        self.agents:list = arena.agents_lst
        self.pokemons:list = arena.pokemons_lst
        self.pygame = pygame
        self.screen = screen
        self.clock = self.pygame.time.Clock()
        self.num_of_moves = arena.info_dict['moves']
        self.num_of_grade = arena.info_dict['grade']
        self.time_to_end = time_to_end
        self.draw_game()


    def draw_arrow_lines(self, scr: pygame.Surface, x1, y1, x2, y2, d, h):
        dx = x2 - x1
        dy = y2 - y1
        D = mh.sqrt(dx * dx + dy * dy)
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
        D1 = mh.sqrt(dx1 * dx1 + dy1 * dy1)
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

    def draw_game(self):
        pokaball_img = self.pygame.image.load(r'..\data\pokeball_PNG30.png')
        picachu_img = self.pygame.image.load(r'..\data\PikachuImage.png')
        squirtel_img = self.pygame.image.load(r'..\data\squirtle-pokemons-squirtle.png')
        background_img = self.pygame.image.load(r'..\data\background.png')

        width = self.screen.get_width()
        height = self.screen.get_height()

        radius = 15
        FONT = pygame.font.SysFont('Arial', 20, bold=True)

        # refresh surface
        # self.screen.fill(Color(0, 0, 0))
        background = pygame.transform.scale(background_img, (1080, 720))
        self.screen.blit(background , (0,0))

        smallfont = pygame.font.SysFont('Ariel', 35)

        main_text = smallfont.render('Time To End:  {}  Number Of Moves: {}   Grade: {}'.format(  int(self.time_to_end) / 1000  ,self.num_of_moves , self.num_of_grade), True, Color(0,0,0))

        self.screen.blit(main_text, (width/10, height/100))

        color = (0, 0, 0)

        # light shade of the button
        color_light = (170, 170, 170)

        # dark shade of the button
        color_dark = (255, 255, 25)

        # stores the width of the
        # screen into a variable

        xwidth = width/1.05
        yheight = height/100

        add_width = 40
        add_height = 30

        text = FONT.render('Quit', True, color)


        mouse = pygame.mouse.get_pos()

        for events in self.pygame.event.get():
            if events.type == pygame.QUIT:
                self.pygame.quit()
                exit(0)
            if events.type == pygame.MOUSEBUTTONDOWN:

                if xwidth <= mouse[0] <= xwidth+add_width and yheight <= mouse[1] <= yheight+add_height:
                    # prints current location of mouse
                    self.pygame.quit()


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
                self.draw_arrow_lines(self.screen, src_x, src_y, dest_x, dest_y, 15, 5)


        # draw agents
        for agent in self.agents:
            x = my_scale(agent.pos.x, x=True)
            y = my_scale(agent.pos.y, y=True)
            self.pygame.draw.circle(self.screen, Color(122, 61, 23),
                               (int(x), int(y)), radius*0.6666)
            pokaball = self.pygame.transform.scale(pokaball_img, (30, 30))
            self.screen.blit(pokaball, (int(x)-14, int(y)-12))
        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
        for p in self.pokemons:
            x = my_scale(p.pos.x, x=True)
            y = my_scale(p.pos.y, y=True)
            if p.type > 0:
                picachu = self.pygame.transform.scale(picachu_img, (35, 35))
                self.screen.blit(picachu, (int(x)-15, int(y)-15))
            else:
                squirtel = self.pygame.transform.scale(squirtel_img, (40, 33))
                self.screen.blit(squirtel, (int(x) - 13, int(y) - 13))
            # self.pygame.draw.circle(self.screen, Color(0, 255, 255), (int(x), int(y)), radius*0.6666)


        # if mouse is hovered on a button it
        # changes to lighter shade
        if xwidth <= mouse[0] <= xwidth + add_width and yheight <= mouse[1] <= yheight + add_height:
            pygame.draw.rect(self.screen, color_light, [xwidth, yheight, add_width, add_height])

        else:
            pygame.draw.rect(self.screen, color_dark, [xwidth, yheight , add_width, add_height])

        # superimposing the text onto our button
        self.screen.blit(text, (xwidth , yheight))

        # update screen changes
        self.pygame.display.update()
        self.clock.tick(60)
        # refresh rate


        # choose next edge