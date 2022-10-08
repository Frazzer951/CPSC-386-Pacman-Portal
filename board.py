import pygame as pg
import game_functions as gf
from graph import Graph
from vector import Vector


class Board:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.graph: Graph = Graph()

        self.create_board()

    def create_board(self):
        self.graph.connect_pos(Vector(0, 0), Vector(0, 1))
        self.graph.connect_pos(Vector(0, 0), Vector(1, 0))
        self.graph.connect_pos(Vector(1, 0), Vector(1, 1))
        self.graph.connect_pos(Vector(0, 1), Vector(1, 1))
        self.graph.connect_pos(Vector(1, 1), Vector(1, 2))

    def is_valid_pos(self, pos):
        return self.graph.is_node_at(pos)

    def draw(self):
        for edge in self.graph.get_edges():
            p1 = gf.world_to_screen(Vector(edge[0][0], edge[0][1]))
            p2 = gf.world_to_screen(Vector(edge[1][0], edge[1][1]))
            pg.draw.line(self.screen, (255, 0, 0), p1, p2, 10)

        for node in self.graph.nodes:
            pos = gf.world_to_screen(node.pos)
            pg.draw.circle(self.screen, (255, 255, 255), pos, 25)
