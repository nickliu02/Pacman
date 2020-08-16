from pygame import *
import glob


def row_into_col(lst):
    """
    Takes in a 2D list and changes it so that the rows become columns and columns become rows
    """
    return [[lst[j][i] for j in range(len(lst))] for i in range(len(lst[0]))]


class Board:
    def __init__(self, board):
        self.board = board
        self.nodes = [(i, j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] == 3]

        # Location of pellets
        self.pellets = row_into_col([[int(i) for i in line.split()] for line in open("Assets/pellets.txt")])

        # Pellet hitboxes
        self.pelletBoxes = [[Rect(i*24 + 10, j*24 + 10, 4, 4) if self.pellets[i][j] else None
                                          for j in range(len(board[i]))] for i in range(len(board))]
        self.state = "chase"  # Board state
        self.level = 1
        self.fruits = [image.load(i) for i in sorted(glob.glob("Assets/Fruit*.png"))]
        self.points = [100, 300, 500, 700, 1000, 2000, 3000, 5000]  # Points for corresponding fruits
        self.mode = ""  # Game mode
        self.consumed_pellets = 0

    def check_collision(self, rect, pos):
        """
        Check collision between player and board and return type of pellet collided with. 1 = small and 2 = large pellet
        """
        if self.pellets[pos[0]][pos[1]] and rect.colliderect(self.pelletBoxes[pos[0]][pos[1]]):
            a = 0
            if self.pellets[pos[0]][pos[1]] == 1:
                a = 1
            elif self.pellets[pos[0]][pos[1]] == 2:
                a = 2
            self.pellets[pos[0]][pos[1]] = 0
            self.pelletBoxes[pos[0]][pos[1]] = None
            return a
        return 0

    def count_pellets(self):
        """
        Count number of pellets remaining on the board by cycling through all cells in the list
        """
        count = 0
        for i in range(len(self.pellets)):
            for j in range(len(self.pellets[i])):
                if self.pellets[i][j]:
                    count += 1

        return count  # Number of pellets remaining

