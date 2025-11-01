from algorithms.exhaustive import tsp_exhaustive
from algorithms.dynamic import tsp_dynamic
from algorithms.greedy import tsp_greedy

import numpy as np
import time

# Generate a set of test distance matrices
cities = (np.random.randint(0, 100, (30, 2)))
D = np.linalg.norm(cities[:, np.newaxis] - cities[np.newaxis, :], axis=-1)

# Test Exhaustive Search
print("# Exhaustive Search\n")
exhaustive_results = []
_, _ = tsp_exhaustive(D[:4, :4])  # Warm-up run
for i in range(4,13):
  start = time.time()
  cost, path = tsp_exhaustive(D[:i+1, :i+1])
  end = time.time()
  exhaustive_results.append([i+1, end-start, cost, path]) 
  print(f"N={i+1}, Runtime={end-start:.6f}s, Cost={cost:.2f}, Path={path}")
print("\n")

# Test Dynamic Programming
print("\n# Dynamic Programming\n")
dynamic_results = []
_, _ = tsp_dynamic(D[:4, :4])  # Warm-up run
for i in range(4,25):
  start = time.time()
  cost, path = tsp_dynamic(D[:i+1, :i+1])
  end = time.time()
  dynamic_results.append([i+1, end-start, cost, path]) 
  print(f"N={i+1}, Runtime={end-start:.6f}s, Cost={cost:.2f}, Path={path}")
print("\n")

# Test Greedy Algorithm
print("# Greedy Algorithm\n")
greedy_results = []
_, _ = tsp_greedy(D[:4, :4])  # Warm-up run
for i in range(4,30):
  start = time.time()
  cost, path = tsp_greedy(D[:i+1, :i+1])
  end = time.time()
  greedy_results.append([i+1, end-start, cost, path]) 
  print(f"N={i+1}, Runtime={end-start:.6f}s, Cost={cost:.2f}, Path={path}")
print("\n")

# Save Results to File
with open("results.txt", "w") as f:
    f.write("# Cities\n")
    np.savetxt(f, cities, fmt="%d")

    f.write("\n# Distance Matrix D\n")
    np.savetxt(f, D, fmt="%.2f")

    f.write("\n# Exhaustive Results\n")
    for row in exhaustive_results:
        N, runtime, cost, path = row
        f.write(f"{N} {runtime:.6f} {cost:.2f} {path}\n")

    f.write("\n# Dynamic Results\n")
    for row in dynamic_results:
        N, runtime, cost, path = row
        f.write(f"{N} {runtime:.6f} {cost:.2f} {path}\n")

    f.write("\n# Greedy Results\n")
    for row in greedy_results:
        N, runtime, cost, path = row
        f.write(f"{N} {runtime:.6f} {cost:.2f} {path}\n")
print("Results saved to results.txt")

