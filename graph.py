import numpy as np
import matplotlib.pyplot as plt
import math

# Read the summary
def extract_summary(filename):
    with open(filename) as f:
        lines = f.readlines()

    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("# Summary (Average Runtime"):
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
    return N, exhaustive, dynamic, greedy

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

# Extrapolate for N = 26–50
N_extrap = np.arange(16, 20)
exh_pred = f_exh(N_extrap)
dyn_pred = f_dyn(N_extrap)
gre_pred = f_gre(N_extrap)

# Plot results
plt.figure(figsize=(10, 6))

plt.plot(N, exhaustive, "o", label="Exhaustive (measured)")
plt.plot(N, dynamic, "o", label="Dynamic (measured)")
plt.plot(N, greedy, "o", label="Greedy (measured)")

plt.plot(N_extrap, exh_pred, "o", label="Exhaustive (extrapolated )")
plt.plot(N_extrap, dyn_pred, "o", label="Dynamic (extrapolated )")
plt.plot(N_extrap, gre_pred, "o", label="Greedy (extrapolated )")

plt.xlabel("Number of Cities (N)")
plt.ylabel("Runtime (seconds)")
plt.title("TSP Algorithm Runtimes")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graph.png", dpi=300)
plt.show()
