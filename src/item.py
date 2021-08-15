from src.entity import *


class Effect:
    def __init__(self, surface, name="DEFAULT", description="DEFAULT", effect="DEFAULT", value=0, attribute="DEFAULT", icon=None):

        self.surface = surface

        # name and description
        self.name = name
        self.description = description

        # effect can be:
        # - fortify [attribute]
        # - restore [attribute] (for restore HP potions, for example)
        # - damage [attribute] (curses)
        # - on-hit (poison extra damage or maybe elemental)
        # value is the actual numbers involved in the enchantment
        # attribute is the attribute used
        # e.g. if we have an Enchantment(effect="Fortify", value="10", attribute="AGI")
        # then it will fortify Agility by 10 points
        self.effect = effect
        self.value = value
        self.attribute = attribute

        # icon that will be used when we draw menus
        self.icon = icon


# An item should be:
#   - placeable on the map
#   - equippable or consumable
#   - have a description
# An equippable should have:
#   - enchantments
#   - slot to equip in
# A consumbale should have:
#   - an effect
# Rest is self-explanatory and
# subject to change.

class Item(Entity):
    def __init__(self, surface, x=0, y=0, name="DEFAULT", description="DEFAULT", isPlaced=False, value=0):
        super().__init__(surface=surface, x=x, y=y, name=name)

        self.description = description
        self.isPlaced = isPlaced


class Equippable(Item):
    def __init__(self, surface, x=0, y=0, name="DEFAULT", isPlaced=False, value=0, slot="DEFAULT"):
        super().__init__(surface=surface, x=x, y=y, name=name, isPlaced=isPlaced, value=value)

        # here we'll have a dictionary of effects used as enchantments on an equippable item
        self.enchantments = dict()
        self.slot = slot


class Weapon(Equippable):
    def __init__(self, surface, x=0, y=0, name="DEFAULT", isPlaced=False, value=0, slot="Weapon", damage=0, specialization="DEFAULT"):
        super().__init__(surface=surface, x=x, y=y, name=name, isPlaced=isPlaced, value=value, slot=slot)

        self.damage = damage
        self.specialization = specialization


class Apparel(Equippable):
    def __init__(self, surface, x=0, y=0, name="DEFAULT", isPlaced=False, value=0, slot="DEFAULT", defense=0):
        super().__init__(surface=surface, x=x, y=y, name=name, isPlaced=isPlaced, value=value, slot=slot)

        self.defense = defense


class Consumable(Item):
    def __init__(self, surface, x=0, y=0, name="DEFAULT", isPlaced=False, value=0, effect=Effect()):
        super().__init__(surface=surface, x=x, y=y, name=name, isPlaced=isPlaced, value=value)

        self.effect = effect
