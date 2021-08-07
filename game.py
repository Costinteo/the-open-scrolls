import pygame
import random
from util import *
from constants import *
from entity import *

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

        self.matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)] 

        walls = 25
        for x in range(1,COLS):
            for y in range(1,ROWS):
                if not walls:
                    break
                isWall = random.randint(0,1)
                if isWall:
                    walls -= 1
                self.matrix[y][x] = isWall


        self.player = Character()
        print(self.matrix)


    def handleMovementEvent(self, key):
        if key == pygame.K_UP:
            if not isPositionOccupied(self.matrix, self.player.x, max(0, self.player.y - 1)):
                self.player.move(self.player.x, max(0, self.player.y - 1))
        elif key == pygame.K_DOWN:
            if not isPositionOccupied(self.matrix, self.player.x, min(ROWS - 1, self.player.y + 1)):
                self.player.move(self.player.x, min(ROWS - 1, self.player.y + 1))
        if key == pygame.K_LEFT:
            if not isPositionOccupied(self.matrix, max(0, self.player.x - 1), self.player.y):
                self.player.move(max(0, self.player.x - 1), self.player.y)
        elif key == pygame.K_RIGHT:
            if not isPositionOccupied(self.matrix, min(COLS - 1, self.player.x + 1), self.player.y):
                self.player.move(min(COLS - 1, self.player.x + 1), self.player.y)
        


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
                    print(self.player.x, self.player.y)
                    # turnEvent()
                    

        self.draw()
        pygame.display.flip()


    def draw(self):
        for x in range(COLS):
            for y in range(ROWS):
                lineThickness = 1
                if (self.matrix[y][x]):
                    lineThickness = 0
                cell = pygame.Rect(getPadding(x, X_OFFSET), getPadding(y, Y_OFFSET), CELL_WIDTH, CELL_HEIGHT) 
                pygame.draw.rect(self.screen, WALLSCOLOUR, cell, lineThickness)
        pygame.draw.rect(self.screen, PLAYERCOLOUR, self.player.sprite)

