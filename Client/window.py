"""
  $ pip install pygame
  $ python window.py
  Player 1: circle, Player 2: fork
  click some space on the board, and close it
  the terminal would print the board
"""
import pygame, sys
import numpy as np

pygame.init()
WIDTH, HEIGHT = 600, 600
RED = (255, 0, 0)
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

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # set the window
pygame.display.set_caption("Tic Tac Toe Game")    # set title
screen.fill(BG_COLOR)                             # set color

# build grid
def draw_lines():
    # draw two horizontal lines
    # (screen, color, start, end, width)
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    # draw two vertical lines
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)

draw_lines()

# build board
board = np.zeros((BOARD_ROWS, BOARD_COLS))
def mark_square(row, col, player):
    board[row][col] = player

# test
# mark_square(0, 0, 1)
# mark_square(1, 1, 2)

# check if the board[r][c] is empty
def checkBoardEmpty(r, c):
    return board[r][c] == 0

# check if the board is full
def checkBoardFull():
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] == 0:
                return False
    return True

# draw player on screen
def draw_player():
    for r in range(BOARD_COLS):
        for c in range(BOARD_COLS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(c * 200 + 100), int(r * 200 + 100)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[r][c] == 2:
                # draw line from (0, 200) -> (200, 0)
                pygame.draw.line(screen, CROSS_COLOR, (c * 200 + SHIFT, r * 200 + 200 - SHIFT), (c * 200 + 200 - SHIFT, r * 200 + SHIFT), CROSS_WIDTH)
                # draw line from (0, 0) -> (200, 200)
                pygame.draw.line(screen, CROSS_COLOR, (c * 200 + SHIFT, r * 200 +SHIFT), (c * 200 + 200 - SHIFT, r * 200 + 200 - SHIFT), CROSS_WIDTH)

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

            if checkBoardEmpty(clicked_row, clicked_col):
                if player == 1:
                    mark_square(clicked_row, clicked_col, 1)
                    player = 2
                elif player == 2:
                    mark_square(clicked_row, clicked_col, 2)
                    player = 1

                draw_player()

                print(board)

    # update the screen
    pygame.display.update()

