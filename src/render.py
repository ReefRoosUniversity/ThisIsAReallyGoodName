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
        for i in range(level_.board_state.size):
            x = i % level_.width
            y = i//level_.width
            colour = COLOUR[level_.board_state[x][y].type]

            pygame.draw.rect(screen, colour,
                             pygame.Rect(
                                 leftAdjust + x * rectWidth +
                                 (x % level_.width),
                                 topAdjust + y * rectWidth +
                                 (y % level_.height),
                                 rectWidth, rectWidth))

            if level_.board_state[x][y].type == level.Tiles.Type.CONVEYOR:
                z = level_.board_state[x][y].direction
                zScreen = (leftAdjust + z[0]*rectWidth + (z[0] % level_.width),
                           leftAdjust + z[1]*rectWidth + (z[1] % level_.width))
                xScreen = leftAdjust + x * rectWidth + (x % level_.width)
                yScreen = topAdjust + y * rectWidth + (y % level_.height)

                pygame.draw.line(screen, "PINK", (xScreen, yScreen), zScreen)
                # pygame.draw.line(screen, "white", c, j)

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
                                 leftAdjust + obj.position[0] * rectWidth,
                                 topAdjust + obj.position[1] * rectWidth,
                                 rectWidth*0.8, rectWidth*0.8))
