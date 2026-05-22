import random
from robot import Robot
from routing import hill_climb_route

# Incremental bid
def incremental_bid(robot, candidate_goal):
    """
    Compute: bid = cost(T + goal) - cost(T) where T = assigned goals
    """
    current_route, current_cost, _ = hill_climb_route(robot.start,robot.assigned_goals)
    new_goals = (robot.assigned_goals + [candidate_goal])
    new_route, new_cost, _ = hill_climb_route(robot.start,new_goals)
    return (new_cost - current_cost)

# Sequential Single Item Auction
def sequential_single_item_auction(robots,goals,verbose=False):
    unassigned = goals.copy()
    trace = []
    round_num = 0

    # Repeat until all goals assigned
    while unassigned:
        all_bids = []
        # Every robot bids on every unassigned goal
        for robot in robots:
            for goal in unassigned:
                bid = incremental_bid(robot, goal)
                all_bids.append((robot, goal, bid))

        # Global winner
        min_bid = min(x[2] for x in all_bids)
        candidates = [x for x in all_bids if x[2] == min_bid]
        winner_robot, winner_goal, winner_bid = (random.choice(candidates))

        # Assign goal
        winner_robot.add_goal(winner_goal)
        unassigned.remove(winner_goal) # remove from set of unassigned goals

        # Recompute route
        route, cost, _ = hill_climb_route(winner_robot.start, winner_robot.assigned_goals)
        winner_robot.update_route(route, cost)
        trace.append({"round": round_num,
                      "winner": winner_robot.id,
                      "goal": winner_goal,
                      "bid": winner_bid,
                      "remaining": len(unassigned)})
        if verbose:
            print("Round:", round_num)
            print("\nAll bids:")
            for r,g,b in all_bids:
                print(f"Robot {r.id} -> Goal {g}| Bid={b:.2f}")
            
            print("\nWinner:")
            print("Robot",winner_robot.id)
            print("Goal", winner_goal)
            print("Winning bid", winner_bid)
            print("\nUpdated route:")
            print(winner_robot.route)
            print("Cost:",winner_robot.route_cost)
            print("\nRemaining goals:")
            print(unassigned)

        round_num += 1

    return robots, trace


def total_distance(robots):
    return sum(r.route_cost for r in robots)


#############################################################
# Example trace
#############################################################

if __name__ == "__main__":


    #########################################################
    # Example:
    #
    # 3 robots
    # 3 goals
    #
    #########################################################

    robots = [

        Robot(
            0,
            (1,1)
        ),

        Robot(
            1,
            (8,8)
        ),

        Robot(
            2,
            (12,2)
        )

    ]


    goals = [

        (2,10),

        (10,10),

        (14,1)

    ]


    robots, trace = (

        sequential_single_item_auction(

            robots,

            goals,

            verbose=True

        )

    )


    print(

        "\n===================="
    )

    print(

        "FINAL"
    )


    for r in robots:


        print(

            "\nRobot",

            r.id

        )


        print(

            "Goals:",

            r.assigned_goals

        )


        print(

            "Route:",

            r.route

        )


        print(

            "Cost:",

            r.route_cost

        )


    print(

        "\nTotal distance:"
    )

    print(

        total_distance(

            robots

        )

    )