"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # sum not EMPTY if even return X if odd return O
    plays = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] is not None:
                plays += 1

    if plays % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # for loop through board. If EMPTY add position to set
    actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                # print(f'Board pos ({i},{j}), value {board[i][j]}')
                actions.add((i,j))

    return actions


def result(board, action):
    """
    Returns the board that result from making move (i, j) on the board.
    """
    # Make deep copy of board
    # Alter board copy with action if possible otherwise return exception
    board_copy = copy.deepcopy(board)

    val = board[action[0]][action[1]]

    if val is not None:
        raise Exception('Invalid move!')
    else:
        plyr = player(board)
        board_copy[action[0]][action[1]] = plyr

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Return X or O if no winner return None
    scores = [0]*8

    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                scores[i] += 1
                scores[3 + j] += 1

                if (i == j):
                    scores[6] += 1
                    if i == 1:
                        # In the middle the diagonals converge
                        scores[7] += 1
                elif (i == (2-j)):
                    scores[7] += 1
            elif board[i][j] == O:
                scores[i] -= 1
                scores[3 + j] -= 1

                if (i == j):
                    scores[6] -= 1
                    if i == 1:
                        # In the middle the diagonals converge
                        scores[7] -= 1
                elif (i == (2-j)):
                    scores[7] -= 1
            else:
                pass

    for s in scores:
        if s == 3:
            return X
        elif s == -3:
            return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    valid_actions = actions(board)

    if valid_actions == set():
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Use winner function to determine utility
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if terminal return None otherwise return optimal action

    if terminal(board):
        return None

    if player(board) == X:
        v = - 100
        action = (0,0)
        for a in actions(board):
            if min_value(result(board, a)) > v:
                v = min_value(result(board, a))
                action = a
        return action
    elif player(board) == O:
        v = 100
        action = (0,0)
        for a in actions(board):
            # print('Action', a)
            # nb = result(board, a)
            # print('New Board', nb)
            mv = max_value(result(board, a))
            # print('Value', mv)
            if mv < v:
                v = mv
                action = a

        return action


def max_value(board):
    if terminal(board):
        return utility(board)

    v = - 100
    for a in actions(board):
        v = max(v, min_value(result(board, a)))

    return v

def min_value(board):
    if terminal(board):
        return utility(board)

    v = 100
    for a in actions(board):
        v = min(v, max_value(result(board, a)))

    return v
