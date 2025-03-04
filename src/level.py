# -*- coding: utf-8 -*-
import numpy as np
import pygame
import os


def _normalize(x: (float, float)):
    n = (x[0]**2 + x[1]**2)**(1/2)
    assert (n != 0)
    return (x[0]/n, x[1]/n)
# %% LEVEL


class Level:
    """
    The level the player will be attemping to solve

    Parameters
    ----------
    n : int, optional
        width. The default is 8.
    m : int, optional
        height. The default is 8.
    winCondition : array[ID], optional
        array of IDs used to check completion. The default is [].

    Returns
    -------
    None.

    """

    def __init__(self, n=8, m=8, winCondition=[""]):
        self.board_state = np.full(
            (n, m), Tiles.BaseTile(), dtype=Tiles.BaseTile)
        self.width = n  # Col
        self.height = m  # Row
        self.goal = winCondition
        self.goal_index = 0
        self.selection = []
        self.packages = []

        self.mouse_initial = (None, None)
        self.mouse_final = (None, None)

    def load_level_file(path):
        # TODO self descriptive and optional
        ""

    def process_mouse(self, current_position: (int, int),
                      screen_dimensions=(1280, 720)):
        """
        processes change in mouse position to find selected tiles.

        Parameters
        ----------
        current_position : (int, int)
            Current mouse position in screen space.
        screen_dimensions : (int, int), optional
            Size of the screen. The default is (1280, 720).

        Returns
        -------
        None.

        """
        grid_coordinates = self.convert_screen_to_grid(
            current_position, screen_dimensions)
        if (self.mouse_initial == (None, None)):
            return
        x = min(grid_coordinates[0], self.mouse_initial[0])
        y = max(grid_coordinates[0], self.mouse_initial[0])
        z = min(grid_coordinates[1], self.mouse_initial[1])
        w = max(grid_coordinates[1], self.mouse_initial[1])
        if y-x > w-z:
            out = [(i, self.mouse_initial[1]) for i in range(x, y+1)]
            if (self.mouse_initial[0] > grid_coordinates[0]):
                out.sort(reverse=True)
        else:  # x-y < z-w:
            out = [(self.mouse_initial[0], i) for i in range(z, w+1)]
            if (self.mouse_initial[1] > grid_coordinates[1]):
                out.sort(reverse=True)

        self.selection = out

    def convert_screen_to_grid(self, position: (int, int),
                               screen_dimensions=(1280, 720)):
        """
        Converts screen coordinates to grid coordinates

        Parameters
        ----------
        position : (int, int)
            position in screen coordinates.
        screen_dimensions : (int, int), optional
            The size of the screen. The default is (1280, 720).

        Returns
        -------
        x : float
            grid x-coordinate.
        y : float
            grid y-coordinate.

        """
        rect_width = min(((screen_dimensions[0]) / float(self.width+1)),
                         ((screen_dimensions[1]) / float(self.height+1)))
        left_adjust = float((screen_dimensions[0])/2) - \
            self.width/2*(rect_width+1)
        top_adjust = float(
            (screen_dimensions[1])/2) - self.height/2*(rect_width+1)

        x = int(np.floor((position[0]-left_adjust)/rect_width))
        y = int(np.floor((position[1]-top_adjust)/rect_width))
        return (x, y)

    def create_conveyor(self):
        """
        Creates a conveyor at all valid selected positions.

        Returns
        -------
        None.

        """
        if len(self.selection) <= 1:
            return
        for i in range(len(self.selection)-1):
            x = self.selection[i]
            if not ((x[0] < self.width and x[0] >= 0)
                    and (x[1] < self.width and x[1] >= 0)):
                continue
            if (self.board_state[x[0]][x[1]].type != Tiles.Type().NONE):
                continue
            self.board_state[x[0]][x[1]] = Tiles.ConveyorTile(
                self.selection[i], self.selection[i+1])

# %% packages
#


class Package:
    """
    The primary object being moved by the tiles

    Parameters
    ----------
    x : (float, float)
        Position of the package on the grid scale.
    ID : Any
        Given by the tile which created it
    size : (float, float), optional
        Size of the packge. The default is (0.8, 0.8).

    Returns
    -------
    None.

    """

    texture = pygame.image.load(os.path.join("../assets/", "box.png"))
    speed = 1.6

    def __init__(self, x: (float, float), ID, size=(0.8, 0.8)):

        self.position = (x[0] + (1-size[0])/2,
                         x[1] + (1-size[1])/2)
        self.ID = ID
        self.velocity = (0.0, 0.0)
        self.scale = size
        self.lifespan = 30*1000  # 10 seconds in measued in milisecond
        self.spawn_time = pygame.time.get_ticks()

    def update(self, delta_time: float, level: Level):
        """
        Updates the position of the package. This should be run once per frame

        Parameters
        ----------
        deltaTime : float
            The time between render frames.
        level : Level
            The current level in use.

        Returns
        -------
        None.

        """

        n = (self.velocity[0]**2 + self.velocity[1]**2)**(1/2)
        if (n != 0.0):  # Normalize velocity
            self.velocity = (self.velocity[0]/n * self.speed,
                             self.velocity[1]/n * self.speed)

        self.position = (self.position[0] + self.velocity[0] * delta_time,
                         self.position[1] + self.velocity[1] * delta_time)
        self.velocity = (0, 0)

        if (self.spawn_time + self.lifespan < pygame.time.get_ticks()):
            level.packages.remove(self)

    def is_collision(self, x: (float, float), size=(1, 1)):
        """
        Checks the collision between a package and axis aligned bounding box.

        Parameters
        ----------
        x : (float, float)
            Position of the opposing object's bounding box.
        size : (float, float), optional
            Size of the opposing bounding box. The default is (1, 1).

        Returns
        -------
        bool
            DESCRIPTION.

        """
        xScale = self.scale[0]
        xPos = self.position[0]

        yScale = self.scale[1]
        yPos = self.position[1]
        xAxis = (((xPos + xScale) >= x[0] and
                  (x[0] + size[0]) >= xPos))
        yAxis = (((yPos + yScale) >= x[1] and
                  (x[1] + size[1]) >= yPos))
        return xAxis and yAxis

    def resolve_direction(self, target: (float, float), size=(1.0, 1.0)):
        """
        Returns the best fit for the resolve direction of an axis aligned
        bounding box collision.

        Parameters
        ----------
        target : (float, float)
            The position of the opposing object on the grid scale
        size : (float, float), optional
            Dimensions of the bounding box of the opposing object.
            The default is (1.0, 1.0).

        Returns
        -------
        best_match : int
            0 -> up,
            1 -> right,
            2 -> down,
            3 -> left,
            4 -> unknown

        """
        sX, sY = size[0], size[1]
        compass = [
            (0.0/sX,  1.0/sY),  # up
            (1.0/sX,  0.0/sY),  # right
            (0.0/sX, -1.0/sY),  # down
            (-1.0/sX, 0.0/sY),  # left
            (0, 0)  # none
        ]
        _max = 0.0
        best_match = 4
        for i in range(len(compass)):
            dot_product = np.dot(_normalize(target), compass[i])
            if (dot_product > _max):
                _max = dot_product
                best_match = i

        return best_match


# %% TILES


class Tiles:
    def convert_tile_images(screen: pygame.Surface):
        """
        Converts all used textures into an optimal format for use in pygame.

        Parameters
        ----------
        screen : pygame.Surface
            Target frame buffer image

        Returns
        -------
        None.

        """
        Tiles.ConveyorTile.texture.convert(screen)
        Tiles.ReceiverTile.texture.convert(screen)
        Tiles.WallTile.texture.convert(screen)
        Tiles.GeneratorTile.texture.convert(screen)
        # packages too
        Package.texture.convert(screen)

    class Type():
        NONE = 0
        WALL = 1
        CONVEYOR = 2
        RECEIVER = 3
        GENERATOR = 4

    class BaseTile:
        """
        Base class for all game tiles.

        """

        def __init__(self):
            self.position = (0, 0)
            self.type = Tiles.Type.NONE

        def update(self, level: Level):
            pass

    class ConveyorTile(BaseTile):
        """
        Moves a package towards a destination.

        Parameters
        ----------
        x : (int, int)
            position of the tile on the grid.
        z : (int, int)
            the conveyor destination.
        """
        texture = pygame.image.load(os.path.join("../assets/", "conveyor.png"))

        def __init__(self, x: (int, int), z: (int, int)):
            self.position = x
            self.type = Tiles.Type.CONVEYOR
            self.direction = z

        def update(self, level: Level):
            for i in level.packages:
                if i.is_collision(self.position):
                    xVel = self.direction[0]-self.position[0]
                    yVel = self.direction[1]-self.position[1]
                    # Move the boxes towards the center along the axis
                    # parallel to movement
                    xVel += abs(yVel) * \
                        (self.position[0]-i.position[0] + (1-i.scale[0])/2)
                    yVel += abs(xVel) * \
                        (self.position[1]-i.position[1] + (1-i.scale[1])/2)

                    i.velocity = ((i.velocity[0] +
                                   xVel),
                                  (i.velocity[1] +
                                   yVel))

    class WallTile(BaseTile):
        """
        A Non-overwriteable tile which blocks the movement of a package

        Parameters
        ----------
        x : (int, int)
            position of the tile on the grid.
        """
        texture = pygame.image.load(os.path.join("../assets/", "wall.png"))

        def __init__(self, x: (int, int)):
            self.position = x
            self.type = Tiles.Type.WALL

        def update(self, level: Level):
            for i in level.packages:
                if not i.is_collision(self.position):
                    continue
                pos = (i.position[0]-self.position[0],
                       i.position[1]-self.position[1])
                match  i.resolve_direction(pos):
                    case 0:
                        y = self.position[1] + 1
                        i.position = (i.position[0], y)
                    case 1:
                        x = self.position[0] + 1
                        i.position = (x, i.position[1])
                    case 2:
                        y = self.position[1] - i.scale[1]
                        i.position = (i.position[0], y)
                    case 3:
                        x = self.position[0] - i.scale[0]
                        i.position = (x, i.position[1])
                    case 4:
                        pass

    class GeneratorTile(BaseTile):

        """
        Generates a package every n-seconds.

        Parameters
        ----------
        x : (int, int)
            position of the tile on the grid.
        y : (int, int)
            destination of packages out of the generator.
        ID : Any
            a unique ID used to track packages.
        cycle : float
            Time between the generation of a package.
        """
        class Colour_ID():
            RED = 'r'
            ORANGE = 'o'
            GREEN = 'g'
            BLUE = 'b'
            PURPLE = 'p'

            def ID_to_Colour(ID: str):
                match ID:
                    case Tiles.GeneratorTile.Colour_ID.RED:
                        return "#eb3449"
                    case Tiles.GeneratorTile.Colour_ID.ORANGE:
                        return "#d97700"
                    case Tiles.GeneratorTile.Colour_ID.GREEN:
                        return "#27db78"
                    case Tiles.GeneratorTile.Colour_ID.BLUE:
                        return "#279cdb"
                    case Tiles.GeneratorTile.Colour_ID.PURPLE:
                        return "#c927db"

        texture = pygame.image.load(
            os.path.join("../assets/", "generator.png"))

        def __init__(self, x: (int, int), y: (int, int), ID, cycle=5.0):

            self.position = x
            self.output = y
            self.ID = ID
            self.type = Tiles.Type.GENERATOR
            self.cycle_time = cycle * 1000.0
            self.time_old = pygame.time.get_ticks()

        def update(self, level: Level):
            if pygame.time.get_ticks() >= self.time_old + self.cycle_time:
                # TODO play animation
                level.packages.append(Package(self.output, self.ID))
                self.time_old = pygame.time.get_ticks()

    class ReceiverTile(BaseTile):
        """
        The tile that collects all packages and progresses the player to
        the win condition.

        Parameters
        ----------
        x : (int, int)
            Position of the tile.
        """
        texture = pygame.image.load(os.path.join("../assets/", "receiver.png"))

        def __init__(self, x: (int, int)):
            self.position = x
            self.type = Tiles.Type.RECEIVER

        def update(self, level: Level):
            for o in level.packages:
                if o.is_collision(self.position):
                    if (level.goal_index < len(level.goal)) and \
                            o.ID == level.goal[level.goal_index]:
                        level.goal_index += 1
                    else:
                        level.goal_index = 0
                    # Remove the Package
                    level.packages.remove(o)
