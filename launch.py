from decimal import HAVE_CONTEXTVAR
from pickle import NONE
from re import S
from struct import pack
import pygame as pg
import sys
from button import Button
from pygame import Surface, mixer
import pygame.font


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (106, 233, 115)
TRANSPARENT = (0,0,0,1.0)


# class ScreenAnim:
#     def __init__(self, pos_x, pos_y):
#         super().__init__()
#         self.sprites = []
        # self.sprites.append(pg.image.load('images/blinky0.png'))
        # self.sprites.append(pg.image.load('images/blinky1.png'))
        # self.sprites.append(pg.image.load('images/clyde0.png'))
        # self.sprites.append(pg.image.load('images/clyde1.png'))
        # self.sprites.append(pg.image.load('images/inky0.png'))
        # self.sprites.append(pg.image.load('images/inky1.png'))
        # self.sprites.append(pg.image.load('images/pinky0.png'))
        # self.sprites.append(pg.image.load('images/blinky1.png'))

        


class Launchscreen:
    pacman = pg.image.load(f'images/Pac-Man-0.png')
    title = pg.image.load('images/title.png')
    bigPacman = pg.transform.scale(pacman, (150,150))
    bigtitle = pg.transform.scale(title, (653,436))
    #font = pg.font.Font('fonts/8-Bit Madness.ttf', 30)
   
    x1 = 290
    y1 = 160
    titlex = 60
    titley = -80
    
    # blinkC, pinkC, inkyC, clydeC = (249, 0, 0), (249, 141, 224), (5, 249, 249), (249, 138, 13)
    # text0 = font.render('Blinky', True, blinkC, (0, 0, 0))
    # text1 = font.render('Pinky', True, pinkC, (0, 0, 0))
    # text2 = font.render('Inky', True, inkyC, (0, 0, 0))
    # text3 = font.render('Clyde', True, clydeC, (0, 0, 0))
    # text4 = font.render('How High Can You Score?', True, (249, 241, 0), (0, 0, 0))
    # textRect0, textRect1, textRect2, textRect3, textRect4 \
    #     = text0.get_rect(), text1.get_rect(), text2.get_rect(), text3.get_rect(), text4.get_rect()
    # textRect0.center, textRect1.center, textRect2.center, textRect3.center, textRect4.center \
    #     = (275, 450), (275, 450), (275, 450), (275, 450), (275, 450)
    


    def __init__(self,game):
        self.screen = game.screen
        self.landing_page_finished = False

        # blinky = self.blinky
        # pinky = self.pinky
        # inky = self.inky
        # clyde = self.clyde
        # blinky.rect.left, blinky.rect.top = 260, 410
        # pinky.rect.left, pinky.rect.top = 260, 410
        # inky.rect.left, inky.rect.top = 260, 410
        # clyde.rect.left, clyde.rect.top = 260, 410
        
        
        
        #self.highscore = game.stats.get_highscore()

        self.mixer = mixer.init()

        self.title_music = pg.mixer.Sound('sounds/launch.mp3')
        self.title_music.play()
        self.title_music.set_volume(0.2)
        self.Surface = pg.display.set_mode((750,900))
        pg.font.init()
        
        font = pg.font.Font('fonts/crackman.ttf', 50)

        #strings = [('PAC', WHITE, headingFont), ('MAN', GREEN, subheadingFont)]
                   


        #self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]

        # self.posns = [150, 230]
        # alien = [60 * x + 400 for x in range(4)]
        # self.posns.extend(alien)
        # self.posns.append(730)
       

        #centerx = self.screen.get_rect().centerx

        self.play_button = Button(self.screen, "Start Game")
        self.play_button.rect.top += 200
        self.play_button.prep_msg("Play Game")

        #n = len(self.texts)
        #self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]
        

    # def get_text(self, font, msg, color):
    #     return font.render(msg, True, color, None)

    # def get_text_rect(self, text, centerx, centery):
    #     rect = text.get_rect()
    #     rect.centerx = centerx
    #     rect.centery = centery
    #     return rect

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
            if e.type == pg.KEYUP and e.key == pg.K_p:   # pretend PLAY BUTTON pressed
                self.landing_page_finished = True        # TODO change to actual PLAY button
                self.music.stop()
            elif e.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if self.play_button.rect.collidepoint(mouse_x, mouse_y):
                    self.landing_page_finished = True
                    self.title_music.stop()
                                                        

    def show(self):
        while not self.landing_page_finished:
            self.draw()
            self.check_events()   # exits game if QUIT pressed

    def draw_text(self):
        pass
        #n = len(self.texts)
        # for i in range(n):
        #     self.screen.blit(self.texts[i], self.rects[i])

    def draw(self):
        #space_bg = pg.image.load(f'images/bg.png').convert()
        #self.screen.fill(BLACK)
        #self.screen.blit(space_bg, (0, 0))
        self.Surface.fill(BLACK)
        self.screen.blit(self.bigPacman,(self.x1,self.y1))
        self.screen.blit(self.bigtitle, (self.titlex, self.titley))
    
        self.draw_text()
        self.play_button.draw_button()
        pg.display.flip()