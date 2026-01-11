"""
Project Name: WDW-Transit-Optimizer
File Name: app/core/graph.py
Description: Graph-related utilities for the WDW Transit Optimizer application.
Author: Joseph Lefkovitz (github.com/lefkovitzj)
Last Modified: 1/10/2026
"""

# Python standard library imports
import heapq
import json
from typing import List

# Local imports
from app.core.config import settings

class GraphManager:
    def __init__(self):
        self.display_names, self.graph = self._load_data()
        self.valid_stops = {
            name: loc_id for name, loc_id in self.display_names.items() 
            if loc_id.endswith("_MAIN")
        }

    def _load_data(self):
        """Loads graph and display names from the specified JSON file."""
        # Load the graph data from the JSON file specified in settings.
        with open(settings.GRAPH_DATA_PATH, 'r') as f:
            data = json.load(f)

        display_names = data.get("display_names", {})
        adjacency_list = {}

        # Parse all connections in graph data.
        for connection in data.get("connections", []):
            src = connection["from"]
            dest = connection["to"]
            weight = connection["weight"]
            mode = connection["mode"]

            if src not in adjacency_list:
                # Handle new source nodes.
                adjacency_list[src] = {}
            adjacency_list[src][dest] = {"weight": weight, "mode": mode}

            # Handle bidirectional edges.
            if connection.get("bidirectional", False):
                if dest not in adjacency_list:
                    # Handle new source node for reverse direction.
                    adjacency_list[dest] = {}
                adjacency_list[dest][src] = {"weight": weight, "mode": mode}

        return display_names, adjacency_list

    def _djikstra(self, start):
        """
        Mode-Aware Dijkstra's algorithm to find the shortest paths from start to all other nodes.
        Expects self.graph format: { node: { neighbor: { 'weight': int, 'mode': str } } }
        """
        queue = [(0, start)]
        min_cost = {start: 0}
        # Stores (parent, mode)
        best_path = {start: (None, None)}

        while queue:
            current_cost, current_node = heapq.heappop(queue)

            if current_cost > min_cost.get(current_node, float('inf')):
                continue

            for neighbor, edge_data in self.graph.get(current_node, {}).items():
                # weight and mode are extracted from the edge metadata
                weight = edge_data['weight']
                mode = edge_data['mode']

                new_cost = current_cost + weight

                if new_cost < min_cost.get(neighbor, float('inf')):
                    min_cost[neighbor] = new_cost
                    best_path[neighbor] = (current_node, mode)
                    heapq.heappush(queue, (new_cost, neighbor))

        return min_cost, best_path

    def _get_minimal_dist_matrix(self, interested_nodes):
        """
        Constructs the distance matrix for TSP and captures all parent 
        pointers for final path reconstruction.
        """
        min_dist_matrix = {}
        all_parents = {} 

        for node in interested_nodes:
            min_costs, parents = self._djikstra(node)
            all_parents[node] = parents
            min_dist_matrix[node] = {
                n: min_costs[n] for n in interested_nodes if n in min_costs
            }

        return min_dist_matrix, all_parents

    def _tsp_solver(self, adj_matrix, start_node, end_node, interested_nodes):
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

    def _stitch_itinerary(self, optimized_order, all_parents):
        """
        Reconstructs the final itinerary including the mode of transport.
        Returns a list of tuples: (node, mode_to_reach_node)
        """
        if not optimized_order:
            return []

        full_itinerary = []

        for i in range(len(optimized_order) - 1):
            start_node = optimized_order[i]
            end_node = optimized_order[i+1]

            parents = all_parents.get(start_node, {})
            segment = []
            curr = end_node

            while curr is not None:
                prev_node, mode = parents.get(curr, (None, None))
                # We store the node and the mode used to arrive AT this node
                segment.append((curr, mode))
                curr = prev_node

            segment.reverse()

            if i == 0:
                full_itinerary.extend(segment)
            else:
                # Skip the first element to avoid doubling up on the resort node
                full_itinerary.extend(segment[1:])

        return full_itinerary

    def plan_itinerary(self, start: str, end: str, stops: List[str]):
        """ Create a planned itinerary given start, end, and must-visit stops. """
        interested = [start, end] + stops
        matrix, all_parents = self._get_minimal_dist_matrix(interested)
        optimized_order, total_time = self._tsp_solver(matrix, start, end, stops)
        full_itinerary = self._stitch_itinerary(optimized_order, all_parents)
        return {
            "itinerary": full_itinerary,
            "total_time": total_time,
            "optimized_order": optimized_order
        }
