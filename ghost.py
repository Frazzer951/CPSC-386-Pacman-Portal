import pygame as pg
import game_functions as gf
from character import Character,Direction
from vector import Vector


class Ghost(Character):
    def __init__(self, game):
        super.__init__(game=game)
        self.movement_images = ()
        self.eye_images = ()
        self.scared = False
        self.pos = Vector(0,0)
        self.color = (0,0,0)
        self.screen = game.screen
        self.next_dir = Direction.NONE
    def draw(self):
        pos = gf.world_to_screen(self.pos)
        pg.draw.circle(self.screen, self.color, pos, 10)
    def update(self):
        self.move()
        self.draw()

class Blinky(Ghost):
    def __init__(self, game):
        self.pos = game.settings.blinky_start
        self.color = (255,0,0)
        self.screen = game.screen
        self.next_dir = Direction.UP

class Inky(Ghost):
    def __init__(self, game):
        self.pos = game.settings.inky_start
        self.color = (0,255,0)
        self.screen = game.screen

class Pinky(Ghost):
    def __init__(self, game):
        self.pos = game.settings.pinky_start
        self.color = (0,0,255)
        self.screen = game.screen

class Clyde(Ghost):
    def __init__(self, game):
        self.pos = game.settings.clyde_start
        self.color = (255,255,255)
        self.screen = game.screen

class Ghosts:
    def __init__(self, game):
        self.game = game
        self.ghosts = [Blinky(self.game), Inky(self.game), Pinky(self.game), Clyde(self.game)]

    def update(self):
        for ghost in self.ghosts:
            ghost.draw()
