import pygame
from level import Level, Tiles, WallTile, GeneratorTile, ConveyorTile, ReceiverTile, Object
from level import convertTileImages
from render import Rengine
import numpy as np
# %%  TODO
# - Bug: Clicks not always registered
# - Add conveyer belt removal
# - ✔️ Pause Menu
# - Start Menu
# - Level loading
# - Colour scheme
# - PEP8 standard
SCREEN_DIMENSIONS = (1280, 720)


def main():
    # %% SETUP
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
    clock = pygame.time.Clock()
    running = True
    paused = False
    stage = Level(8, 8)
    convertTileImages(screen)

    # TEST
    # This should not remain in the code after testing and serves no purpose
    # other than making sure things work. Feel free to experiment with it to
    # understand this mess.
    stage.boardState[2, 2] = WallTile((2, 2))
    stage.boardState[2, 3] = WallTile((2, 3))
    stage.boardState[2, 4] = WallTile((2, 4))

    stage.boardState[4, 2] = GeneratorTile((4, 2), (4, 3), 'test')
    stage.boardState[6, 5] = ConveyorTile((6, 5), (6, 4))
    stage.boardState[2, 1] = ReceiverTile((2, 1))
    stage.objects.append(Object((1, 5), 1))
    # try:

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
                if event.key == pygame.K_r:  # Testing reset key, del later
                    stage.boardState = np.full((8, 8), Tiles(), dtype=Tiles)
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
        if event.type == pygame.MOUSEBUTTONDOWN \
                and pygame.mouse.get_pressed(3)[0]:
            stage.mouseInitial = stage.convertScreenToGrid(
                pygame.mouse.get_pos())
        elif pygame.mouse.get_pressed(3)[0]:
            stage.processMouse(pygame.mouse.get_pos(), screen.get_size())
        elif event.type == pygame.MOUSEBUTTONUP and \
                not pygame.mouse.get_pressed(3)[0]:
            stage.mouseFinal = stage.convertScreenToGrid(
                pygame.mouse.get_pos())
            stage.createConveyor()
        # %% RENDERING
        #

        screen.fill("#16161D")

        for i in stage.boardState:
            for j in i:
                j.update(stage)
        for i in stage.objects:
            i.update(deltaTime, stage)
        Rengine.draw(screen, stage)
        Rengine.drawObjects(screen, stage)
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to FPS
    # except Exception as e:
    #     print(e)
    pygame.quit()


# Forces this file to only run when it is directly ran.
# This makes the file safe to import into other files.
if __name__ == '__main__':
    main()
    del SCREEN_DIMENSIONS
