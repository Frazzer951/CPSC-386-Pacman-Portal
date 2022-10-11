import pygame as pg

import game_functions as gf
from graph import Graph
from vector import Vector


class Gameboard:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.graph: Graph = Graph()

        self.image = pg.transform.rotozoom(pg.image.load("./images/maze.png"), 0, 2.75)
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

        self.create_board()

    def create_board(self):
        gameboard_string = [  # 0 = ignore, 1 = node, 2 = point orb, 3 = power up, 4 = portal
            "11111111111100111111111111",  # 0
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
            "11111111100000000111111111",  # 13
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
            "11111111111111111111111111",  # 28
        ]

        def neighbor_node(from_pos: Vector, to_pos: Vector):
            if to_pos.x < 0 or to_pos.y < 0 or to_pos.x >= len(gameboard_string[0]) or to_pos.y >= len(gameboard_string):
                return
            if gameboard_string[int(to_pos.y)][int(to_pos.x)] == "1":
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

        # "Warp Gate" Nodes
        self.graph.connect_pos(Vector(0, 13), Vector(-1, 13))
        self.graph.connect_pos(Vector(25, 13), Vector(26, 13))
        self.graph.connect_pos(Vector(-1, 13), Vector(26, 13))

    def is_valid_pos(self, pos):
        return self.graph.is_node_at(pos)

    def is_valid_move(self, curpos, pos):
        curnode = self.graph.get_node_at(curpos)
        node = self.graph.get_node_at(pos)
        if node is not None:
            return curnode in node.neighbors
        return False

    def checkwarp(self, pos):
        if pos == Vector(-1, 13):
            return Vector(25, 13)
        if pos == Vector(26, 13):
            return Vector(0, 13)
        return None

    def draw(self):
        self.screen.blit(self.image, self.rect)

        # Draw all node edges
        # for edge in self.graph.get_edges():
        #     p1 = gf.world_to_screen(Vector(edge[0][0], edge[0][1]))
        #     p2 = gf.world_to_screen(Vector(edge[1][0], edge[1][1]))
        #     pg.draw.line(self.screen, (255, 0, 0), p1, p2, 1)

        # Draw all nodes
        for node in self.graph.nodes:
            pos = gf.world_to_screen(node.pos)
            pg.draw.circle(self.screen, (255, 255, 255), pos, 5)
