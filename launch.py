import sys

import pygame as pg
from pygame import mixer
from pygame.sprite import Sprite

from button import Button
from timer import Timer

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (106, 233, 115)
TRANSPARENT = (0, 0, 0, 1.0)


class Animation1(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen

        self.menu = [
            pg.transform.scale(pg.image.load("images/menu0.png"), (350, 100)),
            pg.transform.scale(pg.image.load("images/menu1.png"), (350, 100)),
            pg.transform.scale(pg.image.load("images/menu2.png"), (350, 100)),
        ]
        self.timer = Timer(self.menu, oscillating=True)

        self.x = 650
        self.y = 450

        self.rect = pg.Rect(self.x, self.y, 350, 100)

    def update(self):
        self.rect.x -= 5

    def draw(self):
        self.timer.advance_frame_index()
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)


class Animation2(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen

        self.menu = [
            pg.transform.scale(pg.image.load("images/menu3.png"), (350, 100)),
            pg.transform.scale(pg.image.load("images/menu4.png"), (350, 100)),
            pg.transform.scale(pg.image.load("images/menu5.png"), (350, 100)),
            pg.transform.scale(pg.image.load("images/menu6.png"), (350, 100)),
        ]
        self.timer = Timer(self.menu)

        self.x = -100
        self.y = 350
        self.rect = pg.Rect(self.x, self.y, 350, 100)

    def update(self):
        self.rect.x += 5

    def draw(self):
        self.timer.advance_frame_index()
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)


class IntroduceBlinky:
    pg.font.init()

    def __init__(self, game):
        self.surface = game.screen
        self.small_blinky = pg.image.load("images/blinky0.png")
        self.blinky = pg.transform.scale(self.small_blinky, (120, 120))
        self.font = pg.font.Font("fonts/crackman.ttf", 32)
        self.blinky_text = self.font.render('"Blinky"', True, (255, 0, 0))

    def draw(self):
        self.surface.blit(self.blinky, (265, 350))
        self.surface.blit(self.blinky_text, (250, 500))


class IntroducePinky:
    pg.font.init()

    def __init__(self, game):
        self.surface = game.screen
        self.small_Pinky = pg.image.load("images/pinky0.png")
        self.pinky = pg.transform.scale(self.small_Pinky, (120, 120))
        self.font = pg.font.Font("fonts/crackman.ttf", 32)
        self.pinky_text = self.font.render('"Pinky"', True, ("#FFB8FF"))

    def draw(self):
        self.surface.blit(self.pinky, (265, 350))
        self.surface.blit(self.pinky_text, (255, 500))


class IntroduceInky:
    pg.font.init()

    def __init__(self, game):
        self.surface = game.screen
        self.small_inky = pg.image.load("images/inky0.png")
        self.inky = pg.transform.scale(self.small_inky, (120, 120))
        self.font = pg.font.Font("fonts/crackman.ttf", 32)
        self.inky_text = self.font.render('"Inky"', True, ("#00FFFF"))

    def draw(self):
        self.surface.blit(self.inky, (265, 350))
        self.surface.blit(self.inky_text, (265, 500))


class IntroduceClyde:
    pg.font.init()

    def __init__(self, game):
        self.surface = game.screen
        self.small_Clyde = pg.image.load("images/clyde0.png")
        self.clyde = pg.transform.scale(self.small_Clyde, (120, 120))
        self.font = pg.font.Font("fonts/crackman.ttf", 32)
        self.clyde_text = self.font.render('"Clyde"', True, ("#FFB852"))

    def draw(self):
        self.surface.blit(self.clyde, (265, 350))
        self.surface.blit(self.clyde_text, (255, 500))


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

        self.animation1 = Animation1(game=self)
        self.animation2 = Animation2(game=self)
        self.showBlinky = IntroduceBlinky(game=self)
        self.showInky = IntroduceInky(game=self)
        self.showPinky = IntroducePinky(game=self)
        self.showClyde = IntroduceClyde(game=self)
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
