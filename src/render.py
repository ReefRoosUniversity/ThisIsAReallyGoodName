from level import Level, Tiles, Package
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

        pygame.draw.rect(screen, "#e1e1e1",
                         pygame.Rect(left_adjust, top_adjust, stage.width *
                                     rect_width, stage.height*rect_width))

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
            elif stage.board_state[x][y].type == Tiles.Type.NONE:
                continue
            img = stage.board_state[x][y].getTexture()
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

        left_adjust = screen_dimensions[0]/2 - \
            ((stage.width)/2*(rect_width+1))
        top_adjust = float(
            screen_dimensions[1]*0.5) - stage.height/2*(rect_width+1)

        for obj in stage.packages:
            img = obj.getTexture()
            img = pygame.transform.scale(img,
                                         (rect_width*obj.scale[0],
                                          rect_width*obj.scale[1]))
            alpha = obj.calculate_transparency(pygame.time.get_ticks()) * 256
            #  Temporary for now ^

            img.set_alpha(alpha)
            rect = img.get_rect()
            rect.move_ip(left_adjust + obj.position[0] * rect_width,
                         top_adjust + obj.position[1] * rect_width)
            screen.blit(img, rect)

    def draw_goal(screen: pygame.Surface, stage: Level,
                  screen_dimensions=(1280, 720)):
        rect_width = min((screen_dimensions[0] / float(stage.width+1)),
                         (screen_dimensions[1] / float(stage.height+1)))
        i = 0
        for ID in stage.goal:
            match ID:
                case 'r':
                    img = Package.textures[0]
                case 'b':
                    img = Package.textures[1]
                case 'p':
                    img = Package.textures[2]

            img = pygame.transform.scale(img, (rect_width*0.5, rect_width*0.5))
            rect = img.get_rect()
            rect.move_ip(i*rect_width*0.5, 10)
            if (i < stage.goal_index):
                colour = "#9FE2BF"
            elif i == stage.goal_index:
                colour = "yellow"
            else:
                colour = "#16161D8a"

            sel = pygame.Surface(
                (rect_width*0.5, rect_width*0.5), pygame.SRCALPHA)
            sel.fill(colour)
            screen.blit(sel, rect)

            screen.blit(img, rect)
            i += 1
