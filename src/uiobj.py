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
        self.font = pygame.font.Font(font, size)
        self.surface = self.font.render(self.text, True, const.WHITE)
        self.rect = self.surface.get_rect()
        if pos is not None:
            self.position_center(pos)

    def position_center(self, pos):
        self.rect.center = pos
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)


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
            pygame.draw.circle(screen, const.WHITE, (self.rect.left - 30, self.rect.center[1]), 10)
        screen.blit(self.surface, self.rect)