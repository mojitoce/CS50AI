from nose.tools import *
from tictactoe import tictactoe

X = "X"
O = "O"
EMPTY = None

def test_player():
    board = [[X, EMPTY, EMPTY],
            [EMPTY, O, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

    assert_equal(tictactoe.player(board), 'X')

    board = [[X, EMPTY, EMPTY],
            [EMPTY, O, EMPTY],
            [EMPTY, EMPTY, X]]

    assert_equal(tictactoe.player(board), 'O')

def test_actions():
    board = [[X, EMPTY, EMPTY],
            [O, O, X],
            [O, EMPTY, X]]

    assert_equal(tictactoe.actions(board), {(0,1), (0,2), (2,1)})

    board = [[X, X, X],
            [O, O, X],
            [O, O, X]]

    assert_equal(tictactoe.actions(board), set())

def test_result():
    board = [[X, EMPTY, EMPTY],
            [O, O, X],
            [X, EMPTY, O]]

    assert_equal(tictactoe.result(board, (0,1)),
                [[X, X, EMPTY],
                [O, O, X],
                [X, EMPTY, O]])

    board = [[X, EMPTY, EMPTY],
            [O, O, X],
            [X, X, O]]

    assert_equal(tictactoe.result(board, (0,1)),
                [[X, O, EMPTY],
                [O, O, X],
                [X, X, O]])

    board = [[X, O, EMPTY],
            [O, O, X],
            [X, X, O]]

    assert_raises(Exception, tictactoe.result,
                board,
                (0,1))

def test_winner():
    board = [[X, EMPTY, EMPTY],
            [O, X, O],
            [O, EMPTY, X]]
    board = [['O', 'X', 'X'],
                ['O', 'X', 'O'],
                ['X', 'O', 'X']]

    assert_equal(tictactoe.winner(board), X)

    board = [['X', 'O', 'O'],
                ['X', 'O', 'X'],
                ['O', None, 'X']]

    assert_equal(tictactoe.winner(board), O)

    board = [[X, EMPTY, EMPTY],
            [O, X, X],
            [O, EMPTY, O]]

    assert_equal(tictactoe.winner(board), None)

    board = [[X, O, X],
            [O, X, O],
            [O, X, O]]

    assert_equal(tictactoe.winner(board), None)

def test_terminal():
    board = [[X, X, X],
            [O, O, X],
            [O, O, X]]

    assert_equal(tictactoe.terminal(board), True)

    board = [[X, EMPTY, EMPTY],
            [O, O, X],
            [X, EMPTY, O]]

    assert_equal(tictactoe.terminal(board), False)

def test_utility():
    # X Wins
    board = [[X, EMPTY, EMPTY],
            [O, X, O],
            [O, EMPTY, X]]
    assert_equal(tictactoe.utility(board), 1)

    # O Wins
    board = [[X, EMPTY, EMPTY],
            [O, O, O],
            [O, EMPTY, X]]
    assert_equal(tictactoe.utility(board), -1)

    # Draw


    board = [[X, EMPTY, EMPTY],
            [O, X, O],
            [O, EMPTY, O]]
    assert_equal(tictactoe.utility(board), 0)

def test_minimax():
    board = [[X, O, EMPTY],
            [X, O, X],
            [O, EMPTY, X]]

    assert_equal(tictactoe.minimax(board), (0,2))

    board = [[X, O, EMPTY],
            [X, O, X],
            [EMPTY, EMPTY, O]]

    assert_equal(tictactoe.minimax(board), (2,0))

def test_full_game_draw():
    board = tictactoe.initial_state()

    while not tictactoe.terminal(board):
        a = tictactoe.minimax(board)
        board = tictactoe.result(board, a)

    print('Final board', board)
    assert_equal(tictactoe.utility(board), 0)
