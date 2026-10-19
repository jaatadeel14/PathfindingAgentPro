# Project Report: Heuristic Graph Pathfinding Agent Search Engine

## Objective
Build and evaluate a grid-based virtual agent that navigates around obstacles using informed and uninformed shortest-path search.

## Implemented algorithms
- **A* Search:** prioritizes `g(n) + h(n)`, using Manhattan distance as the heuristic.
- **Dijkstra's Algorithm:** prioritizes `g(n)`, the cost accumulated from the start.

Both algorithms are implemented directly in `src/pathfinding.py` using Python's `heapq` priority queue. Each movement is four-directional and has cost 1.

## Experimental method
The batch benchmark evaluates six reproducible maze configurations ranging from 20x20 to 60x60, with different obstacle probabilities. Each algorithm records whether a path exists, route length, runtime, expanded-node count, expanded-node density, and obstacle density. Text-based visualizations are saved for every algorithm/scenario pair.

## Sample run results
The included benchmark run produced the following observations:
- In the first five test cases, both algorithms found a path and returned the same route length.
- A* expanded fewer nodes than Dijkstra in each of those five reachable cases.
- In the sixth, denser 60x60 maze, both algorithms correctly reported that no path was available for the generated obstacle layout.
- Runtime was measured with `time.perf_counter()` and should be treated as a machine-specific observation, not a guaranteed performance figure.

## Metrics
- **Path steps:** number of moves from start to goal.
- **Runtime:** elapsed search time in milliseconds.
- **Expanded nodes:** nodes expanded by the algorithm before success or frontier exhaustion.
- **Expanded-node density:** expanded nodes divided by the total number of grid cells.
- **Obstacle density:** blocked cells divided by all grid cells.

## Conclusion
The test run demonstrates shortest-path agreement between A* and Dijkstra when a route exists. The Manhattan heuristic helps A* focus its search toward the destination, and the benchmark records the amount of search work rather than relying on runtime alone. Dense mazes can be disconnected, so correctly reporting failure to find a path is also part of robust agent behavior.

## How to reproduce
Run `python app.py` for the interactive desktop interface, or `python benchmarks.py` for the repeatable batch benchmark. Outputs are written to `outputs/`.
