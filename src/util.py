import pygame
from src.constants import *

def getPadding(var, offset, extraOffset = 0):
    return var * offset + PADDING + extraOffset

def checkMovementEvent(key):
    return key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_LEFT or key == pygame.K_RIGHT

def swap(a, b):
    a, b = b, a

# strcmp() style function of comparing stats
def compareStat(statToCompare, firstChar, secondChar):

    # if firstChar has a greater attribute level than secondChar return 1
    if firstChar.attributes[statToCompare] > secondChar.attributes[statToCompare]:
        return 1

    # if firstChar has a lesser attribute level than secondChar return -1    
    if firstChar.attributes[statToCompare] < secondChar.attributes[statToCompare]:
        return -1
    
    # if they're equal return 0
    return 0
    

def isPositionSolid(matrix, x, y):
    return True if matrix[y][x].solid else False


