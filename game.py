from time import time

import pygame as pg

import game_functions as gf
from gameboard import Gameboard
from ghost import Ghosts
from launch import Launchscreen
from pacman import Pacman
from scoreboard import Scoreboard
from settings import Settings
from sound import Sound
from spritesheet import SpriteSheet


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height  # tuple
        self.screen = pg.display.set_mode(size=size)

        # self.sound = Sound(bg_music="sounds/launch.mp3")
        self.scoreboard = Scoreboard(game=self)

        fruits = SpriteSheet("images/fruits.png", "fruits_spritesheet.json")
        self.fruits = [fruits.get_sprite("Cherry.png"),
                       fruits.get_sprite("Strawberry.png"),
                       fruits.get_sprite("Orange.png"),
                       fruits.get_sprite("Apple.png"),
                       fruits.get_sprite("Melon.png"),
                       fruits.get_sprite("Galaxian_Flagship.png"),
                       fruits.get_sprite("Bell.png"),
                       fruits.get_sprite("Key.png")]

        self.gameboard = Gameboard(game=self)
        self.pacman = Pacman(game=self)
        self.ghosts = Ghosts(game=self)

        self.gameover = False

    def reset(self):
        print("Resetting game...")
        self.pacman.reset()
        self.ghosts.reset()
        self.gameboard.reset()

    def game_over(self):
        print("All Lives gone, GAME OVER!")
        # self.sound.gameover()
        self.gameover = True
        # self.sound.stop_bg()

        scores = gf.read_high_scores()
        scores.append(self.scoreboard.score)
        scores.sort(reverse=True)
        scores = scores[:10]
        gf.write_high_scores(scores)

    def play(self):
        # self.sound.play_bg()
        frametime = 1 / 60
        self.timer = time()
        while not self.gameover:
            start_time = time()
            gf.check_events(game=self)
            self.screen.fill(self.settings.bg_color)

            self.gameboard.draw()
            self.pacman.update()
            self.ghosts.update()
            self.scoreboard.update()

            pg.display.flip()
            elapsed = time() - start_time
            while elapsed < frametime:  # run with a max fps of 60
                elapsed = time() - start_time


def main():
    g = Game()
    ls = Launchscreen(game=g)
    ls.show()
    g.play()


if __name__ == "__main__":
    main()
