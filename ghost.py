import pygame as pg

import game_functions as gf
from character import Character, Direction
from vector import Vector
from spritesheet import SpriteSheet
from timer import TimerDict


# def next_move(pos, target_pos, curr_dir, graph):
#     dists = []
    
#     if curr_dir == Direction.UP: back_dir = Direction.DOWN
#     elif curr_dir == Direction.LEFT: back_dir = Direction.RIGHT
#     elif curr_dir == Direction.DOWN: back_dir = Direction.UP
#     elif curr_dir == Direction.RIGHT: back_dir = Direction.LEFT
#     else: back_dir = Direction.NONE

#     # UP
#     up_pos = Vector(pos.x, pos.y - 1)
#     dist = (target_pos.x - up_pos.x) ** 2 + (target_pos.y - up_pos.y) ** 2
#     dists.append((dist, up_pos, Direction.UP))
#     # LEFT
#     left_pos = Vector(pos.x - 1, pos.y)
#     dist = (target_pos.x - left_pos.x) ** 2 + (target_pos.y - left_pos.y) ** 2
#     dists.append((dist, left_pos, Direction.LEFT))
#     # DOWN
#     down_pos = Vector(pos.x, pos.y + 1)
#     dist = (target_pos.x - down_pos.x) ** 2 + (target_pos.y - down_pos.y) ** 2
#     dists.append((dist, down_pos, Direction.DOWN))
#     # RIGHT
#     right_pos = Vector(pos.x + 1, pos.y)
#     dist = (target_pos.x - right_pos.x) ** 2 + (target_pos.y - right_pos.y) ** 2
#     dists.append((dist, right_pos, Direction.RIGHT))

#     dists = sorted(dists, key = lambda x: x[0])
#     for i in range(1, len(dists)):
#         if i > 0 and dists[i][0] == dists[i - 1][0]:
#             if dists[i][2] is Direction.UP:
#                 dists[i], dists[i - 1] = dists[i - 1], dists[i]
#             elif dists[i][2] is Direction.LEFT and dists[i - 1][2] is not Direction.UP:
#                 dists[i], dists[i - 1] = dists[i - 1], dists[i]
#             elif dists[i][2] is Direction.DOWN and dists[i - 1][2] is not Direction.UP and dists[i - 1][2] is not Direction.LEFT:
#                 dists[i], dists[i - 1] = dists[i - 1], dists[i]
#             i -= 1 
    
#     for dir in dists:
#         node = graph.get_node_at(up_pos)
#         if node is not None and dir[1] == node.pos and dir[2] is not back_dir and up_pos != Vector(11, 9) and up_pos != Vector(14, 9) and up_pos != Vector(11, 21) and up_pos != Vector(14, 21):
#             return dir[2]
#         node = graph.get_node_at(left_pos)
#         if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
#             return dir[2]
#         node = graph.get_node_at(down_pos)
#         if node is not None and dir[1] == node.pos and dir[2] is not back_dir and down_pos != Vector(12, 11) and down_pos != Vector(13, 11):
#             return dir[2]
#         node = graph.get_node_at(right_pos)
#         if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
#             return dir[2]

class Ghost(Character):
    def __init__(self, game, screen):
        super().__init__(game=game)
        self.gameboard = game.gameboard
        self.screen = screen
        self.movement_images = ()
        self.scared_images = ()
        self.eye_images = ()
        self.scared = False
        self.eaten = False
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

    def move_to(self):
        if self.game.settings.chase_mode:
            target_pos = self.pacman.pos
        else:
            target_pos = Vector(25, -1)

        # self.next_dir = next_move(self.pos, target_pos, self.dir, self.graph)
        pos = self.pos
        dists = []
        
        if self.dir == Direction.UP: back_dir = Direction.DOWN
        elif self.dir == Direction.LEFT: back_dir = Direction.RIGHT
        elif self.dir == Direction.DOWN: back_dir = Direction.UP
        elif self.dir == Direction.RIGHT: back_dir = Direction.LEFT
        else: back_dir = Direction.NONE

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

        dists = sorted(dists, key = lambda x: x[0])
        for i in range(1, len(dists)):
            if i > 0 and dists[i][0] == dists[i - 1][0]:
                if dists[i][2] is Direction.UP:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                elif dists[i][2] is Direction.LEFT and dists[i - 1][2] is not Direction.UP:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                elif dists[i][2] is Direction.DOWN and dists[i - 1][2] is not Direction.UP and dists[i - 1][2] is not Direction.LEFT:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                i -= 1 
        
        for dir in dists:
            node = self.graph.get_node_at(up_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir and up_pos != Vector(11, 9) and up_pos != Vector(14, 9) and up_pos != Vector(11, 21) and up_pos != Vector(14, 21):
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(left_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(down_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir and down_pos != Vector(12, 11) and down_pos != Vector(13, 11):
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(right_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                self.next_dir = dir[2]; return


class Inky(Ghost):
    def __init__(self, game, images, scared_images, eye_images, pacman, blinky):
        super().__init__(game=game,screen=game.screen)
        self.pos = game.settings.inky_start
        self.color = (0, 255, 0)
        self.screen = game.screen
        self.graph = game.gameboard.graph
        self.pacman = pacman
        self.blinky_pos = blinky

        self.movement_images = images
        self.scared_images = scared_images
        self.eye_images = eye_images

        images_dict = {"forward":[images[0],images[1]],"up":[images[2],images[3]],"down":[images[4],images[5]],
                       "left":[images[6],images[7]],"right":[images[8],images[9]], "scared":[scared_images[0],scared_images[1]],
                       "flashing":[scared_images[0],scared_images[1],scared_images[2],scared_images[3]],
                       "eye_forward":[eye_images[0]], "eye_up":[eye_images[1]],"eye_down":[eye_images[2]],"eye_left":[eye_images[3]],"eye_right":[eye_images[4]]}

        self.timer_dict = TimerDict(images_dict, "forward")

    def move_to(self):
        if self.game.settings.chase_mode:
            if self.pacman.dir is Direction.UP: target_pos = self.pacman.pos + Vector(0, -2)
            elif self.pacman.dir is Direction.LEFT: target_pos = self.pacman.pos + Vector(-2, 0)
            elif self.pacman.dir is Direction.DOWN: target_pos = self.pacman.pos + Vector(0, 2)
            elif self.pacman.dir is Direction.RIGHT: target_pos = self.pacman.pos + Vector(2, 0)
            else: target_pos = Vector(25, 29)
            target_pos = self.blinky_pos - target_pos
            target_pos *= -1
        else:
            target_pos = Vector(25, 29)
        
        # self.next_dir = next_move(self.pos, target_pos, self.dir, self.graph)
        pos = self.pos
        dists = []
        
        if self.dir == Direction.UP: back_dir = Direction.DOWN
        elif self.dir == Direction.LEFT: back_dir = Direction.RIGHT
        elif self.dir == Direction.DOWN: back_dir = Direction.UP
        elif self.dir == Direction.RIGHT: back_dir = Direction.LEFT
        else: back_dir = Direction.NONE

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

        dists = sorted(dists, key = lambda x: x[0])
        for i in range(1, len(dists)):
            if i > 0 and dists[i][0] == dists[i - 1][0]:
                if dists[i][2] is Direction.UP:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                elif dists[i][2] is Direction.LEFT and dists[i - 1][2] is not Direction.UP:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                elif dists[i][2] is Direction.DOWN and dists[i - 1][2] is not Direction.UP and dists[i - 1][2] is not Direction.LEFT:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                i -= 1 
        
        for dir in dists:
            node = self.graph.get_node_at(up_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir and up_pos != Vector(11, 9) and up_pos != Vector(14, 9) and up_pos != Vector(11, 21) and up_pos != Vector(14, 21):
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(left_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(down_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir and down_pos != Vector(12, 11) and down_pos != Vector(13, 11):
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(right_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                self.next_dir = dir[2]; return


class Pinky(Ghost):
    def __init__(self, game, images, scared_images, eye_images, pacman):
        super().__init__(game=game,screen=game.screen)
        self.pos = game.settings.pinky_start
        self.color = (0, 0, 255)
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

    def move_to(self):
        if self.game.settings.chase_mode:
            if self.pacman.dir is Direction.UP: target_pos = self.pacman.pos + Vector(0, -4)
            elif self.pacman.dir is Direction.LEFT: target_pos = self.pacman.pos + Vector(-4, 0)
            elif self.pacman.dir is Direction.DOWN: target_pos = self.pacman.pos + Vector(0, 4)
            elif self.pacman.dir is Direction.RIGHT: target_pos = self.pacman.pos + Vector(4, 0)
            else: target_pos = Vector(0, -1)
        else:
            target_pos = Vector(0, -1)
            
        # self.next_dir = next_move(self.pos, target_pos, self.dir, self.graph)
        pos = self.pos
        dists = []
        
        if self.dir == Direction.UP: back_dir = Direction.DOWN
        elif self.dir == Direction.LEFT: back_dir = Direction.RIGHT
        elif self.dir == Direction.DOWN: back_dir = Direction.UP
        elif self.dir == Direction.RIGHT: back_dir = Direction.LEFT
        else: back_dir = Direction.NONE

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

        dists = sorted(dists, key = lambda x: x[0])
        for i in range(1, len(dists)):
            if i > 0 and dists[i][0] == dists[i - 1][0]:
                if dists[i][2] is Direction.UP:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                elif dists[i][2] is Direction.LEFT and dists[i - 1][2] is not Direction.UP:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                elif dists[i][2] is Direction.DOWN and dists[i - 1][2] is not Direction.UP and dists[i - 1][2] is not Direction.LEFT:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                i -= 1 
        
        for dir in dists:
            node = self.graph.get_node_at(up_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir and up_pos != Vector(11, 9) and up_pos != Vector(14, 9) and up_pos != Vector(11, 21) and up_pos != Vector(14, 21):
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(left_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(down_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir and down_pos != Vector(12, 11) and down_pos != Vector(13, 11):
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(right_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                self.next_dir = dir[2]; return


class Clyde(Ghost):
    def __init__(self, game, images, scared_images, eye_images, pacman):
        super().__init__(game=game,screen=game.screen)
        self.pos = game.settings.clyde_start
        self.color = (255, 255, 255)
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

    def move_to(self):
        if self.game.settings.chase_mode:
            if (self.pos.x - self.pacman.pos.x) ** 2 + (self.pos.y - self.pacman.pos.y) ** 2 > 64:
                target_pos = self.pacman.pos
            else:
                target_pos = Vector(0, 29)
        else:
            target_pos = Vector(0, 29)
        
        # self.next_dir = next_move(self.pos, target_pos, self.dir, self.graph)
        pos = self.pos
        dists = []
        
        if self.dir == Direction.UP: back_dir = Direction.DOWN
        elif self.dir == Direction.LEFT: back_dir = Direction.RIGHT
        elif self.dir == Direction.DOWN: back_dir = Direction.UP
        elif self.dir == Direction.RIGHT: back_dir = Direction.LEFT
        else: back_dir = Direction.NONE

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

        dists = sorted(dists, key = lambda x: x[0])
        for i in range(1, len(dists)):
            if i > 0 and dists[i][0] == dists[i - 1][0]:
                if dists[i][2] is Direction.UP:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                elif dists[i][2] is Direction.LEFT and dists[i - 1][2] is not Direction.UP:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                elif dists[i][2] is Direction.DOWN and dists[i - 1][2] is not Direction.UP and dists[i - 1][2] is not Direction.LEFT:
                    dists[i], dists[i - 1] = dists[i - 1], dists[i]
                i -= 1 
        
        for dir in dists:
            node = self.graph.get_node_at(up_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir and up_pos != Vector(11, 9) and up_pos != Vector(14, 9) and up_pos != Vector(11, 21) and up_pos != Vector(14, 21):
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(left_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(down_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir and down_pos != Vector(12, 11) and down_pos != Vector(13, 11):
                self.next_dir = dir[2]; return
            node = self.graph.get_node_at(right_pos)
            if node is not None and dir[1] == node.pos and dir[2] is not back_dir:
                self.next_dir = dir[2]; return


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

        self.ghosts = [Blinky(self.game, blinky_images, scared_images, eye_images, game.pacman)]
        self.ghosts.append(Inky(self.game, inky_images, scared_images, eye_images, game.pacman, self.ghosts[0].pos))
        self.ghosts.append(Pinky(self.game, pinky_images, scared_images, eye_images, game.pacman))
        self.ghosts.append(Clyde(self.game, clyde_images, scared_images, eye_images, game.pacman))

    def update(self):
        for ghost in self.ghosts:
            ghost.move_to()
            ghost.update()
