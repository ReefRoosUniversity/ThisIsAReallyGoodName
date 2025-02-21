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

        for i in range(level_.boardState.size):
            x = i % level_.width
            y = i//level_.width
            colour = "#e1e1e1"
            if len(level_.selection) > 0 and ((x, y) in level_.selection) and \
                    level_.boardState[x][y].type == level.Tiles.Type.NONE:
                colour = "#9FE2BF"
            r = pygame.Rect(
                leftAdjust + x * rectWidth,
                topAdjust + y * rectWidth,
                rectWidth, rectWidth)

            if (level_.boardState[x][y].type == level.Tiles.Type.NONE):
                pygame.draw.rect(screen, colour, r)
                continue

            img = level_.boardState[x][y].texture
            img = pygame.transform.scale(img, (rectWidth, rectWidth))
            try:
                t = level_.boardState[x][y].direction[0] - \
                    level_.boardState[x][y].position[0]

                j = level_.boardState[x][y].direction[1] - \
                    level_.boardState[x][y].position[1]
                if (j != 0):
                    j += 1

                angle = 90*(j) + -90*t
                img = pygame.transform.rotate(img, angle)
            except AttributeError:
                pass

            rect = img.get_rect()

            rect.move_ip(leftAdjust + x * rectWidth,
                         topAdjust + y * rectWidth)
            screen.blit(img, rect)
            # pygame.draw.rect(screen, colour,
            #                  rect, 1)

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
            r = pygame.Rect(
                leftAdjust + rectWidth*(obj.position[0]),
                topAdjust + rectWidth*(obj.position[1]),
                rectWidth*obj.scale[0], rectWidth*obj.scale[1])

            img = obj.texture
            img = pygame.transform.scale(
                img, (rectWidth*obj.scale[0], rectWidth*obj.scale[1]))

            rect = img.get_rect()

            rect.move_ip(leftAdjust + obj.position[0] * rectWidth,
                         topAdjust + obj.position[1] * rectWidth)
            screen.blit(img, rect)

            # pygame.draw.rect(screen, "lime",
            #                  pygame.Rect(
            #                      leftAdjust + rectWidth*(obj.position[0]),
            #                      topAdjust + rectWidth*(obj.position[1]),
            #                      rectWidth*obj.scale[0], rectWidth*obj.scale[1]))
