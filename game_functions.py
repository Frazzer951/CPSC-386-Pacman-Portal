import sys
from pathlib import Path

import pygame as pg

from vector import Vector


def check_keydown_events(event, settings):
    key = event.key


def check_keyup_events(event):
    key = event.key


def check_events(settings):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            check_keydown_events(event=event, settings=settings)
        elif event.type == pg.KEYUP:
            check_keyup_events(event=event)


def world_to_screen(pos):
    x_offset = 15
    x_scale = 20
    y_offset = 15
    y_scale = 20

    return (pos.x * x_scale + x_offset, pos.y * y_scale + y_offset)


def clamp(posn, rect, settings):
    left, top = posn.x, posn.y
    width, height = rect.width, rect.height
    left = max(0, min(left, settings.screen_width - width))
    top = max(0, min(top, settings.screen_height - height))
    return Vector(x=left, y=top), pg.Rect(left, top, width, height)


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
