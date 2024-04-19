from utils import parse, Clause, print_procedure, print_knowledge

def pl_resolve(clause_1, clause_2, index):
    resolvents, literals_to_delete = set(), set()

    for literal_1 in clause_1.literals:
        for literal_2 in clause_2.literals:
            if negated_literal(literal_1) == literal_2:
                literals_to_delete.add(literal_1) 

    for literal in literals_to_delete:
        clause_1.literals, clause_2.literals = set(clause_1.literals), set(clause_2.literals)
        clause_1.literals.remove(literal)
        clause_2.literals.remove(negated_literal(literal))
        resolvent = clause_1.literals.union(clause_2.literals)

        if len(resolvent) != 0:
            resolvents.add(Clause(frozenset(clause_1.literals.union(clause_2.literals)), index, clause_1, clause_2))
            index += 1
        
        clause_1.literals.add(literal)
        clause_2.literals.add(negated_literal(literal))
        clause_1.literals, clause_2.literals = frozenset(clause_1.literals), frozenset(clause_2.literals)
    
    if len(resolvents) == 0:
        print_procedure(clause_1, clause_2, index)
        
    return resolvents, index

def negated_literal(literal):
    return literal[1:] if literal.startswith("~") else "~" + literal

def remove_tautology(set_of_clauses):
    for clause in set_of_clauses.copy():
        for literal in clause.literals:
            if negated_literal(literal) in clause.literals:
                set_of_clauses.remove(clause)
                break
    return set_of_clauses 

def remove_redundant(set_of_clauses):
    for clause in set_of_clauses.copy():
        for other_clause in set_of_clauses.copy():
            if clause.literals != other_clause.literals and clause.literals.issubset(other_clause.literals):
                set_of_clauses.remove(other_clause)
    return set_of_clauses

def select_clauses(sos, all_clauses):
    selected_clauses = set()
    for clause_s in sos:
        for clause in all_clauses:
            for literal in clause.literals:
                if negated_literal(literal) in clause_s.literals:
                    selected_clauses.add((clause, clause_s))
                    break
    return selected_clauses

def reset_index(clauses, sos):
    for i, clause in enumerate(clauses, 1):
        clause.idx = i
    for i, clause in enumerate(sos, len(clauses) + 1):
        clause.idx = i
    return clauses, sos

def pl_resolution(clauses, sos):
    all_clauses = clauses.union(sos)
    index = len(all_clauses) + 1
    resolved = set()

    while True:
        all_clauses, sos = remove_tautology(all_clauses), remove_tautology(sos)
        all_clauses, sos = remove_redundant(all_clauses), remove_redundant(sos)
        selected_clauses = select_clauses(sos, all_clauses)

        if len(selected_clauses) == 0:
            return False
        
        for (clause_1, clause_2) in selected_clauses:
            if (clause_1, clause_2) not in resolved:
                resolved.add((clause_1, clause_2))
                resolvents, index = pl_resolve(clause_1, clause_2, index)

                if len(resolvents) == 0:
                    return True

                for resolvent_clause in resolvents:
                    for clause in all_clauses.copy():
                        if resolvent_clause.literals.issubset(clause.literals):
                            all_clauses.remove(clause)
                    for clause in sos.copy():
                        if resolvent_clause.literals.issubset(clause.literals):
                            sos.remove(clause)

                for clause in resolvents:
                    all_clauses.add(clause)
                    sos.add(clause)

def query(clauses, sos, goal_clause):
    print(f"User's command: {goal_clause} ?")
    result = pl_resolution(clauses, sos)

    print(f"[CONCLUSION]: {goal_clause} is {'true' if result is True else 'unknown'}\n")

def cook(path, instructions):
    instructions = open(instructions).read().lower().splitlines()
    clauses = parse(path, cooking=True)
    print_knowledge(clauses)

    for instruction in instructions:
        command = instruction[-1]

        if command == '?':
            goal_clause = instruction.split(' ?')[0]
            sos = set()
            for literal in goal_clause.split(' v '):
                sos.add(Clause(frozenset([negated_literal(literal)]), -1))
            
            clauses, sos = reset_index(clauses, sos)
            query(clauses, sos, goal_clause)
        
        elif command == '+':
            clause_to_add = instruction.split(' +')[0]
            literals = frozenset(clause_to_add.split(' v '))
            clauses.add(Clause(literals, 1e9))

            print(f"added {clause_to_add}\n")

        elif command == '-':
            clause_to_delete = instruction.split(' -')[0]
            literals = frozenset(clause_to_delete.split(' v '))
            for clause in clauses.copy():
                if clause.literals == literals:
                    clauses.remove(clause)
                    break
                
            print(f"removed {clause_to_delete}\n")
    