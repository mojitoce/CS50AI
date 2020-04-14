# Example simple board
HEIGHT = 4
WIDTH = 4
MINES = 3

game = minesweeper.Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = minesweeper.MinesweeperAI(height=HEIGHT, width=WIDTH)
game.add_my_mines(set([(0,0), (0,1), (1,1)]))

m1 = (1, 0)
s1 = add_sentence(m1, game, ai)
print(f"Move: {m1} Sentence: {s1.__str__()}")
ai.add_knowledge(m1, s1.count)

m2 = (2, 0)
s2 = add_sentence(m2, game, ai)
print(f"Move: {m2} Sentence: {s2.__str__()}")
ai.add_knowledge(m2, s2.count)

m3 = (2, 1)
s3 = add_sentence(m3, game, ai)
print(f"Move: {m3} Sentence: {s3.__str__()}")
ai.add_knowledge(m3, s3.count)

print(f"Safe moves: {ai.safes - ai.moves_made}")
for s in ai.knowledge:
    print(s.__str__(), end = ', ')



def add_sentence(move, game, ai):
    nearby_mines = game.nearby_mines(move)
    nearby_cells = ai.get_nearby_cells(move)

    return minesweeper.Sentence(nearby_cells, nearby_mines)
