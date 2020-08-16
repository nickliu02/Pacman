from pygame import *


class Player:
    def __init__(self, x, y, mv):
        self.x = x  # x position
        self.y = y  # y position
        self.mv = mv  # Last move
        self.vx = 0  # x velocity
        self.vy = 0  # y velocity
        self.pos = (int((self.x+12) / 24), int((self.y+12) / 24))  # position on grid
        self.frame = [1, 0]  # Sprite frame
        self.oldDir = "left"  # Direction moving
        self.score = 0
        self.lives = 3
        self.rect = Rect(self.x, self.y, 24, 24)
        self.num_eaten = 0  # Number of ghosts eaten in a single energizer session
        self.displayNum = [False, False, False, False]  # List of which consumed ghost scores to display
        self.numTime = [0, 0, 0, 0]  # Times of the consumed ghost scores
        self.displayLocation = [None, None, None, None]  # Locations for the scores to be blitted
        self.fruit_eaten = False  # If fruit has been eaten
        self.fruit_time = 0  # Time for score of eaten fruit to be displayed

    def move(self, board, nodes, speed):
        """
        Moves the player based on user input. Sets the velocity based on what direction is pressed and whether or not
        the player can be moved. If a direction is pressed that cannot be executed, it is queued and executed when
        possible.
        """

        self.pos = (int((self.x + 12) / 24), int((self.y + 12) / 24))  # Calculating position

        # Dealing with the looping part by ensuring player stays within boundaries
        if self.x >= 660:
            self.pos = (27, 17)
        elif self.x <= 0:
            self.pos = (0, 17)

        # Teleporting player from right tunnel to left and vice versa
        if self.pos == (27, 17) and self.x >= 684 and self.vx > 0:
            self.x = -24
            self.pos = (0, 17)
            return
        elif self.pos == (0, 17) and self.x <= -24 and self.vx < 0:
            self.x = 684
            self.pos = (27, 17)
            return

        # Player is on node
        if self.pos in nodes:
            # Adjacent cells
            top = board[self.pos[0]][self.pos[1] - 1]
            bottom = board[self.pos[0]][self.pos[1] + 1]
            left = board[self.pos[0] - 1][self.pos[1]]
            right = board[self.pos[0] + 1][self.pos[1]]

            # Player is exactly on node and can turn (same pixel occupied)
            if (self.x, self.y) == (self.pos[0] * 24, self.pos[1] * 24):
                # Check if player is blocked at node
                if self.vy < 0 and top:
                    pass
                elif self.vy > 0 and bottom:
                    pass
                elif self.vx < 0 and left:
                    pass
                elif self.vx > 0 and right:
                    pass
                # If player is blocked stop all movement
                else:
                    self.vx = 0
                    self.vy = 0

                # If an action is made, execute it if possible
                if top and self.mv == "w":
                    self.vx = 0
                    self.vy = -speed
                    self.mv = ""
                elif bottom and self.mv == "s":
                    self.vx = 0
                    self.vy = speed
                    self.mv = ""
                elif left and self.mv == "a":
                    self.vx = -speed
                    self.vy = 0
                    self.mv = ""
                elif right and self.mv == "d":
                    self.vx = speed
                    self.vy = 0
                    self.mv = ""

            # Player is on node but cannot turn yet
            else:
                if self.vy > 0 and self.mv == "w":
                    self.vx = 0
                    self.vy = -speed
                elif self.vy < 0 and self.mv == "s":
                    self.vx = 0
                    self.vy = speed
                elif self.vx > 0 and self.mv == "a":
                    self.vx = -speed
                    self.vy = 0
                elif self.vx < 0 and self.mv == "d":
                    self.vx = speed
                    self.vy = 0

        # Going up or down on vertical corridor
        if board[self.pos[0]][self.pos[1]] == 2:
            if self.mv == "w":
                self.vx = 0
                self.vy = -speed
                self.mv = ""
            elif self.mv == "s":
                self.vx = 0
                self.vy = speed
                self.mv = ""

        # Going left or right on horizontal corridor
        elif board[self.pos[0]][self.pos[1]] == 1:
            if self.mv == "a":
                self.vx = -speed
                self.vy = 0
                self.mv = ""
            elif self.mv == "d":
                self.vx = speed
                self.vy = 0
                self.mv = ""

        # Update the position
        self.x += self.vx
        self.y += self.vy
        self.rect = Rect(self.x, self.y, 24, 24)

    def update_frame(self):
        """
        Determines what direction the player is moving and updates the sprite to represent the direction.
        """
        if self.vx > 0:
            if self.oldDir == "right":
                self.frame[1] = (self.frame[1]+0.2) % 2  # Cycle between sprites if player is continuing a directon
            else:
                # Starts with first frame if direction had just been changed
                self.frame[0] = 2
                self.frame[1] = 0

            self.oldDir = "right"

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




