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


# Function to fit model and extrapolate
def fit_model(N, T, model_fn):
    f = model_fn(N)
    a, *_ = np.linalg.lstsq(f[:, None], T, rcond=None)
    a = float(a[0])
    return a, lambda n: a * model_fn(n)

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

# Output File 
with open("results.txt", "w") as f:
    avg_per_algo = {}
    cost_per_algo = {}
    wrote_anything = False

    # Summary per Algorithm
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

        avg_per_algo[algo] = np.column_stack((N_values, avg_runtime))

        table = np.column_stack((N_values, runtimes, avg_runtime))
        f.write(f"# {algo} Summary\n")
        np.savetxt(
            f,
            table,
            header="N Test1 Test2 Test3 AvgRuntime",
            fmt=["%d", "%.6f", "%.6f", "%.6f", "%.6f"],
            comments=""
        )
        f.write("\n\n")

    f.write("# Summary (Average Runtime per Algorithm)\n")

    N_max = 30
    all_N = np.arange(5, N_max + 1)

    models = {
        "Exhaustive": lambda n: np.array([math.factorial(int(x)) for x in n]),
        "Dynamic": lambda n: np.array([x**2 * (2**x) for x in n]),
        "Greedy": lambda n: np.array([x**2 for x in n])
    }

    extrapolated = {}

    for algo in ["Exhaustive", "Dynamic", "Greedy"]:
        if algo not in avg_per_algo:
            continue

        N = avg_per_algo[algo][:, 0]
        T = avg_per_algo[algo][:, 1]
        model_fn = models[algo]
        a, f_model = fit_model(N, T, model_fn)
        extrapolated[algo] = f_model(all_N)

    summary_table = np.column_stack([
        all_N,
        extrapolated["Exhaustive"],
        extrapolated["Dynamic"],
        extrapolated["Greedy"]
    ])

    np.savetxt(
        f,
        summary_table,
        header="N Exhaustive Dynamic Greedy",
        fmt=["%d", "%.6f", "%.6f", "%.6f"],
        comments=""
    )
    f.write("\n")

    # Cost Comparison per Test
    test_files = sorted(glob.glob("results/test*-results/results.txt"))
    percent_errors_all = []

    for test_idx, file in enumerate(test_files, start=1):
        print(f"Processing cost summary for {file}...")

        dyn_data = extract_results(file, "# Dynamic Results")
        gre_data = extract_results(file, "# Greedy Results")

        if dyn_data is None or gre_data is None:
            print(f"Skipping {file}: missing data.")
            continue

        dyn_N, dyn_costs = dyn_data[:, 0], dyn_data[:, 2]
        gre_N, gre_costs = gre_data[:, 0], gre_data[:, 2]
        common_N = np.intersect1d(dyn_N, gre_N)

        mask = (common_N >= 5) & (common_N <= 25)
        common_N = common_N[mask]

        dyn_costs_aligned = np.array([dyn_costs[dyn_N == n][0] for n in common_N])
        gre_costs_aligned = np.array([gre_costs[gre_N == n][0] for n in common_N])

        percent_error = (gre_costs_aligned - dyn_costs_aligned) / dyn_costs_aligned * 100
        percent_errors_all.append(percent_error)

        f.write(f"# Test {test_idx} Cost Comparison (N = 5–25)\n")
        summary_cost = np.column_stack([common_N, dyn_costs_aligned, gre_costs_aligned, percent_error])
        np.savetxt(
            f,
            summary_cost,
            header="N Exact_Cost Greedy_Cost Percent_Error(%)",
            fmt=["%d", "%.2f", "%.2f", "%.2f"],
            comments=""
        )
        f.write("\n")

    # Average %Error Across All Tests
    if percent_errors_all:
        avg_error = np.mean(np.vstack(percent_errors_all), axis=0)
        avg_N = common_N 
        f.write("# Average Percent Error Across Tests\n")
        avg_table = np.column_stack([avg_N, avg_error])
        np.savetxt(
            f,
            avg_table,
            header="N Average_%Error",
            fmt=["%d", "%.2f"],
            comments=""
        )
        f.write("\n")


print("Finished writing results.txt with runtime extrapolated to N=30 and cost summary up to N=25")
