import tictactoe

board = tictactoe.initial_state()

while not tictactoe.terminal(board):
    a = tictactoe.minimax(board)
    board = tictactoe.result(board, a)

print('Final board', board)
assert_equal(tictactoe.utility(board), 0)
