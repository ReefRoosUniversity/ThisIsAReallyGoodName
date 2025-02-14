# -*- coding: utf-8 -*-
import level
import pygame
import numpy as np


class Rengine:

    def draw(screen: pygame.Surface, level_: level.Level(),
             screenDimensions=(1280, 720)):
        # Calculate the lowest ratio which will result in all tiles fitting
        # on screen
        RectWidth = min((screenDimensions[0] / float(level_.width+1)),
                        (screenDimensions[1] / float(level_.height+1)))
        # I don't know how to explain myself
        leftAdjust = screenDimensions[0]/2 - \
            ((level_.width)/2*(RectWidth+1))
        topAdjust = float(
            screenDimensions[1]*0.5) - level_.height/2*(RectWidth+1)
        COLOUR = ("white", "red", "black", "yellow", "blue")
        for i in range(level_.board_state.size):
            x = i % level_.width
            y = i//level_.width

            pygame.draw.rect(screen, COLOUR[level_.board_state[x][y].type], pygame.Rect(
                leftAdjust + x * RectWidth + (x % level_.width),
                topAdjust + y * RectWidth + (y % level_.height),
                RectWidth, RectWidth))
