import nltk
import sys


from parser import preprocess


s_dir = 'sentences/10.txt'

with open(s_dir) as file:
    s = file.read()

words = preprocess(s)
