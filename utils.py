"""
Project Name: WDW-Transit-Optimizer
File Name: utils.py
Description: Utility functions for pathfinding algorithms.
Author: Joseph Lefkovitz (github.com/lefkovitzj)
Last Modified: 1/8/2026
"""
import heapq

def djikstra(graph, start):
    """
    Mode-Aware Dijkstra's algorithm to find the shortest paths from start to all other nodes.
    Expects graph format: { node: { neighbor: { 'weight': int, 'mode': str } } }
    """
    queue = [(0, start)]
    min_cost = {start: 0}
    # Stores (parent, mode)
    best_path = {start: (None, None)}

    while queue:
        current_cost, current_node = heapq.heappop(queue)

        if current_cost > min_cost.get(current_node, float('inf')):
            continue

        for neighbor, edge_data in graph.get(current_node, {}).items():
            # weight and mode are extracted from the edge metadata
            weight = edge_data['weight']
            mode = edge_data['mode']

            new_cost = current_cost + weight

            if new_cost < min_cost.get(neighbor, float('inf')):
                min_cost[neighbor] = new_cost
                best_path[neighbor] = (current_node, mode)
                heapq.heappush(queue, (new_cost, neighbor))

    return min_cost, best_path

def reconstruct_path(best_path, start, end):
    """
    Reconstructs a single path.
    """
    path = []
    curr = end
    while curr is not None:
        parent, mode = best_path.get(curr, (None, None))
        path.append((curr, mode))
        curr = parent

    path.reverse()

    if path and path[0][0] == start:
        return path
    return []

def calculate_total_cost(graph, path_with_modes):
    """
    Calculates total time for a path of (node, mode) tuples.
    """
    total_cost = 0
    for i in range(len(path_with_modes) - 1):
        u = path_with_modes[i][0]
        v = path_with_modes[i+1][0]
        # Access weight from the nested dictionary structure
        edge_data = graph.get(u, {}).get(v)
        if edge_data:
            total_cost += edge_data['weight']
    return total_cost
