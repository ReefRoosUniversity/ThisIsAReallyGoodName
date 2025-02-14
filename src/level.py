# -*- coding: utf-8 -*-
import numpy as np
from enum import Enum


class Level:
    def __init__(self, n=8, m=8, winCondition=[]):
        self.board_state = np.full((n, m), Tiles(), dtype=Tiles)
        self.width = n  # Col
        self.height = m  # Row
        self.goal = winCondition

    def loadLevelFile(path):
        # TODO self descriptive and optional
        ""


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

    def isValidMove(Object):
        return False

    def update(level: Level):
        pass


class ConveyorTile(Tiles):
    def __init__(self, x: (int, int), z: (int, int)):
        self.position = x
        self.type = Tiles.Type.CONVEYOR
        self.direction = z

    def isValidMove(Object):
        return True

    def update(level: Level):
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

    def update(level: Level):
        # TODO Create new Object in the Level
        pass


class ReceiverTile(Tiles):
    def __init__(self, x: (int, int)):
        self.position = x
        self.type = Tiles.Type.RECEIVER

    def update(level: Level):
        # TODO remove any objects on the tile
        pass
