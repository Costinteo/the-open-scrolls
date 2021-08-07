from pygame.constants import K_DOWN
from constants import *
import pygame

def getPadding(var, offset, extraOffset = 0):
    return var * offset + PADDING + extraOffset

def checkMovementEvent(key):
    return key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_LEFT or key == pygame.K_RIGHT

def isPositionOccupied(matrix, x, y):
    return True if matrix[y][x] else False