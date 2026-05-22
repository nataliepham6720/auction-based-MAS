# Project 2: Auction-based Multi-agents System
**Goal:** Evaluate a sequential single-item auction against a parallel auction'

## Problem Setting
Assume that 10 robots operate in an empty grid world of size 15 by 15 cells. The robots start execution at time step 0 and, from one time step to the next one, can always move to one of the adjacent cells to north, east, south, or west (unless they would leave the grid) or wait in their current cell (several robots can occupy the same cell at the same time).

Parallel Auction Procedure: Use a uniform distribution to generate the start cells of the robots randomly (it is okay if two or more robots get assigned the same start cell since we do not worry about robot collisions in this project). Use a uniform distribution to generate 20 goal cells randomly (it is okay if several goal cells coincide). Assign the goal cells to the robots using a parallel auction under the assumption that the auctioneer breaks ties randomly. Then, plan an approximately shortest route for each robot that starts at the start cell of the robot and visits all goal cells assigned to it. Calculate the sum of the travel distances of all robots, that is, the travel distance of a robot from its start cell to the last-visited goal cell assigned to the robot, summed over all robots. Repeat the steps outlined in the previous sentences of this paragraph 100 times and report the average sum of the travel distances of all robots over the 100 auction instances created, where an auction instance is given by the start and goal cells.

Sequential Single-Item Auction Procedure: Repeat the steps from the Parallel Auction Procedure with two differences: 
    1) Reuse the same auction instances used to evaluate the parallel auction. 
    2) Use a regular sequential single-item auction with the objective of achieving a small sum of travel distances (by regular, we mean with bundle size 1 and with regular rather than regret clearing) instead of a parallel auction. Remember that a sequential single-item auction assigns goal cells to robots in several rounds, while a parallel auction assigns goal cells to robots in one round. 

## Method

### 1. Shortest Travel Distance on a Grid
We implement the **Manhattan distance** to calculate the shortest travel distance between two points on a grid.
Given start at `(2,3)` and goal at `(8,10)`. The Manhattan distance is $$|8-2| + |10-3| = 6 + 7 = 13 $$

### 2a. Hill-Climbing Algorithm for Path Planning

The hill-climbing algorithm computes a short path for a robot to visit multiple goal cells. Start with a **random ordering** of goal cells. Example initial sequence <Goal1, Goal3, Goal2>. Consider every subsequence (length > 1) and reverse it, for example, possible reversals can be <Goal3, Goal1, Goal2>, <Goal1, Goal2, Goal3>.
Compute travel distances for all candidate routes and replace the current route with the route having minimum cost. Repeat until no improvement is possible (local minimum).

**Example** 
```python
start = (0,0)
goals = [(1,8),(2,9),(12,2),(13,1)]
```
```text
Iter 0 | Cost 34 | Route [(2, 9), (1, 8), (13, 1), (12, 2)]
Iter 1 | Cost 32 | Route [(1, 8), (2, 9), (13, 1), (12, 2)]
Iter 2 | Cost 30 | Route [(1, 8), (2, 9), (12, 2), (13, 1)]
Iter 3 | Cost 30 | Route [(1, 8), (2, 9), (12, 2), (13, 1)]
```

Final route is [(1,8), (2,9), (12,2), (13,1)] and final cost is 30. Local minimum reached after **3 iterations**.

### 2b. Proposed Greedy Algorithm
Our proposed method improves initialization using **Nearest Neighbor (NN)** instead of random ordering.
1. Initialize the route by selecting the nearest unvisited goal using Manhattan distance.
2. Apply subsequence reversal updates (same as hill climbing).
3. Continue until no further improvement.
Since initialization is better, fewer iterations are needed.
**Example** 
```python
start = (0,0)
goals = [(1,8),(2,9),(12,2),(13,1)]
```
```text
Iter 0 | Cost 30 | Route [(1, 8), (2, 9), (12, 2), (13, 1)]
```
Final route is [(1,8), (2,9), (12,2), (13,1)] and final cost is 30. The algorithm reaches the local optimum **immediately**.

### 3. Parallel Auction Example
**Configuration**
```python
robots = [Robot(0,(0,0)),
    Robot(1,(8,8)),
    Robot(2,(14,14))]
goals = [(7,8),(8,7),(6,9)]
```
**Final Assignment**
```text
Robot 0
Start: (0,0)
Goals: []
Route: []
Cost: 0

Robot 1
Start: (8,8)
Goals: [(7,8),(8,7),(6,9)]
Route:
[(7,8),(6,9),(8,7)]
Cost:7

Robot 2
Start: (14,14)
Goals: []
Route: []
Cost: 0

Total distance:7
```

### 4. Sequential Single-Item (SSI) Auction Example
Using the same example as Section 3.

**Final Assignment**
```text
Robot 0
Start: (0,0)
Goals: []
Route: []
Cost: 0

Robot 1
Start: (8,8)
Goals: [(7,8),(6,9),(8,7)]
Route: [(8,7),(7,8),(6,9)]
Cost: 5

Robot 2
Start: (14,14)
Goals: []
Route: []
Cost: 0

Total distance: 5
```

SSI improves total travel distance by $7 - 5 = 2$ units.

---
For Sections **1–4**, execute:
```bash
python traces.py
```
This reproduces all example traces.
---

### 5. Parallel Auction Performance over 100 Instances
Statistics over 100 randomly generated auction instances:
| Metric | Value |
|-------|-------:|
| Mean | 45.67 |
| Std | 5.34 |
| Min | 31 |
| Max | 59 |

### 6. SSI Auction Performance over 100 Instances
Statistics over the same 100 randomly generated auction instances (by fixed seeds)
| Metric | Value |
|-------|-------:|
| Mean | 44.35 |
| Std | 5.26 |
| Min | 31 |
| Max | 58 |

**Average Improvement** SSI reduces average total travel distance by
$\text{Improvement}=\text{Parallel}-\text{SSI}=45.67 - 44.35=1.32$

---
For Sections **5–6**, execute:
```bash
python experiments.py
```
---

### 7. Experimental Evaluation of Algorithms
We compare Parallel Auction and Sequential Single-Item Auction (SSI) using identical 100 auction instances but with the proposed algorithm for sorting goals instead of the Hill-climbing algorithm.

**Parallel Auction**

| Metric | Value |
|-------|-------:|
| Mean | 45.64 |
| Std | 5.46 |
| Min | 31 |
| Max | 60 |

**SSI Auction**

| Metric | Value |
|-------|-------:|
| Mean | 43.54 |
| Std | 4.61 |
| Min | 32 |
| Max | 56 |


**Average Improvement** SSI improves average travel distance by
$45.64 - 43.54=2.10$

### 8. Discussion: Why Proposed Algorithm Performs Better
Our proposed algorithm achieves lower average travel distances because of two key ideas:
- Better Initialization: Hill climbing starts from a **random route**, while the proposed approach starts from a **Nearest Neighbor route**, which can be closer to an optimal solution initially, so it could reduces poor local minima and converges faster. Hence, fewer reversal operations and smaller runtime overhead.
- Nearest Neighbor prioritizes geographically closer goals, reducing detours and total traveled distance.
- Experimental results show

| Method | Average Distance |
|-------|------:|
| Parallel Auction | 45.64 |
| SSI Auction | 43.54 |

SSI consistently achieves lower travel distances on average.


### Conclusion
The proposed SSI-based approach combined with greedy initialization:
- Produces shorter routes
- Converges faster
- Requires fewer iterations
- Improves average travel distance across auction instances
Experimental evaluation confirms that SSI outperforms the parallel auction baseline.



**Reference:** C. Tovey, M. G. Lagoudakis, S. Jain, and S. Koenig, “The generation of bidding rules for auction-based robot coordination,” in Multi-Robot Systems: From Swarms to Intelligent Automata, vol. III, pp. 3–14, 2005. http://idm-lab.org/bib/abstracts/Koen05b.html

