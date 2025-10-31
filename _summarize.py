import numpy as np
import glob
import os

# Find all test result files
files = sorted(glob.glob("results/**/results.txt", recursive=True))
print("Found files:", files)

# Function to extract result sections from file
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
        if line.startswith("#"):
            break
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        try:
            N = int(float(parts[0]))       # number of cities
            runtime = float(parts[1])      # runtime (second column)
            data.append([N, runtime])
        except (ValueError, IndexError):
            continue
    return np.array(data)

sections = {
    "Exhaustive": "# Exhaustive Results",
    "Dynamic": "# Dynamic Results",
    "Greedy": "# Greedy Results"
}

# Collect all results per algorithm
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

# Generate summary tables
with open("results.txt", "w") as f:
    wrote_anything = False
    avg_per_algo = {}

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
        avg_runtime = np.mean(runtimes, axis=1)

        avg_per_algo[algo] = np.column_stack((N_values, avg_runtime))

        table = np.column_stack((N_values, runtimes, avg_runtime))
        f.write(f"# {algo} Summary\n")
        np.savetxt(
            f,
            table,
            header="N Test1 Test2 Test3 Average",
            fmt=["%d", "%.6f", "%.6f", "%.6f", "%.6f"],
            comments=""
        )
        f.write("\n\n")

    # Write overall summary (compare average runtimes per algorithm)
    if avg_per_algo:
        f.write("# Summary (Average Runtime per Algorithm)\n")
        N = avg_per_algo["Exhaustive"][:, 0]
        summary_table = np.column_stack([
            N,
            avg_per_algo["Exhaustive"][:, 1],
            avg_per_algo["Dynamic"][:, 1],
            avg_per_algo["Greedy"][:, 1]
        ])
        np.savetxt(
            f,
            summary_table,
            header="N Exhaustive Dynamic Greedy",
            fmt=["%d", "%.6f", "%.6f", "%.6f"],
            comments=""
        )
        f.write("\n")

    if not wrote_anything:
        f.write("# No valid data found.\n")

print("Finished writing summary to results.txt")
