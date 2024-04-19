from collections import deque
import heapq

class Node:
    def __init__(self, state, cost=None, heuristic=None):
        self.state = state
        self.parent = None
        self.children = []
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        if self.heuristic is None or other.heuristic is None:
            return self.cost < other.cost
        else:
            return self.cost + self.heuristic < other.cost + other.heuristic

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return self.state == other.state  

def BFS(start_state, goal_states, graph):
    found_sol, visited_states, path = False, set(), []

    open_list = deque([Node(start_state)])
    while open_list:
        n = open_list.popleft()
        if n.state in visited_states:
            continue

        visited_states.add(n.state)

        if n.state in goal_states:
            found_sol = True
            path.append(n)
            while n.parent:
                path.append(n.parent)
                n = n.parent
            break

        n.children = graph[n.state]
        for child_state in n.children:
            child = Node(child_state)
            child.parent = n
            open_list.append(child)

    return found_sol, visited_states, path

def UCS(start_state, goal_states, graph):
    found_sol, visited_states, path = False, set(), []

    open_list = [Node(start_state, 0)]
    while open_list:
        n = heapq.heappop(open_list)
        if n.state in visited_states:
            continue

        visited_states.add(n.state)

        if n.state in goal_states:
            found_sol = True
            path.append(n)
            while n.parent:
                path.append(n.parent)
                n = n.parent
            break

        n.children = graph[n.state]
        for child_state in n.children:
            child = Node(child_state[0], child_state[1] + n.cost)
            child.parent = n
            heapq.heappush(open_list, child)

    return found_sol, visited_states, path

def ASTAR(start_state, goal_states, graph, heuristic):
    found_sol, path = False, []

    open_list = [Node(start_state, 0, heuristic[start_state])]
    closed_set = set()
    while open_list:
        n = heapq.heappop(open_list)

        if n.state in goal_states:
            found_sol = True
            path.append(n)
            while n.parent:
                path.append(n.parent)
                n = n.parent
            break
        
        closed_set.add(n)
        n.children = graph[n.state]
        for child_state in n.children:
            child = Node(child_state[0], child_state[1] + n.cost, heuristic[child_state[0]])
            child.parent = n
            flag = False
            if any(child.state == node.state for node in open_list) or child in closed_set:
                for node in open_list:
                    if child.state == node.state:
                        if node.cost < child.cost:
                            flag = True
                            break
                        else:
                            if node in open_list:
                                open_list.remove(node)
                            else:
                                closed_set.remove(node)
            if flag:
                continue
                
            heapq.heappush(open_list, child)
            

    return found_sol, path

def check_optimistic(start_state, goal_states, graph, heuristic):
    result, real_cost = True, {}

    _, _, path = UCS(start_state, goal_states, graph)

    for idx, node in enumerate(reversed(path), 1):
        real_cost[node.state] = path[0].cost - path[-idx].cost

    for node in graph.keys():
        if node not in real_cost.keys():
            _, _, path = UCS(node, goal_states, graph)
            for idx, node in enumerate(reversed(path), 1):
                real_cost[node.state] = path[0].cost - path[-idx].cost

    for state in sorted(real_cost.keys()):
        h, h_star = heuristic[state], real_cost[state]
        if heuristic[state] <= real_cost[state]:
            print(f"[CONDITION]: [OK] h({state}) <= h*: {h} <= {h_star}")
        else:
            result = False
            print(f"[CONDITION]: [ERR] h({state}) <= h*: {h} <= {h_star}")
    
    return result

def check_consistent(graph, heuristic):
    result = True
    for state in graph.keys():
        for child_state, cost in graph[state]:
            if child_state != "#":
                h, h_child = heuristic[state], heuristic[child_state]
                if h <= h_child + cost:
                    print(f"[CONDITION]: [OK] h({state}) <= h({child_state}) + c: {h} <= {h_child} + {cost}")
                else:
                    result = False
                    print(f"[CONDITION]: [ERR] h({state}) <= h({child_state}) + c: {h} <= {h_child} + {cost}")
    
    return result
