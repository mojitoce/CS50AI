from nose.tools import *
from crossword import crossword as cw
from crossword import generate

# Parse command-line arguments
structure = 'crossword/data/structure1.txt'
words = 'crossword/data/words1.txt'
output = 'crossword/output.png'

# Generate crossword
crossword = cw.Crossword(structure, words)

creator = generate.CrosswordCreator(crossword)
creator.enforce_node_consistency()
creator.ac3()

print(creator.domains)

# Variable(6, 5, 'across', 6): ['REASON', 'SEARCH']

creator.select_unassigned_variable(dict())

# assignment = creator.backtrack(dict())
#
# print(assignment)
# creator.print(assignment)
