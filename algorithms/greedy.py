# Input: nxn distance matrix
# Example: D[i][j] is the distance from city i to city j

# Output: a tour (list of cities) and its cost (tour length)
# Note: The tour should always start and end at city 0
# Example: tour = [0, 2, 3, 1, 0], cost = 10.5

def tsp_greedy(D):
  n = len(D)
  
  # A list to keep track of which cities have been visited.
  # Start by marking city 0 as visited.
  visited = [False] * n
  visited[0] = True
  
  # The path starts at city 0
  path = [0]
  total_cost = 0
  
  current_city = 0
  
  # Need to visit n-1 more cities
  for _ in range(n - 1):
    
    # Set the 'nearest_dist' to infinity at the *start* of each
    # search for the next city. This guarantees that the first
    # unvisited city checked will be "nearer" than infinity.
    nearest_dist = float('inf')
    nearest_city = -1
    
    # Look through all possible "next" cities
    for next_city in range(n):
      # Check if it's unvisited AND it's closer than the
      # current "nearest" one found so far
      if not visited[next_city] and D[current_city][next_city] < nearest_dist:
        nearest_dist = D[current_city][next_city]
        nearest_city = next_city
        
    # After checking all cities, 'nearest_city' is the one
    # with the minimum distance.
    
    # Now, "travel" to that city
    path.append(nearest_city)
    visited[nearest_city] = True
    total_cost += nearest_dist
    current_city = nearest_city
    
  # After visiting all cities, return to the start (city 0)
  total_cost += D[current_city][0]
  path.append(0)
  
  # Return the final cost and the path taken
  return total_cost, path

# # ------------------------------------------------------------------
# # Sample Input
D = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

# # Sample Output
# Tracing the output:
# 1. Start at 0. Path: [0]
# 2. From 0, nearest is 1 (cost 10). total_cost=10. Path: [0, 1]
# 3. From 1, nearest unvisited is 3 (cost 25). total_cost=35. Path: [0, 1, 3]
# 4. From 3, nearest unvisited is 2 (cost 30). total_cost=65. Path: [0, 1, 3, 2]
# 5. All visited. Return to 0. From 2, cost to 0 is 15. total_cost=80. Path: [0, 1, 3, 2, 0]

cost, tour = tsp_greedy(D)
print("Cost:", cost)
print("Tour:", tour)
