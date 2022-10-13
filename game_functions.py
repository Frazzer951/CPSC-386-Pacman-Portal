import sys
from pathlib import Path

import pygame as pg

from character import Direction


def check_keydown_events(event, game):
    key = event.key
    if key == pg.K_w:
        game.pacman.next_dir = Direction.UP
    if key == pg.K_a:
        game.pacman.next_dir = Direction.LEFT
    if key == pg.K_s:
        game.pacman.next_dir = Direction.DOWN
    if key == pg.K_d:
        game.pacman.next_dir = Direction.RIGHT


def check_keyup_events(event):
    key = event.key


def check_events(game):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            check_keydown_events(event=event, game=game)
        elif event.type == pg.KEYUP:
            check_keyup_events(event=event)


def world_to_screen(pos):
    x_offset = 50
    y_offset = 105
    x_scale = 22
    y_scale = 22

    return (pos.x * x_scale + x_offset, pos.y * y_scale + y_offset)


def read_high_scores():
    file = Path("highscores.dat")
    file.touch(exist_ok=True)  # create the file if it doesn't exist
    scores = []
    with open("highscores.dat", "r") as file:
        file_content = file.read()
        scores = [] if len(file_content) == 0 else file_content.split(",")
        scores = [int(score) for score in scores]
    return scores


def write_high_scores(scores):
    with open("highscores.dat", "w+") as file:
        scores = str(scores).strip("[]")
        file.write(scores)
