# Ghost
from a_star import a_star
import random
from pygame import *


def nearest(pos, board):
    """
    Finds the nearest valid cell (directly vertically or horizontally) and returns it. Works by looking at the 4
    adjacent cells and checking if they are valid, adding any possible ones into a list and choosing one randomly.
    """

    a, b = pos
    i = 0  # Number of cells away from target
    possible = []  # Possibilities for the nearest cell
    while True:
        added = False
        if a + i <= 27 and board[a+i][b]:  # Right
            possible.append((a+i, b))
            added = True
        if a - i > 0 and board[a-i][b]:  # Left
            possible.append((a-i, b))
            added = True
        if b + i <= 35 and board[a][b+i]:  # Top
            possible.append((a, b+i))
            added = True
        if b - i > 0 and board[a][b-i]:  # Bottom
            possible.append((a, b-i))
            added = True
        if added:
            break
        else:  # If not valid tile is found increment i
            i += 1

    return random.choice(possible)  # Choose a random cell based on all of the possible nearest ones


class Ghost:
    def __init__(self, x, y, corner, sprites, state):
        self.x = x  # x position
        self.y = y  # y position
        self.vx = 0  # x velocity
        self.vy = 0  # y velocity
        self.pos = (int((self.x+12) / 24), int((self.y+12) / 24))  # Position on board
        self.oldDir = "left"  # Direction moving
        self.frame = [1, 0]  # Frame of sprite
        self.sprites = sprites
        self.corner = corner  # Target corner in corner mode
        self.state = state
        self.rect = Rect(x, y, 24, 24)
        self.eaten = False  # If ghost has been eaten or not
        self.speed = 4

    def move(self):
        self.rect = Rect(self.x, self.y, 24, 24)

        if (self.state == "chase" or self.state == "retreat") and (self.x % 4 == 0 and self.y % 4 == 0):
            self.speed = 4
            if abs(self.vx) == 2:
                self.vx *= 2
            if abs(self.vy) == 2:
                self.vy *= 2

        elif self.state == "scatter":
            self.speed = 2
            if abs(self.vx) == 4:
                self.vx /= 2
            if abs(self.vy) == 4:
                self.vy /= 2

        # Update position
        self.x += self.vx
        self.y += self.vy
        self.pos = (int((self.x+12) / 24), int((self.y+12) / 24))

        # Dealing with the looping part. If player goes into left tunnel they come out of the right one and vice versa
        # Keeping coordinates and position in boundary
        if self.x >= 660:
            self.pos = (27, 17)
        elif self.x <= 0:
            self.pos = (0, 17)
        # Teleport player if they reach the area off screen
        if self.pos == (27, 17) and self.x >= 684 and self.vx > 0:
            self.x = -24
            self.pos = (0, 17)
            return
        elif self.pos == (0, 17) and self.x <= -24 and self.vx < 0:
            self.x = 684
            self.pos = (27, 17)
            return

    def update_frame(self):
        """
        Determines what direction the ghost is moving and updates the sprite to represent the direction. Cycles between
        the two sprites as it moves.
        """

        if self.vx > 0:
            if self.oldDir == "right":
                # Toggles between the frames as it moves if it is heading the same direction as before
                self.frame[1] = (self.frame[1]+0.2) % 2
            else:
                # If direction was changed, start on the first frame
                self.frame[0] = 2
                self.frame[1] = 0

            self.oldDir = "right"  # Setting direction

        elif self.vx < 0:
            if self.oldDir == "left":
                self.frame[1] = (self.frame[1]+0.2) % 2
            else:
                self.frame[0] = 1
                self.frame[1] = 0

            self.oldDir = "left"

        elif self.vy > 0:
            if self.oldDir == "down":
                self.frame[1] = (self.frame[1]+0.2) % 2
            else:
                self.frame[0] = 0
                self.frame[1] = 0

            self.oldDir = "down"

        elif self.vy < 0:
            if self.oldDir == "up":
                self.frame[1] = (self.frame[1]+0.2) % 2
            else:
                self.frame[0] = 3
                self.frame[1] = 0

            self.oldDir = "up"

    def get_path(self, g, player_pos):
        """
        Takes the board and the player position as input and returns the path required to get to that position.
        """
        grid = [[g[i][j] for j in range(len(g[0]))] for i in range(len(g))]  # Copy of board

        if self.pos == player_pos and self.pos != (14, 14):  # If the ghost is on target tile force it to target middle
            return self.get_path(grid, (14, 14))

        # Places a "wall" directly behind the ghost for the path calculations, because ghosts are not allowed to reverse
        # directions.
        if self.pos != (0, 17) and self.pos != (27, 17):
            if self.vx > 0:  # Right
                grid[self.pos[0]-1][self.pos[1]] = 0
            elif self.vx < 0:  # Left
                grid[self.pos[0]+1][self.pos[1]] = 0
            elif self.vy > 0:  # Down
                grid[self.pos[0]][self.pos[1]-1] = 0
            elif self.vy < 0:  # Up
                grid[self.pos[0]][self.pos[1]+1] = 0

            # Returning path from a* algorithm
            if a_star(grid, self.pos, player_pos) is not None:
                return a_star(grid, self.pos, player_pos)
            else:
                # If there is no valid path, it finds a close enough path that may not be the most accurate
                return a_star(grid, self.pos, (nearest(player_pos, grid)))

    def chase(self, path):
        """
        Based on the path, sets the velocity of the ghost to follow the path.
        """

        if path is None:
            return

        if self.pos in path:  # If the ghost has reached a cell in its path, the cell is popped
            path.pop(0)

        if len(path) < 1:  # Return if ghost has reached target cell
            return

        # Reset velocities
        self.vx = 0
        self.vy = 0

        # Change velocity based on relative position of ghost to next cell in path
        if self.pos[1] < path[0][1]:  # Right
            self.vy = self.speed
        elif self.pos[1] > path[0][1]:  # Left
            self.vy = -self.speed
        elif self.pos[0] > path[0][0]:  # Up
            self.vx = -self.speed
        elif self.pos[0] < path[0][0]:  # Down
            self.vx = self.speed

    def scatter(self, board):
        """
        In scatter mode, all ghosts move randomly. Whenever the ghost reaches a node, it looks at the 3 adjacent cells
        to the node (the one the ghost came from is removed) and selects one at random.
        """

        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Possible directions
        if self.oldDir == "up":
            dirs.remove((0, 1))
        elif self.oldDir == "down":
            dirs.remove((0, -1))
        elif self.oldDir == "right":
            dirs.remove((-1, 0))
        elif self.oldDir == "left":
            dirs.remove((1, 0))
        possible = [(self.pos[0] + i[0], self.pos[1] + i[1]) for i in dirs
                    if board[self.pos[0] + i[0]][self.pos[1] + i[1]]]

        self.chase([random.choice(possible)])  # Chase a the selected tile

    def inactive(self):
        """
        Moves the ghost up and down within the middle box if the ghost is inacitve.
        """
        if self.y == 384:
            self.vy = 2
        elif self.y == 432:
            self.vy = -2

    def enter(self, state):
        """
        When the ghost enters the field, it first is moved to the middle (x=324), then is moved up and out of the box.
        """
        # Resetting velocity
        self.vx = 0
        self.vy = 0

        # Changing the vx to reach the middle
        if self.x < 324:
            self.vx = 2
        elif self.x > 324:
            self.vx = -2

        # Changing the vy to reach the outside once in the middle
        if self.x == 324:
            if self.y == 336:  # Once the ghost exist the correct state is chosen
                if state == "scatter" and not self.eaten:
                    self.state = "scatter"
                else:
                    self.state = "chase"
                return True  # Indicates ghost is done exiting
            else:
                self.vy = -2
        return False

    def retreat(self):
        """
        If the ghost is in the correct position, it enters the box. Once it reaches the end of the box it swiches
        direction and comes out.
        """
        self.vx = 0
        self.vy = 0
        if self.y == 432:
            self.vy = -2
        else:
            self.vy = 2


class Blinky(Ghost):
    def __init__(self, x, y, corner, sprites, state):
        Ghost.__init__(self, x, y, corner, sprites, state)


class Clyde(Ghost):
    def __init__(self, x, y, corner, sprites, state):
        Ghost.__init__(self, x, y, corner, sprites, state)
        self.close = False  # If ghost is within 8 tiles of player

    def is_close(self, player_pos):
        # Checks if ghost is within 8 tiles of the player position using pythagorean theorem
        return ((self.pos[0] - player_pos[0])**2 + (self.pos[0] - player_pos[0])**2)**0.5 <= 8


class Inky(Ghost):
    def __init__(self, x, y, corner, sprites, state):
        Ghost.__init__(self, x, y, corner, sprites, state)

    def get_target(self, player_pos, direction):
        """
        Gets target based on player position. The target is double the vector between two tiles in front of the player
        and Blinky.
        """

        # Getting tile that is 2 tiles in front of player
        if direction == "left":
            i = player_pos[0] - 2 - self.pos[0]
            j = player_pos[1] - self.pos[1]

        elif direction == "right":
            i = player_pos[0] + 2 - self.pos[0]
            j = player_pos[1] - self.pos[1]

        elif direction == "up":
            i = player_pos[0] - self.pos[0]
            j = player_pos[1] - 2 - self.pos[1]

        elif direction == "down":
            i = player_pos[0] - self.pos[0]
            j = player_pos[1] + 2 - self.pos[1]

        a, b = self.pos[0] + 2*i, self.pos[1] + 2*j  # Doubling the vector

        # Ensuring position is within the boundaries
        if a < 1:
            a = 1
        elif a > 26:
            a = 26

        if b < 4:
            b = 4
        elif b > 32:
            b = 32

        return a, b  # Returning the two positional values


class Pinky(Ghost):
    def __init__(self, x, y, corner, sprites, state):
        Ghost.__init__(self, x, y, corner, sprites, state)

    def get_target(self, player_pos, direction):
        """
        Gets the target for pinky, which is the tile 4 units in front of the player.
        """
        if direction == "left":
            i = player_pos[0] - 4
            if i < 1:  # Making sure it is in boundary
                i = 1
            j = player_pos[1]

        elif direction == "right":
            i = player_pos[0] + 4
            if i > 26:  # Making sure it is in boundary
                i = 26
            j = player_pos[1]

        elif direction == "up":
            i = player_pos[0]
            j = player_pos[1] - 4
            if j < 4:  # Making sure it is in boundary
                j = 4

        elif direction == "down":
            i = player_pos[0]
            j = player_pos[1]
            if j > 32:  # Making sure it is in boundary
                j = 32

        return i, j  # i is horizontal position, j is vertical position

