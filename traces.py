from grid import manhattan_distance
from routing import print_trace, hill_climb_route, nn_and_reverse
from robot import Robot
from parallel_auction import (parallel_auction, total_distance as parallel_total)
from ssi_auction import (sequential_single_item_auction, total_distance as ssi_total)

# 1. Distance example
def distance_trace():
    print("\n==================================================")
    print("1. DISTANCE EXAMPLE")
    print("==================================================")
    start = (2,3)
    goal = (8,10)
    d = manhattan_distance(start,goal)
    print("Start:", start)
    print("Goal:", goal)
    print("\nDistance formula:")
    print(f"|{goal[0]}-{start[0]}|+|{goal[1]}-{start[1]}|")
    print("\nShortest distance:",d)


# 2. Hill climbing trace
def hill_climb_trace():
    print("\n==================================================")
    print("2. HILL CLIMB")
    print("==================================================")
    start = (2,3)
    goals = [(8,2),(1,9),(6,5),(10,10)]
    route, cost, trace = hill_climb_route(start,goals,save_trace=True)
    print_trace(trace)

# 2b. Greedy trace
def nn_trace():
    print("\n==================================================")
    print("2. GREEDY ALG")
    print("==================================================")
    start = (2,3)
    goals = [(8,2),(1,9),(6,5),(10,10)]
    route, cost, trace = nn_and_reverse(start,goals)
    print_trace(trace)

# 3. Parallel auction trace
def parallel_trace():
    print("\n==================================================")
    print("3. PARALLEL AUCTION")
    print("==================================================")
    robots = [Robot(0,(1,1)),
              Robot(1,(8,8)),
              Robot(2,(12,2))]
    goals = [(2,10),(10,10),(14,1)]
    robots, trace = parallel_auction(robots,goals,verbose=True)
    print("\nFinal assignment")
    for r in robots:
        print("\nRobot", r.id)
        print("Start:", r.start)
        print("Goals:", r.assigned_goals)
        print("Route:", r.route)
        print("Cost:", r.route_cost)
    print("\nTotal distance:")
    print(parallel_total(robots))


# 4. SSI trace
def ssi_trace():
    print("\n==================================================")
    print("4. SEQUENTIAL SINGLE ITEM AUCTION")
    print("==================================================")
    robots = [Robot(0,(1,1)),
              Robot(1,(8,8)),
              Robot(2,(12,2))]
    goals = [(2,10),(10,10),(14,1)]
    robots, trace = sequential_single_item_auction(robots,goals,verbose=True)
    print("\nFinal assignment")
    for r in robots:
        print("\nRobot", r.id)
        print("Start:", r.start)
        print("Goals:", r.assigned_goals)
        print("Route:", r.route)
        print("Cost:", r.route_cost)
    print("\nTotal distance:")
    print(ssi_total(robots))


if __name__ == "__main__":
    distance_trace()
    hill_climb_trace()
    nn_trace()
    parallel_trace()
    ssi_trace()