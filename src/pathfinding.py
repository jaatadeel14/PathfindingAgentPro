"""Pathfinding algorithms implemented from scratch for a four-way grid."""
from __future__ import annotations
import heapq
import time
from typing import Callable

Coord = tuple[int, int]
Grid = list[list[int]]  # 0 = free, 1 = obstacle


def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(node: Coord, grid: Grid):
    rows, cols = len(grid), len(grid[0])
    for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        nr, nc = node[0] + dr, node[1] + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            yield nr, nc


def reconstruct_path(parent: dict[Coord, Coord], goal: Coord) -> list[Coord]:
    path = [goal]
    while path[-1] in parent:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def search(grid: Grid, start: Coord, goal: Coord, algorithm: str) -> dict:
    """Run A* or Dijkstra. Returns path, explored nodes, runtime and metrics."""
    if algorithm not in {"A*", "Dijkstra"}:
        raise ValueError("algorithm must be 'A*' or 'Dijkstra'")
    began = time.perf_counter()
    counter = 0
    start_priority = manhattan(start, goal) if algorithm == "A*" else 0
    frontier = [(start_priority, counter, start)]
    parent: dict[Coord, Coord] = {}
    distance = {start: 0}
    closed: set[Coord] = set()
    expanded_order: list[Coord] = []

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in closed:
            continue
        if current == goal:
            elapsed = (time.perf_counter() - began) * 1000
            path = reconstruct_path(parent, goal)
            total_cells = len(grid) * len(grid[0])
            return {
                "algorithm": algorithm,
                "found": True,
                "path": path,
                "steps": len(path) - 1,
                "expanded": len(expanded_order),
                "expanded_density": len(expanded_order) / total_cells,
                "runtime_ms": elapsed,
                "explored": expanded_order,
            }
        closed.add(current)
        expanded_order.append(current)
        for nxt in neighbors(current, grid):
            new_cost = distance[current] + 1
            if new_cost < distance.get(nxt, float("inf")):
                distance[nxt] = new_cost
                parent[nxt] = current
                counter += 1
                priority = new_cost
                if algorithm == "A*":
                    priority += manhattan(nxt, goal)
                heapq.heappush(frontier, (priority, counter, nxt))

    elapsed = (time.perf_counter() - began) * 1000
    total_cells = len(grid) * len(grid[0])
    return {
        "algorithm": algorithm,
        "found": False,
        "path": [],
        "steps": None,
        "expanded": len(expanded_order),
        "expanded_density": len(expanded_order) / total_cells,
        "runtime_ms": elapsed,
        "explored": expanded_order,
    }
