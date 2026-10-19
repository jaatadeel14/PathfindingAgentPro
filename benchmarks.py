"""Reproducible batch benchmarks for multiple maze sizes and densities."""
import csv, json, random, time
from pathlib import Path
from src.pathfinding import search

OUT = Path(__file__).parent / "outputs"
OUT.mkdir(exist_ok=True)

def make_grid(rows, cols, density, seed):
    rng = random.Random(seed)
    grid = [[1 if rng.random() < density else 0 for _ in range(cols)] for _ in range(rows)]
    grid[0][0] = grid[-1][-1] = 0
    return grid

def render(grid, result, start, goal):
    canvas = [["#" if v else "." for v in row] for row in grid]
    for r, c in result["explored"]:
        if canvas[r][c] == ".": canvas[r][c] = "o"
    for r, c in result["path"]:
        if (r, c) not in (start, goal): canvas[r][c] = "*"
    canvas[start[0]][start[1]] = "S"; canvas[goal[0]][goal[1]] = "G"
    return "\n".join("".join(row) for row in canvas)

def main():
    scenarios = [(20, 20, .10), (20, 20, .20), (30, 30, .20), (35, 35, .25), (50, 50, .20), (60, 60, .30)]
    rows_out = []
    for case, (rows, cols, density) in enumerate(scenarios, 1):
        grid = make_grid(rows, cols, density, seed=900 + case)
        start, goal = (0, 0), (rows - 1, cols - 1)
        actual = sum(sum(row) for row in grid) / (rows * cols)
        for algorithm in ("A*", "Dijkstra"):
            result = search(grid, start, goal, algorithm)
            row = {"case": case, "algorithm": algorithm, "rows": rows, "cols": cols,
                   "obstacle_density": round(actual, 4), "path_found": result["found"],
                   "path_steps": result["steps"], "runtime_ms": round(result["runtime_ms"], 4),
                   "expanded_nodes": result["expanded"], "expanded_node_density": round(result["expanded_density"], 4)}
            rows_out.append(row)
            name = "astar" if algorithm == "A*" else "dijkstra"
            report = (f"Algorithm: {algorithm}\nCase: {case}\nGrid: {rows} x {cols}\n"
                      f"Obstacle density: {actual:.1%}\nPath found: {result['found']}\n"
                      f"Path steps: {result['steps']}\nExpanded nodes: {result['expanded']}\n"
                      f"Expanded node density: {result['expanded_density']:.2%}\n"
                      f"Runtime: {result['runtime_ms']:.4f} ms\n\n"
                      "Legend: S=start, G=goal, #=wall, o=explored, *=path\n\n" + render(grid, result, start, goal))
            (OUT / f"maze_case_{case}_{name}.txt").write_text(report, encoding="utf-8")
    with (OUT / "benchmark_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows_out[0].keys()); writer.writeheader(); writer.writerows(rows_out)
    (OUT / "benchmark_results.json").write_text(json.dumps(rows_out, indent=2), encoding="utf-8")
    print("PATHFINDING BENCHMARK COMPLETE")
    print("Case | Algorithm | Found | Steps | Expanded | Density | Runtime (ms)")
    for r in rows_out:
        print(f"{r['case']:>4} | {r['algorithm']:<9} | {str(r['path_found']):<5} | {str(r['path_steps']):>5} | {r['expanded_nodes']:>8} | {r['expanded_node_density']:.4f} | {r['runtime_ms']:.4f}")
    print(f"\nCSV, JSON and maze logs saved to: {OUT.resolve()}")

if __name__ == "__main__": main()
