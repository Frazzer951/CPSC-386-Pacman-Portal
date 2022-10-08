import pygame as pg

import game_functions as gf
from graph import Graph
from vector import Vector


class Gameboard:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.graph: Graph = Graph()

        self.create_board()

    def create_board(self):
        gameboard_string = [  # 0 = ignore, 1 = node, 2 = point orb, 3 = power up, 4 = portal
            "11111111111100111111111111",
            "10000100000100100000100001",
            "10000100000100100000100001",
            "10000100000100100000100001",
            "11111111111111111111111111",
            "10000100100000000100100001",
            "10000100100000000100100001",
            "11111100111100111100111111",
            "00000100000100100000100000",
            "00000100000100100000100000",
            "00000100111111111100100000",
            "00000100100000000100100000",
            "00000100100000000100100000",
            "11111111100000000111111111",
            "00000100100000000100100000",
            "00000100100000000100100000",
            "00000100111111111100100000",
            "00000100100000000100100000",
            "00000100100000000100100000",
            "11111111111100111111111111",
            "10000100000100100000100001",
            "10000100000100100000100001",
            "11100111111111111111100111",
            "00100100100000000100100100",
            "00100100100000000100100100",
            "11111100111100111100111111",
            "10000000000100100000000001",
            "10000000000100100000000001",
            "11111111111111111111111111",
        ]

        def neighbor_node(from_pos: Vector, to_pos: Vector):
            if to_pos.x < 0 or to_pos.y < 0 or to_pos.x >= len(gameboard_string[0]) or to_pos.y >= len(gameboard_string):
                return
            if gameboard_string[to_pos.y][to_pos.x] == "1":
                self.graph.connect_pos(from_pos, to_pos)

        for j, col in enumerate(gameboard_string):
            for i, val in enumerate(col):
                if val == "1":
                    self.graph.add_node(Vector(i, j))
                    neighbor_node(Vector(i, j), Vector(i - 1, j))
                    neighbor_node(Vector(i, j), Vector(i + 1, j))
                    neighbor_node(Vector(i, j), Vector(i, j - 1))
                    neighbor_node(Vector(i, j), Vector(i, j + 1))
                else:
                    continue

    def is_valid_pos(self, pos):
        return self.graph.is_node_at(pos)

    def draw(self):
        for edge in self.graph.get_edges():
            p1 = gf.world_to_screen(Vector(edge[0][0], edge[0][1]))
            p2 = gf.world_to_screen(Vector(edge[1][0], edge[1][1]))
            pg.draw.line(self.screen, (255, 0, 0), p1, p2, 1)

        for node in self.graph.nodes:
            pos = gf.world_to_screen(node.pos)
            pg.draw.circle(self.screen, (255, 255, 255), pos, 5)
