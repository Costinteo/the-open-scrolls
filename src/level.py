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

                if tile == "-":
                    newEntity = Entity(self.screen, x=x, y=y, name="horizontal_wall", solid=True, sprite=f"sprites/{self.tileset}/horizontal_wall.png")
                elif tile == "|":
                    newEntity = Entity(self.screen, x=x, y=y, name="vertical_wall", solid=True, sprite=f"sprites/{self.tileset}/vertical_wall.png")
                elif tile == "/":
                    newEntity = Entity(self.screen, x=x, y=y, name="topleft_wall", solid=True, sprite=f"sprites/{self.tileset}/topleft_wall.png")
                elif tile == "\\":
                    newEntity = Entity(self.screen, x=x, y=y, name="topright_wall", solid=True, sprite=f"sprites/{self.tileset}/topright_wall.png")
                elif tile == "L":
                    newEntity = Entity(self.screen, x=x, y=y, name="botleft_wall", solid=True, sprite=f"sprites/{self.tileset}/botleft_wall.png")
                elif tile == "J":
                    newEntity = Entity(self.screen, x=x, y=y, name="botright_wall", solid=True, sprite=f"sprites/{self.tileset}/botright_wall.png")
                elif tile == ".":
                    newEntity = Entity(self.screen, x=x, y=y, name="floor", solid=False, sprite=f"sprites/{self.tileset}/floor.png")
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

                    newEntity = self.player
                elif tile == "x":
                    # we will read the characters in order they appear
                    # we unpack char data to avoid errors in case of refactoring
                    charName = src.util.trimmedline(charData.readline())
                    name, lvl, exp, hp, st, mg, strg, intl, agi, lck = src.util.DataParser.readCharData(charName)
                    inventory = src.util.DataParser.readInventoryData(charData.readline())
                    newEntity = Character(self.screen, x=x, y=y, name=name, level=lvl, exp=exp, HP=hp, STA=st, MGK=mg, STR=strg, INT=intl, AGI=agi, LCK=lck, inventory=inventory, sprite=f"sprites/{charName}.png")
                    self.enemies[newEntity.id] = newEntity

                # add entity to entity dict regardless of class
                if newEntity:
                    self.entities[newEntity.id] = newEntity
                    if newEntity.name.find("wall") != -1:
                        # we only store static entities in the matrix
                        self.matrix[y].append(newEntity)
                    else:
                        # if the entity we store is not a wall we have to store a walkable for it
                        floorBelowEntity = Entity(self.screen, x=x, y=y, name="floor", solid=False, sprite=f"sprites/{self.tileset}/floor.png")
                        self.matrix[y].append(floorBelowEntity)
                        self.entities[floorBelowEntity.id] = floorBelowEntity
        print() # prints newline
