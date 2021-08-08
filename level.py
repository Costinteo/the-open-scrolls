from entity import *

class Level():
    def __init__(self, levelPath, screen):
        mapInfo = open(levelPath)

        self.screen = screen

        self.name = mapInfo.readline()
        
        self.height, self.width = map(int, mapInfo.readline().split())
        self.matrix = [[] for _ in range(self.height)]

        self.player = None
        self.enemies = {}
        self.entities = {}

        for y in range(self.height):
            line = mapInfo.readline()
            for x in range(self.width):

                tile = line[x]

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
                self.matrix[y].append(newEntity)
        
        del(line)
        del(tile)

    def draw(self):
        for ent in self.entities.values():
            ent.draw()