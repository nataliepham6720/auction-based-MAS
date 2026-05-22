import random
from typing import List, Tuple

Cell = Tuple[int, int]


def manhattan_distance(a: Cell, b: Cell) -> int:
    """
    Compute shortest travel distance in an empty grid world.
    ---- Inputs ------
    a : (x,y)
    b : (x,y)
    ---- Outputs -----
    Manhattan distance (int)
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def random_cell(grid_size: int = 15) -> Cell:
    """
    Generate a uniformly random cell.
    --- Outputs -----
    Grid (x,y)
    """
    return (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))


def generate_robot_starts(
    n_robots: int = 10,
    grid_size: int = 15
) -> List[Cell]:
    """
    Generate robot start positions.
    """
    return [random_cell(grid_size) for _ in range(n_robots)]


def generate_goals(
    n_goals: int = 20,
    grid_size: int = 15
) -> List[Cell]:
    """
    Generate goal cells. Goals may overlap.
    """

    return [random_cell(grid_size) for _ in range(n_goals)]


def generate_auction_instance(
    n_robots: int = 10,
    n_goals: int = 20,
    grid_size: int = 15,
    seed: int = None
):
    """
    Generate one auction instance.
    ---- Outputs -----
    robot_starts : List[(x,y)]
    goals        : List[(x,y)]
    """
    if seed is not None:
        random.seed(seed)

    robot_starts = generate_robot_starts(n_robots, grid_size)
    goals = generate_goals(n_goals, grid_size)

    return robot_starts, goals


if __name__ == "__main__":

    robots, goals = generate_auction_instance(seed=42)

    print("Robots:")
    print(robots)
    print("\nGoals:")
    print(goals)

    print("\nDistance example:", manhattan_distance(robots[0], goals[0]))