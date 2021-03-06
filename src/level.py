import src.util
from src.entity import *
from src.character import *

class Level:

    def __init__(self, levelName, screen, player = None):
        mapInfo = open("levels/" + levelName + ".map")
        charData = open("levels/" + levelName + ".chardata")

        self.screen = screen

        self.name = src.util.trimmedline(mapInfo.readline())
        self.tileset = src.util.trimmedline(mapInfo.readline())

        self.height, self.width = map(int, mapInfo.readline().split())

        # reinitializing the DrawInfo data
        DrawInfo.update(self.height, self.width)

        self.matrix = [[] for _ in range(self.height)]

        self.player = player
        self.enemies = dict()
        self.entities = dict()
        self.exit = None

        self.parseLevelData(mapInfo, charData)

    def set_screen(self, screen):
        self.screen = screen

    def draw(self):
        for ent in self.entities.values():
            # skip player and enemies so they get drawn on top of everything else
            if ent.id == self.player.id or ent.id in self.enemies:
                continue
            ent.draw()

        for enemy in self.enemies.values():
            enemy.draw()
        # draw player on top of everything else
        self.entities[self.player.id].draw()

    def parseLevelData(self, mapInfo, charData):
        # reading and parsing level data
        for y in range(self.height):
            line = mapInfo.readline()
            print() # prints newline
            for x in range(self.width):

                print("." if line[x] == "." else line[x], sep='', end='') # prints matrix

                tile = line[x]

                # see levels/template.map for legend

                newEntity = None
                tileName = None
                isTileSolid = True

                if tile == "-":
                    tileName = "horizontal_wall"
                elif tile == "|":
                    tileName = "vertical_wall"
                elif tile == "/":
                    tileName="topleft_wall"
                elif tile == "\\":
                    tileName="topright_wall"
                elif tile == "L":
                    tileName="botleft_wall"
                elif tile == "J":
                    tileName="botright_wall"
                elif tile == ".":
                    tileName = "floor"
                    isTileSolid = False
                elif tile == "@":
                    tileName = "door"
                    isTileSolid = False
                elif tile == "P":
                    # only create the player if no current character is passed
                    # in constructor of level
                    if not self.player:
                        charName = "testplayer"
                        name, lvl, exp, hp, st, mg, strg, intl, agi, lck = src.util.DataParser.readCharData(charName)
                        # hardcoded for the player character so far
                        # it needs a special type of save structure that I haven't implemented yet
                        # TODO: implement save file that contains all player character data
                        inventory = src.util.DataParser.readInventoryData("[E]scimitar [E]iron_helmet")
                        self.player = Character(self.screen, x=x, y=y, name=name, isPlayer=True, level=lvl, exp=exp, HP=hp, STA=st, MGK=mg, STR=strg, INT=intl, AGI=agi, LCK=lck, inventory=inventory, sprite=f"sprites/Player.png")
                    else:
                        self.player.x = x
                        self.player.y = y
                        self.player.resetHP()
                        self.player.updateSpritePosition(x, y)
                    newEntity = self.player
                elif tile == "x":
                    # we will read the characters in order they appear
                    # we unpack char data to avoid errors in case of refactoring
                    charName = src.util.trimmedline(charData.readline())
                    name, lvl, exp, hp, st, mg, strg, intl, agi, lck = src.util.DataParser.readCharData(charName)
                    inventory = src.util.DataParser.readInventoryData(charData.readline())
                    newEntity = Character(self.screen, x=x, y=y, name=name, level=lvl, exp=exp, HP=hp, STA=st, MGK=mg, STR=strg, INT=intl, AGI=agi, LCK=lck, inventory=inventory, sprite=f"sprites/{charName}.png")
                    self.enemies[newEntity.id] = newEntity

                # used to create static tiles
                if tileName:
                    newEntity = Entity(self.screen, x=x, y=y, name=tileName, solid=isTileSolid, sprite=f"sprites/{self.tileset}/{tileName}.png")
                    if tileName == "door":
                        self.exitDoor = newEntity

                # add entity to entity dict regardless of class
                if newEntity:
                    self.entities[newEntity.id] = newEntity
                    if newEntity.name.find("wall") != -1 or newEntity.name.find("door") != -1:
                        # we only store static entities in the matrix
                        self.matrix[y].append(newEntity)
                    else:
                        # if the entity we store is not a wall we have to store a walkable for it
                        floorBelowEntity = Entity(self.screen, x=x, y=y, name="floor", solid=False, sprite=f"sprites/{self.tileset}/floor.png")
                        self.matrix[y].append(floorBelowEntity)
                        self.entities[floorBelowEntity.id] = floorBelowEntity
        print() # prints newline
