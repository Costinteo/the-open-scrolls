import pygame
import time
from src.constants import *

def getPadding(var, offset, extraOffset = 0):
    return var * offset + PADDING + extraOffset

def checkMovementEvent(key):
    return key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_LEFT or key == pygame.K_RIGHT

def checkAttackChoice(key):
    return key == pygame.K_p or key == pygame.K_m

def swap(a, b):
    a, b = b, a

def sleep(seconds):
    t = time.time()
    while time.time() - t < seconds:
        continue

# strcmp() style function of comparing stats
# but it returns strings informing of the result, for clarity
def compareStat(statToCompare, firstChar, secondChar):

    # if firstChar has a greater attribute level than secondChar return 1
    if firstChar.attributes[statToCompare] > secondChar.attributes[statToCompare]:
        return "greater"

    # if firstChar has a lesser attribute level than secondChar return -1    
    if firstChar.attributes[statToCompare] < secondChar.attributes[statToCompare]:
        return "lower"
    
    # if they're equal return 0
    return "equal"


def trimmedline(line):
    if line[-1] == "\n":
        return line[0:-1]
    return line

# yeah I have no clue how to write this properly
# I feel like this system is overcomplicated and has to be thought out better
def readItemData(itemName, surface = None):
    itemData = open("item_data/" + itemName + ".itemdata")
    fullItemName = itemData.readline()
    fullItemDesc = itemData.readline()
    itemType = itemData.readline()
    equippableDerivatives = {"Equippable", "Weapon", "Apparel"}
    if itemType in equippableDerivatives:
        itemSlot = itemData.readline()
        # todo: not finished yet [27.08.2021]
        return None
        
def readCharData(charName, surface = None):
    dataFile = open("character_data/" + charName)
    name = dataFile.readline()
    lvl, exp = map(int, dataFile.readline().split())
    hp, st, mg = map(int, dataFile.readline().split())
    strg, intl, agi, lck = map(int, dataFile.readline().split())
    # sprite not used yet
    # sprite = dataFile.readline()
    return name, lvl, exp, hp, st, mg, strg, intl, agi, lck

def readInventoryData(inventoryLine):
    inventory = []
    for rawItem in inventoryLine.split():
        itemName = rawItem
        itemCount = 1
        isEquipped = False
        # check if item is equipped
        if rawItem.find("[E]") != -1:
            isEquipped = True
            itemName = rawItem[3:]
        # check item count
        if rawItem.find("[") != -1 and not isEquipped:
            quantityBeginPos = rawItem.find("[")
            quantityEndPos = rawItem.find("]")
            itemName = rawItem[:quantityBeginPos]
            itemCount = int(rawItem[quantityBeginPos + 1 : quantityEndPos])
        print(f"itemname:{itemName}, itemcount:{itemCount}, equipped:{isEquipped}")
        itemData = readItemData(itemName)
        
    return []


def isPositionSolid(matrix, x, y):
    return True if matrix[y][x].solid else False


