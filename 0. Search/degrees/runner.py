import degrees
import csv
import sys


# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


if len(sys.argv) > 2:
    sys.exit("Usage: python degrees.py [directory]")
directory = sys.argv[1] if len(sys.argv) == 2 else "large"

# Load data from files into memory
print("Loading data...")
degrees.load_data(directory)
print("Data loaded.")

print(names)
print(people)
print(movies)
