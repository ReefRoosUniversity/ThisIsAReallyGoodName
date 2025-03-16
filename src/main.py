# %%
import pygame

from level import Level, Tiles, Package
from render import Rengine
# %%  TODO
# - Add conveyer belt removal
# - Start Menu
# - Level loading
# - Colour scheme
# - PEP8 standard
SCREEN_DIMENSIONS = (1280, 720)


def main():
    # %% SETUP
    pygame.init()
    screen = pygame.display.set_mode(
        SCREEN_DIMENSIONS, pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()
    running = True
    paused = False
    stage = Level(8, 8)
    Tiles.convert_tile_images(screen)

    # TEST
    # This should not remain in the code after testing and serves no purpose
    # other than making sure things work. Feel free to experiment with it to
    # understand this mess.
    stage.board_state[2, 2] = Tiles.WallTile((2, 2))
    stage.board_state[2, 3] = Tiles.WallTile((2, 3))
    stage.board_state[2, 4] = Tiles.WallTile((2, 4))
    stage.board_state[4, 2] = Tiles.GeneratorTile(
        (4, 2), (4, 3),
        Tiles.GeneratorTile.Colour_ID().RED)

    stage.board_state[6, 5] = Tiles.ConveyorTile((6, 5), (6, 4), True)
    stage.board_state[2, 1] = Tiles.ReceiverTile((2, 1))
    stage.packages.append(Package((1, 5), 1))

    FPS = 60
    # %% GAMELOOP
    while running:
        deltaTime = clock.tick(FPS)/1000
        # %% KEY POLLING
        #
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    # Quitting should work when paused
                running = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press P to toggle pause
                    paused = not paused
                    # Overlay pause menu, I roughly centered the text
                    font = pygame.font.Font(None, 80)
                    overlay = pygame.Surface(
                        SCREEN_DIMENSIONS, pygame.SRCALPHA)
                    overlay.fill((64, 64, 80, 128))
                    screen.blit(overlay, (0, 0))
                    screen.blit(font.render("PAUSED, PRESS P TO UNPAUSE",
                                True, (255, 255, 255)),
                                ((240), SCREEN_DIMENSIONS[1]//2))
                    pygame.display.flip()
                    clock.tick(FPS)  # limits FPS to FPS
        if paused:
            continue  # does the same of before but with less nesting

        pygame.event.get()
        process_input(event, stage, screen)
        # %% RENDERING
        #

        screen.fill("#16161D")

        for i in stage.board_state:
            for j in i:
                j.update(stage)
        for i in stage.packages:
            i.update(deltaTime, stage)

        Rengine.draw(screen, stage)
        Rengine.draw_packages(screen, stage)
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to FPS

    pygame.quit()


def process_input(event, stage, screen):
    """
    Processes the mouse events

    Parameters
    ----------
    event : pygame.Event
        the pygame event.
    stage : Level
        The current stage.
    screen : pygame.Surface
        currrent window.

    Returns
    -------
    None.

    """

    if event.type == pygame.MOUSEBUTTONDOWN \
            and pygame.mouse.get_pressed(3)[0]:  # MOUSE LEFT PRESS
        stage.mouse_initial = stage.convert_screen_to_grid(
            pygame.mouse.get_pos())
        stage.last_pressed = (True, False)

    elif pygame.mouse.get_pressed(3)[0]:  # MOUSE LEFT HOLD
        stage.process_left_mouse(pygame.mouse.get_pos(), screen.get_size())

    elif event.type == pygame.MOUSEBUTTONUP and \
            stage.last_pressed[0]:  # MOUSE LEFT RELEASE
        stage.mouse_final = stage.convert_screen_to_grid(
            pygame.mouse.get_pos())
        stage.create_conveyor()

    elif event.type == pygame.MOUSEBUTTONDOWN \
            and pygame.mouse.get_pressed(3)[2]:  # MOUSE RIGHT PRESS
        stage.mouse_initial = stage.convert_screen_to_grid(
            pygame.mouse.get_pos())
        stage.last_pressed = (False, True)

    elif pygame.mouse.get_pressed(3)[2]:  # MOUSE RIGHT HOLD
        stage.process_right_mouse(pygame.mouse.get_pos(), screen.get_size())

    elif event.type == pygame.MOUSEBUTTONUP and \
            stage.last_pressed[1]:  # MOUSE RIGHT RELEASE
        stage.mouse_final = stage.convert_screen_to_grid(
            pygame.mouse.get_pos())
        stage.remove_conveyor()


# Forces this file to only run when it is directly ran.
# This makes the file safe to import into other files.
if __name__ == '__main__':
    main()
    del SCREEN_DIMENSIONS
