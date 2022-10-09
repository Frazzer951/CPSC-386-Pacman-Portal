from enum import Enum, auto

import pygame as pg
from pygame.sprite import Sprite

from gameboard import Gameboard
from timer import Timer
from vector import Vector


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()


movement_map = {
    Direction.UP: Vector(0, -1),
    Direction.DOWN: Vector(0, 1),
    Direction.LEFT: Vector(-1, 0),
    Direction.RIGHT: Vector(1, 0),
    Direction.NONE: Vector(0, 0),
}


class Character(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.gameboard: Gameboard = game.gameboard
        # self.sound = game.sound

        self.move_speed = 0.1

        self.dir = Direction.NONE
        self.next_dir = Direction.NONE

        self.pos = Vector()
        self.target_pos = Vector()
        self.move_vec = Vector()

        self.isMoving = False
        self.move_steps = 1 / self.move_speed
        self.move_step = 0

        self.timer = Timer(image_list=[pg.image.load("images/placeholder_32.png")])
        self.rect = self.timer.image().get_rect()

    def move(self):
        if self.isMoving:
            if self.move_step >= self.move_steps:
                self.isMoving = False
                self.pos = self.target_pos
                warp_pos = self.gameboard.checkwarp(self.pos)
                if warp_pos is not None:
                    self.pos = warp_pos
            else:
                self.pos += self.move_vec * self.move_speed
                self.move_step += 1
        else:
            self.dir = self.next_dir
            if self.dir == Direction.NONE:
                return  # If the move direction is NONE, then return

            self.move_vec = movement_map[self.dir]
            self.target_pos = self.pos + self.move_vec
            if self.gameboard.is_valid_move(self.pos, self.target_pos):
                self.move_step = 0
                self.isMoving = True
            else:
                self.dir = self.next_dir = Direction.NONE
                self.target_pos = self.pos

    def update(self):
        self.move()

    def draw(self):
        image = self.timer.image()
        self.screen.blit(image, self.rect)
