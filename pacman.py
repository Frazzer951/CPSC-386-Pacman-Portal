import pygame as pg

from vector import Vector
from character import Character
from game import Game


class Pacman(Character):
    def __init__(self, game: Game):
        super.__init__(game=game)
        self.game = game
        self.lives = 4
        self.pos = Vector(game.settings.initial_x, game.settings.initial_y)
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

    def update(self):
        # implement moving pacman
        self.check_collision()

        super.update()  # use parent class' update since it can handle the movement

    def draw(self):
        pass
        # image = self.timer.image()
        # self.screen.blit(image, self.rect)
