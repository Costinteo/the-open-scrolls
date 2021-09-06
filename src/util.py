import pygame
import time
import src.item
from src.constants import *

def getPadding(var, offset, extraOffset=0):
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
        fullEffectName = trimmedline(effectData.readline())
        fullEffectDesc = trimmedline(effectData.readline())
        effectType = trimmedline(effectData.readline())
        effectValue = int(effectData.readline())
        effectAttribute = trimmedline(effectData.readline())
        return fullEffectName, fullEffectDesc, effectType, effectValue, effectAttribute

    @staticmethod
    def readItemData(itemName, surface=None, isEquipped=False):
        itemData = open(f"item_data/{itemName}.itemdata")
        fullItemName = trimmedline(itemData.readline())
        fullItemDesc = trimmedline(itemData.readline())
        itemType = trimmedline(itemData.readline())
        equippableDerivatives = {"Equippable", "Weapon", "Apparel"}

        # SLOT
        if itemType in equippableDerivatives:
            itemSlot = trimmedline(itemData.readline())

        # EFFECTS
        itemEffectLine = trimmedline(itemData.readline())
        itemEffects = []
        if itemEffectLine != "None":
            for effectName in itemEffectLine.split():
                fullEffectName, fullEffectDesc, effectType, effectValue, effectAttribute = DataParser.readEffectData(effectName)
                newEffect = src.item.Effect(surface=surface, name=fullEffectName, description=fullEffectDesc,
                                   effect=effectType, value=effectValue, attribute=effectAttribute)
                itemEffects.append(newEffect)

        # DMG/DEF + SPECIALIZATION
        if itemType in equippableDerivatives and itemType != "Equippable":
            # this can be either damage or defense
            itemValue = int(trimmedline(itemData.readline()))
            if itemType == "Weapon":
                itemSpec = trimmedline(itemData.readline())

        # dude HOW was I SO stupid, this is disastrous
        # it has to be refactored in classes!!!!
        # C procedural programming has ruined me
        if itemType == "Weapon":
            return src.item.Weapon(surface=surface, name=fullItemName, description=fullItemDesc, slot=itemSlot, damage=itemValue, specialization=itemSpec, enchantments=itemEffects, isEquipped=isEquipped)
        elif itemType == "Apparel":
            return src.item.Apparel(surface=surface, name=fullItemName, description=fullItemDesc, slot=itemSlot, defense=itemValue, enchantments=itemEffects, isEquipped=isEquipped)
        elif itemType == "Equippable":
            return src.item.Equippable(surface=surface, name=fullItemName, description=fullItemDesc, slot=itemSlot, enchantments=itemEffects, isEquipped=isEquipped)
        elif itemType == "Consumable":
            return src.item.Consumable(surface=surface, name=fullItemName, description=fullItemDesc, effect=itemEffects)

        return None

    @staticmethod
    def readCharData(charName, surface=None):
        dataFile = open(f"character_data/{charName}")
        name = trimmedline(dataFile.readline())
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
                itemCount = int(rawItem[quantityBeginPos + 1: quantityEndPos])
            item = DataParser.readItemData(itemName, isEquipped=isEquipped)
            inventory.append(item)

        return inventory
