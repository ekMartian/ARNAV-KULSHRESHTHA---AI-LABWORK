# Laboratory Exercise – Search and A*

## Task 0: Understand the Search Problem
* **State $S$**: The $(x, y)$ coordinate of the robot in the grid.
* **Actions $A$**: Up, Down, Left, Right.
* **Transition $T$**: $T(s, a) = s'$ where $s'$ is the adjacent cell in the direction of $a$.
* **Initial state $s_0$**: The coordinate of `S`.
* **Goal $G$**: The coordinate of `G`.
* **Cost $c$**: Cost of 1 per valid transition.

(a) **What information is necessary to specify a state?** The row and column coordinates.
(b) **What makes an action invalid?** If the adjacent cell is out of bounds or is an obstacle `#`.
(c) **Is this a deterministic search problem?** Yes, actions always result in the expected adjacent cell.
(d) **What would constitute a solution?** A sequence of valid actions resulting in a path from $S$ to $G$.

## Task 4: Inspect the A* Algorithm
* **State**: Tuples of `(row, col)`.
* **Action**: Delta tuples `(-1,0), (1,0), (0,-1), (0,1)`.
* **Transition**: Adding the action delta to the current state tuple.
* **Goal test**: `if curr == goal:`
* **$g(n)$**: The `g` or `tentative_g` variable tracking path length from start.
* **$h(n)$**: The Manhattan distance function `h(pos)`.
* **$f(n)$**: The `f_score` variable, sum of $g$ and $h$.
* **Frontier**: A priority queue (min-heap) implemented with Python's `heapq`.
* **Visited states**: The `visited_for_expansion` set and `g_score` dictionary.
* **Path reconstruction**: Tracing backward using the `came_from` dictionary from goal to start.

(a) **What data structure is used for the A* frontier?** A min-heap (Priority Queue).
(b) **How does the program select the next state to expand?** By popping the element with the lowest $f(n)$ from the heap.
(c) **Where is the heuristic calculated?** In the inner function `h(pos)`.
(d) **Does the program explicitly calculate $f(n) = g(n) + h(n)$?** Yes, via `f_score = tentative_g + h(nxt)`.
(e) **How does the program prevent unnecessary repeated exploration?** By maintaining a `g_score` mapping and a `visited_for_expansion` set to only expand a state if we found a strictly shorter path to it.

## Task 5: Compare A* with Blind Search
| Measure | BFS | A* |
| :--- | :--- | :--- |
| Solution found | Yes | Yes |
| Path length | 33 | 33 |
| States expanded | 87 | 37 |

(a) **Did both algorithms find a solution?** Yes.
(b) **Did they find paths of the same length?** Yes, both are optimal (length 33).
(c) **Which algorithm expanded fewer states?** A* (37 compared to BFS's 87).
(d) **Why might A* expand fewer states?** A* uses the heuristic $h(n)$ to prioritize expanding states that are physically closer to the goal, avoiding exploration in opposite directions (unlike BFS, which explores equally in all directions).

## Task 6: Investigate the Heuristic
**Appropriateness of Manhattan distance**: Since the robot can only move horizontally and vertically (no diagonals), the Manhattan distance perfectly matches the geometry of the grid and represents the exact shortest path length without obstacles. Thus, it is admissible (never overestimates).

* **$h(n) = 0$**: Path Length = 33, Expanded = 87 (Degenerates into BFS/Dijkstra).
* **Euclidean distance**: Path Length = 33, Expanded = 45 (Admissible, but less informed than Manhattan, so it expands slightly more nodes).
* **$h(n) \times 2$**: Path Length = 33, Expanded = 34 (Becomes inadmissible. It can theoretically return a suboptimal path, though it returned the optimal path in this specific grid geometry by heavily prioritizing the goal direction).

## Final Reflection
1. **Formulating the search problem** ensures you clearly define the state space, transition rules, and costs, which are required mathematically before you can apply generic search algorithms.
2. **A* is an "informed" search algorithm** because it uses problem-specific knowledge (the heuristic) to guide the search towards the goal, rather than searching blindly.
3. **The choice of heuristic matters** because it dictates the trade-off between optimality and search speed. An admissible heuristic guarantees the shortest path, while a tighter (closer to true cost) heuristic drastically reduces the number of states expanded.
4. **The LLM contributed** to the engineering process by rapidly producing the boilerplate code for the BFS and A* implementations, priority queue management, and path reconstruction logic.
5. **If an engineer accepts LLM-generated code without testing**, edge cases (like unreachable goals or cycles) might cause infinite loops, or the path returned might be suboptimal if the heuristic or cost tracking was implemented incorrectly.
