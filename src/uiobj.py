import pygame
from pygame.constants import *
import src.constants as const

pygame.font.init()

class PlainText:
    def __init__(self, text, font, size, pos=None):
        """
            text : string - contents
            font : string - path to font file
            size : integer
            pos : (x, y) - coordinates of the center *optional*
        """
        self.text = text
        self.font = font
        self.size = size
        font = pygame.font.Font(self.font, self.size)
        self.surface = font.render(self.text, True, const.WHITE)
        self.rect = self.surface.get_rect()
        if pos is not None:
            self.position_center(pos)

    def position_center(self, pos):
        self.rect.center = pos

    def recenter(self, width, height):
        ratio_w, ratio_h = width / const.WIDTH, height / const.HEIGHT
        self.size = int(self.size * ratio_w)
        font = pygame.font.Font(self.font, self.size)
        self.surface = font.render(self.text, True, const.WHITE)
        old_rect = self.rect
        self.rect = self.surface.get_rect()
        self.position_center((old_rect.center[0] * ratio_w, old_rect.center[1] * ratio_h))
    
    def set_text(self, text, size=None):
        if size:
            self.size = size
        font = pygame.font.Font(self.font, self.size)
        self.text = text
        self.surface = font.render(self.text, True, const.WHITE)
        old_rect = self.rect
        self.rect = self.surface.get_rect()
        self.position_center((old_rect.center[0], old_rect.center[1]))
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)
    
    def move(self, new_x, new_y):
        self.position_center((new_x, new_y))
    
    def out_of_bounds(self):
        return self.rect.center[0] <= 0 or self.rect.center[1] <= 0 or self.rect.center[0] >= const.WIDTH or self.rect.center[1] >= const.HEIGHT


class Button(PlainText):
    def __init__(self, text, font, size, flag, func=None, params=None, pos=None):
        """
            text : string - contents
            font : string - path to font file
            size : int
            flag : constant - used for game state switching
            func : function - called when button is pressed *optional*
            params : tuple of any length and any type - is passed into func when button is pressed *optional*
            pos : tuple (int/float, int/float) - coordinates of the center *optional*
        """
        super().__init__(text, font, size, pos)
        self.flag = flag
        self.func = func
        self.params = params
        self.selected = False

    def trigger_bttn(self):
        return (self.flag, self.func(*self.params) if self.func is not None else None)
    
    def draw(self, screen):
        if self.selected:
            pygame.draw.circle(screen, const.WHITE, (self.rect.left - 30, self.rect.center[1]), const.WIDTH * 0.008)
        screen.blit(self.surface, self.rect)