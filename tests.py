from algorithms.exhaustive import tsp_exhaustive
from algorithms.dynamic import tsp_dynamic
from algorithms.greedy import tsp_greedy

from tabulate import tabulate
import numpy as np
import time

# Generate a set of test distance matrices
cities = (np.random.randint(0, 100, (30, 2)))
D = np.round(np.linalg.norm(cities[:, np.newaxis] - cities[np.newaxis, :], axis=-1))

# Test Exhaustive Search
print("\Exhaustive Search\n")
exhaustive_results = []
for i in range(4,15):
  start = time.time()
  cost, path = tsp_exhaustive(D[:i+1, :i+1])
  end = time.time()
  exhaustive_results.append([i+1, end-start, cost, path]) 
  print(f"N={i+1}, Runtime={end-start:.6f}s, Cost={cost}, Path={path}")
print("\n")

# Test Dynamic Programming
print("\nDynamic Programming\n")
dynamic_results = []
for i in range(4,15):
  start = time.time()
  cost, path = tsp_dynamic(D[:i+1, :i+1])
  end = time.time()
  dynamic_results.append([i+1, end-start, cost, path]) 
  print(f"N={i+1}, Runtime={end-start:.6f}s, Cost={cost}, Path={path}")
print("\n")

# Test Greedy Algorithm
print("\Greedy Algorithm\n")
greedy_results = []
for i in range(4,15):
  start = time.time()
  cost, path = tsp_greedy(D[:i+1, :i+1])
  end = time.time()
  greedy_results.append([i+1, end-start, cost, path]) 
  print(f"N={i+1}, Runtime={end-start:.6f}s, Cost={cost}, Path={path}")
print("\n")

# Save Results to File
with open("results.txt", "w") as f:
  f.write("# Distance Matrix D\n")
  np.savetxt(f, D, fmt="%d")
  f.write("\n# Exhaustive Results\n")
  np.savetxt(f, exhaustive_results, fmt="%.6f")
  f.write("\n# Dynamic Results\n")
  np.savetxt(f, dynamic_results, fmt="%.6f")
  f.write("\n# Greedy Results\n")
  np.savetxt(f, greedy_results, fmt="%.6f")

