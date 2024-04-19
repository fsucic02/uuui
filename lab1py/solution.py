import argparse
from algorithms import BFS, UCS, ASTAR, check_optimistic, check_consistent
from utils import parse_bfs, parse_ucs, parse_astar, parse_heuristic, print_alg, print_check

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    arguments = ["--alg", "--ss", "--h"]
    for argument in ["--alg", "--ss", "--h"]:
        parser.add_argument(argument)
    for argument in ["--check-consistent", "--check-optimistic"]:
        parser.add_argument(argument, action='store_true')
    args = parser.parse_args()

    algorithm, state_space, heuristic = args.alg, args.ss, args.h

    if algorithm == "bfs" or algorithm == "ucs":
        print(f"# {"BFS" if algorithm == "bfs" else "UCS"} {state_space}")
        start_state, goal_states, graph = parse_bfs(state_space) if algorithm == "bfs" else parse_ucs(state_space)
        found_sol, visited_states, path = BFS(start_state, goal_states, graph) if algorithm == "bfs" else UCS(start_state, goal_states, graph)
        print_alg(algorithm, found_sol, visited_states, path)

    elif algorithm == "astar":
        print(f"# ASTAR {heuristic}")
        start_state, goal_state, graph = parse_astar(state_space)
        heuristic = parse_heuristic(heuristic)
        found_sol, path = ASTAR(start_state, goal_state, graph, heuristic)
        print_alg("astar", found_sol, "100", path)
    
    else:
        start_state, goal_states, graph = parse_ucs(state_space)
        heuristic = parse_heuristic(heuristic)
        result = check_optimistic(start_state, goal_states, graph, heuristic) if args.check_optimistic else check_consistent(graph, heuristic)
        option = "optimistic" if args.check_optimistic else "consistent"
        print_check(option, result)