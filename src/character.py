from src.entity import *

# base class for enemies / players
# they have attributes (placeholder / unfinished)
class Character(Entity):
    def __init__(self, surface, x = 0, y = 0, name = "DEFAULT", level = 1, exp = 0, HP = 100, STA = 100, MGK = 100, STR = 10, INT = 10, AGI = 10):

        super().__init__(surface=surface, x=x, y=y, name=name)

        self.level = level
        self.exp = exp

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

        self.inventory = dict()

        # base attributes
        self.attributes["HP"] = HP      # Health
        self.attributes["STA"] = STA    # Stamina
        self.attributes["MGK"] = MGK    # Magicka

        # extra attributes
        self.attributes["STR"] = STR    # Strength
        self.attributes["INT"] = INT    # Intelligence
        self.attributes["AGI"] = AGI    # Agility

        # bool that keeps track whether or not character is dead
        self.isDead = False

    def updateSpritePosition(self, newX, newY):
        x = getPadding(newX, DrawInfo.X_OFFSET, 5)
        y = getPadding(newY, DrawInfo.Y_OFFSET, 5)
        self.sprite = pygame.Rect(x + 5, y + 5, DrawInfo.ENTITY_WIDTH, DrawInfo.ENTITY_HEIGHT)
        # we add 5 to each coordinate to center the sprite on the tile,
        # considering the origin of the sprite is top left and the difference
        # in width and height between cells and dynamic entities is 10

    def pickWeapon(self, itemName = "RANDOM"):
        # random is currently implemented for the AI enemy
        if itemName == "RANDOM":
            return random.choice(list(self.inventory.values()))

        return self.inventory[itemName]

    def isItemEquipped(self, item):
        return self.currentlyEquipped[item.slotEquipped] == item

    def physicalAttack(self, other, item):
        # the attribute the item favours adds 10% of its value to the damage 
        # 30% of the damage gets substracted if the item isn't equipped
        damage = item.damage + 0.1 * self.attributes[item.specialization] - 0.3 * (not self.isItemEquipped(item))
        self.dealDamage(other, damage)

    def dealDamage(self, other, value):
        other.receiveDamage(value)

    def receiveDamage(self, value):
        self.attributes["HP"] -= value
        self.isDead = self.attributes["HP"] <= 0