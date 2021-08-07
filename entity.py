from util import *
from constants import *
import pygame

# unused
class Attribute():
    def __init__(self, name, value):
        self.name = name
        self.value = value

# base class for any entity that has position and sprite
class Entity():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.updateSpritePosition(self.x, self.y)

    def move(self, newX, newY):
        self.x = newX
        self.y = newY
        self.updateSpritePosition(self.x, self.y)

    def updateSpritePosition(self, newX, newY):
        self.sprite = pygame.Rect(getPadding(newX, X_OFFSET, 5), getPadding(newY, Y_OFFSET, 5), ENTITY_WIDTH, ENTITY_HEIGHT)

# base class for enemies / players
# they have attributes (placeholder / unfinished)
class Character(Entity):
    def __init__(self, x = 0, y = 0, level = 1, exp = 0, HP = 100, STA = 100, MGK = 100, STR = 10, INT = 10, AGI = 10):

        super().__init__(x, y)

        self.level = level
        self.exp = exp

        # we use a dict for attributes
        self.attributes = dict()

        # base attributes
        self.attributes["HP"] = HP      # Health
        self.attributes["STA"] = STA    # Stamina
        self.attributes["MGK"] = MGK    # Magicka

        # extra attributes
        self.attributes["STR"] = STR    # Strength
        self.attributes["INT"] = INT    # Intelligence
        self.attributes["AGI"] = AGI    # Agility

