import random
from typing import List, Tuple, Dict, Optional
from grid import manhattan_distance

Cell = Tuple[int, int]

# Route cost
def route_cost(start: Cell, route: List[Cell]) -> int:
    """
    Compute total travel distance: start -> g1 -> g2 -> ... -> gn
    Note that no return to start needed
    """
    if len(route) == 0:
        return 0

    cost = manhattan_distance(start, route[0])
    
    for i in range(len(route)-1):
        cost = cost + manhattan_distance(route[i], route[i+1])

    return cost

# Random initialization
def random_route(goals: List[Cell]) -> List[Cell]:
    route = goals.copy()
    random.shuffle(route)
    return route

# Reverse subsequence
def reverse_subsequence(route, i, j):
    candidate = route.copy()
    candidate[i:j+1] = reversed(candidate[i:j+1])
    return candidate

# Assignment-required hill climbing
def hill_climb_route(
    start: Cell,
    goals: List[Cell],
    save_trace=False
):
    """
    Hill climbing via repeated subsequence reversal.
    ---- Outputs ---
    best_route
    best_cost
    trace
    """
    if len(goals) <= 1:
        return (goals, route_cost(start, goals), [])

    current = random_route(goals)
    current_cost = route_cost(start, current)
    trace = []
    improved = True
    iteration = 0

    while improved:
        improved = False
        best_route = current
        best_cost = current_cost
        neighbors = []
        # Try all subsequence reversals
        for i in range(len(current)):
            for j in range(i+1, len(current)):
                candidate = reverse_subsequence(current, i, j)
                candidate_cost = route_cost(start, candidate)
                neighbors.append((candidate, candidate_cost))
        
        random.shuffle(neighbors)
        for candidate, candidate_cost in neighbors:
            if candidate_cost < best_cost:
                best_route = candidate
                best_cost = candidate_cost
                improved = True

        if improved:
            current = best_route
            current_cost = best_cost

        # Trace logging
        if save_trace:
            trace.append({"iteration": iteration,
                          "route": current.copy(),
                          "cost": current_cost})
        iteration += 1
    return current, current_cost, trace


# Use nearest neighbor to improve goal assignment
def nearest_neighbor_route(start, goals):
    unvisited = goals.copy()
    current = start
    route = []

    while unvisited:
        next_goal = min(unvisited,key=lambda g: manhattan_distance(current, g))
        route.append(next_goal)
        unvisited.remove(next_goal)
        current = next_goal
    return route

# nearest neighbor & reverse
def nn_and_reverse(start, goals, save_trace=True):
    route = nearest_neighbor_route(start, goals)
    best_cost = route_cost(start, route)
    trace = []
    if save_trace:
        trace.append({
            "iteration": 0,
            "route": route.copy(),
            "cost": best_cost,
            "action": "Nearest Neighbor Initialization"
        })
    improved = True
    iteration = 1

    while improved:
        improved = False
        current_best_route = route
        current_best_cost = best_cost
        # Try all subsequence reversals 
        for i in range(len(route)):
            for j in range(i+1, len(route)):
                candidate = reverse_subsequence(route,i,j)
                candidate_cost = route_cost(start,candidate)
                if candidate_cost < current_best_cost:
                    current_best_route = candidate
                    current_best_cost = candidate_cost
                    improved = True

        if improved: # Update if improvement found
            route = current_best_route
            best_cost = current_best_cost
            if save_trace:
                trace.append({"iteration": iteration,
                              "route": route.copy(),
                              "cost": best_cost,
                              "action": "reversal update"})
            iteration += 1

    return route, best_cost, trace


# Trace printing 
def print_trace(trace):
    print("\nTRACE")
    for step in trace:
        print( f"Iter {step['iteration']} | "
               f"Cost {step['cost']} | "
               f"Route {step['route']}")