import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        # Creates a domain with all crossword words for each variable
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == 'down' else 0)
                j = variable.j + (k if direction == 'across' else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains.keys():
            var_len = var.length
            words = self.domains[var]

            self.domains[var] = [w for w in words if len(w) == var_len]



    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if x not in self.crossword.neighbors(y):
            return False
        else:
            overlap = self.crossword.overlaps[x, y]
            words = self.domains[x]

            char_y = set(w[overlap[1]] for w in self.domains[y])

            self.domains[x] = [w for w in words if (w[overlap[0]] in char_y)]

            if len(words) != len(self.domains[x]):
                return True
            else:
                return False



    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            queue = set(x for x in self.crossword.overlaps.keys())
        else:
            queue = arcs

        while len(queue) > 0:
            arc = queue.pop()

            if self.revise(arc[0], arc[1]):
                if len(self.domains[arc[0]]) == 0:
                    return False

                for z in (self.crossword.neighbors(arc[0]) - {arc[1]}):
                    queue.add((z, arc[0]))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        ass_vars = set(x for x in assignment.keys())

        if self.crossword.variables == ass_vars:
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # All words correct length
        for var in assignment:
            if var.length != len(assignment[var]):
                return False

        # All values distinct
        cw_unique_words = set(w for v, w in assignment.items())
        cw_words = [w for v,w in assignment.items()]
        if len(cw_unique_words) != len(cw_words):
            return False

        # No conflicts in overlaps
        for var1 in assignment:
            for var2 in assignment:
                if var1.__eq__(var2):
                    continue
                o = self.crossword.overlaps[var1, var2]

                if o is not None:
                    if assignment[var1][o[0]] != assignment[var2][o[1]]:
                        return False

        return True



    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        nbrs = self.crossword.neighbors(var)
        value_dict = {}

        for value in self.domains[var]:
            invalid = 0
            for y in nbrs:
                if y in assignment:
                    continue
                o = self.crossword.overlaps[var, y]
                char_y = set(w[o[1]] for w in self.domains[y])

                if value[o[0]] not in char_y:
                    invalid += 1
            value_dict[value] = invalid

        # Use sort according to param key
        return sorted(value_dict, key = value_dict.get)


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        p_vars = [v for v in self.crossword.variables if v not in assignment.keys()]

        domain_len_d = {v:len(k) for v, k in self.domains.items() if v in p_vars}
        min_len = domain_len_d[min(domain_len_d, key = domain_len_d.get)]

        p_vars = [k for k, v in domain_len_d.items() if v == min_len]

        if p_vars == 1:
            return p_vars.pop()

        n_nbrs_dict = {v:len(self.crossword.neighbors(v)) for v in p_vars}
        max_nbr = max(n_nbrs_dict, key = n_nbrs_dict.get)

        return max_nbr



    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value

            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)

                if result is not None:
                    return result
        return None



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
