from typing import List, Tuple, Optional

Cell = Tuple[int, int]

class Robot:
    """
    Robot state for auctions and routing.
    ---- Inputs ------
    id (int): Robot identifier
    start (grid (x,y)): Initial location
    assigned_goals (list[(x,y)]): Goals allocated to robot
    route (list[(x,y)]): Optimized visiting order
    route_cost (float): Total travel distance
    """

    def __init__(self, robot_id: int, start: Cell):
        self.id = robot_id
        self.start = start
        self.assigned_goals: List[Cell] = []
        self.route: List[Cell] = []
        self.route_cost: float = 0.0
    
    # Goal management
    def add_goal(self, goal: Cell):
        """
        Assign new goal to robot.
        """
        self.assigned_goals.append(goal)

    def remove_goal(self, goal: Cell):
        """
        Remove goal assignment.
        """
        if goal in self.assigned_goals:
            self.assigned_goals.remove(goal)

    def clear_goals(self):
        """
        Remove all assigned goals.
        """
        self.assigned_goals = []
        self.route = []
        self.route_cost = 0

    # Route updates
    def update_route(self, optimized_route: List[Cell], cost: float):
        """
        Update optimized route and travel cost.
        """
        self.route = optimized_route
        self.route_cost = cost

    # Incremental auction bidding support
    def copy_with_extra_goal(self, goal: Cell):
        """
        Return temporary goal list after adding a candidate goal.
        Used for auction bidding:
            bid = cost(T & {goal}) - cost(T)
        """
        return self.assigned_goals + [goal]

    # Convenience methods
    def num_goals(self):
        return len(self.assigned_goals)

    def has_goals(self):
        return len(self.assigned_goals) > 0

    # Representation
    def __repr__(self):
        return (
            f"Robot("
            f"id={self.id}, "
            f"start={self.start}, "
            f"goals={len(self.assigned_goals)}, "
            f"cost={self.route_cost}"
            f")"
        )