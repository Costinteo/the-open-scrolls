import pygame
from pygame.constants import *
from src.constants import *


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
        self.surface = self.font.render(self.text, True, WHITE)
        self.rect = self.surface.get_rect()
        if pos is not None:
            self.position_center(pos)

    def position_center(self, pos):
        self.rect.center = pos
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class Button(PlainText):
    def __init__(self, text, font, size, action, pos=None, ):
        """
            text : string - contents
            font : string - path to font file
            size : integer
            pos : (x, y) - coordinates of the center *optional*
            action : data returned when button is selected
        """
        super().__init__(text, font, size, pos)
        self.action = action
        self.selected = False

    def is_clicked(self, click_pos):
        x, y = click_pos
        return x >= self.rect.left and x <= self.rect.left + self.rect.width and y >= self.rect.top and y <= self.rect.top + self.rect.height

    def handle_event(self, event):
        # if event.type == MOUSEBUTTONDOWN and self.is_clicked(pygame.mouse.get_pos()): -- clicking on buttons with the mouse
        #    return self.action
        if event.type == pygame.KEYDOWN and event.key == K_RETURN and self.selected:
            return self.action
        return None
    
    def draw(self, screen):
        # tempsurface = self.font.render(self.text, True, NAVY) if self.rect.collidepoint(pygame.mouse.get_pos()) else self.surface -- mouse hover effect
        if self.selected:
            pygame.draw.circle(screen, WHITE, (self.rect.left - 30, self.rect.center[1]), 10)
        screen.blit(self.surface, self.rect)