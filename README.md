# Pathfinding Agent Search Engine

An interactive maze-navigation project implementing **A* Search** and **Dijkstra's Algorithm** from scratch. It includes a desktop GUI, editable grid obstacles, live search visualization, reproducible benchmark scenarios, and CSV/JSON/text exports.

## Features
- Interactive 22 x 30 grid: click cells to add or remove walls.
- Start and goal cells are fixed and protected from obstacle placement.
- Run A*, Dijkstra, or compare both on the same maze.
- Visualize explored nodes and the final path.
- Track path steps, runtime, expanded nodes, expanded-node density, and obstacle density.
- Export benchmark results to CSV and JSON.
- Batch test multiple maze sizes and obstacle probabilities.
- ASCII visualization logs generated for each batch test.
- Uses Python standard library only; no `pip install` required.

## Requirements
- Python 3.10+ recommended.
- Tkinter must be available in the Python installation (normally included with Python on Windows).

## Run the interactive application
Open this folder in VS Code, open **Terminal → New Terminal**, then run:

```bash
python app.py
```

On Windows, if needed:

```bash
py app.py
```

## Run the batch benchmark
```bash
python benchmarks.py
```

This creates `outputs/benchmark_results.csv`, `outputs/benchmark_results.json`, and text maze logs for each algorithm/scenario.

## Legend
- `S`: start
- `G`: goal
- `#`: obstacle/wall
- `o`: expanded/explored node
- `*`: final path

In the GUI, these states are shown with colors and a legend.

## Algorithm notes
### A* Search
Uses `f(n) = g(n) + h(n)`, where `g(n)` is the cost from the start and `h(n)` is Manhattan distance to the goal. With four-direction movement, unit step costs, and this admissible heuristic, A* finds an optimal path when one exists.

### Dijkstra's Algorithm
Uses `f(n) = g(n)` and expands the lowest known cumulative-cost node first. It also finds an optimal path for this unweighted/unit-cost grid.

## Metrics
- **Path steps:** number of moves in the returned route (`number of path cells - 1`).
- **Runtime (ms):** measured using `time.perf_counter`; small values vary across runs and computers.
- **Expanded nodes:** nodes expanded before the goal is popped from the frontier.
- **Expanded-node density:** expanded nodes divided by total grid cells. This is a normalized search-effort measure and may exceed 100% in some graph definitions, though it should not here because nodes are closed once.
- **Obstacle density:** obstacle cells divided by all grid cells.

## Project structure
```text
PathfindingAgentPro/
├── app.py
├── benchmarks.py
├── README.md
├── src/
│   ├── __init__.py
│   └── pathfinding.py
└── outputs/                 # generated after running
```

## Limitations
- Four-direction movement only; diagonal moves are not enabled.
- All traversable moves have the same cost (1).
- The GUI visualizes A* when using **Compare Both**, while a dialog compares metrics for both algorithms.
- Batch mazes are seeded for repeatable layouts; runtime can still vary.
