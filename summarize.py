import numpy as np
import glob

# Step 1: Find all test result files
files = sorted(glob.glob("results/test*-results.txt"))
print("Found files:", files)

# Step 2: Helper to extract result sections from file
def extract_results(filename, section):
    with open(filename) as f:
        lines = f.readlines()

    start = None
    for i, line in enumerate(lines):
        if section in line:
            start = i + 1
            break
    if start is None:
        return None

    data = []
    for line in lines[start:]:
        if line.startswith("#"):  # stop at next section
            break
        line = line.strip()
        if line:
            data.append(list(map(float, line.split())))
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
        if data is not None:
            algorithm_data[name].append(data)
        else:
            print(f"Warning: {section} not found in {file}")

# Generate summary tables
with open("results.txt", "w") as f:
    for algo, datasets in algorithm_data.items():
        if not datasets:
            continue

        min_len = min(len(d) for d in datasets)
        datasets = [d[:min_len] for d in datasets]

        stacked = np.stack(datasets, axis=2)  
        N_values = stacked[:, 0, 0].astype(int)
        runtimes = stacked[:, 1, :] 
        avg_runtime = np.mean(runtimes, axis=1)

        table = np.column_stack((N_values, runtimes, avg_runtime))

        # Write to file
        f.write(f"# {algo} Summary\n")
        header = "N Test1 Test2 Test3 Average"
        np.savetxt(f, table, header=header, fmt="%.6f", comments="")
        f.write("\n\n")

    # Create overall summary (compare algorithms)
    f.write("# Summary\n")
    min_len = min(len(algorithm_data["Exhaustive"][0]),
                  len(algorithm_data["Dynamic"][0]),
                  len(algorithm_data["Greedy"][0]))

    N_values = algorithm_data["Exhaustive"][0][:min_len, 0].astype(int)
    avg_exhaustive = np.mean([d[:min_len, 1] for d in algorithm_data["Exhaustive"]], axis=0)
    avg_dynamic = np.mean([d[:min_len, 1] for d in algorithm_data["Dynamic"]], axis=0)
    avg_greedy = np.mean([d[:min_len, 1] for d in algorithm_data["Greedy"]], axis=0)

    summary_table = np.column_stack((N_values, avg_exhaustive, avg_dynamic, avg_greedy))
    header = "N Exhaustive Dynamic Greedy"
    np.savetxt(f, summary_table, header=header, fmt="%d %.6f %.6f %.6f", comments="")

print("✅ results.txt created successfully.")
