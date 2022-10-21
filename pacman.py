import pygame as pg

import game_functions as gf
from character import Character, Direction


class Pacman(Character):
    def __init__(self, game):
        super().__init__(game=game)
        self.game = game
        self.lives = 4
        self.pos = game.settings.pacman_start
        self.start_pos = self.pos
        self.target_pos = game.settings.pacman_start
        self.image = pg.image.load('images/placeholder_32.png')
        self.rect = self.image.get_rect()

        self.next_dir = Direction.NONE

    def die(self):
        pass

    def update(self):
        if not self.isMoving:
            self.gameboard.pacman_collision_check(self.pos)
        self.move()
        self.draw()

    def draw(self):
        pos = gf.world_to_screen(self.pos)
        # pg.draw.circle(self.screen, self.color, pos, 10
        self.rect.center = pos[0], pos[1]
        self.screen.blit(self.image, self.rect)
