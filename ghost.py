from random import randint
from time import time

import game_functions as gf
from character import Character, Direction
from spritesheet import SpriteSheet
from timer import TimerDict
from vector import Vector
import pygame as pg


class Ghosts:
    def __init__(self, game):
        self.game = game

        self.times = [7.0, 20.0, 7.0, 20.0, 5.0, 20.0, 5.0]
        self.timer = 0.0
        self.timer_index = 0

        self.scared_time = 10.0
        self.scared_timer = 0.0
        self.scared_mode = False

        self.ghost_images = SpriteSheet("images/ghosts.png", "ghosts_spritesheet.json")
        blinky_images = [self.ghost_images.get_sprite(f"Blinky_{n}.png") for n in range(1, 11)]
        inky_images = [self.ghost_images.get_sprite(f"Inky_{n}.png") for n in range(1, 11)]
        pinky_images = [self.ghost_images.get_sprite(f"Pinky_{n}.png") for n in range(1, 11)]
        clyde_images = [self.ghost_images.get_sprite(f"Clyde_{n}.png") for n in range(1, 11)]
        eye_images = [self.ghost_images.get_sprite(f"Eyes_{n}.png") for n in range(1, 6)]
        scared_images = [
            self.ghost_images.get_sprite("Running_1.png"),
            self.ghost_images.get_sprite("Running_2.png"),
            self.ghost_images.get_sprite("Flashing_1.png"),
            self.ghost_images.get_sprite("Flashing_2.png"),
        ]

        self.ghosts = [Blinky(self.game, blinky_images, scared_images, eye_images)]
        self.ghosts.append(Inky(self.game, inky_images, scared_images, eye_images, self.ghosts[0].pos))
        self.ghosts.append(Pinky(self.game, pinky_images, scared_images, eye_images))
        self.ghosts.append(Clyde(self.game, clyde_images, scared_images, eye_images))

    def switch_mode(self):
        for ghost in self.ghosts:
            ghost.switch = True

            if ghost.dir is Direction.UP:
                ghost.next_dir = Direction.DOWN
            elif ghost.dir is Direction.LEFT:
                ghost.next_dir = Direction.RIGHT
            elif ghost.dir is Direction.DOWN:
                ghost.next_dir = Direction.UP
            elif ghost.dir is Direction.RIGHT:
                ghost.next_dir = Direction.LEFT
            else:
                ghost.next_dir = Direction.NONE

    def unscare(self):
        for ghost in self.ghosts:
            ghost.scared = False

    def scare(self):
        for ghost in self.ghosts:
            ghost.scared = True

    def update(self):
        if self.timer_index < len(self.times) and time() - self.timer > self.times[self.timer_index]:
            self.switch_mode()
            self.timer_index += 1
            self.timer = time()

        if self.scared_mode is True:
            self.scared_timer = time()
            self.scared_mode = False
            self.scare()
        elif time() - self.scared_timer > self.scared_time:
            self.unscare()

        for ghost in self.ghosts:
            ghost.update()
            if ghost.scared:
                ghost.scared_move()
                if pg.sprite.collide_rect(ghost, self.game.pacman):
                    print('Ghost eaten')
                    ghost.eaten = True
            else:
                ghost.move_to()
                ghost.eaten = False
                if pg.sprite.collide_rect(ghost, self.game.pacman):
                    self.game.pacman.lives -= 1
                    print('Pacman got no scoped')
            


class Ghost(Character):
    def __init__(self, game):
        super().__init__(game=game)
        self.gameboard = game.gameboard
        self.graph = game.gameboard.graph
        self.screen = game.screen
        self.pacman = game.pacman

        self.movement_images = ()
        self.scared_images = ()
        self.eye_images = ()
        self.chase = False
        self.switch = False
        self.scared = False
        self.just_scared = False
        self.eaten = False
        self.color = (0, 0, 0)
        self.screen = game.screen
        self.timer_dict = {}
        self.rect = None
        self.image = None
        self.pos = None

        self.temp = 0

    def scared_move(self):
        if self.isMoving:
            if self.eaten:  # To be implemented
                pos = self.pos
                target_pos = Vector(13, 13)
                if pos == target_pos:
                    self.eaten = False
                else:
                    dists = []

                    if self.dir == Direction.UP:
                        back_dir = Direction.DOWN
                    elif self.dir == Direction.LEFT:
                        back_dir = Direction.RIGHT
                    elif self.dir == Direction.DOWN:
                        back_dir = Direction.UP
                    elif self.dir == Direction.RIGHT:
                        back_dir = Direction.LEFT
                    else:
                        back_dir = Direction.NONE

                    # UP
                    up_pos = Vector(pos.x, pos.y - 1)
                    dist = (target_pos.x - up_pos.x) ** 2 + (target_pos.y - up_pos.y) ** 2
                    dists.append((dist, up_pos, Direction.UP))
                    # LEFT
                    left_pos = Vector(pos.x - 1, pos.y)
                    dist = (target_pos.x - left_pos.x) ** 2 + (target_pos.y - left_pos.y) ** 2
                    dists.append((dist, left_pos, Direction.LEFT))
                    # DOWN
                    down_pos = Vector(pos.x, pos.y + 1)
                    dist = (target_pos.x - down_pos.x) ** 2 + (target_pos.y - down_pos.y) ** 2
                    dists.append((dist, down_pos, Direction.DOWN))
                    # RIGHT
                    right_pos = Vector(pos.x + 1, pos.y)
                    dist = (target_pos.x - right_pos.x) ** 2 + (target_pos.y - right_pos.y) ** 2
                    dists.append((dist, right_pos, Direction.RIGHT))

                    dists = sorted(dists, key=lambda x: x[0])
                    for i in range(1, len(dists)):
                        if i > 0 and dists[i][0] == dists[i - 1][0]:
                            if dists[i][2] is Direction.UP:
                                dists[i], dists[i - 1] = dists[i - 1], dists[i]
                            elif dists[i][2] is Direction.LEFT and dists[i - 1][2] is not Direction.UP:
                                dists[i], dists[i - 1] = dists[i - 1], dists[i]
                            elif (
                                dists[i][2] is Direction.DOWN
                                and dists[i - 1][2] is not Direction.UP
                                and dists[i - 1][2] is not Direction.LEFT
                            ):
                                dists[i], dists[i - 1] = dists[i - 1], dists[i]
                            i -= 1

                    for dir in dists:
                        node = self.graph.get_node_at(up_pos)
                        if (
                            node is not None
                            and dir[1] == node.pos
                            and dir[2] is not back_dir
                            and up_pos != Vector(11, 9)
                            and up_pos != Vector(14, 9)
                            and up_pos != Vector(11, 21)
                            and up_pos != Vector(14, 21)
                        ):
                            self.next_dir = dir[2]
                            return
                        node = self.graph.get_node_at(left_pos)
                        if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                            self.next_dir = dir[2]
                            return
                        node = self.graph.get_node_at(down_pos)
                        if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                            self.next_dir = dir[2]
                            return
                        node = self.graph.get_node_at(right_pos)
                        if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                            self.next_dir = dir[2]
                            return

            else:
                if self.just_scared:
                    self.switch = False
                    if self.chase:
                        self.chase = False
                    else:
                        self.chase = True

                else:
                    pos = self.pos

                    if self.dir == Direction.UP:
                        back_dir = Direction.DOWN
                    elif self.dir == Direction.LEFT:
                        back_dir = Direction.RIGHT
                    elif self.dir == Direction.DOWN:
                        back_dir = Direction.UP
                    elif self.dir == Direction.RIGHT:
                        back_dir = Direction.LEFT
                    else:
                        back_dir = Direction.NONE

                    dirs = []

                    # UP
                    node = self.graph.get_node_at(Vector(pos.x, pos.y - 1))
                    if node is not None and back_dir is not Direction.UP:
                        dirs.append(Direction.UP)
                    # LEFT
                    node = self.graph.get_node_at(Vector(pos.x - 1, pos.y))
                    if node is not None and back_dir is not Direction.LEFT:
                        dirs.append(Direction.LEFT)
                    # DOWN
                    node = self.graph.get_node_at(Vector(pos.x, pos.y + 1))
                    if node is not None and back_dir is not Direction.DOWN:
                        dirs.append(Direction.DOWN)
                    # RIGHT
                    node = self.graph.get_node_at(Vector(pos.x + 1, pos.y))
                    if node is not None and back_dir is not Direction.RIGHT:
                        dirs.append(Direction.RIGHT)

                    if len(dirs) == 0:
                        self.next_dir = Direction.NONE
                    elif len(dirs) == 1:
                        self.next_dir = dirs[0]
                    else:
                        self.next_dir = dirs[randint(0, len(dirs) - 1)]

    def update(self):
        if self.scared is True:
            self.timer_dict.switch_timer("scared")
        elif self.eaten is True:
            if self.next_dir is Direction.UP:
                self.timer_dict.switch_timer("eye_up")
            elif self.next_dir is Direction.DOWN:
                self.timer_dict.switch_timer("eye_down")
            elif self.next_dir is Direction.LEFT:
                self.timer_dict.switch_timer("eye_left")
            elif self.next_dir is Direction.RIGHT:
                self.timer_dict.switch_timer("eye_right")
            else:
                self.timer_dict.switch_timer("eye_forward")
        else:
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

    def draw(self):
        pos = gf.world_to_screen(self.pos)
        # pg.draw.circle(self.screen, self.color, pos, 10)
        self.timer_dict.advance_frame_index()
        self.image = self.timer_dict.imagerect()
        self.rect = self.image.get_rect()
        self.rect.center = pos[0], pos[1]
        self.screen.blit(self.image, self.rect)


class Blinky(Ghost):
    def __init__(self, game, images, scared_images, eye_images):
        super().__init__(game=game)
        self.pos = game.settings.blinky_start
        self.color = (255, 0, 0)

        self.movement_images = images
        self.scared_images = scared_images
        self.eye_images = eye_images

        images_dict = {
            "forward": [images[0], images[1]],
            "up": [images[2], images[3]],
            "down": [images[4], images[5]],
            "left": [images[6], images[7]],
            "right": [images[8], images[9]],
            "scared": [scared_images[0], scared_images[1]],
            "flashing": [scared_images[0], scared_images[1], scared_images[2], scared_images[3]],
            "eye_forward": [eye_images[0]],
            "eye_up": [eye_images[1]],
            "eye_down": [eye_images[2]],
            "eye_left": [eye_images[3]],
            "eye_right": [eye_images[4]],
        }

        self.timer_dict = TimerDict(images_dict, "forward")

    def move_to(self):
        if not self.isMoving:
            if self.switch:
                self.switch = False
                if self.chase:
                    self.chase = False
                else:
                    self.chase = True

            else:
                if self.chase:
                    target_pos = self.pacman.pos
                else:
                    target_pos = Vector(25, -1)

                # self.next_dir = next_move(self.pos, target_pos, self.dir, self.graph)
                pos = self.pos
                dists = []

                if self.dir == Direction.UP:
                    back_dir = Direction.DOWN
                elif self.dir == Direction.LEFT:
                    back_dir = Direction.RIGHT
                elif self.dir == Direction.DOWN:
                    back_dir = Direction.UP
                elif self.dir == Direction.RIGHT:
                    back_dir = Direction.LEFT
                else:
                    back_dir = Direction.NONE

                # UP
                up_pos = Vector(pos.x, pos.y - 1)
                dist = (target_pos.x - up_pos.x) ** 2 + (target_pos.y - up_pos.y) ** 2
                dists.append((dist, up_pos, Direction.UP))
                # LEFT
                left_pos = Vector(pos.x - 1, pos.y)
                dist = (target_pos.x - left_pos.x) ** 2 + (target_pos.y - left_pos.y) ** 2
                dists.append((dist, left_pos, Direction.LEFT))
                # DOWN
                down_pos = Vector(pos.x, pos.y + 1)
                dist = (target_pos.x - down_pos.x) ** 2 + (target_pos.y - down_pos.y) ** 2
                dists.append((dist, down_pos, Direction.DOWN))
                # RIGHT
                right_pos = Vector(pos.x + 1, pos.y)
                dist = (target_pos.x - right_pos.x) ** 2 + (target_pos.y - right_pos.y) ** 2
                dists.append((dist, right_pos, Direction.RIGHT))

                dists = sorted(dists, key=lambda x: x[0])
                for i in range(1, len(dists)):
                    if i > 0 and dists[i][0] == dists[i - 1][0]:
                        if dists[i][2] is Direction.UP:
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        elif dists[i][2] is Direction.LEFT and dists[i - 1][2] is not Direction.UP:
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        elif (
                            dists[i][2] is Direction.DOWN
                            and dists[i - 1][2] is not Direction.UP
                            and dists[i - 1][2] is not Direction.LEFT
                        ):
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        i -= 1

                for dir in dists:
                    node = self.graph.get_node_at(up_pos)
                    if (
                        node is not None
                        and dir[1] == node.pos
                        and dir[2] is not back_dir
                        and up_pos != Vector(11, 9)
                        and up_pos != Vector(14, 9)
                        and up_pos != Vector(11, 21)
                        and up_pos != Vector(14, 21)
                    ):
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(left_pos)
                    if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(down_pos)
                    if (
                        node is not None
                        and dir[1] == node.pos
                        and dir[2] is not back_dir
                        and down_pos != Vector(12, 11)
                        and down_pos != Vector(13, 11)
                    ):
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(right_pos)
                    if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                        self.next_dir = dir[2]
                        return


class Inky(Ghost):
    def __init__(self, game, images, scared_images, eye_images, blinky):
        super().__init__(game=game)
        self.pos = game.settings.inky_start
        self.color = (0, 255, 0)
        self.blinky_pos = blinky

        self.movement_images = images
        self.scared_images = scared_images
        self.eye_images = eye_images

        images_dict = {
            "forward": [images[0], images[1]],
            "up": [images[2], images[3]],
            "down": [images[4], images[5]],
            "left": [images[6], images[7]],
            "right": [images[8], images[9]],
            "scared": [scared_images[0], scared_images[1]],
            "flashing": [scared_images[0], scared_images[1], scared_images[2], scared_images[3]],
            "eye_forward": [eye_images[0]],
            "eye_up": [eye_images[1]],
            "eye_down": [eye_images[2]],
            "eye_left": [eye_images[3]],
            "eye_right": [eye_images[4]],
        }

        self.timer_dict = TimerDict(images_dict, "forward")

    def move_to(self):
        if not self.isMoving:
            if self.switch:
                self.switch = False
                if self.chase:
                    self.chase = False
                else:
                    self.chase = True

            else:
                if self.chase:
                    if self.pacman.dir is Direction.UP:
                        target_pos = self.pacman.pos + Vector(0, -2)
                    elif self.pacman.dir is Direction.LEFT:
                        target_pos = self.pacman.pos + Vector(-2, 0)
                    elif self.pacman.dir is Direction.DOWN:
                        target_pos = self.pacman.pos + Vector(0, 2)
                    elif self.pacman.dir is Direction.RIGHT:
                        target_pos = self.pacman.pos + Vector(2, 0)
                    else:
                        target_pos = self.pacman.pos
                    target_pos = self.blinky_pos - target_pos
                    target_pos *= -1
                else:
                    target_pos = Vector(25, 29)

                # self.next_dir = next_move(self.pos, target_pos, self.dir, self.graph)
                pos = self.pos
                dists = []

                if self.dir == Direction.UP:
                    back_dir = Direction.DOWN
                elif self.dir == Direction.LEFT:
                    back_dir = Direction.RIGHT
                elif self.dir == Direction.DOWN:
                    back_dir = Direction.UP
                elif self.dir == Direction.RIGHT:
                    back_dir = Direction.LEFT
                else:
                    back_dir = Direction.NONE

                # UP
                up_pos = Vector(pos.x, pos.y - 1)
                dist = (target_pos.x - up_pos.x) ** 2 + (target_pos.y - up_pos.y) ** 2
                dists.append((dist, up_pos, Direction.UP))
                # LEFT
                left_pos = Vector(pos.x - 1, pos.y)
                dist = (target_pos.x - left_pos.x) ** 2 + (target_pos.y - left_pos.y) ** 2
                dists.append((dist, left_pos, Direction.LEFT))
                # DOWN
                down_pos = Vector(pos.x, pos.y + 1)
                dist = (target_pos.x - down_pos.x) ** 2 + (target_pos.y - down_pos.y) ** 2
                dists.append((dist, down_pos, Direction.DOWN))
                # RIGHT
                right_pos = Vector(pos.x + 1, pos.y)
                dist = (target_pos.x - right_pos.x) ** 2 + (target_pos.y - right_pos.y) ** 2
                dists.append((dist, right_pos, Direction.RIGHT))

                dists = sorted(dists, key=lambda x: x[0])
                for i in range(1, len(dists)):
                    if i > 0 and dists[i][0] == dists[i - 1][0]:
                        if dists[i][2] is Direction.UP:
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        elif dists[i][2] is Direction.LEFT and dists[i - 1][2] is not Direction.UP:
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        elif (
                            dists[i][2] is Direction.DOWN
                            and dists[i - 1][2] is not Direction.UP
                            and dists[i - 1][2] is not Direction.LEFT
                        ):
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        i -= 1

                for dir in dists:
                    node = self.graph.get_node_at(up_pos)
                    if (
                        node is not None
                        and dir[1] == node.pos
                        and dir[2] is not back_dir
                        and up_pos != Vector(11, 9)
                        and up_pos != Vector(14, 9)
                        and up_pos != Vector(11, 21)
                        and up_pos != Vector(14, 21)
                    ):
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(left_pos)
                    if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(down_pos)
                    if (
                        node is not None
                        and dir[1] == node.pos
                        and dir[2] is not back_dir
                        and down_pos != Vector(12, 11)
                        and down_pos != Vector(13, 11)
                    ):
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(right_pos)
                    if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                        self.next_dir = dir[2]
                        return


class Pinky(Ghost):
    def __init__(self, game, images, scared_images, eye_images):
        super().__init__(game=game)
        self.pos = game.settings.pinky_start
        self.color = (0, 0, 255)

        self.movement_images = images
        self.scared_images = scared_images
        self.eye_images = eye_images

        images_dict = {
            "forward": [images[0], images[1]],
            "up": [images[2], images[3]],
            "down": [images[4], images[5]],
            "left": [images[6], images[7]],
            "right": [images[8], images[9]],
            "scared": [scared_images[0], scared_images[1]],
            "flashing": [scared_images[0], scared_images[1], scared_images[2], scared_images[3]],
            "eye_forward": [eye_images[0]],
            "eye_up": [eye_images[1]],
            "eye_down": [eye_images[2]],
            "eye_left": [eye_images[3]],
            "eye_right": [eye_images[4]],
        }

        self.timer_dict = TimerDict(images_dict, "forward")

    def move_to(self):
        if not self.isMoving:
            if self.switch:
                self.switch = False
                if self.chase:
                    self.chase = False
                else:
                    self.chase = True

            else:
                if self.chase:
                    if self.pacman.dir is Direction.UP:
                        target_pos = self.pacman.pos + Vector(0, -4)
                    elif self.pacman.dir is Direction.LEFT:
                        target_pos = self.pacman.pos + Vector(-4, 0)
                    elif self.pacman.dir is Direction.DOWN:
                        target_pos = self.pacman.pos + Vector(0, 4)
                    elif self.pacman.dir is Direction.RIGHT:
                        target_pos = self.pacman.pos + Vector(4, 0)
                    else:
                        target_pos = self.pacman.pos
                else:
                    target_pos = Vector(0, -1)

                # self.next_dir = next_move(self.pos, target_pos, self.dir, self.graph)
                pos = self.pos
                dists = []

                if self.dir == Direction.UP:
                    back_dir = Direction.DOWN
                elif self.dir == Direction.LEFT:
                    back_dir = Direction.RIGHT
                elif self.dir == Direction.DOWN:
                    back_dir = Direction.UP
                elif self.dir == Direction.RIGHT:
                    back_dir = Direction.LEFT
                else:
                    back_dir = Direction.NONE

                # UP
                up_pos = Vector(pos.x, pos.y - 1)
                dist = (target_pos.x - up_pos.x) ** 2 + (target_pos.y - up_pos.y) ** 2
                dists.append((dist, up_pos, Direction.UP))
                # LEFT
                left_pos = Vector(pos.x - 1, pos.y)
                dist = (target_pos.x - left_pos.x) ** 2 + (target_pos.y - left_pos.y) ** 2
                dists.append((dist, left_pos, Direction.LEFT))
                # DOWN
                down_pos = Vector(pos.x, pos.y + 1)
                dist = (target_pos.x - down_pos.x) ** 2 + (target_pos.y - down_pos.y) ** 2
                dists.append((dist, down_pos, Direction.DOWN))
                # RIGHT
                right_pos = Vector(pos.x + 1, pos.y)
                dist = (target_pos.x - right_pos.x) ** 2 + (target_pos.y - right_pos.y) ** 2
                dists.append((dist, right_pos, Direction.RIGHT))

                dists = sorted(dists, key=lambda x: x[0])
                for i in range(1, len(dists)):
                    if i > 0 and dists[i][0] == dists[i - 1][0]:
                        if dists[i][2] is Direction.UP:
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        elif dists[i][2] is Direction.LEFT and dists[i - 1][2] is not Direction.UP:
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        elif (
                            dists[i][2] is Direction.DOWN
                            and dists[i - 1][2] is not Direction.UP
                            and dists[i - 1][2] is not Direction.LEFT
                        ):
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        i -= 1

                for dir in dists:
                    node = self.graph.get_node_at(up_pos)
                    if (
                        node is not None
                        and dir[1] == node.pos
                        and dir[2] is not back_dir
                        and up_pos != Vector(11, 9)
                        and up_pos != Vector(14, 9)
                        and up_pos != Vector(11, 21)
                        and up_pos != Vector(14, 21)
                    ):
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(left_pos)
                    if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(down_pos)
                    if (
                        node is not None
                        and dir[1] == node.pos
                        and dir[2] is not back_dir
                        and down_pos != Vector(12, 11)
                        and down_pos != Vector(13, 11)
                    ):
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(right_pos)
                    if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                        self.next_dir = dir[2]
                        return


class Clyde(Ghost):
    def __init__(self, game, images, scared_images, eye_images):
        super().__init__(game=game)
        self.pos = game.settings.clyde_start
        self.color = (255, 255, 255)

        self.movement_images = images
        self.scared_images = scared_images
        self.eye_images = eye_images

        images_dict = {
            "forward": [images[0], images[1]],
            "up": [images[2], images[3]],
            "down": [images[4], images[5]],
            "left": [images[6], images[7]],
            "right": [images[8], images[9]],
            "scared": [scared_images[0], scared_images[1]],
            "flashing": [scared_images[0], scared_images[1], scared_images[2], scared_images[3]],
            "eye_forward": [eye_images[0]],
            "eye_up": [eye_images[1]],
            "eye_down": [eye_images[2]],
            "eye_left": [eye_images[3]],
            "eye_right": [eye_images[4]],
        }

        self.timer_dict = TimerDict(images_dict, "forward")

    def move_to(self):
        if not self.isMoving:
            if self.switch:
                self.switch = False
                if self.chase:
                    self.chase = False
                else:
                    self.chase = True

            else:
                if self.chase:
                    if (self.pos.x - self.pacman.pos.x) ** 2 + (self.pos.y - self.pacman.pos.y) ** 2 > 64:
                        target_pos = self.pacman.pos
                    else:
                        target_pos = Vector(0, 29)
                else:
                    target_pos = Vector(0, 29)

                # self.next_dir = next_move(self.pos, target_pos, self.dir, self.graph)
                pos = self.pos
                dists = []

                if self.dir == Direction.UP:
                    back_dir = Direction.DOWN
                elif self.dir == Direction.LEFT:
                    back_dir = Direction.RIGHT
                elif self.dir == Direction.DOWN:
                    back_dir = Direction.UP
                elif self.dir == Direction.RIGHT:
                    back_dir = Direction.LEFT
                else:
                    back_dir = Direction.NONE

                # UP
                up_pos = Vector(pos.x, pos.y - 1)
                dist = (target_pos.x - up_pos.x) ** 2 + (target_pos.y - up_pos.y) ** 2
                dists.append((dist, up_pos, Direction.UP))
                # LEFT
                left_pos = Vector(pos.x - 1, pos.y)
                dist = (target_pos.x - left_pos.x) ** 2 + (target_pos.y - left_pos.y) ** 2
                dists.append((dist, left_pos, Direction.LEFT))
                # DOWN
                down_pos = Vector(pos.x, pos.y + 1)
                dist = (target_pos.x - down_pos.x) ** 2 + (target_pos.y - down_pos.y) ** 2
                dists.append((dist, down_pos, Direction.DOWN))
                # RIGHT
                right_pos = Vector(pos.x + 1, pos.y)
                dist = (target_pos.x - right_pos.x) ** 2 + (target_pos.y - right_pos.y) ** 2
                dists.append((dist, right_pos, Direction.RIGHT))

                dists = sorted(dists, key=lambda x: x[0])
                for i in range(1, len(dists)):
                    if i > 0 and dists[i][0] == dists[i - 1][0]:
                        if dists[i][2] is Direction.UP:
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        elif dists[i][2] is Direction.LEFT and dists[i - 1][2] is not Direction.UP:
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        elif (
                            dists[i][2] is Direction.DOWN
                            and dists[i - 1][2] is not Direction.UP
                            and dists[i - 1][2] is not Direction.LEFT
                        ):
                            dists[i], dists[i - 1] = dists[i - 1], dists[i]
                        i -= 1

                for dir in dists:
                    node = self.graph.get_node_at(up_pos)
                    if (
                        node is not None
                        and dir[1] == node.pos
                        and dir[2] is not back_dir
                        and up_pos != Vector(11, 9)
                        and up_pos != Vector(14, 9)
                        and up_pos != Vector(11, 21)
                        and up_pos != Vector(14, 21)
                    ):
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(left_pos)
                    if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(down_pos)
                    if (
                        node is not None
                        and dir[1] == node.pos
                        and dir[2] is not back_dir
                        and down_pos != Vector(12, 11)
                        and down_pos != Vector(13, 11)
                    ):
                        self.next_dir = dir[2]
                        return
                    node = self.graph.get_node_at(right_pos)
                    if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                        self.next_dir = dir[2]
                        return
