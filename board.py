import pygame as pg
from graph import Graph


class Board:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.graph = Graph()

        self.create_board()

    def create_board(self):
        self.graph.connect_pos((0, 0), (0, 1))
        self.graph.connect_pos((0, 0), (1, 0))
        self.graph.connect_pos((1, 0), (1, 1))
        self.graph.connect_pos((0, 1), (1, 1))
        self.graph.connect_pos((1, 1), (1, 2))

    def world_to_screen(self, pos):
        return (pos[0] * 125 + 25, pos[1] * 125 + 25)

    def draw(self):
        for edge in self.graph.get_edges():
            p1 = self.world_to_screen(edge[0])
            p2 = self.world_to_screen(edge[1])
            pg.draw.line(self.screen, (255, 0, 0), p1, p2, 10)

        for node in self.graph.nodes:
            pos = self.world_to_screen(node.pos)
            pg.draw.circle(self.screen, (255, 255, 255), pos, 25)
