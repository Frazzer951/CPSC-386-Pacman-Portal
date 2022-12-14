import pygame as pg
from pygame import mixer

from graph import Graph, NodeType
from vector import Vector


class Gameboard:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.graph: Graph = Graph()

        self.bitesound = pg.mixer.Sound("sounds/pacman_bite.wav")
        self.fruitsound = pg.mixer.Sound("sounds/pacman_eatfruit.wav")
        self.bitesound.set_volume(0.2)
        self.fruitsound.set_volume(0.2)

        self.image = pg.transform.rotozoom(pg.image.load("./images/maze.png"), 0, 2.75)
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

        self.portal_1_placed = False
        self.portal_1_pos = Vector()
        self.portal_2_placed = False
        self.portal_2_pos = Vector()

        self.fruit_spawned = False

        self.create_board()

    def create_board(self):
        gameboard_string = [  # 0 = ignore, 1 = node, 2 = point orb, 3 = power up
            "22222222222200222222222222",  # 0
            "20000200000200200000200002",
            "30000200000200200000200003",
            "20000200000200200000200002",
            "22222222222222222222222222",
            "20000200200000000200200002",
            "20000200200000000200200002",
            "22222200222200222200222222",
            "00000200000100100000200000",
            "00000200000100100000200000",
            "00000200111111111100200000",
            "00000200100011000100200000",
            "00000200100011000100200000",
            "11111211100111100111211111",  # 13
            "00000200100000000100200000",
            "00000200100000000100200000",
            "00000200111111111100200000",
            "00000200100000000100200000",
            "00000200100000000100200000",
            "22222222222200222222222222",
            "20000200000200200000200002",
            "20000200000200200000200002",
            "32200222222222222222200223",
            "00200200200000000200200200",
            "00200200200000000200200200",
            "22222200222200222200222222",
            "20000000000200200000000002",
            "20000000000200200000000002",
            "22222222222222222222222222",  # 28
        ]

        num_to_type = {
            "1": NodeType.NONE,
            "2": NodeType.POINT,
            "3": NodeType.POWER_UP,
        }

        def neighbor_node(from_pos: Vector, to_pos: Vector):
            if to_pos.x < 0 or to_pos.y < 0 or to_pos.x >= len(gameboard_string[0]) or to_pos.y >= len(gameboard_string):
                return

            val = gameboard_string[int(to_pos.y)][int(to_pos.x)]
            if val in ["1", "2", "3"]:
                self.graph.add_node(to_pos)
                self.graph.connect_pos(from_pos, to_pos)

        for j, col in enumerate(gameboard_string):
            for i, val in enumerate(col):
                if val in ["1", "2", "3"]:
                    self.graph.add_node(Vector(i, j))
                    neighbor_node(Vector(i, j), Vector(i - 1, j))
                    neighbor_node(Vector(i, j), Vector(i + 1, j))
                    neighbor_node(Vector(i, j), Vector(i, j - 1))
                    neighbor_node(Vector(i, j), Vector(i, j + 1))
                else:
                    continue

        self.initial_point_orbs = 0
        for j, col in enumerate(gameboard_string):
            for i, val in enumerate(col):
                if val in ["1", "2", "3"]:
                    type = num_to_type[val]
                    if type != NodeType.NONE:
                        self.initial_point_orbs += 1
                        self.graph.set_node_at(Vector(i, j), type)
        # print(f"Total orbs = {self.initial_point_orbs}")

        # "Warp Gate" Nodes
        self.graph.connect_pos(Vector(0, 13), Vector(-1, 13))
        self.graph.connect_pos(Vector(25, 13), Vector(26, 13))
        self.graph.connect_pos(Vector(-1, 13), Vector(26, 13))

    def reset(self):
        self.graph = Graph()
        self.portal_1_placed = False
        self.portal_1_pos = Vector()
        self.portal_2_placed = False
        self.portal_2_pos = Vector()
        self.fruit_spawned = False
        self.create_board()

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

    def set_portal(self, pos, portal):
        node = self.graph.get_node_at(pos)
        if portal == 1:
            if self.portal_1_placed:
                self.graph.set_node_at(self.portal_1_pos, NodeType.NONE)
            self.portal_1_placed = True
            self.portal_1_pos = pos
            node.type = NodeType.PORTAL_1
        if portal == 2:
            if self.portal_2_placed:
                self.graph.set_node_at(self.portal_2_pos, NodeType.NONE)
            self.portal_2_placed = True
            self.portal_2_pos = pos
            node.type = NodeType.PORTAL_2

    def clear_portals(self):
        self.portal_1_placed = False
        self.portal_2_placed = False
        self.graph.set_node_at(self.portal_1_pos, NodeType.NONE)
        self.graph.set_node_at(self.portal_2_pos, NodeType.NONE)

    def pacman_collision_check(self, pos):
        node = self.graph.get_node_at(pos)
        self.mixer = mixer.init()

        if node.type == NodeType.POINT:
            self.game.scoreboard.increment_score(self.settings.point_orb_score)
            node.type = NodeType.NONE
            if self.bitesound.get_num_channels() == 0:
                self.bitesound.play()
        if node.type == NodeType.POWER_UP:
            self.game.scoreboard.increment_score(self.settings.power_up_score)
            self.game.ghosts.scared_mode = True
            node.type = NodeType.NONE
            self.fruitsound.play()
        if node.type == NodeType.FRUIT:
            self.game.scoreboard.increment_score(self.settings.fruit_score)
            node.type = NodeType.NONE
            self.fruitsound.play()

        if self.portal_1_placed and self.portal_2_placed:
            if node.type == NodeType.PORTAL_1:
                self.game.pacman.pos = self.portal_2_pos
                self.clear_portals()
            if node.type == NodeType.PORTAL_2:
                self.game.pacman.pos = self.portal_1_pos
                self.clear_portals()

    def count_orbs(self):
        count = 0
        for node in self.graph.nodes:
            if node.type in [NodeType.POINT, NodeType.POWER_UP]:
                count += 1
        return count

    def update(self):
        count = self.count_orbs()
        if not self.fruit_spawned:
            if count / self.initial_point_orbs < 0.5:
                self.fruit_spawned = True
                self.graph.set_node_at(Vector(12, 16), NodeType.FRUIT)
        if count == 0:
            self.game.reset()
            self.game.round_number += 1
        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)

        # Draw all node edges
        # for edge in self.graph.get_edges():
        #     p1 = gf.world_to_screen(Vector(edge[0][0], edge[0][1]))
        #     p2 = gf.world_to_screen(Vector(edge[1][0], edge[1][1]))
        #     pg.draw.line(self.screen, (255, 0, 0), p1, p2, 1)

        # Draw all nodes
        for node in self.graph.nodes:
            node.draw(self.game)
