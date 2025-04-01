# %%
import pygame
import time

from level import Tiles, Level
from render import Rengine

SCREEN_DIMENSIONS = (1280, 720)
FPS = 60


def pregame_screen(screen):
    font = pygame.font.SysFont("courier", 32, bold=True)
    text_color = (255, 255, 255)  # max light
    margin = 40
    line_spacing = 10
    word_delay = 0.2

    infile = open("../assets/pregametext.txt", "r")   # open to read
    full_text = infile.read()

    # Process the text (remove extra whitespace and split into words)
    words = ' '.join(full_text.split()).split(' ')

    last_word_time = time.time()
    clock = pygame.time.Clock()
    current_words = []
    word_index = 0

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True

        # Add words with delay
        if word_index < len(words) and \
                time.time() - last_word_time > word_delay:
            current_words.append(words[word_index])
            word_index += 1
            last_word_time = time.time()

        screen.fill("black")

        # Word wrapping test and logic
        lines = []
        current_line = ""
        for word in current_words:
            test_line = f"{current_line} {word}" if current_line else word
            if font.size(test_line)[0] < SCREEN_DIMENSIONS[0] - 2*margin:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Wrap text starting from top
        y_pos = margin
        for line in lines:
            text_surface = font.render(line, True, text_color)
            screen.blit(text_surface, (margin, y_pos))
            y_pos += font.get_height() + line_spacing  # move down

        pygame.display.flip()
        clock.tick(FPS)


def main():
    # %% SETUP
    pygame.init()
    screen = pygame.display.set_mode(
        SCREEN_DIMENSIONS, pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()

    # Show pregame screen
    if not pregame_screen(screen):
        pygame.quit()
        return

    running = True
    paused = False
    Tiles.convert_tile_images(screen)
    level_queue = ["../assets/1.lvl", "../assets/2.lvl", "../assets/3.lvl"]
    level_select = 0
    stage = Level.load_level_file("../assets/1.lvl")  # Load the first level

    # %% GAMELOOP
    while running:
        deltaTime = clock.tick(FPS)/1000

        # %% KEY POLLING
        #
        # pygame.QUIT event means the user clicked X to close your window

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    # Quitting should work when paused
                running = False
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused
                display_pause_screen(screen)

            # Process input for each event
            if not paused:
                process_input(event, stage, screen)

        if paused:
            continue  # does the same of before but with less nesting

        # %% RENDERING
        #

        screen.fill("#16161D")

        if stage.goal_index >= len(stage.goal):
            # Display win screen
            # Load next level
            level_select += 1
            if (level_select > len(level_queue)):
                break  # Out of levels.
            stage = Level.load_level_file(level_queue[level_select])
            continue

        stage.update(deltaTime)

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


def display_pause_screen(screen):
    # Overlay pause menu, I roughly centered the text
    font = pygame.font.Font(None, 80)
    overlay = pygame.Surface(
        SCREEN_DIMENSIONS, pygame.SRCALPHA)
    overlay.fill((64, 64, 80, 128))
    screen.blit(overlay, (0, 0))
    screen.blit(font.render("PAUSED, PRESS ESC TO UNPAUSE",
                True, (255, 255, 255)),
                ((240), SCREEN_DIMENSIONS[1]//2))
    pygame.display.flip()


# Forces this file to only run when it is directly ran.
# This makes the file safe to import into other files.
if __name__ == '__main__':
    main()
    del SCREEN_DIMENSIONS, FPS
