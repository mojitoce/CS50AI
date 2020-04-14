for i in range(0, 10):
    print(i)
# import pygame
# import sys
# import time
#
# from minesweeper import Minesweeper, MinesweeperAI, Sentence
#
# HEIGHT = 8
# WIDTH = 8
# MINES = 8
#
# # Colors
# BLACK = (0, 0, 0)
# GRAY = (180, 180, 180)
# WHITE = (255, 255, 255)
#
# # Create game and AI agent
# game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
# ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
#
#
# # Keep track of revealed cells, flagged cells, and if a mine was hit
# revealed = set()
# flags = set()
# lost = False
#
#
# sentence = Sentence({(1, 2), (1, 3), (1, 5), (2, 7)}, 3)
# print(sentence.__str__())
#
# print(not True)
# sentence.mark_mine((1, 2))
# print(sentence.count)
# sentence.mark_safe((2, 7))
# print(sentence.cells)
#
# print(game.is_mine((5,1)))
# print(game.nearby_mines((5,1)))
#
# ai.add_knowledge((5, 1), game.nearby_mines((5,1)))
# ai.add_knowledge((5,2), game.nearby_mines((5, 2)))
#
# print('moves', ai.moves_made)
# print('safes', ai.safes)
# print('knowledge', ai.knowledge[0].__str__())
