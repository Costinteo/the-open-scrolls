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
