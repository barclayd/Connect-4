import numpy as np

# setup of connect 4 matrix
COL_COUNT = 7
ROW_COUNT = 6
PLAYER_1_PIECE = 1
PLAYER_2_PIECE = 2


# class definitions
def create_board():
    # matrix to represent board
    board = np.zeros((ROW_COUNT, COL_COUNT))
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


def check_is_four_in_row():
    pass


def change_board_orientation(board):
    print(np.flip(board, 0))


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


# game status
game_status = True
turn = 0

# instantiations
board = create_board()
change_board_orientation(board)

while game_status:
    # player 1 input
    if turn % 2 == 0:
        col = int(input('Player 1 - Make your move! (0-6): '))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_1_PIECE)
            if winning_move(board, PLAYER_1_PIECE):
                print('Player 1 wins!')
                game_status = False
                break

    if turn % 2 != 0:
        col = int(input('Player 2 - Make your move! (0-6): '))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_2_PIECE)
            if winning_move(board, PLAYER_2_PIECE):
                print('Player 2 wins!')
                game_status = False
                break

    turn += 1
    change_board_orientation(board)
    # player 2 input