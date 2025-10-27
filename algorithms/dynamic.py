import numpy as np

# Traveling Salesman Problem using Dynamic Programming (Held-Karp Algorithm)
# Reference: https://rosettacode.org/wiki/Held%E2%80%93Karp_algorithm
def tsp_dynamic(D):
    n = len(D)
    DP = np.full((1 << n, n), np.inf)
    parent = np.full((1 << n, n), -1, dtype=int)

    DP[1][0] = 0  # start at city 0

    for S in range(1 << n):
        for u in range(n):
            if DP[S][u] == np.inf:
                continue
            for v in range(n):
                if S & (1 << v) == 0:  # city v not yet visited
                    next_mask = S | (1 << v)
                    new_cost = DP[S][u] + D[u][v]
                    if new_cost < DP[next_mask][v]:
                        DP[next_mask][v] = new_cost
                        parent[next_mask][v] = u  # record previous city

    # Final step: close the tour (return to city 0)
    all_visited = (1 << n) - 1
    min_cost = np.inf
    last_city = -1

    for u in range(1, n):
        cost = DP[all_visited][u] + D[u][0]
        if cost < min_cost:
            min_cost = cost
            last_city = u

    # Reconstruct path
    path = [0] * n
    mask = all_visited
    current = last_city

    for i in range(n - 1, 0, -1):
        path[i] = current
        prev = parent[mask][current]
        mask = mask ^ (1 << current)  # remove current from mask
        current = prev

    path[0] = 0  # start city
    path.append(0)  # return to start
    path = list(map(int, path))

    return min_cost, path

# ------------------------------------------------------------------
# Sample Input
# D = [
#     [0, 10, 15, 20],
#     [10, 0, 35, 25],
#     [15, 35, 0, 30],
#     [20, 25, 30, 0]
# ]

# # Sample Output
# cost, tour = tsp_dynamic(D)
# print("Cost:", cost)
# print("Tour:", tour)