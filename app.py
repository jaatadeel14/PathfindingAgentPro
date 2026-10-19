"""Interactive Tkinter GUI for the Pathfinding Agent Search Engine."""
from __future__ import annotations
import csv
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from src.pathfinding import search

ROWS, COLS, CELL = 22, 30, 25
START, GOAL = (1, 1), (ROWS - 2, COLS - 2)
OUT = Path(__file__).parent / "outputs"
OUT.mkdir(exist_ok=True)

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        root.title("Pathfinding Agent | A* vs Dijkstra")
        root.geometry("1120x760")
        root.minsize(960, 680)
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.results = []
        self.active_result = None
        self._style()
        self._build_ui()
        self.draw_grid()

    def _style(self):
        style = ttk.Style()
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground="#172554")
        style.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#475569")
        style.configure("Metric.TLabel", font=("Segoe UI", 11, "bold"), foreground="#0f172a")
        style.configure("TButton", font=("Segoe UI", 10), padding=7)

    def _build_ui(self):
        outer = ttk.Frame(self.root, padding=16)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="PATHFINDING AGENT", style="Title.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Interactive grid search • A* heuristic search • Dijkstra uniform-cost search", style="Sub.TLabel").pack(anchor="w", pady=(2, 12))

        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=(0, 12))
        ttk.Button(controls, text="Run A*", command=lambda: self.run_algorithm("A*")).pack(side="left", padx=(0, 7))
        ttk.Button(controls, text="Run Dijkstra", command=lambda: self.run_algorithm("Dijkstra")).pack(side="left", padx=7)
        ttk.Button(controls, text="Compare Both", command=self.compare).pack(side="left", padx=7)
        ttk.Button(controls, text="Random Maze", command=self.random_maze).pack(side="left", padx=7)
        ttk.Button(controls, text="Clear Walls", command=self.clear_walls).pack(side="left", padx=7)
        ttk.Button(controls, text="Export CSV + JSON", command=self.export_results).pack(side="right")

        content = ttk.Frame(outer)
        content.pack(fill="both", expand=True)
        left = ttk.Frame(content)
        left.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(left, width=COLS*CELL, height=ROWS*CELL, bg="white", highlightthickness=1, highlightbackground="#cbd5e1")
        self.canvas.pack(anchor="nw", fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.toggle_wall)

        right = ttk.Frame(content, padding=(18, 0, 0, 0), width=245)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)
        ttk.Label(right, text="RUN METRICS", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))
        self.metric_vars = {}
        for key, label in [("algorithm", "Algorithm"), ("found", "Path found"), ("steps", "Path steps"), ("runtime_ms", "Runtime (ms)"), ("expanded", "Expanded nodes"), ("expanded_density", "Expanded density")]:
            box = ttk.LabelFrame(right, text=label, padding=8)
            box.pack(fill="x", pady=4)
            var = tk.StringVar(value="—")
            self.metric_vars[key] = var
            ttk.Label(box, textvariable=var, style="Metric.TLabel").pack(anchor="w")
        ttk.Separator(right).pack(fill="x", pady=12)
        ttk.Label(right, text="LEGEND", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        for color, text in [("#16a34a", "Start"), ("#dc2626", "Goal"), ("#334155", "Obstacle"), ("#bfdbfe", "Explored node"), ("#f59e0b", "Final shortest path")]:
            line = ttk.Frame(right); line.pack(fill="x", pady=3)
            swatch = tk.Canvas(line, width=18, height=18, highlightthickness=0)
            swatch.create_rectangle(1, 1, 17, 17, fill=color, outline=color); swatch.pack(side="left")
            ttk.Label(line, text=text).pack(side="left", padx=8)
        ttk.Label(outer, text="Tip: Click cells to add/remove walls. Start and goal positions are fixed. Obstacles are never placed over them.", style="Sub.TLabel").pack(anchor="w", pady=(10, 0))
        self.status = tk.StringVar(value="Ready. Choose an algorithm or click Compare Both.")
        ttk.Label(outer, textvariable=self.status, style="Sub.TLabel").pack(anchor="w", pady=(4, 0))

    def draw_grid(self, result=None):
        self.canvas.delete("all")
        explored = set(result["explored"]) if result else set()
        path = set(result["path"]) if result else set()
        for r in range(ROWS):
            for c in range(COLS):
                coord = (r, c)
                x1, y1 = c*CELL, r*CELL
                color = "#ffffff"
                if self.grid[r][c]: color = "#334155"
                if coord in explored and not self.grid[r][c]: color = "#bfdbfe"
                if coord in path: color = "#f59e0b"
                if coord == START: color = "#16a34a"
                if coord == GOAL: color = "#dc2626"
                self.canvas.create_rectangle(x1, y1, x1+CELL, y1+CELL, fill=color, outline="#e2e8f0", width=1)
                if coord in (START, GOAL):
                    self.canvas.create_text(x1+CELL/2, y1+CELL/2, text="S" if coord == START else "G", fill="white", font=("Segoe UI", 10, "bold"))

    def toggle_wall(self, event):
        c, r = event.x // CELL, event.y // CELL
        if not (0 <= r < ROWS and 0 <= c < COLS): return
        if (r, c) in (START, GOAL): return
        self.grid[r][c] = 0 if self.grid[r][c] else 1
        self.active_result = None
        self.draw_grid()
        self.status.set("Maze edited. Run an algorithm to refresh metrics.")

    def run_algorithm(self, name):
        result = search(self.grid, START, GOAL, name)
        self.active_result = result
        self.draw_grid(result)
        self.show_metrics(result)
        self.results.append(self.as_export_row(result, "interactive"))
        self.status.set(f"{name}: path found in {result['steps']} steps." if result["found"] else f"{name}: no path exists for this maze.")

    def compare(self):
        a = search(self.grid, START, GOAL, "A*")
        d = search(self.grid, START, GOAL, "Dijkstra")
        self.results.extend([self.as_export_row(a, "interactive"), self.as_export_row(d, "interactive")])
        self.active_result = a
        self.draw_grid(a)
        self.show_metrics(a)
        if a["found"] and d["found"]:
            self.status.set(f"Comparison complete. A*: {a['steps']} steps, {a['expanded']} expanded; Dijkstra: {d['steps']} steps, {d['expanded']} expanded. Showing A* path.")
        else:
            self.status.set("Comparison complete. At least one algorithm could not reach the goal. Showing A* exploration.")
        messagebox.showinfo("Algorithm comparison", self.comparison_text(a, d))

    def comparison_text(self, a, d):
        return (f"A* Search\n  Path found: {a['found']}\n  Path steps: {a['steps']}\n  Expanded nodes: {a['expanded']}\n  Runtime: {a['runtime_ms']:.4f} ms\n\n"
                f"Dijkstra\n  Path found: {d['found']}\n  Path steps: {d['steps']}\n  Expanded nodes: {d['expanded']}\n  Runtime: {d['runtime_ms']:.4f} ms\n\n"
                "The highlighted grid shows A*. Runtime can vary between runs.")

    def show_metrics(self, result):
        values = {"algorithm": result["algorithm"], "found": "Yes" if result["found"] else "No",
                  "steps": str(result["steps"]) if result["steps"] is not None else "N/A",
                  "runtime_ms": f"{result['runtime_ms']:.4f}", "expanded": str(result["expanded"]),
                  "expanded_density": f"{result['expanded_density']:.2%}"}
        for key, value in values.items(): self.metric_vars[key].set(value)

    def random_maze(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                if (r, c) not in (START, GOAL) and random.random() < 0.25:
                    self.grid[r][c] = 1
        self.active_result = None
        self.draw_grid()
        self.status.set("Random maze generated (approximately 25% obstacle probability).")

    def clear_walls(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.active_result = None
        self.draw_grid()
        self.status.set("All obstacles cleared.")

    def as_export_row(self, result, source):
        return {"source": source, "algorithm": result["algorithm"], "rows": ROWS, "cols": COLS,
                "path_found": result["found"], "path_steps": result["steps"],
                "expanded_nodes": result["expanded"], "expanded_node_density": round(result["expanded_density"], 6),
                "runtime_ms": round(result["runtime_ms"], 6),
                "obstacle_density": round(sum(sum(row) for row in self.grid)/(ROWS*COLS), 6)}

    def export_results(self):
        if not self.results:
            messagebox.showwarning("No results", "Run A*, Dijkstra or Compare Both before exporting.")
            return
        csv_path = filedialog.asksaveasfilename(title="Save benchmark CSV", defaultextension=".csv", initialfile="pathfinding_benchmarks.csv", filetypes=[("CSV files", "*.csv")])
        if not csv_path: return
        json_path = str(Path(csv_path).with_suffix(".json"))
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
            writer.writeheader(); writer.writerows(self.results)
        Path(json_path).write_text(json.dumps(self.results, indent=2), encoding="utf-8")
        messagebox.showinfo("Export complete", f"Saved files:\n{csv_path}\n{json_path}")

if __name__ == "__main__":
    root = tk.Tk()
    PathfindingApp(root)
    root.mainloop()
