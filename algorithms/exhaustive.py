import itertools

# Traveling Salesman Problem using Exhaustive Search
# Reference: https://www.geeksforgeeks.org/dsa/traveling-salesman-problem-tsp-implementation/
def tsp_exhaustive(D):
    n = len(D)
    cities = list(range(1, n))

    min_cost = float("inf")
    best_path = []

    # Try every permutation of the remaining cities
    for perm in itertools.permutations(cities):
        path = [0] + list(perm) + [0]  # start and end at city 0
        cost = sum(D[path[i]][path[i + 1]] for i in range(n))

        if cost < min_cost:
            min_cost = cost
            best_path = path

    return min_cost, best_path
