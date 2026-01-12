from utils import get_minimal_dist_matrix, stitch_itinerary
from tsp import tsp_solver

def simulate_greedy(matrix, start, end, stops):
    current = start
    unvisited = list(stops)
    path = [start]
    total_cost = 0
    
    while unvisited:
        # Greedy always picks the absolute closest next stop
        next_node = min(unvisited, key=lambda x: matrix[current][x])
        total_cost += matrix[current][next_node]
        path.append(next_node)
        unvisited.remove(next_node)
        current = next_node
        
    total_cost += matrix[current][end]
    path.append(end)
    return path, total_cost

def run_greedy_trap_test():
    # Simple WDW Graph
    graph = {
        'AoA': {
            'Yacht': {'weight': 5, 'mode': 'Bus'},    # CLOSE: Greedy will go here first
            'MK': {'weight': 15, 'mode': 'Bus'}       # FARTHER: TSP will likely choose this
        },
        'Yacht': {
            'AoA': {'weight': 5, 'mode': 'Bus'},
            'Beach': {'weight': 2, 'mode': 'Walk'},   # The End!
            'MK': {'weight': 40, 'mode': 'Bus'}       # HUGE PENALTY for backtracking
        },
        'MK': {
            'Poly': {'weight': 5, 'mode': 'Monorail'},
            'AoA': {'weight': 15, 'mode': 'Bus'},
            'Yacht': {'weight': 40, 'mode': 'Bus'}
        },
        'Poly': {
            'MK': {'weight': 5, 'mode': 'Monorail'},
            'Beach': {'weight': 40, 'mode': 'Bus'}    # Huge penalty to finish from here
        },
        'Beach': {
            'Yacht': {'weight': 2, 'mode': 'Walk'}
        }
    }

    # Keep these the same:
    start = 'AoA'
    end = 'Beach'
    must_visit = ['Poly', 'MK', 'Yacht']

    print("--- Running Greedy Trap Test ---")
    interested = [start, end] + must_visit
    matrix, all_parents = get_minimal_dist_matrix(graph, interested)
    
    optimized_order, total_time = tsp_solver(matrix, start, end, must_visit)
    
    print(f"TSP Optimal Route: {' -> '.join(optimized_order)}")
    print(f"Total Time: {total_time} mins")

    greedy_path, greedy_cost = simulate_greedy(matrix, start, end, must_visit)
    optimized_order, tsp_cost = tsp_solver(matrix, start, end, must_visit)

    print(f"Greedy Path: {' -> '.join(greedy_path)} | Cost: {greedy_cost}")
    print(f"TSP Path:    {' -> '.join(optimized_order)} | Cost: {tsp_cost}")

    if tsp_cost < greedy_cost:
        print("✅ TSP wins!")
    elif tsp_cost == greedy_cost:
        print("🤝 Tie (Greedy found the optimal path by luck)")
    else:
        print("❌ TSP logic error")
    # 3. Use the Stitcher to reveal every single node visited
    full_path = stitch_itinerary(optimized_order, all_parents)

    # 4. Print the results
    print(f"--- FULL ITINERARY (Total: {total_time} mins) ---")
    for i, (location, mode) in enumerate(full_path):
        if mode is None:
            print(f"{i}. Start at {location}")
        else:
            print(f"{i}. Take {mode} to {location}")
            
run_greedy_trap_test()