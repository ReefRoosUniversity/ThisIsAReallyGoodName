# -*- coding: utf-8 -*-
import level
import pygame


class Rengine:

    def draw(screen: pygame.Surface, level_: level.Level(),
             screenDimensions=(1280, 720)):
        # Calculate the lowest ratio which will result in all tiles fitting
        # on screen
        rectWidth = min((screenDimensions[0] / float(level_.width+1)),
                        (screenDimensions[1] / float(level_.height+1)))

        # I don't know how to explain myself
        leftAdjust = screenDimensions[0]/2 - \
            ((level_.width)/2*(rectWidth+1))
        topAdjust = float(
            screenDimensions[1]*0.5) - level_.height/2*(rectWidth+1)

        COLOUR = ("white", "red", "black", "yellow", "blue")
        for i in range(level_.boardState.size):
            x = i % level_.width
            y = i//level_.width
            colour = COLOUR[level_.boardState[x][y].type]
            if len(level_.selection) > 0 and ((x, y) in level_.selection) and \
                    colour == "white":
                colour = "#9FE2BF"
            pygame.draw.rect(screen, colour,
                             pygame.Rect(
                                 leftAdjust + x * rectWidth +
                                 (x % level_.width),
                                 topAdjust + y * rectWidth +
                                 (y % level_.height),
                                 rectWidth, rectWidth))

    def drawObjects(screen: pygame.Surface, level_: level.Level,
                    screenDimensions=(1280, 720)):
        # Calculate the lowest ratio which will result in all tiles fitting
        # on screen
        rectWidth = min((screenDimensions[0] / float(level_.width+1)),
                        (screenDimensions[1] / float(level_.height+1)))

        # I don't know how to explain myself
        leftAdjust = screenDimensions[0]/2 - \
            ((level_.width)/2*(rectWidth+1))
        topAdjust = float(
            screenDimensions[1]*0.5) - level_.height/2*(rectWidth+1)

        for obj in level_.objects:
            pygame.draw.rect(screen, "lime",
                             pygame.Rect(
                                 leftAdjust +
                                     (obj.position[0] -
                                      obj.scale[0]/2) * rectWidth,
                                 topAdjust +
                                     (obj.position[1] -
                                      obj.scale[1]/2) * rectWidth,
                                 rectWidth*obj.scale[0], rectWidth*obj.scale[1]))
