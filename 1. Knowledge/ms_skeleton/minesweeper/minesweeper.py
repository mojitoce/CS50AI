import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")


    def add_my_mines(self, my_mines):
        self.board = []
        self.mines = set()

        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        for mine in my_mines:
            i, j = mine
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True



    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count


    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if (len(self.cells) == self.count):
            return self.cells
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if (self.count == 0):
            return self.cells
        else:
            return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        self.update_knowledge()

        nearby_cells, new_count = self.get_nearby_cells(cell, count)
        p_sentence = Sentence(nearby_cells, new_count)


        self.knowledge.append(p_sentence)
        print(f"Adding new sentence {p_sentence.__str__()}")
        self.update_knowledge()

        print('Knowledge Base')
        for s in self.knowledge:
            print(s.__str__(), end = ', ')
        print('\n')




    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        safe_moves = list(self.safes - self.moves_made)

        if len(safe_moves) == 0:
            return None
        else:
            rand_index = random.randrange(len(safe_moves))
            move = safe_moves[rand_index]
            return move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_moves = []
        for i in range(self.height):
            for j in range(self.width):
                if ((i,j) not in self.moves_made) and ((i,j) not in self.mines):
                    random_moves.append((i,j))

        if len(random_moves) == 0:
            return None
        else:
            rand_index = random.randrange(len(random_moves))
            move = random_moves[rand_index]
            # for s in self.knowledge:
            #     print(s.__str__(), end = ', ')
            # print(move)
            return move

    def get_nearby_cells(self, cell, count):
        cells = set()
        new_count = count
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    if ((i,j) in self.safes or (i,j) in self.moves_made):
                        pass
                    elif (i,j) in self.mines:
                        new_count -= 1
                    else:
                        cells.add((i, j))
        return cells, new_count

    def update_knowledge(self):
        while True:
            print('Relooping')
            self.rm_empty_sentences()

            rerun = False
            for s in self.knowledge:
                add_rerun = self.check_add(s)
                if add_rerun:
                    rerun = add_rerun
                    break
            if rerun:
                continue

            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if (not s1.__eq__(s2)):
                        subset_rerun = self.check_subset(s1, s2)
                        if subset_rerun:
                            rerun = subset_rerun
                            break
            if rerun:
                continue
            break

    def rm_empty_sentences(self):
        for s in self.knowledge:
            if len(s.cells) == 0:
                self.knowledge.remove(s)

    def check_add(self, sentence):
        if sentence.known_mines() is not None:
            mines_rm = sentence.known_mines()
            print(f"Adding mines. Removing sentence {sentence.__str__()}")
            print(f"Mines added: {sentence.cells}")
            self.knowledge.remove(sentence)
            for cell in mines_rm:
                self.mark_mine(cell)
            return True
        elif sentence.known_safes() is not None:
            safes_rm = sentence.known_safes()
            print(f"Adding safes. Removing sentence {sentence.__str__()}")
            print(f"Safe cells added: {sentence.cells}")
            self.knowledge.remove(sentence)
            for cell in safes_rm:
                self.mark_safe(cell)
            return True
        else:
            return False

    def check_subset(self, s1, s2):
        if s1.cells.issubset(s2.cells):
            print(f"{s1.__str__()} is subset of {s2.__str__()}")
            p_sentence = Sentence(s2.cells - s1.cells, s2.count - s1.count)
            print(f"Adding {p_sentence.__str__()} and removing {s2.__str__()}")
            self.knowledge.remove(s2)
            self.knowledge.append(p_sentence)
            return True
        else:
            return False
