from gameboard import Gameboard
from scoreboard import Scoreboard
from settings import Settings
from sound import Sound
from time import time
import game_functions as gf
import pygame as pg
from pacman import Pacman


class Game:
    def __init__(self):
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height  # tuple
        self.screen = pg.display.set_mode(size=size)

        # self.sound = Sound(bg_music="sounds/startrek.wav")
        # self.scoreboard = Scoreboard(game=self)

        self.gameboard = Gameboard(game=self)
        self.pacman = Pacman(game=self)

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
        while True:
            if self.gameover:
                break

            start_time = time()
            gf.check_events(settings=self.settings)
            self.screen.fill(self.settings.bg_color)

            self.gameboard.draw()
            self.pacman.update()

            pg.display.flip()
            elapsed = time() - start_time
            while elapsed < frametime:  # run with a max fps of 60
                elapsed = time() - start_time


def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()
