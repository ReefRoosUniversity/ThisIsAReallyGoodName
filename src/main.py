import pygame
from level import Level, WallTile, GeneratorTile, ConveyorTile, ReceiverTile
from render import Rengine


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
    stage.board_state[6, 5] = ConveyorTile((6, 5), (1, 1))
    stage.board_state[2, 1] = ReceiverTile((2, 1))

    try:
        # %% GAMELOOP
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill("#16161D")
            Rengine.draw(screen, stage)

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60
    except Exception as e:
        print(e)
    pygame.quit()


# Forces this file to only run when it is directly ran.
# This makes the file safe to import into other files.
if __name__ == '__main__':
    main()
