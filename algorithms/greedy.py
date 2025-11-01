# Traveling Salesman Problem using Greedy Algorithm (Nearest Neighbor)
# References:
# - https://youtu.be/RQpFffcI-ZI?si=baHRkECt97xX4WnV
# - https://medium.com/@suryabhagavanchakkapalli/solving-the-traveling-salesman-problem-in-python-using-the-nearest-neighbor-algorithm-48fcf8db289a

def tsp_greedy(D):
  n = len(D)
  
  # Start by marking city 0 as visited.
  visited = [False] * n
  visited[0] = True
  
  # The path starts at city 0
  path = [0]
  total_cost = 0
  
  current_city = 0
  
  # Need to visit n-1 more cities
  for _ in range(n - 1):
    
    # Set the 'nearest_dist' to infinity at the start of each
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
  
  return total_cost, path
