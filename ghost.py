import pygame as pg

import game_functions as gf
from character import Character, Direction
from vector import Vector
from spritesheet import SpriteSheet
from timer import TimerDict


class Ghost(Character):
    def __init__(self, game, screen):
        super().__init__(game=game)
        self.gameboard = game.gameboard
        self.screen = screen
        self.movement_images = ()
        self.scared_images = ()
        self.eye_images = ()
        self.scared = False
        #self.pos = Vector(0, 0)
        self.color = (0, 0, 0)
        self.screen = game.screen
        self.timer_dict = {}

        self.temp = 0

    def draw(self):
        pos = gf.world_to_screen(self.pos)
        #pg.draw.circle(self.screen, self.color, pos, 10)
        self.timer_dict.advance_frame_index()
        image = self.timer_dict.imagerect()
        rect = image.get_rect()
        rect.center = pos[0], pos[1]
        self.screen.blit(image, rect)

    def update(self):
        # if not self.isMoving:
        #     self.next_dir = Direction.UP
        #     self.timer_dict.switch_timer("forward")
        # else:
        #     self.next_dir = Direction.NONE
        #     self.timer_dict.switch_timer("up")
        #a = {0:Direction.UP, 1:Direction.RIGHT, 2:Direction.DOWN, 3:Direction.LEFT}

        #if self.isMoving is False:
        #    self.temp += 1
        #    self.temp %= 4
        #    self.next_dir = a[self.temp]

        if self.next_dir is Direction.UP:
            self.timer_dict.switch_timer("up")
        elif self.next_dir is Direction.DOWN:
            self.timer_dict.switch_timer("down")
        elif self.next_dir is Direction.LEFT:
            self.timer_dict.switch_timer("left")
        elif self.next_dir is Direction.RIGHT:
            self.timer_dict.switch_timer("right")
        else:
            self.timer_dict.switch_timer("forward")
        self.move()
        self.draw()


class Blinky(Ghost):
    def __init__(self, game, images, scared_images, eye_images, pacman):
        super().__init__(game=game,screen=game.screen)
        self.pos = game.settings.blinky_start
        self.color = (255, 0, 0)
        self.screen = game.screen
        self.graph = game.gameboard.graph
        self.pacman = pacman

        self.movement_images = images
        self.scared_images = scared_images
        self.eye_images = eye_images

        images_dict = {"forward":[images[0],images[1]],"up":[images[2],images[3]],"down":[images[4],images[5]],
                       "left":[images[6],images[7]],"right":[images[8],images[9]], "scared":[scared_images[0],scared_images[1]],
                       "flashing":[scared_images[0],scared_images[1],scared_images[2],scared_images[3]],
                       "eye_forward":[eye_images[0]], "eye_up":[eye_images[1]],"eye_down":[eye_images[2]],"eye_left":[eye_images[3]],"eye_right":[eye_images[4]]}

        self.timer_dict = TimerDict(images_dict, "forward")

    def next_move(self):
        if self.isMoving:
            return
        pac_pos = self.pacman.target_pos
        Q = []
        neighbors = self.graph.get_neighbors(pac_pos)
        for neighbor in neighbors:
            Q.append((neighbor.pos, pac_pos))
        visit = [pac_pos]
        curr_pos = None
        while True:
            curr_pos = Q[0][0]
            last_pos = Q[0][1]
            visit.append(curr_pos)

            if curr_pos == self.pos:
                x = last_pos.x - curr_pos.x
                y = last_pos.y - curr_pos.y
                if x < 0: self.next_dir = Direction.LEFT
                elif x > 0: self.next_dir = Direction.RIGHT
                elif y < 0: self.next_dir = Direction.UP
                elif y > 0: self.next_dir = Direction.DOWN
                else: self.next_dir = Direction.NONE
                return

            if len(Q) < 2:
                Q = []
            else:
                Q = Q[1:]
            
            neighbors = self.graph.get_neighbors(curr_pos)
            for neighbor in neighbors:
                if neighbor.pos not in visit:
                    Q.append((neighbor.pos, curr_pos))
            


class Inky(Ghost):
    def __init__(self, game, images, scared_images, eye_images):
        super().__init__(game=game,screen=game.screen)
        self.pos = game.settings.inky_start
        self.color = (0, 255, 0)
        self.screen = game.screen

        self.movement_images = images
        self.scared_images = scared_images
        self.eye_images = eye_images

        images_dict = {"forward":[images[0],images[1]],"up":[images[2],images[3]],"down":[images[4],images[5]],
                       "left":[images[6],images[7]],"right":[images[8],images[9]], "scared":[scared_images[0],scared_images[1]],
                       "flashing":[scared_images[0],scared_images[1],scared_images[2],scared_images[3]],
                       "eye_forward":[eye_images[0]], "eye_up":[eye_images[1]],"eye_down":[eye_images[2]],"eye_left":[eye_images[3]],"eye_right":[eye_images[4]]}

        self.timer_dict = TimerDict(images_dict, "forward")

    def next_move(self): pass


class Pinky(Ghost):
    def __init__(self, game, images, scared_images, eye_images):
        super().__init__(game=game,screen=game.screen)
        self.pos = game.settings.pinky_start
        self.color = (0, 0, 255)
        self.screen = game.screen

        self.movement_images = images
        self.scared_images = scared_images
        self.eye_images = eye_images

        images_dict = {"forward":[images[0],images[1]],"up":[images[2],images[3]],"down":[images[4],images[5]],
                       "left":[images[6],images[7]],"right":[images[8],images[9]], "scared":[scared_images[0],scared_images[1]],
                       "flashing":[scared_images[0],scared_images[1],scared_images[2],scared_images[3]],
                       "eye_forward":[eye_images[0]], "eye_up":[eye_images[1]],"eye_down":[eye_images[2]],"eye_left":[eye_images[3]],"eye_right":[eye_images[4]]}

        self.timer_dict = TimerDict(images_dict, "forward")

    def next_move(self): pass


class Clyde(Ghost):
    def __init__(self, game, images, scared_images, eye_images):
        super().__init__(game=game,screen=game.screen)
        self.pos = game.settings.clyde_start
        self.color = (255, 255, 255)
        self.screen = game.screen

        self.movement_images = images
        self.scared_images = scared_images
        self.eye_images = eye_images

        images_dict = {"forward":[images[0],images[1]],"up":[images[2],images[3]],"down":[images[4],images[5]],
                       "left":[images[6],images[7]],"right":[images[8],images[9]], "scared":[scared_images[0],scared_images[1]],
                       "flashing":[scared_images[0],scared_images[1],scared_images[2],scared_images[3]],
                       "eye_forward":[eye_images[0]], "eye_up":[eye_images[1]],"eye_down":[eye_images[2]],"eye_left":[eye_images[3]],"eye_right":[eye_images[4]]}

        self.timer_dict = TimerDict(images_dict, "forward")

    def next_move(self): pass


class Ghosts:
    def __init__(self, game):
        self.game = game

        self.ghost_images = SpriteSheet("images/ghosts.png", "ghosts_spritesheet.json")
        blinky_images = [self.ghost_images.get_sprite(f"Blinky_{n}.png") for n in range(1,11)]
        inky_images = [self.ghost_images.get_sprite(f"Inky_{n}.png") for n in range(1,11)]
        pinky_images = [self.ghost_images.get_sprite(f"Pinky_{n}.png") for n in range(1,11)]
        clyde_images = [self.ghost_images.get_sprite(f"Clyde_{n}.png") for n in range(1,11)]
        eye_images = [self.ghost_images.get_sprite(f"Eyes_{n}.png") for n in range(1,6)]
        scared_images = [self.ghost_images.get_sprite("Running_1.png"), self.ghost_images.get_sprite("Running_2.png"),
                         self.ghost_images.get_sprite("Flashing_1.png"), self.ghost_images.get_sprite("Flashing_2.png")]

        self.ghosts = [Blinky(self.game, blinky_images, scared_images, eye_images, game.pacman), Inky(self.game, inky_images, scared_images, eye_images), 
                       Pinky(self.game, pinky_images, scared_images, eye_images), Clyde(self.game, clyde_images, scared_images, eye_images)]

    def update(self):
        for ghost in self.ghosts:
            ghost.next_move()
            ghost.update()
