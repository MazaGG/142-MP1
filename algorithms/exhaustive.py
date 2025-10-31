def tsp_exhaustive(D):
  n = len(D)
  
  # A set of cities that still need to be visited.
  # We only need to find permutations for cities 1 through n-1.
  remaining_cities = set(range(1, n))
  
  # Use mutable lists to store the minimum cost and best path
  # so they can be updated by the nested recursive function.
  min_cost = [float('inf')]
  best_tour = [[]]
  
  def find_path(current_city, current_path, current_cost, remaining):
    """
    Recursive helper function to explore all possible paths
    using a decrease-by-one approach.
    
    current_city: The last city visited
    current_path: The list of cities visited so far (e.g., [0, 2])
    current_cost: The cost of that path so far
    remaining: A set of unvisited cities
    """
    
    # Base Case: No more cities are left to visit.
    # This means 'current_path' holds a full permutation (e.g., [0, 2, 1, 3])
    if not remaining:
      # Calculate the final cost by adding the trip back to city 0
      total_cost = current_cost + D[current_city][0]
      
      # If this path is the best one found so far, save it.
      if total_cost < min_cost[0]:
        min_cost[0] = total_cost
        best_tour[0] = current_path + [0] # Add 0 to complete the tour
      return

    # Recursive Step (Decrease-by-One)
    # Iterate over all cities still left to visit.
    # We use list(remaining) to "freeze" the set for iteration
    # while we modify the set in the recursive call.
    for next_city in list(remaining):
      
      # 1. "Decrease" the problem:
      # Create a new set of remaining cities *without* the 'next_city'.
      new_remaining = remaining - {next_city}
      
      new_cost = current_cost + D[current_city][next_city]
      
      # Pruning: If the path *so far* is already worse than the
      # best *complete* path we've found, don't bother continuing
      # down this branch.
      if new_cost < min_cost[0]:
        # 2. "Recurse" on the smaller problem:
        # Find the best path from 'next_city' visiting all 'new_remaining'.
        find_path(
            next_city,
            current_path + [next_city],
            new_cost,
            new_remaining
        )
      
      # 3. "Unchoose" is handled automatically because we pass
      # *new* sets/lists to the recursion. The 'remaining' set
      # in *this* function's loop is not modified.

  # --- Start the search ---
  # We always start at city 0.
  initial_path = [0]
  initial_cost = 0
  
  # Call the recursive function to start the process.
  find_path(0, initial_path, initial_cost, remaining_cities)
  
  # After all permutations are checked, return the best one found.
  return min_cost[0], best_tour[0]

