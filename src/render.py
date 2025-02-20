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
            r = pygame.Rect(
                leftAdjust + x * rectWidth,
                topAdjust + y * rectWidth,
                rectWidth, rectWidth)
            if (colour == "black"):  # adapt later for other images
                img = level.ConveyorTile.texture
                img = pygame.transform.scale(img, (rectWidth, rectWidth))
                t = level_.boardState[x][y].direction[0] - \
                    level_.boardState[x][y].position[0]

                j = level_.boardState[x][y].direction[1] - \
                    level_.boardState[x][y].position[1]
                if (j != 0):
                    j += 1

                angle = 90*(j) + -90*t
                img = pygame.transform.rotate(img, angle)
                rect = img.get_rect()

                rect.move_ip(leftAdjust + x * rectWidth,
                             topAdjust + y * rectWidth)
                screen.blit(img, rect)
                # pygame.draw.rect(screen, colour,
                #                  rect, 1)
                continue
            pygame.draw.rect(screen, colour, r)

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
                                 leftAdjust + rectWidth*(obj.position[0]),
                                 topAdjust + rectWidth*(obj.position[1]),
                                 rectWidth*obj.scale[0], rectWidth*obj.scale[1]))
