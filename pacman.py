import pygame as pg

import game_functions as gf
from character import Character, Direction
from spritesheet import SpriteSheet
from timer import TimerDict, Timer


class Pacman(Character):
    def __init__(self, game):
        super().__init__(game=game)
        self.game = game
        self.lives = 3
        self.pos = game.settings.pacman_start
        self.start_pos = self.pos
        self.target_pos = game.settings.pacman_start

        self.images = SpriteSheet("images/pacman.png", "pacman_spritesheet.json")

        images_dict = {
            "start": [self.images.get_sprite("Pacman_Circle.png")],
            "up": [
                self.images.get_sprite("Pacman_Circle.png"),
                self.images.get_sprite("Pacman_Up1.png"),
                self.images.get_sprite("Pacman_Up2.png"),
                self.images.get_sprite("Pacman_Up1.png"),
            ],
            "left": [
                self.images.get_sprite("Pacman_Circle.png"),
                self.images.get_sprite("Pacman_Left1.png"),
                self.images.get_sprite("Pacman_Left2.png"),
                self.images.get_sprite("Pacman_Left1.png"),
            ],
            "down": [
                self.images.get_sprite("Pacman_Circle.png"),
                self.images.get_sprite("Pacman_Down1.png"),
                self.images.get_sprite("Pacman_Down2.png"),
                self.images.get_sprite("Pacman_Down1.png"),
            ],
            "right": [
                self.images.get_sprite("Pacman_Circle.png"),
                self.images.get_sprite("Pacman_Right1.png"),
                self.images.get_sprite("Pacman_Right2.png"),
                self.images.get_sprite("Pacman_Right1.png"),
            ],
            "dead": [self.images.get_sprite(f"Pacman_Dying{n}.png") for n in range(1, 17)],
        }

        self.timer_dict = TimerDict(dict_frames=images_dict, first_key="start", wait=100)
        self.dying_timer = Timer(frames=images_dict["dead"], looponce=True)
        self.next_dir = Direction.NONE

        self.dying = False
        self.init_speed()

    def init_speed(self):
        round = self.game.round_number
        if round == 0:
            print("80% move speed")
            self.move_speed = self.game.settings.base_speed * 0.8
        elif round < 4:
            print("80% move speed")
            self.move_speed = self.game.settings.base_speed * 0.9
        else:
            print("80% move speed")
            self.move_speed = self.game.settings.base_speed * 1.0
        print(f"Move speed: {self.move_speed}")

    def reset(self):
        super().reset()
        self.dying = False
        self.pos = self.game.settings.pacman_start
        self.start_pos = self.pos
        self.target_pos = self.pos
        self.init_speed()

    def die(self):
        print("Pacman killed!")
        self.dying = True
        self.dying_timer.reset()
        self.lives -= 1
        print(f"{self.lives} lives remaining")

    def update(self):
        if not self.isMoving:
            self.gameboard.pacman_collision_check(self.pos)

        if not self.dying:
            self.move()

            if self.dir is Direction.UP:
                self.timer_dict.switch_timer("up")
            elif self.dir is Direction.LEFT:
                self.timer_dict.switch_timer("left")
            elif self.dir is Direction.DOWN:
                self.timer_dict.switch_timer("down")
            elif self.dir is Direction.RIGHT:
                self.timer_dict.switch_timer("right")

        if self.dying and self.dying_timer.finished:
            if self.lives > 0:
                self.game.reset()
            else:
                self.game.game_over()
            return

        self.draw()

    def draw(self):
        pos = gf.world_to_screen(self.pos)
        if self.dying:
            self.dying_timer.advance_frame_index()
            image = self.dying_timer.imagerect()
        else:
            if self.dir is not Direction.NONE:
                self.timer_dict.advance_frame_index()
            image = self.timer_dict.imagerect()

        rect = image.get_rect()
        rect.center = pos[0], pos[1]
        self.screen.blit(image, rect)
