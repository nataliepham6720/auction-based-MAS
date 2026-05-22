import random
import numpy as np

from grid import generate_auction_instance
from robot import Robot

from parallel_auction import (parallel_auction, total_distance as parallel_total)
from ssi_auction import (sequential_single_item_auction, total_distance as ssi_total)


def initialize_robots(starts):
    robots = []
    for i, start in enumerate(starts):
        robots.append(Robot(robot_id=i,start=start))

    return robots

# Run one auction instance
def run_instance(starts,goals):
    # Parallel auction
    robots_parallel = initialize_robots(starts)
    robots_parallel, _ = parallel_auction(robots_parallel, goals, verbose=False)
    parallel_cost = parallel_total(robots_parallel)

    # SSI
    robots_ssi = initialize_robots(starts)
    robots_ssi, _ = (sequential_single_item_auction(robots_ssi, goals, verbose=False))
    ssi_cost = ssi_total(robots_ssi)
    return (parallel_cost, ssi_cost)


# Run experiments
def run_experiments(n_trials=100,
                    n_robots=10,
                    n_goals=20,
                    grid_size=15,
                    seed=42):

    random.seed(seed)
    np.random.seed(seed)
    parallel_results = []
    ssi_results = []

    for trial in range(n_trials):
        starts, goals = (generate_auction_instance(n_robots=n_robots,
                                                   n_goals=n_goals,
                                                   grid_size=grid_size,
                                                   seed=trial))

        parallel_cost, ssi_cost = (run_instance(starts,goals))
        parallel_results.append(parallel_cost)
        ssi_results.append(ssi_cost)
        print(f"Trial {trial+1}/{n_trials} | Parallel={parallel_cost:.1f} | SSI={ssi_cost:.1f}")
    
    # Statistics
    stats = {"parallel_mean": np.mean(parallel_results),
             "parallel_std": np.std(parallel_results),
             "parallel_min": np.min(parallel_results),
             "parallel_max": np.max(parallel_results),
             "ssi_mean": np.mean(ssi_results),
             "ssi_std": np.std(ssi_results),
             "ssi_min": np.min(ssi_results),
             "ssi_max": np.max(ssi_results)}

    return (parallel_results, ssi_results, stats)

def print_report(stats):
    print("EXPERIMENT RESULTS")
    print("\nParallel auction:")
    print(f"Mean: {stats['parallel_mean']:.2f}")
    print(f"Std: {stats['parallel_std']:.2f}")
    print(f"Min: {stats['parallel_min']:.2f}")
    print(f"Max: {stats['parallel_max']:.2f}")
    print("\nSSI auction:")
    print(f"Mean: {stats['ssi_mean']:.2f}")
    print(f"Std: {stats['ssi_std']:.2f}")
    print(f"Min: {stats['ssi_min']:.2f}")
    print(f"Max: {stats['ssi_max']:.2f}")
    improvement = (stats["parallel_mean"] - stats["ssi_mean"])

    print("\nAverage improvement = (Parallel − SSI):")
    print(f"{improvement:.2f}")
