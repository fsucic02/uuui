from collections import deque

class Clause:
    def __init__(self, literals, idx, parent_1=None, parent_2=None):
        self.literals = literals
        self.idx = idx
        self.parent_1 = parent_1
        self.parent_2 = parent_2

    def __lt__(self, other):
        return self.idx < other.idx
    
def parse(path, cooking=False):
    clauses = set()
    lines = open(path, 'r').read().strip().lower().splitlines()
    lines = [line for line in lines if not line.startswith('#')]
    goal = set(lines[-1].split(' v '))
    index = 1
    for clause in lines[:-1]:
        temp = []
        for literal in clause.split(' v '):
            temp.append(literal)
        clauses.add(Clause(frozenset(temp), index))
        index += 1

    if cooking == True:
        temp = []
        for literal in lines[-1].split(' v '):
            temp.append(literal)
        clauses.add(Clause(frozenset(temp), index))
        return clauses
    
    temp = []
    for literal in goal:
        temp.append(literal[1:] if literal.startswith('~') else '~' + literal)

    sos = set()
    for l in temp:
        sos.add(Clause(frozenset([l]), index))
        index += 1

    """
    for clause in sorted(clauses):
        print(f"{clause.idx}. {" v ".join(clause.literals)}")

    for literal in sorted(sos):
        print(f"{literal.idx}. {" v ".join(literal.literals)}")

    print("===============")
    """ 

    return goal, clauses, sos

def print_procedure(clause_1, clause_2, index):
    nil_clause = Clause('NIL', index, clause_1, clause_2)
    q = deque([nil_clause])
    visited = set()
    while q:
        clause = q.popleft()
        
        if clause in visited:
            continue

        visited.add(clause)
        for parent in [clause.parent_1, clause.parent_2]:
            if parent != None:
                q.append(parent)
    
    visited = sorted(visited)
    print_eq = True
    fun = {}
    for i, clause in enumerate(visited, 1):
        fun[clause.idx] = i

    for clause in visited:
        if clause.parent_1 is None:
            print(f"{fun[clause.idx]}. {' v '.join(clause.literals)}")
        else:
            if print_eq:
                print('===============')
                print_eq = False
            
            print(f"{fun[clause.idx]}. {' v '.join(clause.literals) if clause.literals != 'NIL' else 'NIL'} ({min(fun[clause.parent_1.idx], fun[clause.parent_2.idx])}, {max(fun[clause.parent_1.idx], fun[clause.parent_2.idx])})")

    print('===============')

def print_knowledge(clauses):
    print("Constructed with knowledge:")
    for clause in clauses:
        print(' v '.join(clause.literals))
    print('')