from nose.tools import *
from minesweeper import minesweeper

HEIGHT = 4
WIDTH = 4
MINES = 3

def test_rm_empty_sentence():
    ai = minesweeper.MinesweeperAI(height=HEIGHT, width=WIDTH)
    ai.knowledge.append(minesweeper.Sentence(set(), 0))

    ai.rm_empty_sentences()

    assert_equal(ai.knowledge, [])

def test_add_my_mines():
    game = minesweeper.Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
    ai = minesweeper.MinesweeperAI(height=HEIGHT, width=WIDTH)

    game.add_my_mines(set([(0,0), (0,1), (1,1)]))

    move = (1,0)
    is_mine = game.is_mine(move)
    assert_equal(False, is_mine)

    move = (1,1)
    is_mine = game.is_mine(move)
    assert_equal(True, is_mine)

def test_nearby_cells_func():
    HEIGHT = 4
    WIDTH = 4
    MINES = 3

    game = minesweeper.Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
    ai = minesweeper.MinesweeperAI(height=HEIGHT, width=WIDTH)
    game.add_my_mines(set([(0,0), (0,1), (1,1)]))

    # Make safe move
    move = (2,2)
    nearby = game.nearby_mines(move)

    nearby_cells, count = ai.get_nearby_cells(move, 1)
    assert_equal(nearby_cells,
        {(1,1), (1,2), (1,3),
         (2,1), (2,3),
          (3,1), (3,2), (3,3)})

    ai.mark_safe((2,1))
    ai.mark_mine((1,1))

    nearby_cells, count = ai.get_nearby_cells(move, 1)
    assert_equal(nearby_cells,
        {(1,2), (1,3),
         (2,3),
          (3,1), (3,2), (3,3)})

def test_four_four():
    HEIGHT = 4
    WIDTH = 4
    MINES = 3

    game = minesweeper.Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
    ai = minesweeper.MinesweeperAI(height=HEIGHT, width=WIDTH)
    game.add_my_mines(set([(0,0), (0,1), (1,1)]))

    lost = False
    move_type = ''
    while not lost:
        move = None

        if len(ai.mines) == MINES:
            print("THE AI TRIUMPHED!!!")
            break

        move = ai.make_safe_move()
        if move is None:
            move = ai.make_random_move()
            if move is None:
                # flags = ai.mines.copy()
                print("No moves left to make.")
            else:
                move_type = 'random'
                print(f"No known safe moves, AI making random move. Move: {move}")
        else:
            print(f"AI making safe move. Move: {move}")

        if move:
            if game.is_mine(move):
                lost = True
                assert_equal(move_type, 'random')
                print('You lost!')
            else:
                nearby = game.nearby_mines(move)
                # revealed.add(move)
                ai.add_knowledge(move, nearby)

def test_4_4_randm():
    HEIGHT = 4
    WIDTH = 4
    MINES = 3

    game = minesweeper.Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
    ai = minesweeper.MinesweeperAI(height=HEIGHT, width=WIDTH)

    lost = False
    move_type = ''
    while not lost:
        move = None

        if len(ai.mines) == MINES:
            print("THE AI TRIUMPHED!!!")
            break

        move = ai.make_safe_move()
        if move is None:
            move = ai.make_random_move()
            if move is None:
                # flags = ai.mines.copy()
                print("No moves left to make.")
            else:
                move_type = 'random'
                print(f"No known safe moves, AI making random move. Move: {move}")
        else:
            print(f"AI making safe move. Move: {move}")

        if move:
            if game.is_mine(move):
                lost = True
                assert_equal(move_type, 'random')
                print('You lost!')
                break
            else:
                nearby = game.nearby_mines(move)
                # revealed.add(move)
                ai.add_knowledge(move, nearby)

def test_9_9_randm():
    HEIGHT = 9
    WIDTH = 9
    MINES = 8

    game = minesweeper.Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
    ai = minesweeper.MinesweeperAI(height=HEIGHT, width=WIDTH)

    lost = False
    move_type = ''
    while not lost:
        move = None

        if ai.mines == game.mines:
            print('Mines in game: ', game.mines)
            print('Mines found by AI: ', ai.mines)
            print("THE AI TRIUMPHED!!!")
            break

        move = ai.make_safe_move()
        if move is None:
            move = ai.make_random_move()
            if move is None:
                # flags = ai.mines.copy()
                print("No moves left to make.")
            else:
                move_type = 'random'
                print(f"No known safe moves, AI making random move. Move: {move}")
        else:
            print(f"AI making safe move. Move: {move}")

        if move:
            if game.is_mine(move):
                lost = True
                assert_equal(move_type, 'random')
                print('You lost!')
                break
            else:
                nearby = game.nearby_mines(move)
                # revealed.add(move)
                ai.add_knowledge(move, nearby)
