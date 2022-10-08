from typing import List

from vector import Vector


class Node:
    def __init__(self, pos: Vector, nodes=None):
        self.pos = pos
        self.neighbors = []
        if nodes is not None:
            for n in nodes:
                self.connect(n)

    def __eq__(self, node):
        return self.pos == node.pos

    def connect(self, node):
        self.neighbors.append(node)
        node.neighbors.append(self)

    def disconnect(self, node):
        self.neighbors.remove(node)
        node.neighbors.remove(self)


class Graph:
    def __init__(self, nodes: List[Node] = []):
        self.nodes = nodes

    def get_neighbors(self, pos):
        for n in self.nodes:
            if n.pos == pos:
                return n.neighbors

    def get_edges(self):
        edges = set()
        for node in self.nodes:
            p1 = (node.pos.x, node.pos.y)
            for neighbor in node.neighbors:
                p2 = (neighbor.pos.x, neighbor.pos.y)
                edges.add(tuple(sorted([p1, p2])))
        return edges

    def is_node_at(self, pos):
        for n in self.nodes:
            if n.pos == pos:
                return True
        return False

    def connect_pos(self, pos1, pos2):
        a = b = None
        for node in self.nodes:
            if node.pos == pos1:  # find node for first position
                a = node
            if node.pos == pos2:  # find node for second position
                b = node

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
