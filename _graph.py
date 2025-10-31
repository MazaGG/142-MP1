import numpy as np
import matplotlib.pyplot as plt
import math

# Read the summary
def extract_summary(filename):
    with open(filename) as f:
        lines = f.readlines()

    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("# Summary (Average Runtime per Algorithm)"):
            start = i + 2  # skip header line
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
    print(N, exhaustive, dynamic, greedy)
    return N, exhaustive, dynamic, greedy

# Read the input data
def extract_cities(filename):
    with open(filename) as f:
        lines = f.readlines()

    data = []
    for line in lines[1:]:
        line = line.strip()
        if not line or line.startswith("#"):
            break
        data.append(list(map(float, line.split())))
    
    data = np.array(data)
    return data

# Read the paths
def extract_paths(filename, algo):
    with open(filename) as f:
        lines = f.readlines()
    
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith(f"# {algo} Results"):
            start = i + 1
            break
    if start is None:
        raise ValueError(f"{algo} section not found")

    data = []
    for line in lines[start:]:
        line = line.strip()
        if not line or line.startswith("#"):
            break
        parts = line.split(None, 3)
        try:
            path_str = " ".join(parts[3:])
            path = eval(path_str)
            data.append(path)
        except (ValueError, IndexError, SyntaxError):
            continue
    
    # Convert to rectangular NumPy array (pad shorter ones)
    max_len = max(len(p) for p in data)
    matrix = np.full((len(data), max_len), -1, dtype=int)
    for i, path in enumerate(data):
        matrix[i, :len(path)] = path
    return matrix


# Define model fitting
def fit_model(N, T, model_fn):
    f = model_fn(N)
    a, *_ = np.linalg.lstsq(f[:, None], T, rcond=None)
    a = float(a[0])
    return a, lambda n: a * model_fn(n)

# Load data
N, exhaustive, dynamic, greedy = extract_summary("results.txt")

# Fit models to measured data
a_exh, f_exh = fit_model(N, exhaustive, lambda n: np.array([math.factorial(int(x)) for x in n]))
a_dyn, f_dyn = fit_model(N, dynamic, lambda n: n**2 * (2**n))
a_gre, f_gre = fit_model(N, greedy, lambda n: n**2)

# Extrapolate for N = 16–30
N_extrap = np.arange(16, 30)
exh_pred = f_exh(N_extrap)
dyn_pred = f_dyn(N_extrap)
gre_pred = f_gre(N_extrap)

# Plot small N
plt.figure(figsize=(10, 6))

# plt.plot(N[:10], exhaustive[:10], "-o", color="red", label="Exhaustive (measured)")
plt.plot(N[:10], dynamic[:10], "-o", color="blue", label="Dynamic (measured)")
plt.plot(N[:10], greedy[:10], "-o", color="green", label="Greedy (measured)")

plt.xlabel("Number of Cities (N)")
plt.ylabel("Runtime (seconds)")
plt.title("TSP Algorithm Runtimes for Small N")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/small-n.png", dpi=300)
plt.show()

# Plot log scale for small N
plt.figure(figsize=(10, 6))

plt.plot(N[:10], exhaustive[:10], "-o", color="red", label="Exhaustive (measured)")
plt.plot(N[:10], dynamic[:10], "-o", color="blue", label="Dynamic (measured)")
plt.plot(N[:10], greedy[:10], "-o", color="green", label="Greedy (measured)")

plt.yscale("log")
plt.xlabel("Number of Cities (N)")
plt.ylabel("Runtime (log scale)")
plt.title("TSP Algorithm Runtimes for Small N")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/logscale.png", dpi=300)
plt.show()

# Plot big N
plt.figure(figsize=(10, 6))

# Plot measured data
plt.plot(N, exhaustive, "o", color="red", label="Exhaustive (measured)")
plt.plot(N, dynamic, "o", color="blue", label="Dynamic (measured)")
plt.plot(N, greedy, "o", color="green", label="Greedy (measured)")

N_cont = np.linspace(N.min(), 30, 300)
exh_fit = f_exh(N_cont)
dyn_fit = f_dyn(N_cont)
gre_fit = f_gre(N_cont)

plt.plot(N_cont, exh_fit, "-", color="lightcoral", label="Exhaustive (fitted curve)")
plt.plot(N_cont, dyn_fit, "-", color="cornflowerblue", label="Dynamic (fitted curve)")
plt.plot(N_cont, gre_fit, "-", color="limegreen", label="Greedy (fitted curve)")

plt.xlabel("Number of Cities (N)")
plt.ylabel("Runtime (seconds)")
plt.title("TSP Algorithm Runtime Growth up to N = 30 (Fitted Models)")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/fitted-curves.png", dpi=300)
plt.show()
