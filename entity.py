import pygame
from util import *
from constants import *

# unused
class Attribute():
    def __init__(self, name, value):
        self.name = name
        self.value = value

# base class for any entity that has position and sprite
class Entity():
    # variables used as "static", shared amongst instances of this class
    # every time the class is instantiated they are incremented (and used to set ID)
    # every time objects of this class are deleted entityCount is decremented
    entityCount = 0
    lastIdUsed = -1
    def __init__(self, surface, x = 0, y = 0, solid = False, name = "DEFAULT", ):
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
        self.sprite = pygame.Rect(getPadding(newX, X_OFFSET, 5), getPadding(newY, Y_OFFSET, 5), CELL_WIDTH, CELL_HEIGHT)

    def draw(self):
        colour = WALLSCOLOUR if self.name == "Wall" or self.name == "Walkable" \
        else ENEMYCOLOUR if self.name == "Enemy" \
        else PLAYERCOLOUR
        lineThickness = 1 if self.name == "Walkable" else 0
        pygame.draw.rect(self.surface, colour, self.sprite, lineThickness)

    def __del__(self):
        Entity.entityCount -= 1

# base class for enemies / players
# they have attributes (placeholder / unfinished)
class Character(Entity):
    def __init__(self, surface, x = 0, y = 0, name = "DEFAULT", level = 1, exp = 0, HP = 100, STA = 100, MGK = 100, STR = 10, INT = 10, AGI = 10):

        super().__init__(surface=surface, x=x, y=y, name=name)

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

    def updateSpritePosition(self, newX, newY):
        self.sprite = pygame.Rect(getPadding(newX, X_OFFSET, 5), getPadding(newY, Y_OFFSET, 5), ENTITY_WIDTH, ENTITY_HEIGHT)