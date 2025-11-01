import numpy as np
import matplotlib.pyplot as plt

# --- Read Summary ---
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

# --- Load summary data ---
N, exhaustive, dynamic, greedy = extract_summary("results.txt")

# Known measured limits
max_exh = 15
max_dyn = 20
max_gre = 30 

# Split measured vs extrapolated regions
mask_exh_meas = N <= max_exh
mask_exh_ext  = N > max_exh
mask_dyn_meas = N <= max_dyn
mask_dyn_ext  = N > max_dyn
mask_gre_meas = N <= max_gre
mask_gre_ext  = N > max_gre

# --- Plot for small N ---
plt.figure(figsize=(10, 6))

plt.plot(N[:10], exhaustive[:10], "o", color="red", label="Exhaustive")
plt.plot(N[:10], dynamic[:10], "o", color="blue", label="Dynamic")
plt.plot(N[:10], greedy[:10], "o", color="green", label="Greedy")

plt.xlabel("Number of Cities (N)")
plt.ylabel("Runtime (seconds)")
plt.title("TSP Algorithm Runtime for Small N")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/small-n.png", dpi=300)
plt.show()

# --- Plot for small N w/o exhaustive ---
plt.figure(figsize=(10, 6))

plt.plot(N[:10], dynamic[:10], "o", color="blue", label="Dynamic")
plt.plot(N[:10], greedy[:10], "o", color="green", label="Greedy")

plt.xlabel("Number of Cities (N)")
plt.ylabel("Runtime (seconds)")
plt.title("TSP Algorithm Runtime for Small N")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/small-n2.png", dpi=300)
plt.show()

# --- Plot for large N ---
plt.figure(figsize=(10, 6))

# Exhaustive
plt.plot(N[mask_exh_meas], exhaustive[mask_exh_meas], "o", color="red", label="Exhaustive (measured)")
if np.any(mask_exh_ext):
    plt.plot(N[mask_exh_ext], exhaustive[mask_exh_ext], "o", color="maroon", label="Exhaustive (extrapolated)")

# Dynamic
plt.plot(N[mask_dyn_meas], dynamic[mask_dyn_meas], "o", color="blue", label="Dynamic (measured)")
if np.any(mask_dyn_ext):
    plt.plot(N[mask_dyn_ext], dynamic[mask_dyn_ext], "o", color="cyan", label="Dynamic (extrapolated)")

# Greedy
plt.plot(N[mask_gre_meas], greedy[mask_gre_meas], "o", color="green", label="Greedy (measured)")
if np.any(mask_gre_ext):
    plt.plot(N[mask_gre_ext], greedy[mask_gre_ext], "o", color="lime", label="Greedy (extrapolated)")

# Labels and styling
plt.xlabel("Number of Cities (N)")
plt.ylabel("Runtime (seconds)")
plt.title("TSP Algorithm Runtime Growth")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/large-n.png", dpi=300)
plt.show()

# --- Plot for large N (log scale) ---
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
plt.title("TSP Algorithm Runtime Growth (Log Scale)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/large-n-logscale.png", dpi=300)
plt.show()
