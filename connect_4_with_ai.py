import numpy
import pygame
import sys
import math
import random

# setup of connect 4 matrix
COL_COUNT = 7
ROW_COUNT = 6
PLAYER_1_PIECE = 1
PLAYER_2_PIECE = 2

# players
PLAYER = 0
AI = 1

# connect 4 board set up
BLUE = (0, 0, 225)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# functions
def create_board():
    # matrix to represent board
    board = numpy.zeros((ROW_COUNT, COL_COUNT))
    return board


def drop_piece(board, row, col, piece):
    # 0 - empty space, 1 - player 1 piece, 2 - player2 piece
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def increment_turn(increment):
    global turn
    turn += increment
    turn = turn % 2


def change_board_orientation(board):
    print(numpy.flip(board, 0))


def winning_move(board, piece):
    # check row for 4 in a row: horizontal
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check row for 4 in a row: vertical
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # check row for 4 in a row: negative diagonal
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                    board[r - 3][c + 3] == piece:
                return True

    # check row for 4 in a row: positive diagonal
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and \
                    board[r+3][c+3] == piece:
                return True


def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, ((c * SQUARE_SIZE),
                                            (r * SQUARE_SIZE) + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                draw_circle(c, r, RED)
            if board[r][c] == 2:
                draw_circle(c, r, YELLOW)
    pygame.display.update()


def draw_circle(c, r, colour):
    pygame.draw.circle(screen, colour, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                        height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)


def winning_text():
    if turn % 2 == 0:
        winning_player = 'Player 1'
        label = win_text.render("{} wins!".format(winning_player), 1, RED)
    else:
        winning_player = 'Player 2'
        label = win_text.render("{} wins!".format(winning_player), 1, RED)
    screen.blit(label, (40, 10))


# game status
game_over = False
turn = random.choice([PLAYER, AI])

pygame.init()

# screen set up
SQUARE_SIZE = 100
width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE
RADIUS = int(SQUARE_SIZE/2 - (SQUARE_SIZE/10))

size = (width, height)

screen = pygame.display.set_mode(size)

# instantiations
board = create_board()
change_board_orientation(board)
draw_board(board)
pygame.display.update()

win_text = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            pos_x = event.pos[0]
            if turn % 2 == PLAYER:
                pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            if turn == PLAYER:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_1_PIECE)
                    if winning_move(board, PLAYER_1_PIECE):
                        label = win_text.render("Player 1 wins!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

                    increment_turn(1)

    # AI move
    if turn == AI and not game_over:

        col = random.randint(0, COL_COUNT-1)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_2_PIECE)
            if winning_move(board, PLAYER_2_PIECE):
                label = win_text.render("Player 1 wins!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            change_board_orientation(board)
            draw_board(board)

            increment_turn(1)

        if game_over:
            pygame.time.wait(3000)
