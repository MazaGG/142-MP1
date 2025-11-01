import numpy as np
import glob
import math

# Function to extract results
def extract_results(filename, section):
    with open(filename) as f:
        lines = f.readlines()

    start = None
    for i, line in enumerate(lines):
        if section in line.strip():
            start = i + 1
            break
    if start is None:
        return None

    data = []
    for line in lines[start:]:
        if line.startswith("#") or not line.strip():
            break
        parts = line.split(None, 3)
        try:
            N = int(float(parts[0]))
            runtime = float(parts[1])
            cost = float(parts[2])
            data.append([N, runtime, cost])
        except (ValueError, IndexError):
            continue
    return np.array(data)

# Function to fit model
def fit_model(N, T, model_fn):
    f = model_fn(N)
    a, *_ = np.linalg.lstsq(f[:, None], T, rcond=None)
    a = float(a[0])
    return a, lambda n: a * model_fn(n)

# Save summarized results to results.txt
files = sorted(glob.glob("results/**/results.txt", recursive=True))
print("Found files:", files)

sections = {
    "Exhaustive": "# Exhaustive Results",
    "Dynamic": "# Dynamic Results",
    "Greedy": "# Greedy Results"
}

algorithm_data = {}
for name, section in sections.items():
    algorithm_data[name] = []
    for file in files:
        data = extract_results(file, section)
        if data is not None and len(data) > 0:
            algorithm_data[name].append(data)
            print(f"Parsed {file} for {name}: {data.shape}")
        else:
            print(f"Warning: no data found for {name} in {file}")

with open("results.txt", "w") as f:
    avg_per_algo = {}
    cost_per_algo = {}
    wrote_anything = False

    for algo, datasets in algorithm_data.items():
        if not datasets:
            f.write(f"# {algo} Summary\nNo data found.\n\n")
            continue

        wrote_anything = True
        min_len = min(len(d) for d in datasets)
        datasets = [d[:min_len] for d in datasets]

        stacked = np.stack(datasets, axis=2)
        N_values = stacked[:, 0, 0].astype(int)
        runtimes = stacked[:, 1, :]
        costs = stacked[:, 2, :]
        avg_runtime = np.mean(runtimes, axis=1)
        avg_cost = np.mean(costs, axis=1)

        avg_per_algo[algo] = np.column_stack((N_values, avg_runtime))
        cost_per_algo[algo] = np.column_stack((N_values, avg_cost))

        table = np.column_stack((N_values, runtimes, avg_runtime, avg_cost))
        f.write(f"# {algo} Summary\n")
        np.savetxt(
            f,
            table,
            header="N Test1 Test2 Test3 AvgRuntime AvgCost",
            fmt=["%d", "%.6f", "%.6f", "%.6f", "%.6f", "%.3f"],
            comments=""
        )
        f.write("\n\n")

    # Runtime summary
    if avg_per_algo:
        f.write("# Summary (Average Runtime per Algorithm)\n")
        N = avg_per_algo["Exhaustive"][:, 0]
        summary_table = np.column_stack([
            N,
            avg_per_algo["Exhaustive"][:, 1],
            avg_per_algo["Dynamic"][:, 1],
            avg_per_algo["Greedy"][:, 1],
        ])
        np.savetxt(
            f,
            summary_table,
            header="N Exhaustive Dynamic Greedy",
            fmt=["%d", "%.6f", "%.6f", "%.6f"],
            comments=""
        )
        f.write("\n")

    # Cost summary
    if "Dynamic" in cost_per_algo and "Greedy" in cost_per_algo:
        dyn_cost = cost_per_algo["Dynamic"][:, 1]
        gre_cost = cost_per_algo["Greedy"][:, 1]
        N = cost_per_algo["Dynamic"][:, 0]
        percent_error = (gre_cost - dyn_cost) / dyn_cost * 100

        f.write("# Summary (Average Cost Comparison)\n")
        summary_cost = np.column_stack([N, dyn_cost, gre_cost, percent_error])
        np.savetxt(
            f,
            summary_cost,
            header="N Dynamic_Cost Greedy_Cost Percent_Error(%)",
            fmt=["%d", "%.3f", "%.3f", "%.2f"],
            comments=""
        )
        f.write("\n")

print("Finished writing results.txt with runtime + cost summaries")
