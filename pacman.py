import pygame as pg

import game_functions as gf
from character import Character, Direction


class Pacman(Character):
    def __init__(self, game):
        super().__init__(game=game)
        self.game = game
        self.lives = 4
        self.pos = game.settings.pacman_start
        # self.image = pg.image.load('images/pacman.bmp')
        # self.rect = self.image.get_rect()

        self.next_dir = Direction.NONE

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
        self.move()
        self.draw()

    def draw(self):
        pos = gf.world_to_screen(self.pos)
        pg.draw.circle(self.screen, (255, 255, 0), pos, 10)
        # image = self.timer.image()
        # self.screen.blit(image, self.rect)
