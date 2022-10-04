import pygame as pg

from enum import Enum, auto
from pygame import Sprite
from game import Game
from timer import Timer


class Movement(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()


class Character(Sprite):
    def __init__(self, game: Game):
        self.game = game
        self.screen = game.screen
        self.sound = game.sound

        self.dir = Movement.NONE
        self.next_dir = Movement.NONE

        self.game_pos = (0, 0)  # Cordinate in graph
        self.world_pos = (0, 0)  # Cordinate in pixels

        self.isMoving = False

        self.timer = Timer(image_list=[pg.image.load("images/placeholder_32.png")])
        self.rect = self.timer.image().get_rect()

    def update(self):
        if self.isMoving:  # Move from our current node to the next
            pass
        else:  # Get the next move direction
            # WIP idk if this is how we'll do it
            self.dir = self.next_dir
            if self.dir is not Movement.NONE:
                self.isMoving = True

    def draw(self):
        image = self.timer.image()
        self.screen.blit(image, self.rect)
