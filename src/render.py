# -*- coding: utf-8 -*-
from level import Level, Tiles
import pygame


class Rengine:

    def draw(screen: pygame.Surface, stage: Level,
             screen_dimensions=(1280, 720)):
        """
        renders all tiles in the level

        Parameters
        ----------
        screen : pygame.Surface
            The image frame buffer to be written to.
        stage : Level
            Current level.
        screen_dimensions : (int, int), optional
            Size of the screen. The default is (1280, 720).

        Returns
        -------
        None.

        """
        # Calculate the lowest ratio which will result in all tiles fitting
        # on screen
        rect_width = min((screen_dimensions[0] / float(stage.width+1)),
                         (screen_dimensions[1] / float(stage.height+1)))

        # I don't know how to explain myself
        left_adjust = screen_dimensions[0]/2 - \
            ((stage.width)/2*(rect_width+1))
        top_adjust = float(
            screen_dimensions[1]*0.5) - stage.height/2*(rect_width+1)

        for i in range(stage.board_state.size):
            x = i % stage.width
            y = i//stage.width
            colour = "#e1e1e1"

            if len(stage.selection) > 0 and ((x, y) in stage.selection) and \
                    stage.board_state[x][y].type == Tiles.Type.NONE:
                colour = "#9FE2BF"

            if (stage.board_state[x][y].type == Tiles.Type.NONE):
                if ((x, y) in stage.selection_removal):
                    colour = "#ed9da7"
                pygame.draw.rect(screen, colour,
                                 pygame.Rect(
                                     left_adjust + x * rect_width,
                                     top_adjust + y * rect_width,
                                     rect_width, rect_width))
                continue

            img = stage.board_state[x][y].texture
            img = pygame.transform.scale(img, (rect_width, rect_width))

            try:
                t = stage.board_state[x][y].direction[0] - \
                    stage.board_state[x][y].position[0]

                j = stage.board_state[x][y].direction[1] - \
                    stage.board_state[x][y].position[1]
                if (j != 0):
                    j += 1

                angle = 90*(j) + -90*t
                img = pygame.transform.rotate(img, angle)
            except AttributeError:
                pass

            rect = img.get_rect()

            rect.move_ip(left_adjust + x * rect_width,
                         top_adjust + y * rect_width)
            screen.blit(img, rect)

            if len(stage.selection_removal) > 0 and \
                    ((x, y) in stage.selection_removal):
                colour = "#eb40348a"
                sel = pygame.Surface((rect_width, rect_width), pygame.SRCALPHA)
                sel.fill(colour)
                screen.blit(sel, rect)

    def draw_packages(screen: pygame.Surface, stage: Level,
                      screen_dimensions=(1280, 720)):
        """
        Renders all packages.
        Should be ran **after** the regular draw function.

        Parameters
        ----------
        screen : pygame.Surface
            The image frame buffer to be written to.
        stage : Level
            Current level.
        screen_dimensions : (int, int), optional
            Size of the screen. The default is (1280, 720).

        Returns
        -------
        None.

        """
        # Calculate the lowest ratio which will result in all tiles fitting
        # on screen
        rect_width = min((screen_dimensions[0] / float(stage.width+1)),
                         (screen_dimensions[1] / float(stage.height+1)))

        # I don't know how to explain myself
        left_adjust = screen_dimensions[0]/2 - \
            ((stage.width)/2*(rect_width+1))
        top_adjust = float(
            screen_dimensions[1]*0.5) - stage.height/2*(rect_width+1)

        for obj in stage.packages:
            img = obj.texture
            img = pygame.transform.scale(img,
                                         (rect_width*obj.scale[0],
                                          rect_width*obj.scale[1]))
            rect = img.get_rect()
            rect.move_ip(left_adjust + obj.position[0] * rect_width,
                         top_adjust + obj.position[1] * rect_width)
            screen.blit(img, rect)
