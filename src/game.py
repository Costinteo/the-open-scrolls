import pygame
import random
import time
from src.util import *
from src.constants import *
from src.entity import *
from src.level import *
from src.combat import *

# init pygame
successes, failures = pygame.init()
print(f"{successes} successes and {failures} failures")


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("The Open Scrolls")
        self.clock = pygame.time.Clock()

        self.currentLevel = Level("levels/dungeon.map", self.screen)

        self.inCombat = False
        self.combat = None

        self.timeSinceEnemyMovement = time.time()

    def update(self):
        # sleep to sync with fps
        self.clock.tick(FPS)
        
        # colour screen
        self.screen.fill(BACKGROUNDCOLOUR)

        if not self.inCombat:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                elif event.type == pygame.KEYDOWN:
                    # handle movement events
                    if checkMovementEvent(event.key):
                        self.handleMovementEvent(event.key)
                        print(self.currentLevel.player.x, self.currentLevel.player.y)
            
            self.handleEnemyMovement()
            
            enemy = self.checkForCombat()
            
            if enemy:
                self.combat = Combat(self.currentLevel.player, enemy)
                self.inCombat = True

        self.draw()
        pygame.display.flip()


    def draw(self):
        if not self.inCombat:
            self.currentLevel.draw()

# ----------- GAME LOGIC METHODS -----------

    # handles player movement events
    def handleMovementEvent(self, key):

        if key == pygame.K_UP:
            newX = self.currentLevel.player.x
            newY = max(0, self.currentLevel.player.y - 1)
        elif key == pygame.K_DOWN:
            newX = self.currentLevel.player.x
            newY = min(self.currentLevel.height - 1, self.currentLevel.player.y + 1)

        if key == pygame.K_LEFT:
            newX = max(0, self.currentLevel.player.x - 1)
            newY = self.currentLevel.player.y
        elif key == pygame.K_RIGHT:
            newX = min(self.currentLevel.width - 1, self.currentLevel.player.x + 1)
            newY = self.currentLevel.player.y

        if not isPositionSolid(self.currentLevel.matrix, newX, newY):
            self.currentLevel.player.move(newX, newY)

        
    
    # randomly moves enemies
    def handleEnemyMovement(self):
        if time.time() - self.timeSinceEnemyMovement <= 2:
            return
        self.timeSinceEnemyMovement = time.time()
        for enemy in self.currentLevel.enemies.values():
            newX = enemy.x + random.randint(-1, 1)
            newY = enemy.y + random.randint(-1, 1)
            if not isPositionSolid(self.currentLevel.matrix, newX, newY):
                enemy.move(newX, newY)

    # sets self.inCombat to true
    # returns the enemy playered entered in combat with
    # returns None if player hasn't entered combat
    def checkForCombat(self):
        for enemy in self.currentLevel.enemies.values():
            if enemy.x == self.currentLevel.player and enemy.y == self.currentLevel.player:
                self.inCombat = True
                return enemy
        return None

