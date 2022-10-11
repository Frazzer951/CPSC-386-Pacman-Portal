from enum import Enum, auto
from typing import List

import pygame as pg

import game_functions as gf
from vector import Vector


class NodeType(Enum):
    POINT = auto()
    POWER_UP = auto()
    FRUIT = auto()
    NONE = auto()


class Node:
    def __init__(self, pos: Vector, type: NodeType = NodeType.NONE, nodes=None):
        self.pos = pos
        self.type = type
        self.neighbors: List = []

        if nodes is not None:
            for n in nodes:
                self.connect(n)

    def __eq__(self, node):
        return self.pos == node.pos

    def connect(self, node):
        if node not in self.neighbors:
            self.neighbors.append(node)
        if self not in node.neighbors:
            node.neighbors.append(self)

    def disconnect(self, node):
        self.neighbors.remove(node)
        node.neighbors.remove(self)

    def draw(self, screen):
        pos = gf.world_to_screen(self.pos)
        if self.type == NodeType.NONE:
            pass  # pg.draw.circle(screen, (255, 255, 255), pos, 1)
        if self.type == NodeType.POINT:
            pg.draw.circle(screen, (255, 255, 255), pos, 2)
        if self.type == NodeType.POWER_UP:
            pg.draw.circle(screen, (255, 255, 255), pos, 5)
        if self.type == NodeType.FRUIT:
            pg.draw.circle(screen, (255, 0, 0), pos, 10)


class Graph:
    def __init__(self, nodes: List[Node] = []):
        self.nodes = nodes

    def get_neighbors(self, pos):
        for n in self.nodes:
            if n.pos == pos:
                return n.neighbors

    def is_node_at(self, pos):
        for n in self.nodes:
            if n.pos == pos:
                return True
        return False

    def get_node_at(self, pos):
        for n in self.nodes:
            if n.pos == pos:
                return n
        return None

    def add_node(self, pos):
        if not self.is_node_at(pos):
            self.nodes.append(Node(pos))

    def get_edges(self):
        edges = set()
        for node in self.nodes:
            p1 = (node.pos.x, node.pos.y)
            for neighbor in node.neighbors:
                p2 = (neighbor.pos.x, neighbor.pos.y)
                edges.add(tuple(sorted([p1, p2])))
        return edges

    def connect_pos(self, pos1, pos2):
        a = self.get_node_at(pos1)
        b = self.get_node_at(pos2)

        if a is None:  # create Node A if it couldn't be found
            a = Node(pos1)
            self.nodes.append(a)
        if b is None:  # create Node B if it couldn't be found
            b = Node(pos2)
            self.nodes.append(b)

        a.connect(b)  # connect the Nodes

    def connect_nodes(self, node1: Node, node2: Node):
        if node1 not in self.nodes:  # Add Node1 if it isn't in nodes list
            self.nodes.append(node1)
        if node2 not in self.nodes:  # Add Node2 if it isn't in nodes list
            self.nodes.append(node2)
        node1.connect(node2)  # connect the nodes
