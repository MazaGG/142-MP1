import numpy as np
import glob

# Find all test result files
files = sorted(glob.glob("results/**/results.txt", recursive=True))
print("Found files:", files)

# Function to extract result sections from file
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
        if line.startswith("#"):
            break
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        try:
            N = int(float(parts[0]))          # number of cities
            runtime = float(parts[1])          # runtime (second column)
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
