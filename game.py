from time import time

import pygame as pg

import game_functions as gf
from gameboard import Gameboard
from ghost import Ghosts
from pacman import Pacman
from scoreboard import Scoreboard
from settings import Settings
from sound import Sound


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height  # tuple
        self.screen = pg.display.set_mode(size=size)

        # self.sound = Sound(bg_music="sounds/startrek.wav")
        # self.scoreboard = Scoreboard(game=self)

        self.gameboard = Gameboard(game=self)
        self.pacman = Pacman(game=self)
        self.ghost = Ghosts(game=self)

        self.times = [7.0,20.0,7.0,20.0,5.0,20.0,5.0]
        self.timer = 0.0
        self.timer_index = 0
        self.scared_time = 10.0
        self.scared_timer = 0.0

        self.gameover = False

    def reset(self):
        print("Resetting game...")

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
        while True:
            if self.gameover:
                break

            start_time = time()
            gf.check_events(game=self)
            self.screen.fill(self.settings.bg_color)

            if self.timer_index < len(self.times) and time() - self.timer > self.times[self.timer_index]:
                self.ghost.switch_mode()
                self.timer_index += 1
                self.timer = time()

            self.gameboard.draw()
            self.pacman.update()
            self.ghost.update()

            if self.settings.scared_mode is True:
                self.scared_timer = time()
                self.settings.scared_mode = False
            elif time() - self.scared_timer > self.scared_time:
                self.ghost.unscare()                    

            pg.display.flip()
            elapsed = time() - start_time
            while elapsed < frametime:  # run with a max fps of 60
                elapsed = time() - start_time


def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()
