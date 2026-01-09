"""
Project Name: WDW-Transit-Optimizer
File Name: tsp.py
Description: TSP functions for pathfinding algorithms.
Author: Joseph Lefkovitz (github.com/lefkovitzj)
Last Modified: 1/9/2026
"""

def tsp_solver(adj_matrix, start_node, end_node, interested_nodes):
    """ Held-Karp implementation with fixed start and end. """
    nodes = list(interested_nodes)
    n = len(nodes)

    # Bitmask (performance optimal over list) of visited nodes.
    memoization = {}

    def visit(bitmask, current_node):
        """ Recursive DP node visitation. """
        # Base case - bitmask all 1s.
        if bitmask == (1 << n) - 1:
            return adj_matrix[current_node].get(end_node, float('inf')), None

        # Check for already computed answer.
        state = (bitmask, current_node)
        if state in memoization:
            return memoization[state]

        # Standard selection.
        best_cost = float('inf')
        best_next = None

        for i in range(n):
            next_node = nodes[i]
            # Check stop i has not been visited yet (0 in bitmask).
            if not (bitmask & (1 << i)):
                # Compute costs.
                cost_to_next = adj_matrix[current_node].get(next_node, float('inf'))
                future_cost, _ = visit(bitmask | (1 << i), next_node)

                total_cost = cost_to_next + future_cost

                # Cost selection when applicable.
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_next = i

        memoization[state] = (best_cost, best_next)
        return best_cost, best_next

    # Begin recursion with start_node.
    global_min_cost, _ = visit(0, start_node)

    # Path reconstruction backtracking.
    optimized_order = [start_node]
    current_bitmask = 0
    current_node = start_node

    while current_bitmask < ((1 << n) - 1):
        # Retrieve next index from DP solution.
        _, next_index = memoization[(current_bitmask, current_node)]
        if next_index is None:
            # Path does not exist.
            break
        next_node = nodes[next_index]
        optimized_order.append(next_node)

        # Update bitmask and node for next iteration.
        current_bitmask |= (1 << next_index)
        current_node = next_node

    optimized_order.append(end_node)

    return optimized_order, global_min_cost
