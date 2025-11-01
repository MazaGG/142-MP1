import numpy as np
import matplotlib.pyplot as plt
import glob
import ast
import os

# Function to extract summary data
def extract_summary(filename):
    with open(filename) as f:
        lines = f.readlines()

    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("# Summary (Average Runtime per Algorithm)"):
            start = i + 2  # skip header
            break
    if start is None:
        raise ValueError("Summary section not found")

    data = []
    for line in lines[start:]:
        line = line.strip()
        if not line or line.startswith("#"):
            break
        data.append(list(map(float, line.split())))

    data = np.array(data)
    N = data[:, 0].astype(int)
    exhaustive = data[:, 1]
    dynamic = data[:, 2]
    greedy = data[:, 3]
    return N, exhaustive, dynamic, greedy

# Function to extract city coordinates
def extract_cities(filename):
    with open(filename) as f:
        lines = f.readlines()

    cities = []
    for line in lines:
        if line.strip().startswith("# Distance Matrix"):
            break
        if not line.strip() or line.strip().startswith("#"):
            continue
        parts = line.strip().split()
        if len(parts) == 2 and all(p.replace('.', '', 1).isdigit() for p in parts):
            cities.append(list(map(float, parts)))
    return np.array(cities)

# Function to extract path for a given algorithm and N
def extract_path(filename, algo, N_target):
    with open(filename) as f:
        lines = f.readlines()

    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith(f"# {algo} Results"):
            start = i + 1
            break
    if start is None:
        raise ValueError(f"{algo} Results not found in {filename}")

    for line in lines[start:]:
        if not line.strip() or line.startswith("#"):
            break
        parts = line.strip().split(None, 3)
        if len(parts) < 4:
            continue
        try:
            N = int(parts[0])
            if N == N_target:
                path_str = parts[3]
                return ast.literal_eval(path_str)
        except Exception:
            continue
    raise ValueError(f"No path found for N={N_target} in {algo} of {filename}")

# Function to plot TSP path
def plot_path(cities, path, color, algo, test_name, N_target):
    plt.figure(figsize=(8, 6))
    ax = plt.gca()

    ordered = cities[path]
    ax.plot(ordered[:, 0], ordered[:, 1], "-o", color=color, label=f"{algo} Path")
    for i, (x, y) in enumerate(cities):
        ax.text(x + 1, y + 1, str(i), fontsize=8, color="black")

    plt.title(f"{algo} TSP Path for N={N_target}")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    os.makedirs("graphs", exist_ok=True)
    output_file = f"graphs/{test_name}-{algo.lower()}-path-N{N_target}.png"
    plt.savefig(output_file, dpi=300)
    plt.close()
    print(f"Saved → {output_file}")

# Load summary data
N, exhaustive, dynamic, greedy = extract_summary("results.txt")

# Define maximum N for measured data
max_exh = 10
max_dyn = 15
max_gre = 20 

# Split measured vs extrapolated regions
mask_exh_meas = N <= max_exh
mask_exh_ext  = N > max_exh
mask_dyn_meas = N <= max_dyn
mask_dyn_ext  = N > max_dyn
mask_gre_meas = N <= max_gre
mask_gre_ext  = N > max_gre

# ----------------------------- PLOTTING ----------------------------- 

# Plot for small N
plt.figure(figsize=(10, 6))

plt.plot(N[:6], exhaustive[:6], "o", color="red", label="Exhaustive")
plt.plot(N[:6], dynamic[:6], "o", color="blue", label="Dynamic")
plt.plot(N[:6], greedy[:6], "o", color="green", label="Greedy")

plt.xlabel("Number of Cities (N)")
plt.ylabel("Runtime (seconds)")
plt.title("TSP Algorithm Runtime for Small N")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/small-n.png", dpi=300)
plt.show()

# Plot for small N (zoomed in)
plt.figure(figsize=(10, 6))
MAX_Y = 0.002 

plt.plot(N[:6][(exhaustive[:6] < MAX_Y)], exhaustive[:6][(exhaustive[:6] < MAX_Y)], "o", color="red", label="Exhaustive")
plt.plot(N[:6][(dynamic[:6] < MAX_Y)], dynamic[:6][(dynamic[:6] < MAX_Y)], "o", color="blue", label="Dynamic")
plt.plot(N[:6][(greedy[:6] < MAX_Y)], greedy[:6][(greedy[:6] < MAX_Y)], "o", color="green", label="Greedy")

plt.ylim(top=MAX_Y)
plt.xlabel("Number of Cities (N)")
plt.ylabel("Runtime (seconds)")
plt.title("TSP Algorithm Runtime for Small N (Zoomed In)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/small-n-zoomed.png", dpi=300)
plt.show()

# Plot for large N
plt.figure(figsize=(10, 6))

plt.plot(N[mask_exh_meas], exhaustive[mask_exh_meas], "o", color="red", label="Exhaustive (measured)")
if np.any(mask_exh_ext):
    plt.plot(N[mask_exh_ext], exhaustive[mask_exh_ext], "o", color="maroon", label="Exhaustive (extrapolated)")
plt.plot(N[mask_dyn_meas], dynamic[mask_dyn_meas], "o", color="blue", label="Dynamic (measured)")
if np.any(mask_dyn_ext):
    plt.plot(N[mask_dyn_ext], dynamic[mask_dyn_ext], "o", color="cyan", label="Dynamic (extrapolated)")
plt.plot(N[mask_gre_meas], greedy[mask_gre_meas], "o", color="green", label="Greedy (measured)")
if np.any(mask_gre_ext):
    plt.plot(N[mask_gre_ext], greedy[mask_gre_ext], "o", color="lime", label="Greedy (extrapolated)")

plt.xlabel("Number of Cities (N)")
plt.ylabel("Runtime (seconds)")
plt.title("TSP Algorithm Runtime for Large N")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/large-n.png", dpi=300)
plt.show()

# Plot for large N (log scale)
plt.figure(figsize=(10, 6))

plt.plot(N[mask_exh_meas], exhaustive[mask_exh_meas], "o", color="red", label="Exhaustive (measured)")
if np.any(mask_exh_ext):
    plt.plot(N[mask_exh_ext], exhaustive[mask_exh_ext], "o", color="maroon", label="Exhaustive (extrapolated)")
plt.plot(N[mask_dyn_meas], dynamic[mask_dyn_meas], "o", color="blue", label="Dynamic (measured)")
if np.any(mask_dyn_ext):
    plt.plot(N[mask_dyn_ext], dynamic[mask_dyn_ext], "o", color="cyan", label="Dynamic (extrapolated)")
plt.plot(N[mask_gre_meas], greedy[mask_gre_meas], "o", color="green", label="Greedy (measured)")
if np.any(mask_gre_ext):
    plt.plot(N[mask_gre_ext], greedy[mask_gre_ext], "o", color="lime", label="Greedy (extrapolated)")

plt.yscale("log")
plt.xlabel("Number of Cities (N)")
plt.ylabel("Runtime (log scale)")
plt.title("TSP Algorithm Runtime for Large N (Log Scale)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/large-n-logscale.png", dpi=300)
plt.show()

# Plot of paths for each test case (N = 10)
N_target = 10 
result_files = sorted(glob.glob("results/test*-results/results.txt"))
os.makedirs("graphs", exist_ok=True)

for file in result_files:
    folder_name = os.path.basename(os.path.dirname(file)) 
    test_name = folder_name.replace("test", "Test ").replace("-results", "")
    print(f"Processing {test_name}...")

    cities = extract_cities(file)
    cities_n = cities[:N_target]

    for algo, color in [("Dynamic", "blue"), ("Greedy", "green")]:
        try:
            path = extract_path(file, algo, N_target)
            plot_path(cities_n, path, color, algo, test_name, N_target)
        except ValueError as e:
            print(f"Skipping {algo} for {test_name}: {e}")

print("Finished generating all test plots.")

# Plot of paths for each test case (N = 15)
N_target = 15
result_files = sorted(glob.glob("results/test*-results/results.txt"))
os.makedirs("graphs", exist_ok=True)

for file in result_files:
    folder_name = os.path.basename(os.path.dirname(file)) 
    test_name = folder_name.replace("test", "Test ").replace("-results", "")
    print(f"Processing {test_name}...")

    cities = extract_cities(file)
    cities_n = cities[:N_target]

    for algo, color in [("Dynamic", "blue"), ("Greedy", "green")]:
        try:
            path = extract_path(file, algo, N_target)
            plot_path(cities_n, path, color, algo, test_name, N_target)
        except ValueError as e:
            print(f"Skipping {algo} for {test_name}: {e}")

print("Finished generating all test plots.")
