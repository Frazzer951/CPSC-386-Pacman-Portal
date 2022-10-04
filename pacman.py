from turtle import dot
import pygame as pg
from pygame import Sprite
from vector import Vector

class Pacman(Sprite):
    def __init__(self, game):
        super.__init__()
        self.game = game
        self.lives = 4
        self.posn = Vector(game.settings.initial_x, game.settings.initial_y)
        # self.image = pg.image.load('images/pacman.bmp')
        # self.rect = self.image.get_rect()
    
    def check_collision(self):
        # if small dot
        # if big dot
        # if fruit
        # if ghost (not scared)
        # if ghost (scared)
        pass
    def die(self):
        pass
    def draw(self):
        pass
    def update(self):
        # implement moving pacman
        self.check_collision()
        self.draw()
        


