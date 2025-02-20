# -*- coding: utf-8 -*-
import numpy as np

# %% LEVEL


class Level:
    def __init__(self, n=8, m=8, winCondition=[]):
        self.boardState = np.full((n, m), Tiles(), dtype=Tiles)
        self.width = n  # Col
        self.height = m  # Row
        self.goal = winCondition
        self.selection = []
        self.objects = []

        self.mouseInitial = (None, None)
        self.mouseFinal = (None, None)

    def loadLevelFile(path):
        # TODO self descriptive and optional
        ""

    def processMouse(self, currentPosition: (int, int),
                     screenDimensions=(1280, 720)):
        gridCoordinates = self.convertScreenToGrid(
            currentPosition, screenDimensions)
        if (self.mouseInitial == (None, None)):
            return
        x = min(gridCoordinates[0], self.mouseInitial[0])
        y = max(gridCoordinates[0], self.mouseInitial[0])
        z = min(gridCoordinates[1], self.mouseInitial[1])
        w = max(gridCoordinates[1], self.mouseInitial[1])
        if y-x > w-z:
            out = [(i, self.mouseInitial[1]) for i in range(x, y+1)]
            if (self.mouseInitial[0] > gridCoordinates[0]):
                out.sort(reverse=True)
        else:  # x-y < z-w:
            out = [(self.mouseInitial[0], i) for i in range(z, w+1)]
            if (self.mouseInitial[1] > gridCoordinates[1]):
                out.sort(reverse=True)

        self.selection = out

    def convertScreenToGrid(self, position: (int, int),
                            screenDimensions=(1280, 720)):
        RectWidth = min(((screenDimensions[0]) / float(self.width+1)),
                        ((screenDimensions[1]) / float(self.height+1)))
        leftAdjust = float((screenDimensions[0])/2) - \
            self.width/2*(RectWidth+1)
        topAdjust = float(
            (screenDimensions[1])/2) - self.height/2*(RectWidth+1)

        x = int(np.floor((position[0]-leftAdjust)/RectWidth))
        y = int(np.floor((position[1]-topAdjust)/RectWidth))
        return (x, y)

    def createConveyor(self):
        if len(self.selection) <= 1:
            return
        for i in range(len(self.selection)-1):
            x = self.selection[i]
            if not ((x[0] < self.width and x[0] >= 0)
                    and (x[1] < self.width and x[1] >= 0)):
                continue
            if (self.boardState[x[0]][x[1]].type != Tiles.Type().NONE):
                continue
            self.boardState[x[0]][x[1]] = ConveyorTile(
                self.selection[i], self.selection[i+1])

# %% OBJECTS


class Object:
    def __init__(self, x: (float, float), ID, size=(0.8, 0.8)):
        self.position = (x[0]+size[0]/2, x[1]+size[1]/2)
        self.ID = ID
        self.velocity = (0.0, 0.0)
        self.scale = size

    def update(self, deltaTime: float):
        self.position = (self.position[0] + self.velocity[0] * deltaTime,
                         self.position[1] + self.velocity[1] * deltaTime)
        self.velocity = (0, 0)

    def isCollision(self, x: (float, float), size: (float, float)):
        # TODO
        pass

# %% TILES


class Tiles:
    # Base class for all game tiles

    class Type():
        NONE = 0
        WALL = 1
        CONVEYOR = 2
        RECEIVER = 3
        GENERATOR = 4

    def __init__(self):
        self.position = (0, 0)
        self.type = Tiles.Type.NONE

    def isValidMove(self, Object):
        return False

    def update(self, level: Level):
        pass


class ConveyorTile(Tiles):
    def __init__(self, x: (int, int), z: (int, int)):
        self.position = x
        self.type = Tiles.Type.CONVEYOR
        self.direction = z

    def isValidMove(self, Object):
        return True

    def update(self, level: Level):
        # TODO Move the object in the facing direction
        for i in level.objects:
            if (i.position[0] >= self.position[0]
                and i.position[1] >= self.position[1]) \
                    and (i.position[0] < self.position[0]+1
                         and i.position[1] < self.position[1]+1):
                i.velocity = (
                    self.direction[0]-self.position[0],
                    self.direction[1]-self.position[1])


class WallTile(Tiles):
    def __init__(self, x: (int, int)):
        self.position = x
        self.type = Tiles.Type.WALL


class GeneratorTile(Tiles):
    def __init__(self, x: (int, int), y: (int, int), ID):
        self.position = x
        self.output = y
        self.type = Tiles.Type.GENERATOR

    def update(self, level: Level):
        # TODO Create new Object in the Level
        pass


class ReceiverTile(Tiles):
    def __init__(self, x: (int, int)):
        self.position = x
        self.type = Tiles.Type.RECEIVER

    def update(self, evel: Level):
        # TODO remove any objects on the tile
        pass
