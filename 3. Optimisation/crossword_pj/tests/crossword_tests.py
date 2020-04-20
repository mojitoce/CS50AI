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



def test_node_consistency():
    print(creator.domains)
