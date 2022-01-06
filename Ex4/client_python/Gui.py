
import json
import pygame
import time
from pygame import *
from pygame import gfxdraw
from types import SimpleNamespace


class Gui:
    def __init__(self, g):
        self.g = g
        pygame.init()
        WIDTH, HEIGHT = 1080, 720
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        FONT = pygame.font.SysFont('Arial', 20, bold=True)
        graph_json = self.g.client.get_graph()
        FONT = pygame.font.SysFont('Arial', 20, bold=True)
        # load the json string into SimpleNamespace Object
        my_image = pygame.image.load('pok.jpg')
        graph = json.loads(
            graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

        nodes = []
        edges = []
        for e in graph.Edges:
            edges.append(e)
        for n in graph.Nodes:
            x, y, _ = n.pos.split(',')
            n.pos = SimpleNamespace(x=float(x), y=float(y))

        # get data proportions
        self.min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
        self.min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
        self.max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
        self.max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y

        radius = 20

        self.g.client.start()
        while self.g.client.is_running() == 'true':
            pokemons = json.loads(self.g.client.get_pokemons(),
                                  object_hook=lambda d: SimpleNamespace(**d)).Pokemons
            pokemons = [p.Pokemon for p in pokemons]
            for p in pokemons:
                x, y, _ = p.pos.split(',')
                p.pos = SimpleNamespace(x=self.my_scale(
                    float(x), x=True), y=self.my_scale(float(y), y=True))
            agents = json.loads(self.g.client.get_agents(),
                                object_hook=lambda d: SimpleNamespace(**d)).Agents
            agents = [agent.Agent for agent in agents]
            for a in agents:
                x, y, _ = a.pos.split(',')
                a.pos = SimpleNamespace(x=self.my_scale(
                    float(x), x=True), y=self.my_scale(float(y), y=True))
            # check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            # refresh surface
            self.screen.fill(pygame.Color(0, 0, 0))
            self.screen.blit(my_image, (self.screen.get_width()/2 - 350, self.screen.get_height()/2 - 200))

            # draw nodes
            for n in graph.Nodes:
                x = self.my_scale(n.pos.x, x=True)
                y = self.my_scale(n.pos.y, y=True)

                # its just to get a nice antialiased circle
                gfxdraw.filled_circle(self.screen, int(x), int(y),
                                      radius, pygame.Color(64, 80, 174))
                gfxdraw.aacircle(self.screen, int(x), int(y),
                                 radius, pygame.Color(255, 255, 255))

                # draw the node id
                id_srf = FONT.render(str(n.id), True, pygame.Color(255, 255, 255))
                rect = id_srf.get_rect(center=(x, y))
                self.screen.blit(id_srf, rect)

            # draw edges
            for e in graph.Edges:
                # find the edge nodes
                src = next(n for n in graph.Nodes if n.id == e.src)
                dest = next(n for n in graph.Nodes if n.id == e.dest)

                # scaled positions
                src_x = self.my_scale(src.pos.x, x=True)
                src_y = self.my_scale(src.pos.y, y=True)
                dest_x = self.my_scale(dest.pos.x, x=True)
                dest_y = self.my_scale(dest.pos.y, y=True)

                # draw the line
                pygame.draw.line(self.screen, pygame.Color(61, 72, 126),
                                 (src_x, src_y), (dest_x, dest_y))

            # draw agents
            for agent in agents:
                pygame.draw.circle(self.screen, pygame.Color(122, 61, 23),
                                   (int(agent.pos.x), int(agent.pos.y)), 10)
            # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
            for p in pokemons:
                pygame.draw.circle(self.screen, pygame.Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

            # update screen changes
            display.update()

            # refresh rate
            self.g.client.start()
            self.g.get_agents()
            self.g.get_pokemon()
            self.g.next_station()
            time.sleep(0.1)
            display.update()

    def scale(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    # decorate scale with the correct values

    def my_scale(self, data, x=False, y=False):
        if x:
            return self.scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return self.scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)

    """
    The code below should be improved significantly:
    The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
    """
