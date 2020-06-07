import pygame
import random
import logging

class Settings():
    def __init__(self):
        self.screen_width = 800
        self.screen_height = self.screen_width
        self.bg_color = (0,0,0)
        self.square_size=20
        self.startx=180
        self.starty=180
        self.snake_color=(200,0,0)
        self.crumb_color=(0,200,0)

class Snake(pygame.sprite.Sprite):
    def __init__(self,screen,settings,cellx,celly, direction):
        super(Snake,self).__init__()
        self.screen=screen
        self.rect=pygame.Rect(cellx,celly,settings.square_size,settings.square_size)
        self.settings=settings
        self.instruction=""
        self.moving_up=False
        self.moving_right=False
        self.moving_down=False
        self.moving_left=False
        self.direction=direction
    def draw_snake(self):
        pygame.draw.rect(self.screen, self.settings.snake_color, self.rect)

class Crumbs(pygame.sprite.Sprite):
    def __init__(self,screen,settings):
        super(Crumbs,self).__init__()
        self.screen=screen
        self.settings=settings
        self.x=self.crumb_place()[0]
        self.y=self.crumb_place()[1]
        self.rect=pygame.Rect(self.x,self.y,settings.square_size,settings.square_size)
    def draw_crumb(self):
        pygame.draw.rect(self.screen, self.settings.crumb_color, self.rect)
    def crumb_place(self):
        squares_on_axis=self.settings.screen_width/self.settings.square_size
        ordinates=[x for x in range(0,self.settings.screen_width,self.settings.square_size)]
        ordinate_x=ordinates[random.randint(0,squares_on_axis-1)]
        ordinate_y=ordinates[random.randint(0,squares_on_axis-1)]
        coordinate=(ordinate_x,ordinate_y)
        return coordinate

class Button():
    def __init__(self,screen,msg):
        self.screen=screen
        self.screen_rect=screen.get_rect()
        self.width=200
        self.height=50
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Build the button's rect object and center it. 
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # The button message needs to be prepped only once. 
        self.prep_msg(msg)
    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        #logging.debug('prep_msg')
    def draw_button(self):
        # Draw blank button and then draw message. 
        #logging.debug('over class')
        self.screen.blit(self.msg_image, self.msg_image_rect)