import numpy as np
import glob
import math

# --- Helper functions ---
def extract_results(filename, section):
    """Extract [N, runtime] pairs from a given algorithm section."""
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
            N = int(float(parts[0]))
            runtime = float(parts[1])
            data.append([N, runtime])
        except (ValueError, IndexError):
            continue
    return np.array(data)


def fit_model(N, T, model_fn):
    """Fit a runtime model T ≈ a * model_fn(N) using least squares."""
    f = model_fn(N)
    a, *_ = np.linalg.lstsq(f[:, None], T, rcond=None)
    a = float(a[0])
    return a, lambda n: a * model_fn(n)


# --- Main summary generation ---
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

# --- Summarize results ---
with open("results.txt", "w") as f:
    avg_per_algo = {}
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
        avg_runtime = np.mean(runtimes, axis=1)

        avg_per_algo[algo] = np.column_stack((N_values, avg_runtime))

        # Save per-algorithm table
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

    # --- Combine into unified summary (up to N = 30) ---
    if avg_per_algo:
        f.write("# Summary (Average Runtime per Algorithm)\n")

        # Step 1: collect real data
        N_exh, T_exh = avg_per_algo["Exhaustive"][:, 0], avg_per_algo["Exhaustive"][:, 1]
        N_dyn, T_dyn = avg_per_algo["Dynamic"][:, 0], avg_per_algo["Dynamic"][:, 1]
        N_gre, T_gre = avg_per_algo["Greedy"][:, 0], avg_per_algo["Greedy"][:, 1]

        # Step 2: fit models for extrapolation
        a_exh, f_exh = fit_model(N_exh, T_exh, lambda n: np.array([math.factorial(int(x)) for x in n]))
        a_dyn, f_dyn = fit_model(N_dyn, T_dyn, lambda n: n**2 * (2**n))
        a_gre, f_gre = fit_model(N_gre, T_gre, lambda n: n**2)

        # Step 3: extend up to N = 30
        N_full = np.arange(4, 31)
        exh_full = np.array([f_exh([n])[0] if n > max(N_exh) else T_exh[n - N_exh[0]] for n in N_full])
        dyn_full = np.array([f_dyn([n])[0] if n > max(N_dyn) else T_dyn[n - N_dyn[0]] for n in N_full])
        gre_full = np.array([f_gre([n])[0] if n > max(N_gre) else T_gre[n - N_gre[0]] for n in N_full])

        # Step 4: write combined summary
        summary_table = np.column_stack((N_full, exh_full, dyn_full, gre_full))
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

print("Finished writing summary with extrapolation to results.txt")
