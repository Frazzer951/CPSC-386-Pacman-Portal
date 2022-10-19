import sys
from decimal import HAVE_CONTEXTVAR
from pickle import NONE
from re import S
from struct import pack
from tkinter import X
from turtle import Screen
from urllib.parse import SplitResult

import pygame
import pygame as pg
import pygame.font
from pygame import Surface, mixer
import pygame.font
import pygame, sys

from button import Button

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (106, 233, 115)
TRANSPARENT = (0,0,0,1.0)



 
class Animation1(pygame.sprite.Sprite):
    def __init__(self, game ):
        super().__init__()
        self.screen = game.screen
        #--------------------------------------------------
        self.sprites1 = []
        self.menu0 = pg.image.load("images/menu0.png")
        fixedmenu0 = pg.transform.scale(self.menu0, (350, 100))
        self.sprites1.append(fixedmenu0)

        self.menu1 = pg.image.load("images/menu1.png")
        fixedmenu1 = pg.transform.scale(self.menu1, (350, 100))
        self.sprites1.append(fixedmenu1)

        self.menu2 = pg.image.load("images/menu2.png")
        fixedmenu2 = pg.transform.scale(self.menu2, (350, 100))
        self.sprites1.append(fixedmenu2)

        self.currentsprite1 = 0
        self.image = self.sprites1[self.currentsprite1]
<<<<<<< HEAD
=======

        self.x = 650
        self.y= 450
    
        self.rect = pg.Rect(self.x, self.y, 350, 100)
       
>>>>>>> 24f200b (update animation)
        
        self.rect = pg.Rect(200, 500, 350, 100)
        #--------------------------------------------------
        
    # def move(self):
    #     if self.vel > 0:
    #         if self.x + self.vel < self.path[1]:
    #             self.x += self.vel
    
    
        
    def update(self):

        self.currentsprite1 += 1
        
        if self.currentsprite1 >= len(self.sprites1):
            self.currentsprite1 = 0
            self.rect.x -= 15
        self.image = self.sprites1[self.currentsprite1]


#
###
#
#
#___))ONJKBHFUYIUHIKFG

class Animation2(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        
        self.sprites2 = []
        self.menu3 = pg.image.load("images/menu3.png")
        fixedmenu3 = pg.transform.scale(self.menu3, (350, 100))
        self.sprites2.append(fixedmenu3)

        self.menu4 = pg.image.load("images/menu4.png")
        fixedmenu4 = pg.transform.scale(self.menu4, (350, 100))
        self.sprites2.append(fixedmenu4)

        self.menu5 = pg.image.load("images/menu5.png")
        fixedmenu5 = pg.transform.scale(self.menu5, (350, 100))
        self.sprites2.append(fixedmenu5)

        self.menu6 = pg.image.load("images/menu5.png")
        fixedmenu6 = pg.transform.scale(self.menu6, (350, 100))
        self.sprites2.append(fixedmenu6)

        self.currentsprite2 = 0
        self.image = self.sprites2[self.currentsprite2]

<<<<<<< HEAD
        self.rect = pg.Rect(200, 350, 350, 100)


=======
        self.x = -100
        self.y= 350
        self.rect = pg.Rect(self.x, self.y, 350, 100)
        #------------------------------------------------------------
>>>>>>> 24f200b (update animation)
       
    def update(self):
        self.currentsprite2 += 1

        if self.currentsprite2 >= len(self.sprites2):
            self.currentsprite2 = 0
            self.rect.x += 15
        self.image = self.sprites2[self.currentsprite2]
        

<<<<<<< HEAD
        
       





<<<<<<< HEAD
class Launchscreen:
    pacman = pg.image.load(f"images/Pac-Man-0.png")
    title = pg.image.load("images/title.png")
    bigPacman = pg.transform.scale(pacman, (150, 150))
    bigtitle = pg.transform.scale(title, (653, 436))

    # font = pg.font.Font('fonts/8-Bit Madness.ttf', 30)

    x1 = 290
=======
    
    #font = pg.font.Font('fonts/8-Bit Madness.ttf', 30)
=======
class IntroduceBlinky:

    pg.font.init()

    def __init__(self, game):

        self.surface = game.screen
        self.smallblinky = pg.image.load(f'images/blinky0.png')
        self.blinky = pg.transform.scale(self.smallblinky, (120,120))
        
        self.font = pg.font.Font('fonts/crackman.ttf',32 )

        self.blinkytext = self.font.render('"Blinky"',True,(255, 0, 0)  )

  
    def draw(self):
        self.surface.blit(self.blinky, (265,350))
        self.surface.blit(self.blinkytext, (250, 500))
        


class IntroducePinky:
    pg.font.init()

    def __init__(self, game):

        self.surface = game.screen
        self.smallPinky = pg.image.load(f'images/pinky0.png')
        self.pinky = pg.transform.scale(self.smallPinky, (120,120))
        
        self.font = pg.font.Font('fonts/crackman.ttf',32 )

        self.pinkytext = self.font.render('"Pinky"',True,('#FFB8FF'))

  
    def draw(self):
        self.surface.blit(self.pinky, (265,350))
        self.surface.blit(self.pinkytext, (255, 500))

class IntroduceInky:
    pg.font.init()

    def __init__(self, game):

        self.surface = game.screen
        self.smallinky = pg.image.load(f'images/inky0.png')
        self.inky = pg.transform.scale(self.smallinky, (120,120))
        
        self.font = pg.font.Font('fonts/crackman.ttf',32 )

        self.inkytext = self.font.render('"Inky"',True,('#00FFFF')  )

  
    def draw(self):
        self.surface.blit(self.inky, (265,350))
        self.surface.blit(self.inkytext, (265, 500))

class IntroduceClyde:
    pg.font.init()

    def __init__(self, game):

        self.surface = game.screen
        self.smallClyde = pg.image.load(f'images/clyde0.png')
        self.clyde = pg.transform.scale(self.smallClyde, (120,120))
        
        self.font = pg.font.Font('fonts/crackman.ttf',32 )

        self.clydetext = self.font.render('"Clyde"',True,('#FFB852')  )

  
    def draw(self):
        self.surface.blit(self.clyde, (265,350))
        self.surface.blit(self.clydetext, (255, 500))

class Howhigh:
    pg.font.init()
    def __init__(self, game):
        self.surface = game.screen
        self.font = pg.font.Font('fonts/crackman.ttf', 42)
        self.howhigh = self.font.render('How high can you score?',True,(249, 241, 0))
    def draw(self):
        self.surface.blit(self.howhigh, (40, 420))
        
       

class Launchscreen():
    pacman = pg.image.load(f'images/Pac-Man-0.png')
    title = pg.image.load('images/title.png')
    bigPacman = pg.transform.scale(pacman, (150,150))
    bigtitle = pg.transform.scale(title, (653,436))
    pg.font.init()

>>>>>>> 3dc5ca4 (all animations in. only need to work on highscores)
   
    x1 = 240
>>>>>>> 24f200b (update animation)
    y1 = 160
    titlex = 10
    titley = -80

    def __init__(self, game):
        self.screen = game.screen
        self.landing_page_finished = False

        self.myanimation = Animation1(game=self)
        self.myanimation2 = Animation2(game=self)
        self.showblinky = IntroduceBlinky(game=self)
        self.showInky = IntroduceInky(game=self)
        self.showPinky = IntroducePinky(game=self)
        self.showClyde = IntroduceClyde(game=self)
        self.howHigh = Howhigh(game=self)
        

        self.mygroup = pg.sprite.Group(self.myanimation)
        self.mygroup2 = pg.sprite.Group(self.myanimation2)
        self.clock = pg.time.Clock()
        #
        
        #
        #self.animation_1 = Animation(500,200, game=self)

        self.mixer = mixer.init()

        self.title_music = pg.mixer.Sound("sounds/launch.mp3")
        self.title_music.play()
        self.title_music.set_volume(0.2)
<<<<<<< HEAD
        self.Surface = pg.display.set_mode(size=(game.settings.screen_width, game.settings.screen_height))
=======
        self.Surface = pg.display.set_mode((650,800))
>>>>>>> 24f200b (update animation)
        pg.font.init()
<<<<<<< HEAD

        font = pg.font.Font("fonts/crackman.ttf", 50)

        self.play_button = Button(self.screen, "Start Game")
        self.play_button.rect.top += 230
        self.play_button.prep_msg("Play Game")

=======
        
     
        self.play_button = Button(self.screen, "Start Game")
        self.play_button.rect.top += 230
        self.play_button.prep_msg("Play Game")
   
>>>>>>> 3dc5ca4 (all animations in. only need to work on highscores)
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

    def draw_text(self):
        pass

    def update(self):
        pass
        self.mygroup.update()
        self.mygroup2.update()
        self.showblinky.update()
        self.showClyde.update()
        self.showInky.update()
        self.showPinky.update()
        
    

    def draw(self):
        self.mygroup.update()
        self.mygroup2.update()
        self.Surface.fill(BLACK)
        self.screen.blit(self.bigPacman, (self.x1, self.y1))
        self.screen.blit(self.bigtitle, (self.titlex, self.titley))
        self.mygroup.draw(self.screen)
        self.mygroup2.draw(self.screen)

<<<<<<< HEAD
        
    
        self.draw_text()
        self.play_button.draw_button()
    
        pg.display.update()
        pg.display.flip()
        self.clock.tick(20)
      
        
=======
            
            self.current_time=0
            self.current_time= pg.time.get_ticks()
            if self.current_time >= 5500 and self.current_time <= 7500:
                self.showblinky.draw()
            if self.current_time >= 7500 and self.current_time <= 9500:
                self.showPinky.draw()
            if self.current_time >= 9500 and self.current_time <= 11500:
                self.showInky.draw()
            if self.current_time >= 11500 and self.current_time <= 13000:
                self.showClyde.draw()
            if self.current_time >= 13000 and self.current_time <=13500:
                self.howHigh.draw()
            if self.current_time >= 14000 and self.current_time <=14500:
                self.howHigh.draw()
            if self.current_time >= 15000 and self.current_time <=15500:
                self.howHigh.draw()
            if self.current_time >= 16000 and self.current_time <=16500:
                self.howHigh.draw()
            if self.current_time >= 17000 and self.current_time <=17500:
                self.howHigh.draw()
                
            self.current_time = pg.time.get_ticks()

            self.draw_text()
            self.play_button.draw_button()
        
            pg.display.update()
            pg.display.flip()
            self.clock.tick(45)
>>>>>>> 3dc5ca4 (all animations in. only need to work on highscores)
