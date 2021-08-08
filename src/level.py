from src.entity import *

class Level:

    def __init__(self, levelPath, screen):
        mapInfo = open(levelPath)

        self.screen = screen

        self.name = mapInfo.readline()
        
        self.height, self.width = map(int, mapInfo.readline().split())

        # reinitializing the DrawInfo data
        DrawInfo.update(self.height, self.width)

        self.matrix = [[] for _ in range(self.height)]

        self.player = None
        self.enemies = dict()
        self.entities = dict()

        for y in range(self.height):
            line = mapInfo.readline()
            for x in range(self.width):

                tile = line[x]

                # legend:
                # + : Wall
                # . : Walkable
                # P : Player origin
                # x : Enemy origin

                if tile == "+":
                    newEntity = Entity(self.screen, x=x, y=y, name="Wall", solid=True)
                elif tile == ".":
                    newEntity = Entity(self.screen, x=x, y=y, name="Walkable", solid=False)
                elif tile == "P":
                    newEntity = Character(self.screen, x=x, y=y, name="Player")
                    self.player = newEntity
                elif tile == "x":
                    newEntity = Character(self.screen, x=x, y=y, name="Enemy")
                    self.enemies[newEntity.id] = newEntity

                # add entity to entity dict regardless of class
                self.entities[newEntity.id] = newEntity

                if tile == "+":
                    newEntityForMatrix = Entity(self.screen, x=x, y=y, name="Wall", solid=True)
                else:
                    newEntityForMatrix = Entity(self.screen, x=x, y=y, name="Walkable", solid=False)
                    
                self.matrix[y].append(newEntityForMatrix)

        # print current map
        for y in range(self.height):
            for x in range(self.width):
                print("+" if self.matrix[y][x].name == "Wall" else ".", end="")
            print("\n", end="")

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