import pygame
import random
import time
import math
from src.util import *
from src.constants import *
from src.entity import *
from src.level import *
from src.combat import *

# init pygame
successes, failures = pygame.init()
print(f"{successes} successes and {failures} failures")

# Game is a singleton class as it only gets instanced once
class Game:
    instance = None
    def __init__(self):
        if Game.instance:
            raise Exception("Singleton class!")
        else:
            Game.instance = self

            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("The Open Scrolls")
            self.clock = pygame.time.Clock()

            # used when player is in game, to change focus to level handling
            self.inGame = True
            self.currentLevel = Level("azuratemple01", self.screen)

            # used when player enters a menu so the game knows to pause
            # and change focus to menu handling
            self.inMenu = False
            self.menu = None

            # used when player enters combat to change focus to combat handling
            self.inCombat = False
            self.combat = None

            self.timeSinceEnemyMovement = time.time()

    @staticmethod
    def getInstance():
        if not Game.instance:
            Game()

        return Game.instance


    def update(self):
        # sleep to sync with fps
        self.clock.tick(FPS)

        # colour screen
        self.screen.fill(NAVY)

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
                        # print(self.currentLevel.player.x, self.currentLevel.player.y)

            self.handleEnemyMovement()
            self.checkForCombat()
        else:
            # combat.update() function is recursive
            # it will only stop when one side wins
            while not self.combat.current.isDead and not self.combat.other.isDead:
                winner, loser = self.combat.update()
            self.inCombat = False
            if winner.id == self.currentLevel.player.id:
                # Whenever the player wins an encounter, a random percent between 15%-30% of his max hp is replenished
                hpAdded = math.ceil(random.randint(15, 30)/100 * self.currentLevel.player.attributes["HP"])
                print("---------")
                print(f"You win! Your life replenishes... {hpAdded} health healed.")
                # take the minimum between the current HP + hpAdded and the max hp
                self.currentLevel.player.hp = min(self.currentLevel.player.hp + hpAdded, self.currentLevel.player.attributes["HP"])
                print(f"Current HP: {self.currentLevel.player.hp}")
                self.killEnemy(loser)
            else:
                print("Life fades from your eyes! Tamriel will succumb to Oblivion, despite your best efforts...")
                exit()


        # print(self.inCombat)

        self.draw()
        pygame.display.flip()
        if len(self.currentLevel.enemies) == 0:
            self.changeLevel("azuratemple02")

    def draw(self):
        if not self.inCombat:
            self.currentLevel.draw()
        else:
            self.combat.draw()

    def changeLevel(self, levelName):
        player = self.currentLevel.player
        # we pass the current player to the next level
        self.currentLevel = Level(levelName, self.screen, player=player)

# ----------- GAME LOGIC METHODS -----------

    # handles player movement events
    def handleMovementEvent(self, key):

        if key == pygame.K_UP:
            newX = self.currentLevel.player.x
            newY = max(0, self.currentLevel.player.y - 1)
        elif key == pygame.K_DOWN:
            newX = self.currentLevel.player.x
            newY = min(self.currentLevel.height - 1,
                       self.currentLevel.player.y + 1)

        if key == pygame.K_LEFT:
            newX = max(0, self.currentLevel.player.x - 1)
            newY = self.currentLevel.player.y
        elif key == pygame.K_RIGHT:
            newX = min(self.currentLevel.width - 1,
                       self.currentLevel.player.x + 1)
            newY = self.currentLevel.player.y

        if not src.util.isPositionSolid(self.currentLevel.matrix, newX, newY):
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


    # deletes loser of combat
    def killEnemy(self, enemy):
        del self.currentLevel.entities[enemy.id]
        del self.currentLevel.enemies[enemy.id]


    # sets self.inCombat to true
    # begins combat
    def checkForCombat(self):
        for enemy in self.currentLevel.enemies.values():
            if enemy.x == self.currentLevel.player.x and enemy.y == self.currentLevel.player.y:
                self.inCombat = True
                self.combat = Combat(self.currentLevel.player, enemy)
                break
