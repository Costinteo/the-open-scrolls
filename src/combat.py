import pygame
from src.util import *

class Combat:
    def __init__(self, first, second):
        # using a tuple for the two combatants
        self.combatants = (first, second)

        # combatant that goes first is the one with higher AGI
        # second goes first if AGI for first is lower, otherwise, first goes first
        self.currentCombatant = 1 if compareStat("AGI", first, second) == -1 else 0

        # the turn number
        self.turn = 0

    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if checkAttackChoice(event.key):
                    self.handleAttackChoice(event.key)

        itemUsed = self.combatants[self.currentCombatant].pickWeapon()
        # make sure our tuple gets iterated circullary
        self.currentCombatant = (self.currentCombatant + 1) % 2

    def drawInventory(self):
        pass

    def drawMagic(self):
        pass

    def draw(self):
        pass
    
    def handleWeaponPicking(self, ):
        while True:
            self.drawInventory()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pass
            pygame.display.flip()

    def handleAttackChoice(self, key):
        if key == pygame.K_p:
            weaponUsed = self.handleWeaponPicking()
