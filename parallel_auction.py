import random
from robot import Robot
from routing import (hill_climb_route, nn_and_reverse, route_cost)


# Compute incremental bid
def incremental_bid(robot,candidate_goal):
    """
    Compute: bid = cost(T union goal) - cost(T)
    """
    current_goals = robot.assigned_goals.copy()
    current_route, current_cost, _ = hill_climb_route(robot.start, current_goals)
    # current_route, current_cost, _ = nn_and_reverse(robot.start, current_goals)
    new_goals = current_goals + [candidate_goal]
    new_route, new_cost, _ = hill_climb_route(robot.start, new_goals)
    # new_route, new_cost, _ = nn_and_reverse(robot.start, new_goals)
    return (new_cost - current_cost)


# Parallel auction
def parallel_auction(
    robots,
    goals,
    verbose=False
):

    trace = []
    # each goal independently assigned
    for goal in goals:
        bids = []
        for robot in robots:
            bid = incremental_bid(robot,goal)
            bids.append((robot,bid))
        # Find winner
        min_bid = min(x[1] for x in bids)
        winners = [r for r,b in bids if b == min_bid]
        winner = random.choice(winners)
        winner.add_goal(goal)
        # Update winner route
        route, cost, _ = hill_climb_route(winner.start, winner.assigned_goals)
        winner.update_route(route,cost)

        # Save trace
        trace.append({"goal": goal,
                      "winner": winner.id,
                      "winning_bid": min_bid,
                      "all_bids": {r.id:b for r,b in bids}})

        if verbose:
            print("\nGoal:",goal)
            for r,b in bids:
                print(f"Robot {r.id}: bid={b:.2f}")
            
            print("Winner:",winner.id)
            print("Updated route:", winner.route)
            print("Cost:", winner.route_cost)

    return robots, trace


# Total travel distance
def total_distance(robots):
    return sum(r.route_cost for r in robots)