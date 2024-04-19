import heapq

def parse_bfs(state_space):
    lines = open(state_space, "r", encoding="utf-8").read().splitlines()
    i = lines[0] != "#"

    start_state = lines[1-i]
    goal_states = set()
    graph = {}
    for state in lines[2-i].split(" "):
        goal_states.add(state)
    
    for line in lines[3-i:]:
        if line[0] == "#" or len(line.split(": ")) == 1:
            continue
        
        parent = line.split(": ")[0]
        graph[parent] = []
        for child in line.split(": ")[1].split():
            state = child.split(",")[0]
            heapq.heappush(graph[parent], state)

    return start_state, goal_states, graph

def parse_ucs(state_space):
    lines = open(state_space, "r", encoding="utf-8").read().splitlines()
    i = lines[0] != "#"

    start_state = lines[1-i]
    goal_states = set()
    graph = {}
    for state in lines[2-i].split(" "):
        goal_states.add(state)
    
    for line in lines[3-i:]:
        if line[0] == "#":
            continue
        if len(line.split(": ")) == 1:
            graph[line.split(": ")[0][:-1]] = [("#", -1e9)]
            continue

        parent = line.split(": ")[0]
        graph[parent] = []
        for child in line.split(": ")[1].split():
            state, cost = child.split(",")[0], float(child.split(",")[1])
            graph[parent].append((state, cost))   
        
    return start_state, goal_states, graph

def parse_heuristic(heuristic):
    heuristic_tree = {}
    lines = open(heuristic, "r", encoding="utf-8").read().splitlines()

    for line in lines:
        if line[0] == "#":
            continue
            
        state, h = line.split(": ")
        heuristic_tree[state] = float(h)

    return heuristic_tree

def parse_astar(state_space):
    state_space_f = open(state_space, "r", encoding="utf-8").read().splitlines()
    i = state_space_f[0] != "#"
    
    start_state = state_space_f[1-i]
    goal_states = set()
    graph = {}

    for state in state_space_f[2-i].split(" "):
        goal_states.add(state)

    for line in state_space_f[3-i:]:
        if line[0] == "#" or len(line.split(": ")) == 1:
            continue
        
        parent = line.split(": ")[0]
        graph[parent] = []
        for child in line.split(": ")[1].split():
            state, cost = child.split(",")[0], float(child.split(",")[1])
            graph[parent].append((state, cost))   

    return start_state, goal_states, graph

def print_alg(algorithm, found_sol, visited_states, path):
    if found_sol:
        print("[FOUND_SOLUTION]: yes")
        print(f"[STATES_VISITED]: {len(visited_states)}")
        print(f"[PATH_LENGTH]: {len(path)}")
        print(f"[TOTAL_COST]: {sum([node.cost - node.parent.cost if node.parent is not None else node.cost for node in path]) if algorithm == "ucs" or algorithm == "astar" else "100"}")
        print("[PATH]: " + " => ".join(reversed([node.state for node in path])))
    else:
        print(f"[FOUND_SOLUTION]: no")

def print_check(option, result):
        if result:
            print("[CONCLUSION]: Heuristic is optimistic." if option == "optimistic" else "[CONCLUSION]: Heuristic is consistent.")
        else:
            print("[CONCLUSION]: Heuristic is not optimistic." if option == "optimistic" else "[CONCLUSION]: Heuristic is not consistent.")