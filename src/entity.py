import pygame
import random
import src.util
from src.constants import *

# base class for any entity that has position and sprite
class Entity:
    # variables used as "static", shared amongst instances of this class
    # every time the class is instantiated they are incremented (and used to set ID)
    # every time objects of this class are deleted entityCount is decremented
    entityCount = 0
    lastIdUsed = -1
    def __init__(self, surface, x = 0, y = 0, solid = False, name = "DEFAULT", sprite=None):
        self.name = name

        # surface to draw on
        self.surface = surface
        self.sprite = None
        if sprite:
            picture = pygame.image.load(sprite)
            picture = pygame.transform.scale(picture, (DrawInfo.CELL_WIDTH, DrawInfo.CELL_HEIGHT))
            self.sprite = picture.convert_alpha()

        self.id = Entity.lastIdUsed + 1
        Entity.lastIdUsed += 1
        Entity.entityCount += 1

        self.x = x
        self.y = y

        self.drawX = src.util.getPadding(self.x, DrawInfo.X_OFFSET, 5)
        self.drawY = src.util.getPadding(self.y, DrawInfo.Y_OFFSET, 5)
        # solid attribute will define collision
        self.solid = solid
        self.updateSpritePosition(self.x, self.y)

    def move(self, newX, newY):
        self.x = newX
        self.y = newY
        self.updateSpritePosition(self.x, self.y)

    def updateSpritePosition(self, newX, newY):
        self.drawX = src.util.getPadding(newX, DrawInfo.X_OFFSET, 5)
        self.drawY = src.util.getPadding(newY, DrawInfo.Y_OFFSET, 5)
        if not self.sprite:
            self.sprite = pygame.Rect(self.drawX, self.drawY, DrawInfo.CELL_WIDTH, DrawInfo.CELL_HEIGHT)

    def draw(self):

        if not self.sprite:
            colour = WALLSCOLOUR
            lineThickness = 1 if self.name == "floor" else 0

            pygame.draw.rect(self.surface, colour, self.sprite, lineThickness)
        else:
            self.surface.blit(self.sprite, (self.drawX, self.drawY))

    def __del__(self):
        Entity.entityCount -= 1
