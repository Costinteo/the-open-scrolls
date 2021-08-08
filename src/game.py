import pygame
import random
from util import *
from constants import *
from entity import *
from level import *

# init pygame
successes, failures = pygame.init()
print(f"{successes} successes and {failures} failures")


# settingsFile = None

# try:
#     settingsFile = open("settings.txt")
# except:
#     print("Settings file not found! Resuming with default values.")

# # if settings exist, then we parse them
# if settingsFile:
#     screenSize = settingsFile.readline().split()
#     WIDTH, HEIGHT = int(screenSize[0]), int(screenSize[1])

#     screenSize = settingsFile.readline().split()
#     ROWS, COLS = int(screenSize[0]), int(screenSize[1])
#     X_OFFSET = ((WIDTH - PADDING * 2) // COLS)
#     Y_OFFSET = ((HEIGHT - PADDING * 2) // ROWS)

#     BACKGROUNDCOLOUR = tuple(list(map(int, settingsFile.readline().split())))
#     DOTSCOLOUR = tuple(list(map(int, settingsFile.readline().split())))
#     P1COLOUR = tuple(list(map(int, settingsFile.readline().split())))
#     P2COLOUR = tuple(list(map(int, settingsFile.readline().split())))

#     PVP = bool(int(settingsFile.readline()))
#     ALGORITHM, DEPTH = settingsFile.readline().split()
#     DEPTH = int(DEPTH)



class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("The Open Scrolls")
        self.clock = pygame.time.Clock()

        self.currentLevel = Level("levels/dungeon.map", self.screen)


    def handleMovementEvent(self, key):
        if key == pygame.K_UP:
            if not isPositionSolid(self.currentLevel.matrix, self.currentLevel.player.x, max(0, self.currentLevel.player.y - 1)):
                self.currentLevel.player.move(self.currentLevel.player.x, max(0, self.currentLevel.player.y - 1))
        elif key == pygame.K_DOWN:
            if not isPositionSolid(self.currentLevel.matrix, self.currentLevel.player.x, min(self.currentLevel.height, self.currentLevel.player.y + 1)):
                self.currentLevel.player.move(self.currentLevel.player.x, min(self.currentLevel.height - 1, self.currentLevel.player.y + 1))
        if key == pygame.K_LEFT:
            if not isPositionSolid(self.currentLevel.matrix, max(0, self.currentLevel.player.x - 1), self.currentLevel.player.y):
                self.currentLevel.player.move(max(0, self.currentLevel.player.x - 1), self.currentLevel.player.y)
        elif key == pygame.K_RIGHT:
            if not isPositionSolid(self.currentLevel.matrix, min(self.currentLevel.width - 1, self.currentLevel.player.x + 1), self.currentLevel.player.y):
                self.currentLevel.player.move(min(self.currentLevel.width - 1, self.currentLevel.player.x + 1), self.currentLevel.player.y)
        


    def update(self):
        # sleep to sync with fps
        self.clock.tick(FPS)
        
        # colour screen
        self.screen.fill(BACKGROUNDCOLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.KEYDOWN:
                # handle movement events
                # if player presses movement key, a turn happens
                if checkMovementEvent(event.key):
                    self.handleMovementEvent(event.key)
                    print(self.currentLevel.player.x, self.currentLevel.player.y)
                    # turnEvent()
                    

        self.draw()
        pygame.display.flip()


    def draw(self):
        self.currentLevel.draw()

