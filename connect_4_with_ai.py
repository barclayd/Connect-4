import numpy
import pygame
import sys
import math
import random

# setup of connect 4 matrix
COL_COUNT = 7
ROW_COUNT = 6
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY_PIECE = 0
WINDOW_LENGTH = 4

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


def increment_turn():
    global turn
    turn += 1
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


def score_window(window, piece):
    score = 0

    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY_PIECE) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY_PIECE) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(EMPTY_PIECE) == 1:
        score -= 4

    return score


def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, ((c * SQUARE_SIZE),
                                            (r * SQUARE_SIZE) + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                draw_circle(c, r, RED)
            if board[r][c] == AI_PIECE:
                draw_circle(c, r, YELLOW)
    pygame.display.update()


def draw_circle(c, r, colour):
    pygame.draw.circle(screen, colour, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                        height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)


def score_position(board, piece):
    score = 0
    # prioritise the centre of the board
    centre_array = [int(i) for i in list(board[:, COL_COUNT // 2])]
    centre_count = centre_array.count(piece)
    score += centre_count * 3

    # check horizontal score
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COL_COUNT - 3):
            # breaking matrix up into slices of 4
            window = row_array[c:c+WINDOW_LENGTH]
            score += score_window(window, piece)

    # check vertical score
    for c in range(COL_COUNT):
        column_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            # breaking matrix up into slices of 4
            window = column_array[r:r+WINDOW_LENGTH]
            score += score_window(window, piece)

    # check positively sloped diagonal score
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece)

    # check negatively sloped diagonal score
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece)

    return score


def get_valid_locations(board):
    valid_locations = []
    for column in range(COL_COUNT):
        if is_valid_location(board, column):
            valid_locations.append(column)
    return valid_locations


def choose_optimum_move(board, piece):
    # returns the column of the best column in which to drop the next piece
    best_score = -10000
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    # simulate dropping in a piece to calculate highest possible scores
    for column in valid_locations:
        row = get_next_open_row(board, column)
        # copy existing board to create a temporary board without modifying existing board
        temp_board = board.copy()
        drop_piece(temp_board, row, column, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = column

    return best_col


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximising_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            # game is over
            if winning_move(board, AI_PIECE):
                return None, 10000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -10000000
            else:
                return None, 0
        else:
            # depth = 0
            return None, score_position(board, AI_PIECE)

    if maximising_player:
        value = -math.inf
        chosen_column = random.choice(valid_locations)

        for column in valid_locations:
            row = get_next_open_row(board, column)
            board_copy = board.copy()
            drop_piece(board_copy, row, column, AI_PIECE)
            new_score = minimax(board_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                chosen_column = column
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return chosen_column, value

    else:
        # minimising player
        value = math.inf
        chosen_column = random.choice(valid_locations)

        for column in valid_locations:
            row = get_next_open_row(board, column)
            board_copy = board.copy()
            drop_piece(board_copy, row, column, PLAYER_PIECE)
            new_score = minimax(board_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                chosen_column = column
            beta = min(beta, value)
            if alpha >= beta:
                break
        return chosen_column, value


# game status
game_over = False
turn = random.randint(0, 1)

pygame.init()

# screen set up
SQUARE_SIZE = 100
width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE
RADIUS = int(SQUARE_SIZE/2 - (SQUARE_SIZE/10))

size = (width, height)

screen = pygame.display.set_mode(size)

pygame.display.set_caption('Connect 4')

# instantiations
board = create_board()
change_board_orientation(board)
draw_board(board)
pygame.display.update()

win_text = pygame.font.SysFont("helvetica", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            pos_x = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            if turn == PLAYER:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        label = win_text.render("You win!", 1, RED)
                        screen.blit(label, (width / 2 - label.get_width() / 2, 25))
                        game_over = True

                    increment_turn()

    # AI move
    if turn == AI and not game_over:

        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                label = win_text.render("AI wins!", 1, YELLOW)
                screen.blit(label, (width / 2 - label.get_width() / 2, 25))
                game_over = True

            change_board_orientation(board)
            draw_board(board)

            increment_turn()

        if game_over:
            pygame.time.wait(3000)
