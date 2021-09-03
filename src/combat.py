import pygame
import time
from src.util import *

class Combat:
    def __init__(self, first, second):
        # using a tuple for the two combatants
        self.combatants = (first, second)

        # toPlay holds the index of the combatant to currently play this turn
        # combatant that goes first is the one with higher AGI
        # second goes first if AGI for first is lower, otherwise, first goes first
        self.toPlay = 1 if compareStat("AGI", first, second) == "lower" else 0

        # current is a reference to the combatant currently at play
        # other is a reference to the combatant that waits their turn
        self.current = self.combatants[self.toPlay]
        self.other = self.combatants[1 - self.toPlay]

        # the turn number
        self.turn = 0

        self.magicMenu = None # this is where the magic menu will be
        self.inventoryMenu = None # this is where the inventory menu will be

    def update(self):

        print(f"{self.combatants[0].name}: [HP:{self.combatants[0].attributes['HP']}]")
        print(f"{self.combatants[1].name}: [HP:{self.combatants[1].attributes['HP']}]")
        print(f"{self.current.name}'s turn!")
        # only iterate through events and check for keys if player to play
        if self.current.id == self.getPlayerCharacter().id:
            # iterate until player actually picks something
            picked = False
            while not picked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            exit()
                    elif event.type == pygame.KEYDOWN:
                        if checkAttackChoice(event.key):
                            self.handleAttackChoice(event.key)

                            picked = True
        else:
            # this is for the AI enemy
            # atm it only attacks using currently equipped weapon, always
            # this surely can be refactored so we only call physical attack once in update
            self.current.physicalAttack(self.other, self.current.currentlyEquipped["Weapon"])

        if self.other.isDead:
            # returns the WINNER and the LOSER
            return self.current, self.other

        # make sure our tuple gets iterated circullary
        self.toPlay = 1 - self.toPlay
        self.current = self.combatants[self.toPlay]
        self.other = self.combatants[1 - self.toPlay]

        # incremenet turn
        self.turn += 1

        # to have a distinction between turns
        print("---------")

        return self.update()

    def handleAttackChoice(self, key):
        if key == pygame.K_p:
            # attack other with currently equipped weapon
            self.current.physicalAttack(self.other, self.current.currentlyEquipped["Weapon"])
            #weaponUsed = self.handleWeaponPicking()
        elif key == pygame.K_m:
            pass
            #magicUsed = self.handleMagicPicking()

    def getPlayerCharacter(self):
        return self.combatants[0]
