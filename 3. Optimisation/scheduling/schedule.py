vars = ["A", "B", "C", "D", "E", "F", "G"]

constraints = [
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "C"),
    ("B", "D"),
    ("C", "E"),
    ("B", "E"),
    ("C", "F"),
    ("D", "E"),
    ("E", "F"),
    ("E", "G"),
    ("F", "G")
]



def backtrack(assignment):
    if len(assignment) == len(vars):
        return assignment

    var = select_unassigned_var(assignment)
    print(var.__str__())

    for val in ['Monday', 'Tuesday', 'Wednesday']:
        new_assignment = assignment.copy()
        new_assignment[var] = val

        if check_consistent(new_assignment):
            result = backtrack(new_assignment)

            if result is not None:
                return result

    return None



def select_unassigned_var(assignment):
    for var in vars:
        if var not in assignment.keys():
            return var
    return None

def check_consistent(assignment):
    for x, y in constraints:
        if x not in assignment or y not in assignment:
            continue

        if assignment[x] == assignment[y]:
            return False

    return True




assignment = {}
solution = backtrack(assignment)

print(solution)
