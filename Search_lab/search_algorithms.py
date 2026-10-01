import heapq
from collections import deque

def parse_map(ascii_map):
    grid = [list(row) for row in ascii_map]
    start, goal = None, None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'G':
                goal = (r, c)
    return grid, start, goal

def get_neighbors(grid, r, c):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            neighbors.append((nr, nc))
    return neighbors

def bfs_search(ascii_map):
    grid, start, goal = parse_map(ascii_map)
    if not start or not goal: return None, 0, 0
    frontier = deque([start])
    came_from = {start: None}
    visited = {start}
    expanded = 0
    while frontier:
        curr = frontier.popleft()
        expanded += 1
        if curr == goal:
            path = []
            while curr:
                path.append(curr)
                curr = came_from[curr]
            return path[::-1], len(path)-1, expanded
        for nxt in get_neighbors(grid, curr[0], curr[1]):
            if nxt not in visited:
                visited.add(nxt)
                came_from[nxt] = curr
                frontier.append(nxt)
    return None, 0, expanded

def astar_search(ascii_map, heuristic_mult=1.0, use_euclidean=False):
    import math
    grid, start, goal = parse_map(ascii_map)
    if not start or not goal: return None, 0, 0
    def h(pos):
        if use_euclidean:
            return heuristic_mult * math.sqrt((pos[0]-goal[0])**2 + (pos[1]-goal[1])**2)
        return heuristic_mult * (abs(pos[0]-goal[0]) + abs(pos[1]-goal[1]))
    frontier = []
    heapq.heappush(frontier, (0 + h(start), 0, start))
    came_from = {start: None}
    g_score = {start: 0}
    expanded = 0
    visited_for_expansion = set()
    while frontier:
        f, g, curr = heapq.heappop(frontier)
        if curr in visited_for_expansion:
            continue
        visited_for_expansion.add(curr)
        expanded += 1
        if curr == goal:
            path = []
            while curr:
                path.append(curr)
                curr = came_from[curr]
            return path[::-1], len(path)-1, expanded
        for nxt in get_neighbors(grid, curr[0], curr[1]):
            tentative_g = g + 1
            if nxt not in g_score or tentative_g < g_score[nxt]:
                g_score[nxt] = tentative_g
                f_score = tentative_g + h(nxt)
                heapq.heappush(frontier, (f_score, tentative_g, nxt))
                came_from[nxt] = curr
    return None, 0, expanded

if __name__ == "__main__":
    map_orig = [
        "#####################",
        "#S....#............G#",
        "#.##....##########..#",
        "#....##.............#",
        "#.######.###.#.###..#",
        "#........#..........#",
        "#####################",
    ]
    path_bfs, len_bfs, exp_bfs = bfs_search(map_orig)
    path_astar, len_astar, exp_astar = astar_search(map_orig)
    print("--- BFS vs A* (Original Map) ---")
    print(f"BFS: Path Length = {len_bfs}, Expanded = {exp_bfs}")
    print(f"A*:  Path Length = {len_astar}, Expanded = {exp_astar}")
    
    print("\n--- Heuristic Investigations (A*) ---")
    _, l1, e1 = astar_search(map_orig, heuristic_mult=0.0)
    print(f"h(n) = 0: Length = {l1}, Expanded = {e1}")
    _, l2, e2 = astar_search(map_orig, use_euclidean=True)
    print(f"Euclidean: Length = {l2}, Expanded = {e2}")
    _, l3, e3 = astar_search(map_orig, heuristic_mult=2.0)
    print(f"h(n) * 2: Length = {l3}, Expanded = {e3}")
