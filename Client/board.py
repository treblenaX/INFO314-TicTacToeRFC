"""
  $ pip install pygame
  $ python window.py
  Player 1: circle, Player 2: fork
  click some space on the board, and close it
  the terminal would print the board
"""
import pygame, sys
import numpy as np

WIDTH, HEIGHT = 600, 600
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3

CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CIRCLE_COLOR = (239, 231, 200)

CROSS_COLOR = (66, 66, 66)
CROSS_WIDTH = 25
SHIFT = 55

class Board():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # set the window
        pygame.display.set_caption("Tic Tac Toe Game")    # set title
        self.screen.fill(BG_COLOR)                             # set color
        self.draw_lines()

        # build board
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))

        player = 1

        # start the window of game
        while True:
            for event in pygame.event.get():
                # check if the user close the window
                if event.type == pygame.QUIT:
                    sys.exit()

                # check if the user clicks the screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX = event.pos[0] # x
                    mouseY = event.pos[1] # y

                    # match board to screen
                    clicked_row = int(mouseY // 200)
                    clicked_col = int(mouseX // 200)
                    # print(clicked_row, clicked_col)

                    if self.checkBoardEmpty(clicked_row, clicked_col):
                        if player == 1:
                            self.mark_square(clicked_row, clicked_col, 1)
                            player = 2
                        elif player == 2:
                            self.mark_square(clicked_row, clicked_col, 2)
                            player = 1

                        self.draw_player()

                        print(self.board)

            # update the screen
            pygame.display.update()


    # build grid
    def draw_lines(self):
        # draw two horizontal lines
        # (screen, color, start, end, width)
        pygame.draw.line(self.screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
        # draw two vertical lines
        pygame.draw.line(self.screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)


    def mark_square(self, row, col, player):
        self.board[row][col] = player

# test
# mark_square(0, 0, 1)
# mark_square(1, 1, 2)

    # check if the board[r][c] is empty
    def checkBoardEmpty(self, r, c):
        return self.board[r][c] == 0

    # check if the board is full
    def checkBoardFull(self):
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if self.board[r][c] == 0:
                    return False
        return True

    # draw player on screen
    def draw_player(self):
        for r in range(BOARD_COLS):
            for c in range(BOARD_COLS):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, CIRCLE_COLOR, (int(c * 200 + 100), int(r * 200 + 100)), CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.board[r][c] == 2:
                    # draw line from (0, 200) -> (200, 0)
                    pygame.draw.line(self.screen, CROSS_COLOR, (c * 200 + SHIFT, r * 200 + 200 - SHIFT), (c * 200 + 200 - SHIFT, r * 200 + SHIFT), CROSS_WIDTH)
                    # draw line from (0, 0) -> (200, 200)
                    pygame.draw.line(self.screen, CROSS_COLOR, (c * 200 + SHIFT, r * 200 +SHIFT), (c * 200 + 200 - SHIFT, r * 200 + 200 - SHIFT), CROSS_WIDTH)


if __name__ == "__main__":
    Board()