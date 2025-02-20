# -*- coding: utf-8 -*-
import numpy as np
import pygame
import os
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
        self.position = (x[0] + (1-size[0])/2,
                         x[1] + (1-size[1])/2)
        self.ID = ID
        self.velocity = (0.0, 0.0)
        self.scale = size
        self.lifespan = 100*1000  # 10 seconds in measued in milisecond
        self.spawnTime = pygame.time.get_ticks()

    def update(self, deltaTime: float, level: Level):
        n = (self.velocity[0]**2 + self.velocity[1]**2)**(1/2)
        if (n != 0.0):  # Normalize velocity
            self.velocity = (self.velocity[0]/n, self.velocity[1]/n)
        self.position = (self.position[0] + self.velocity[0] * deltaTime,
                         self.position[1] + self.velocity[1] * deltaTime)
        self.velocity = (0, 0)
        if (self.spawnTime + self.lifespan < pygame.time.get_ticks()):
            level.objects.remove(self)

    def isCollision(self, x: (float, float), size=(1, 1)):
        # TODO
        xScale = self.scale[0]
        xPos = self.position[0]

        yScale = self.scale[1]
        yPos = self.position[1]
        xAxis = (((xPos + xScale) >= x[0] and
                  (x[0] + size[0]) >= xPos))
        yAxis = (((yPos + yScale) >= x[1] and
                  (x[1] + size[1]) >= yPos))
        return xAxis and yAxis

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

    def update(self, level: Level):
        pass


class ConveyorTile(Tiles):
    texture = pygame.image.load(os.path.join("../assets/", "conveyor.png"))

    def __init__(self, x: (int, int), z: (int, int)):
        self.position = x
        self.type = Tiles.Type.CONVEYOR
        self.direction = z

    def update(self, level: Level):
        # TODO  Add gaurd rails

        for i in level.objects:
            if i.isCollision(self.position):
                i.velocity = ((i.velocity[0] +
                               self.direction[0]-self.position[0]),
                              (i.velocity[1] +
                              self.direction[1]-self.position[1]))


class WallTile(Tiles):
    def __init__(self, x: (int, int)):
        self.position = x
        self.type = Tiles.Type.WALL


class GeneratorTile(Tiles):
    def __init__(self, x: (int, int), y: (int, int), ID, cycle=5.0):
        self.position = x
        self.output = y
        self.ID = ID
        self.type = Tiles.Type.GENERATOR
        self.cycleTime = cycle * 1000.0
        self.timeOld = pygame.time.get_ticks()

    def update(self, level: Level):
        if pygame.time.get_ticks() >= self.timeOld + self.cycleTime:
            # TODO play animation
            level.objects.append(Object(self.output, self.ID))
            self.timeOld = pygame.time.get_ticks()


class ReceiverTile(Tiles):
    def __init__(self, x: (int, int)):
        self.position = x
        self.type = Tiles.Type.RECEIVER

    def update(self, level: Level):
        # TODO remove any objects on the tile
        for o in level.objects:
            if o.isCollision(self.position):
                level.objects.remove(o)
