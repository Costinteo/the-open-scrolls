import random
from src.item import *
from src.entity import *

# base class for enemies / players
# they have attributes (placeholder / unfinished)
class Character(Entity):
    def __init__(self, surface, x = 0, y = 0, isPlayer = False, name = "DEFAULT", level = 1, exp = 0, HP = 100, STA = 100, MGK = 100, STR = 10, INT = 10, AGI = 10, LCK = 1):

        super().__init__(surface=surface, x=x, y=y, name=name)

        self.level = level
        self.exp = exp
        
        # for differentiating between PC and NPC
        self.isPlayer = isPlayer

        # we use a dict for attributes
        self.attributes = dict()

        self.currentlyEquipped = {
            "Head" : None,
            "Chest" : None,
            "Hands" : None,
            "Legs" : None,
            "Feet" : None,
            "Ring" : None,
            "Weapon" : None
        }

        self.inventory = []

        # base attributes
        # their names are of length 2 (important for differentiating them in code)
        self.attributes["HP"] = HP      # Health
        self.attributes["ST"] = STA     # Stamina
        self.attributes["MG"] = MGK     # Magicka

        # extra attributes
        self.attributes["STR"] = STR    # Strength
        self.attributes["INT"] = INT    # Intelligence
        self.attributes["AGI"] = AGI    # Agility
        self.attributes["LCK"] = LCK    # Luck

        # bool that keeps track whether or not character is dead
        self.isDead = False

    def updateSpritePosition(self, newX, newY):
        x = getPadding(newX, DrawInfo.X_OFFSET, 5)
        y = getPadding(newY, DrawInfo.Y_OFFSET, 5)
        self.sprite = pygame.Rect(x + 5, y + 5, DrawInfo.ENTITY_WIDTH, DrawInfo.ENTITY_HEIGHT)
        # we add 5 to each coordinate to center the sprite on the tile,
        # considering the origin of the sprite is top left and the difference
        # in width and height between cells and dynamic entities is 10

    def draw(self):

        colour = PLAYERCOLOUR if self.isPlayer else ENEMYCOLOUR

        pygame.draw.rect(self.surface, colour, self.sprite)


    def addItemToInventory(self, item):
        self.inventory.append(item)

    def equipItem(self, item):
        if item in self.inventory:
            self.currentlyEquipped[item.slot] = item

    def isItemEquipped(self, item):
        return self.currentlyEquipped[item.slot] == item

    def physicalAttack(self, other, item):
        if item.slot != "Weapon":
            # if item used isn't a weapon
            # we use some funky calculations with Luck to see the damage

            # list of all the extra attributes
            # it uses the fact the base attributes have a length of 2 characters
            extraAttrList = [self.attributes[k] if len(k) > 2 else 0 for k in self.attributes.keys()]

            # this takes the max extra attribute and applies it as damage,
            # if Luck added to a randint manages to pass a check
            # currently there's a (5 + LCK)% chance to make it happen
            hasAttackPassed = (self.attributes["LCK"] + random.randint(0, 100) > 95)

            # damage can in the end range from 0 to max extra attribute
            damage = random.randint(0, max(extraAttrList)) * hasAttackPassed
        else:
            # the attribute the item favours adds 10% of its value to the damage 
            # 30% of the damage gets substracted if the item isn't equipped
            damage = item.damage + 0.1 * self.attributes[item.specialization] - 0.3 * (not self.isItemEquipped(item))
        self.dealDamage(other, damage)

    def dealDamage(self, other, value):
        other.receiveDamage(value)
        print(f"{self.other.name} suffered {value} damage!")

    def receiveDamage(self, value):
        self.attributes["HP"] -= value
        self.isDead = self.attributes["HP"] <= 0