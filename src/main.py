import pygame
from level import Level, WallTile, GeneratorTile, ConveyorTile, ReceiverTile, Object
from render import Rengine

# %%  TODO
# - Conveyor placement bug:
#       Dragging upwards or left leaves the conveyers placed 1 tile behind
#       where they should be.
# - Generator Objects
# - Pause Menu
# - Start Menu
# - Level loading
# - Textures (probably max of 64x64)
# - Colour scheme
# - PEP8 standard


def main():
    # %% SETUP
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    stage = Level(8, 8)
    # TEST
    # This should not remain in the code after testing and serves no purpose
    # other than making sure things work. Feel free to experiment with it to
    # understand this mess.
    stage.board_state[2, 2] = WallTile((2, 2))
    stage.board_state[4, 2] = GeneratorTile((4, 2), (1, 1), 'test')
    stage.board_state[6, 5] = ConveyorTile((6, 5), (6, 4))
    stage.board_state[2, 1] = ReceiverTile((2, 1))
    stage.objects.append(Object((1, 5), 1))
    # try:
    # %% GAMELOOP
    FPS = 60
    while running:
        deltaTime = clock.tick(FPS)/1000  # fast divide by 1024

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and pygame.mouse.get_pressed(3)[0]:
                stage.mouseInitial = stage.convertScreenToGrid(
                    pygame.mouse.get_pos())
        if pygame.mouse.get_pressed(3)[0]:
            stage.processMouse(pygame.mouse.get_pos(), screen.get_size())
        screen.fill("#16161D")

        for i in stage.board_state:
            for j in i:
                j.update(stage)
        for i in stage.objects:
            i.update(deltaTime)
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
