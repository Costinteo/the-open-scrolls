import pygame
import time
from src.item import *
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


def isPositionSolid(matrix, x, y):
    return True if matrix[y][x].solid else False

######################################################
# yeah I have no clue how to write this properly
# I feel like this system is overcomplicated and 
# has to be thought out better
######################################################
# UPDATE: I thought about it and maybe this should
# be moved in each class and used as an initializer,
# or maybe add an optional boolean param in the constr 
# and read from file if true
# TODO: refactor this in classes after first functional draft
######################################################
class DataParser:

    @staticmethod        
    def readEffectData(effectName):
        effectData = open(f"effect_data/{effectName}.effectdata")
        fullEffectName = effectData.readline()
        fullEffectDesc = effectData.readline()
        effectType = effectData.readline()
        effectValue = int(effectData.readline())
        effectAttribute = effectData.readline()
        return fullEffectName, fullEffectDesc, effectType, effectValue, effectAttribute


    @staticmethod
    def readItemData(itemName, surface = None):
        itemData = open(f"item_data/{itemName}.itemdata")
        fullItemName = itemData.readline()
        fullItemDesc = itemData.readline()
        itemType = itemData.readline()
        equippableDerivatives = {"Equippable", "Weapon", "Apparel"}
        
        # SLOT
        if itemType in equippableDerivatives:
            itemSlot = itemData.readline()

        # EFFECTS
        itemEffectLine = itemData.readline()
        itemEffects = []
        if itemEffectLine != "None":
            for effectName in itemEffectLine.split():
                fullEffectName, fullEffectDesc, effectType, effectValue, effectAttribute = DataParser.readEffectData(effectName)
                newEffect = Effect(surface=surface, name=fullEffectName, description=fullEffectDesc, effect=effectType, value=effectValue, attribute=effectAttribute)
                itemEffects.append(newEffect)
        
        # DMG/DEF + SPECIALIZATION
        if itemType in equippableDerivatives:
            # this can be either damage or defense
            itemValue = itemData.readline()
            if itemType == "Weapon":
                itemSpec = itemData.readline()

        # dude HOW was I SO stupid, this is disastrous
        # it has to be refactored in classes!!!!
        # C procedural programming has ruined me
        if itemType == "Weapon":
            return Weapon(surface=surface, name=fullItemName, description=fullItemDesc, slot=itemSlot, damage=itemValue, specialization=itemSpec, enchantments=itemEffects)
        elif itemType == "Apparel":
            return Apparel(surface=surface, name=fullItemName, description=fullItemDesc, slot=itemSlot, defense=itemValue, enchantments=itemEffects)
        elif itemType == "Consumable":
            return Consumable(surface=surface, name=fullItemName, description=fullItemDesc, effect=itemEffects)

        return None

    @staticmethod        
    def readCharData(charName, surface = None):
        dataFile = open(f"character_data/{charName}")
        name = dataFile.readline()
        lvl, exp = map(int, dataFile.readline().split())
        hp, st, mg = map(int, dataFile.readline().split())
        strg, intl, agi, lck = map(int, dataFile.readline().split())
        # sprite not used yet
        # sprite = dataFile.readline()
        return name, lvl, exp, hp, st, mg, strg, intl, agi, lck
    
    @staticmethod
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
            itemData = DataParser.readItemData(itemName)
            
        return []



