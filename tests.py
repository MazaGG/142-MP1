from algorithms.dynamic import tsp_dynamic
# from algorithms.exhaustive import tsp_exhaustive
# from algorithms.greedy import tsp_greedy

from tabulate import tabulate
import numpy as np
import time

# Generate a set of test distance matrices
cities = (np.random.randint(0, 100, (30, 2)))
D = np.round(np.linalg.norm(cities[:, np.newaxis] - cities[np.newaxis, :], axis=-1))

# Test Exhaustive Search
# print("\Exhaustive Search\n")
# exhaustive_results = []
# for i in range(4,30):
#   start = time.time()
#   cost, path = tsp_exhaustive(D[:i+1, :i+1])
#   end = time.time()
#   exhaustive_results.append([i+1, end-start, cost, path]) 
# print(tabulate(exhaustive_results, headers=["N", "Runtime", "Cost", "Path"], tablefmt="simple"))
# print("\n")

# Test Dynamic Programming
print("\nDynamic Programming\n")
dynamic_results = []
for i in range(4,25):
  start = time.time()
  cost, path = tsp_dynamic(D[:i+1, :i+1])
  end = time.time()
  dynamic_results.append([i+1, end-start, cost, path]) 
  print(f"N={i+1}, Runtime={end-start:.6f}s, Cost={cost}, Path={path}")
print("\n")

# Test Greedy Algorithm
# print("\Greedy Algorithm\n")
# greedy_results = []
# for i in range(4,30):
#   start = time.time()
#   cost, path = tsp_dynamic(D[:i+1, :i+1])
#   end = time.time()
#   greedy_results.append([i+1, end-start, cost, path]) 
# print(tabulate(greedy_results, headers=["N", "Runtime", "Cost", "Path"], tablefmt="simple"))
# print("\n")

with open("results.txt", "w") as f:
    # f.write("Exhaustive Search Results\n")
    # f.write(tabulate(exhaustive_results, headers=["N", "Runtime", "Cost", "Path"], tablefmt="simple"))
    # f.write("\n\n")
    f.write("Dynamic Programming Results\n")
    f.write(tabulate(dynamic_results, headers=["N", "Runtime", "Cost", "Path"], tablefmt="simple"))
    f.write("\n\n")
    # f.write("Greedy Algorithm Results\n")
    # f.write(tabulate(greedy_results, headers=["N", "Runtime", "Cost", "Path"], tablefmt="simple"))
    # f.write("\n\n")
print("Results saved to results.txt")

