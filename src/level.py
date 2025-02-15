# -*- coding: utf-8 -*-
import numpy as np


class Level:
    def __init__(self, n=8, m=8, winCondition=[]):
        self.board_state = np.full((n, m), Tiles(), dtype=Tiles)
        self.width = n  # Col
        self.height = m  # Row
        self.goal = winCondition
        self.selection = []
        self.objects = []

        self.mouseInitial = (0, 0)
        self.mouseFinal = (0, 0)

    def loadLevelFile(path):
        # TODO self descriptive and optional
        ""

    def processMouse(self, currentPosition: (int, int),
                     screenDimensions=(1280, 720)):
        gridCoordinates = self.convertScreenToGrid(currentPosition)
        x = min(gridCoordinates[0], self.mouseInitial[0])
        y = max(gridCoordinates[0], self.mouseInitial[0])
        z = min(gridCoordinates[1], self.mouseInitial[1])
        w = max(gridCoordinates[1], self.mouseInitial[1])
        if y-x > w-z:
            out = [(i, self.mouseInitial[1]) for i in range(x, y)]
            if (self.mouseInitial[0] > gridCoordinates[0]):
                out.sort(reverse=True)
        else:  # x-y < z-w:
            out = [(self.mouseInitial[0], i) for i in range(z, w)]
            if (self.mouseInitial[1] > gridCoordinates[1]):
                out.sort(reverse=True)

        self.selection = out
        self.createConveyor(gridCoordinates)

    def convertScreenToGrid(self, position: (int, int),
                            screenDimensions=(1280, 720)):
        RectWidth = min(((screenDimensions[0]) / float(self.width+1)),
                        ((screenDimensions[1]) / float(self.height+1)))+1
        leftAdjust = float((screenDimensions[0])/2) - \
            self.width/2*(RectWidth+1)
        topAdjust = float(
            (screenDimensions[1])/2) - self.height/2*(RectWidth+1)

        x = int(np.floor((position[0]-leftAdjust)/RectWidth))
        y = int(np.floor((position[1]-topAdjust)/RectWidth))
        return (x, y)

    def createConveyor(self, pos: (int, int)):
        x = self.mouseInitial[0]
        y = self.mouseInitial[1]
        if x in range(self.width) and y in range(self.height) \
                and len(self.selection) > 1:
            if self.board_state[x][y].type == 0:
                self.board_state[x][y] = ConveyorTile(
                    (x, y), self.selection[1])
        if len(self.selection) > 1:
            if (self.mouseInitial == self.selection[0]):
                self.selection.pop(0)
            self.mouseInitial = self.selection.pop(0)


class Object:
    def __init__(self, x: (float, float), ID):
        self.position = x
        self.ID = ID


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
        pass


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
