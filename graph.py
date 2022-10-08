from tkinter import N
import pygame as pg

class Node:
    def __init__(self, pos, nodes = None):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.neighbors = []
        if nodes is not None:
            for n in nodes:
                self.neighbors.append(self.connect(n))

    def __eq__(self, node):
        if self.pos == node.pos: return True
        else: return False
    def connect(self, n2):
        return n2.pos
    def disconnect(self, n2):
        self.neighbors.remove(n2)


class Graph:
    def __init__(self, nodes = []):
        self.nodes = nodes
    def get_neighbors(self, node):
        for n in self.nodes:
            if n.pos == node.pos:
                return n.neighbors
    def connect(self, node1, node2):
        a = b = -1
        for i in range(len(self.nodes)):
            if self.nodes[i] == node1: a = i
            if self.nodes[i] == node2: b = i
        if a < 0 or b < 0: return
        self.nodes[a].connect(self.nodes[b])
        self.nodes[b].connect(self.nodes[a])
