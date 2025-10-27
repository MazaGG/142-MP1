# Input: nxn distance matrix
# Example: D[i][j] is the distance from city i to city j

# Output: a tour (list of cities) and its cost (tour length)
# Note: The tour should always start and end at city 0
# Example: tour = [0, 2, 3, 1, 0], cost = 10.5

# Sample Input
D = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

def tsp_exhaustive(D):
  return 1