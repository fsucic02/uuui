import sys
from algorithms import pl_resolution, cook
from utils import parse

if __name__ == "__main__":
    if sys.argv[1] == "resolution":
        goal, clauses, sos = parse(sys.argv[2])
        result = pl_resolution(clauses, sos)
        print(f"[CONCLUSION]: {' v '.join(goal)} is {'true' if result is True else 'unknown'}")
    else:
        cook(sys.argv[2], sys.argv[3])
