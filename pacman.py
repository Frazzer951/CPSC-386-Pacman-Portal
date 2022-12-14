import pygame
from pygame import mixer, transform

import game_functions as gf
from character import Character, Direction
from spritesheet import SpriteSheet
from timer import Timer, TimerDict


class Pacman(Character):
    def __init__(self, game):
        super().__init__(game=game)
        self.game = game
        self.lives = 3
        self.pos = game.settings.pacman_start
        self.start_pos = self.pos
        self.target_pos = game.settings.pacman_start

        self.images = SpriteSheet("images/pacman.png", "pacman_spritesheet.json")
        self.lives_image = self.images.get_sprite("Pacman_Right1.png")
        self.lives_image = transform.scale(self.lives_image, (50, 50))

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
        self.dying_timer = Timer(frames=images_dict["dead"], wait=200, looponce=True)
        self.next_dir = Direction.NONE

        self.dying = False
        self.init_speed()

    def init_speed(self):
        round = self.game.round_number
        if round == 0:
            self.move_speed = self.game.settings.base_speed * 0.8
        elif round < 4:
            self.move_speed = self.game.settings.base_speed * 0.9
        else:
            self.move_speed = self.game.settings.base_speed * 1.0

    def reset(self):
        super().reset()
        self.dying = False
        self.pos = self.game.settings.pacman_start
        self.start_pos = self.pos
        self.target_pos = self.pos
        self.init_speed()

    def die(self):
        self.game.sound.stop()
        self.mixer = mixer.init()
        self.deadsound = pygame.mixer.Sound("sounds/pacman_death.wav")
        self.deadsound.set_volume(0.2)
        # print("Pacman killed!")
        self.dying = True
        self.deadsound.play()
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
                # self.game.reset()
                self.reset()
                self.game.ghosts.reset()
                self.game.sound.play(-1)
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

        rect.center = 40, 780
        for _ in range(self.lives):
            self.screen.blit(self.lives_image, rect)
            rect.x += 40

        image = self.game.fruits[min(self.game.round_number, 7)]
        rect = image.get_rect()
        rect.center = 610, 775
        self.screen.blit(image, rect)
