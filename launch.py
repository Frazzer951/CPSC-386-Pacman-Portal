import sys

import pygame as pg
from pygame import mixer
from pygame.sprite import Sprite

from button import Button
from spritesheet import SpriteSheet
from timer import Timer

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (106, 233, 115)
TRANSPARENT = (0, 0, 0, 1.0)


class Animation1(Sprite):
    def __init__(self, game, pacman_images, ghost_images):
        super().__init__()
        self.screen = game.screen

        self.menu = [
            pg.transform.scale(pg.image.load("images/menu0.png"), (350, 100)),
            pg.transform.scale(pg.image.load("images/menu1.png"), (350, 100)),
            pg.transform.scale(pg.image.load("images/menu2.png"), (350, 100)),
        ]
        self.timer = Timer(self.menu, oscillating=True)

        # self.x = 650
        self.pacman_x = 450
        self.blinky_x = 550
        self.pinky_x = 650
        self.inky_x = 750
        self.clyde_x = 850
        self.y = 450

        # self.rect = pg.Rect(self.x, self.y, 350, 100)

        blinky_images = [ghost_images[0], ghost_images[1]]
        pinky_images = [ghost_images[2], ghost_images[3]]
        inky_images = [ghost_images[4], ghost_images[5]]
        clyde_images = [ghost_images[6], ghost_images[7]]

        self.timer_pacman = Timer(frames=pacman_images, wait=100)
        self.timer_blinky = Timer(frames=blinky_images, wait=200)
        self.timer_pinky = Timer(frames=pinky_images, wait=200)
        self.timer_inky = Timer(frames=inky_images, wait=200)
        self.timer_clyde = Timer(frames=clyde_images, wait=200)

    def update(self):
        self.pacman_x -= 5
        self.blinky_x -= 5
        self.pinky_x -= 5
        self.inky_x -= 5
        self.clyde_x -= 5

    def draw(self):
        # self.timer.advance_frame_index()
        # image = self.timer.imagerect()
        # rect = image.get_rect()
        # rect.left, rect.top = self.rect.left, self.rect.top
        # self.screen.blit(image, rect)

        self.timer_pacman.advance_frame_index()
        image = self.timer_pacman.imagerect()
        image = pg.transform.scale(image, (150, 150))
        rect = image.get_rect()
        rect.left, rect.top = self.pacman_x, self.y
        self.screen.blit(image, rect)

        self.timer_blinky.advance_frame_index()
        image = self.timer_blinky.imagerect()
        image = pg.transform.scale(image, (150, 150))
        rect = image.get_rect()
        rect.left, rect.top = self.blinky_x, self.y
        self.screen.blit(image, rect)

        self.timer_pinky.advance_frame_index()
        image = self.timer_pinky.imagerect()
        image = pg.transform.scale(image, (150, 150))
        rect = image.get_rect()
        rect.left, rect.top = self.pinky_x, self.y
        self.screen.blit(image, rect)

        self.timer_inky.advance_frame_index()
        image = self.timer_inky.imagerect()
        image = pg.transform.scale(image, (150, 150))
        rect = image.get_rect()
        rect.left, rect.top = self.inky_x, self.y
        self.screen.blit(image, rect)

        self.timer_clyde.advance_frame_index()
        image = self.timer_clyde.imagerect()
        image = pg.transform.scale(image, (150, 150))
        rect = image.get_rect()
        rect.left, rect.top = self.clyde_x, self.y
        self.screen.blit(image, rect)


class Animation2(Sprite):
    def __init__(self, game, pacman_images, ghost_images):
        super().__init__()
        self.screen = game.screen

        self.menu = [
            pg.transform.scale(pg.image.load("images/menu3.png"), (350, 100)),
            pg.transform.scale(pg.image.load("images/menu4.png"), (350, 100)),
            pg.transform.scale(pg.image.load("images/menu5.png"), (350, 100)),
            pg.transform.scale(pg.image.load("images/menu6.png"), (350, 100)),
        ]
        self.timer = Timer(self.menu)

        # self.x = -100
        self.pacman_x = -350
        self.ghost1_x = -250
        self.ghost2_x = -150
        self.ghost3_x = -50
        self.ghost4_x = 50
        self.y = 290
        # self.rect = pg.Rect(self.x, self.y, 350, 100)

        self.timer_pacman = Timer(frames=pacman_images, wait=100)
        self.timer_ghost = Timer(frames=ghost_images, wait=200)

    def update(self):
        self.pacman_x += 5
        self.ghost1_x += 5
        self.ghost2_x += 5
        self.ghost3_x += 5
        self.ghost4_x += 5

    def draw(self):
        # self.timer.advance_frame_index()
        # image = self.timer.imagerect()
        # rect = image.get_rect()
        # rect.left, rect.top = self.rect.left, self.rect.top
        # self.screen.blit(image, rect)

        self.timer_pacman.advance_frame_index()
        image = self.timer_pacman.imagerect()
        image = pg.transform.scale(image, (150, 150))
        rect = image.get_rect()
        rect.left, rect.top = self.pacman_x, self.y
        self.screen.blit(image, rect)

        self.timer_ghost.advance_frame_index()
        image = self.timer_ghost.imagerect()
        image = pg.transform.scale(image, (150, 150))
        rect = image.get_rect()
        rect.left, rect.top = self.ghost1_x, self.y
        self.screen.blit(image, rect)

        rect.left, rect.top = self.ghost2_x, self.y
        self.screen.blit(image, rect)

        rect.left, rect.top = self.ghost3_x, self.y
        self.screen.blit(image, rect)

        rect.left, rect.top = self.ghost4_x, self.y
        self.screen.blit(image, rect)


class IntroduceBlinky:
    pg.font.init()

    def __init__(self, game, images):
        self.surface = game.screen
        # self.small_blinky = pg.image.load("images/blinky0.png")
        # self.blinky = pg.transform.scale(self.small_blinky, (120, 120))
        self.blinky = [images[0], images[1]]
        self.font = pg.font.Font("fonts/crackman.ttf", 32)
        self.blinky_text = self.font.render('"Blinky"', True, (255, 0, 0))

        self.timer = Timer(frames=self.blinky, wait=200)

    def draw(self):
        self.timer.advance_frame_index()
        image = self.timer.imagerect()
        image = pg.transform.scale(image, (200, 200))
        rect = image.get_rect()
        rect.center = 325, 420
        text_rect = self.blinky_text.get_rect()
        text_rect.center = 325, 520
        self.surface.blit(image, rect)
        self.surface.blit(self.blinky_text, text_rect)  # (250, 500)


class IntroducePinky:
    pg.font.init()

    def __init__(self, game, images):
        self.surface = game.screen
        # self.small_Pinky = pg.image.load("images/pinky0.png")
        # self.pinky = pg.transform.scale(self.small_Pinky, (120, 120))
        self.pinky = [images[0], images[1]]
        self.font = pg.font.Font("fonts/crackman.ttf", 32)
        self.pinky_text = self.font.render('"Pinky"', True, ("#FFB8FF"))

        self.timer = Timer(frames=self.pinky, wait=200)

    def draw(self):
        self.timer.advance_frame_index()
        image = self.timer.imagerect()
        image = pg.transform.scale(image, (200, 200))
        rect = image.get_rect()
        rect.center = 325, 420
        text_rect = self.pinky_text.get_rect()
        text_rect.center = 325, 520
        self.surface.blit(image, rect)
        self.surface.blit(self.pinky_text, text_rect)


class IntroduceInky:
    pg.font.init()

    def __init__(self, game, images):
        self.surface = game.screen
        # self.small_inky = pg.image.load("images/inky0.png")
        # self.inky = pg.transform.scale(self.small_inky, (120, 120))
        self.inky = [images[0], images[1]]
        self.font = pg.font.Font("fonts/crackman.ttf", 32)
        self.inky_text = self.font.render('"Inky"', True, ("#00FFFF"))

        self.timer = Timer(frames=self.inky, wait=200)

    def draw(self):
        self.timer.advance_frame_index()
        image = self.timer.imagerect()
        image = pg.transform.scale(image, (200, 200))
        rect = image.get_rect()
        rect.center = 325, 420
        text_rect = self.inky_text.get_rect()
        text_rect.center = 325, 520
        self.surface.blit(image, rect)
        self.surface.blit(self.inky_text, text_rect)


class IntroduceClyde:
    pg.font.init()

    def __init__(self, game, images):
        self.surface = game.screen
        # self.small_Clyde = pg.image.load("images/clyde0.png")
        # self.clyde = pg.transform.scale(self.small_Clyde, (120, 120))
        self.clyde = [images[0], images[1]]
        self.font = pg.font.Font("fonts/crackman.ttf", 32)
        self.clyde_text = self.font.render('"Clyde"', True, ("#FFB852"))

        self.timer = Timer(frames=self.clyde, wait=200)

    def draw(self):
        self.timer.advance_frame_index()
        image = self.timer.imagerect()
        image = pg.transform.scale(image, (200, 200))
        rect = image.get_rect()
        rect.center = 325, 420
        text_rect = self.clyde_text.get_rect()
        text_rect.center = 325, 520
        self.surface.blit(image, rect)
        self.surface.blit(self.clyde_text, text_rect)


class Howhigh:
    pg.font.init()

    def __init__(self, game):
        self.surface = game.screen
        self.font = pg.font.Font("fonts/crackman.ttf", 42)
        self.howhigh = self.font.render("How high can you score?", True, (249, 241, 0))

    def draw(self):
        self.surface.blit(self.howhigh, (40, 420))


class Launchscreen:
    pacman = pg.image.load("images/Pac-Man-0.png")
    title = pg.image.load("images/title.png")
    bigPacman = pg.transform.scale(pacman, (150, 150))
    bigtitle = pg.transform.scale(title, (653, 436))
    pg.font.init()

    x1 = 240
    y1 = 160
    titlex = 10
    titley = -80

    def __init__(self, game):
        self.screen = game.screen
        self.landing_page_finished = False

        pacman_sprites = SpriteSheet("images/pacman.png", "pacman_spritesheet.json")
        pacman_images1 = [
            pacman_sprites.get_sprite("Pacman_Circle.png"),
            pacman_sprites.get_sprite("Pacman_Left1.png"),
            pacman_sprites.get_sprite("Pacman_Left2.png"),
            pacman_sprites.get_sprite("Pacman_Left1.png"),
        ]
        pacman_images2 = [
            pacman_sprites.get_sprite("Pacman_Circle.png"),
            pacman_sprites.get_sprite("Pacman_Right1.png"),
            pacman_sprites.get_sprite("Pacman_Right2.png"),
            pacman_sprites.get_sprite("Pacman_Right1.png"),
        ]

        ghost_sprites = SpriteSheet("images/ghosts.png", "ghosts_spritesheet.json")
        blinky_images = [ghost_sprites.get_sprite(f"Blinky_{n}.png") for n in range(1, 11)]
        inky_images = [ghost_sprites.get_sprite(f"Inky_{n}.png") for n in range(1, 11)]
        pinky_images = [ghost_sprites.get_sprite(f"Pinky_{n}.png") for n in range(1, 11)]
        clyde_images = [ghost_sprites.get_sprite(f"Clyde_{n}.png") for n in range(1, 11)]
        scared_images = [ghost_sprites.get_sprite("Running_1.png"), ghost_sprites.get_sprite("Running_2.png")]

        ghost_images = [
            blinky_images[6],
            blinky_images[7],
            pinky_images[6],
            pinky_images[7],
            inky_images[6],
            inky_images[7],
            clyde_images[6],
            clyde_images[7],
        ]

        self.animation1 = Animation1(game=self, pacman_images=pacman_images1, ghost_images=ghost_images)
        self.animation2 = Animation2(game=self, pacman_images=pacman_images2, ghost_images=scared_images)
        self.showBlinky = IntroduceBlinky(game=self, images=blinky_images)
        self.showInky = IntroduceInky(game=self, images=inky_images)
        self.showPinky = IntroducePinky(game=self, images=pinky_images)
        self.showClyde = IntroduceClyde(game=self, images=clyde_images)
        self.howHigh = Howhigh(game=self)

        self.clock = pg.time.Clock()

        self.mixer = mixer.init()

        self.title_music = pg.mixer.Sound("sounds/launch.mp3")
        self.title_music.play()
        self.title_music.set_volume(0.2)
        self.Surface = pg.display.set_mode(size=(game.settings.screen_width, game.settings.screen_height))

        pg.font.init()

        self.play_button = Button(self.screen, "Start Game")
        self.play_button.rect.top += 230
        self.play_button.prep_msg("Play Game")

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
            if e.type == pg.KEYUP and e.key == pg.K_p:  # pretend PLAY BUTTON pressed
                self.landing_page_finished = True  # TODO change to actual PLAY button
                self.music.stop()
            elif e.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if self.play_button.rect.collidepoint(mouse_x, mouse_y):
                    self.landing_page_finished = True
                    self.title_music.stop()

    def show(self):
        while not self.landing_page_finished:
            self.draw()
            self.check_events()  # exits game if QUIT pressed

    def draw(self):
        self.animation1.update()
        self.animation2.update()
        self.Surface.fill(BLACK)
        self.screen.blit(self.bigPacman, (self.x1, self.y1))
        self.screen.blit(self.bigtitle, (self.titlex, self.titley))
        self.animation1.draw()
        self.animation2.draw()

        self.current_time = 0
        self.current_time = pg.time.get_ticks()
        if self.current_time >= 5500 and self.current_time <= 7500:
            self.showBlinky.draw()
        if self.current_time >= 7500 and self.current_time <= 9500:
            self.showPinky.draw()
        if self.current_time >= 9500 and self.current_time <= 11500:
            self.showInky.draw()
        if self.current_time >= 11500 and self.current_time <= 13000:
            self.showClyde.draw()
        if self.current_time >= 13000 and self.current_time <= 13500:
            self.howHigh.draw()
        if self.current_time >= 14000 and self.current_time <= 14500:
            self.howHigh.draw()
        if self.current_time >= 15000 and self.current_time <= 15500:
            self.howHigh.draw()
        if self.current_time >= 16000 and self.current_time <= 16500:
            self.howHigh.draw()
        if self.current_time >= 17000 and self.current_time <= 17500:
            self.howHigh.draw()

        self.current_time = pg.time.get_ticks()

        self.play_button.draw_button()

        pg.display.update()
        pg.display.flip()
        self.clock.tick(45)
