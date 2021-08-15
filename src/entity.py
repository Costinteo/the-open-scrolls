import pygame
import random
from src.util import *
from src.constants import *

# base class for any entity that has position and sprite
class Entity:
    # variables used as "static", shared amongst instances of this class
    # every time the class is instantiated they are incremented (and used to set ID)
    # every time objects of this class are deleted entityCount is decremented
    entityCount = 0
    lastIdUsed = -1
    def __init__(self, surface, x = 0, y = 0, solid = False, name = "DEFAULT"):
        self.name = name

        # surface to draw on
        self.surface = surface

        self.id = Entity.lastIdUsed + 1
        Entity.lastIdUsed += 1
        Entity.entityCount += 1
        
        self.x = x
        self.y = y
        # solid attribute will define collision
        self.solid = solid
        self.updateSpritePosition(self.x, self.y)

    def move(self, newX, newY):
        self.x = newX
        self.y = newY
        self.updateSpritePosition(self.x, self.y)

    def updateSpritePosition(self, newX, newY):
        x = getPadding(newX, DrawInfo.X_OFFSET, 5)
        y = getPadding(newY, DrawInfo.Y_OFFSET, 5)
        self.sprite = pygame.Rect(x, y, DrawInfo.CELL_WIDTH, DrawInfo.CELL_HEIGHT)

    def draw(self):

        colour = WALLSCOLOUR if self.name == "Wall" or self.name == "Walkable" \
        else ENEMYCOLOUR if self.name == "Enemy" \
        else PLAYERCOLOUR
        
        lineThickness = 1 if self.name == "Walkable" else 0

        pygame.draw.rect(self.surface, colour, self.sprite, lineThickness)

    def __del__(self):
        Entity.entityCount -= 1

