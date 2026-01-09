import json

class TransitGraph():
    def __init__(self, size):
        """ Initialize the data structure. """
        self.adj_nodes = [ ([0] * size) for i in range(size)]
        self.adj_node_descriptions = [ ([""] * size) for i in range(size)]
        self.size = size
        self.node_data = [""] * size # Store the name.
        self.node_description = [""] * size # Store the description.
    def add_node(self, index, name, description):
        """ Add a new node to the graph. """
        if 0 <= index < self.size:
            self.node_data[index] = name
            self.node_description[index] = description
    def add_adj(self, index_from, index_to, weight, description):
        """ Add a new vertex between two nodes at a set weight. """
        if 0 <= index_from < self.size and 0<= index_from < self.size:
            self.adj_nodes[index_from][index_to] = weight
            self.adj_node_descriptions[index_from][index_to] = description
    def dijkstra(self, start_node_name):
        """Run Dijkstra's algorithm to compute shortest distances and paths."""
        start_node_index = self.node_data.index(start_node_name)
        distances = [float("inf")] * self.size
        predecessors = [-1] * self.size  # Keeps track of the path
        distances[start_node_index] = 0
        visited = [False] * self.size

        for _ in range(self.size):
            min_distance = float("inf")
            current_node = None
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    current_node = i

            if current_node is None:
                break
            visited[current_node] = True

            for neighbor in range(self.size):
                if self.adj_nodes[current_node][neighbor] != 0 and not visited[neighbor]:
                    alt = distances[current_node] + self.adj_nodes[current_node][neighbor]
                    if alt < distances[neighbor]:
                        distances[neighbor] = alt
                        predecessors[neighbor] = current_node

        # Function to reconstruct the path
        def get_path(target_node_index):
            path = []
            while target_node_index != -1:
                path.insert(0, self.node_data[target_node_index])
                target_node_index = predecessors[target_node_index]
            return path

        # Return both distances and paths for all nodes
        result = {self.node_data[i]: (distances[i], get_path(i)) for i in range(self.size)}
        return result



if __name__ == "__main__":
    locs = []
    monorails = [
        ("Ticket & Transportation Center - Resort Monorail", "Disney's Polynesian Village Resort - Resort Monorail", 4, "Resort Monorail", False),
        ("Disney's Polynesian Village Resort - Resort Monorail", "Disney's Grand Floridian Resort & Spa - Resort Monorail", 4, "Resort Monorail", False),
        ("Disney's Grand Floridian Resort & Spa - Resort Monorail", "Magic Kingdom - Resort Monorail", 4, "Resort Monorail", False),
        ("Magic Kingdom - Resort Monorail", "Disney's Contemporary Resort - Resort Monorail", 4, "Resort Monorail", False),
        ("Disney's Contemporary Resort - Resort Monorail", "Ticket & Transportation Center - Resort Monorail", 4, "Resort Monorail", False),
        ("Ticket & Transportation Center - Express Monorail", "Magic Kingdom - Express Monorail", 7, "Express Monorail", False),
        ("Magic Kingdom - Express Monorail", "Ticket & Transportation Center - Express Monorail", 5, "Express Monorail", False),
        ("Ticket & Transportation Center - Epcot Monorail", "Epcot - Epcot Monorail", 10, "Epcot Monorail", True),
    ]
    busses = []
    boats = [
        ("Ticket & Transportation Center - Ferry", "Magic Kingdom", 11, "Ferry", True),

        ("Disney's Polynesian Village - Gold Flag Launch", "Magic Kingdom - Gold Flag Launch", 7, "Gold Flag Launch", False),
        ("Disney's Grand Floridian Resort & Spa - Gold Flag Launch", "Disney's Polynesian Village - Gold Flag Launch", 7, "Gold Flag Launch", False),
        ("Magic Kingdom - Gold Flag Launch", "Disney's Grand Floridian Resort & Spa - Gold Flag Launch", 7, "Gold Flag Launch", False),

        ("Magic Kingdom - Green Flag Launch", "Disney's Fort Wilderness Resort & Campground - Green Flag Launch", 15, "Gold Flag Launch", True),

        ("Disney's Wilderness Lodge Resort - Red Flag Launch", "Magic Kingdom - Red Flag Launch", 7, "Red Flag Launch", True),

        ("Disney's Contemporary Resort - Blue Flag Launch", "Disney's Fort Wilderness Resort & Campground - Blue Flag Launch", 7, "Blue Flag Launch", True),
        ("Disney's Wilderness Lodge Resort - Blue Flag Launch", "Disney's Fort Wilderness Resort & Campground - Blue Flag Launch", 7, "Blue Flag Launch", True),
        ("Disney's Wilderness Lodge Resort - Blue Flag Launch", "Disney's Contemporary Resort - Blue Flag Launch", 7, "Blue Flag Launch", True),

        ("Hollywood Studios - Crescent Lake Friendship Boat to Epcot", "Swan and Dolphin Hotel - Crescent Lake Friendship Boat to Epcot", 8, "Crescent Lake Friendship Boat to Epcot", False),
        ("Swan and Dolphin Hotel - Crescent Lake Friendship Boat to Epcot", "Disney's Yacht and Beach Club Resorts - Crescent Lake Friendship Boat to Epcot", 8, "Crescent Lake Friendship Boat to Epcot", False),
        ("Disney's Yacht and Beach Club Resorts - Crescent Lake Friendship Boat to Epcot", "Disney's Boardwalk Inn - Crescent Lake Friendship Boat to Epcot", 8, "Crescent Lake Friendship Boat to Epcot", False),
        ("Disney's Boardwalk Inn - Crescent Lake Friendship Boat to Epcot", "Epcot International Gateway - Crescent Lake Friendship Boat to Epcot", 8, "Crescent Lake Friendship Boat to Epcot", False),

        ("Swan and Dolphin Hotel - Crescent Lake Friendship Boat to Hollywood Studios", "Hollywood Studios - Crescent Lake Friendship Boat to Hollywood Studios", 8, "Crescent Lake Friendship Boat to Hollywood Studios", False),
        ("Disney's Yacht and Beach Club Resorts - Crescent Lake Friendship Boat to Hollywood Studios", "Swan and Dolphin Hotel - Crescent Lake Friendship Boat to Hollywood Studios", 8, "Crescent Lake Friendship Boat to Hollywood Studios", False),
        ("Disney's Boardwalk Inn - Crescent Lake Friendship Boat to Hollywood Studios", "Disney's Yacht and Beach Club Resorts - Crescent Lake Friendship Boat to Hollywood Studios", 8, "Crescent Lake Friendship Boat to Hollywood Studios", False),
        ("Epcot International Gateway - Crescent Lake Friendship Boat to Hollywood Studios", "Disney's Boardwalk Inn - Crescent Lake Friendship Boat to Hollywood Studios", 8, "Crescent Lake Friendship Boat to Hollywood Studios", False),

        ("Disney's Port Orleans French Quarter Resort - Purple Flag Sassagoula River Ferry Boat", "Disney Springs Marketplace - Purple Flag Sassagoula River Ferry Boat", 20, "Purple Flag Sassagoula River Ferry Boat", True),
        ("Disney's Port Orleans Riverside Resort - Yellow Flag Sassagoula River Ferry Boat", "Disney Springs Marketplace - Yellow Flag Sassagoula River Ferry Boat", 17, "Yellow Flag Sassagoula River Ferry Boat", True),
        ("Disney's Saratogoa Springs Resort and Tree Houses - Blue Flag Sassagoula River Ferry Boat", "Disney Springs Landing - Blue Flag Sassagoula River Ferry Boat", 15, "Blue Flag Sassagoula River Ferry Boat", True),
        ("Disney's Old Key West Resort - Green Flag Sassagoula River Ferry Boat", "Disney Springs Landing - Green Flag Sassagoula River Ferry Boat", 10, "Green Flag Sassagoula River Ferry Boat", True),

    ]
    skyliners = [
        ("Disney's Caribbean Beach Resort - Epcot Skyliner", "Disney Vacation Club Riviera Resort - Epcot Skyliner", 4, "Epcot Skyliner", True),
        ("Disney Vacation Club Riviera Resort - Epcot Skyliner", "Epcot International Gateway - Epcot Skyliner", 10, "Epcot Skyliner", True),

        ("Disney's Caribbean Beach Resort - Epcot Skyliner", "Hollywood Studios - Hollywood Studios Skyliner", 10, "Hollywood Studios Skyliner", True),

        ("Disney's Caribbean Beach Resort - Pop Century/Art of Animation Skyliner", "Generation Gap Bridge - Pop Century/Art of Animation Skyliner", 5, "Pop Century/Art of Animation Skyliner", True),
    ]
    connections = [
        ("Magic Kingdom", "Magic Kingdom - Resort Monorail", 7, "Walk", False),
        ("Magic Kingdom - Resort Monorail", "Magic Kingdom", 1, "Walk", False),
        ("Magic Kingdom", "Magic Kingdom - Express Monorail", 7, "Walk", False),
        ("Magic Kingdom - Express Monorail", "Magic Kingdom", 1, "Walk", False),
        ("Magic Kingdom", "Magic Kingdom - Gold Flag Launch", 11, "Walk", False),
        ("Magic Kingdom - Gold Flag Launch", "Magic Kingdom", 1, "Walk", False),
        ("Magic Kingdom", "Magic Kingdom - Green Flag Launch", 15, "Walk", False),
        ("Magic Kingdom - Green Flag Launch", "Magic Kingdom", 1, "Walk", False),
        ("Magic Kingdom", "Magic Kingdom - Red Flag Launch", 20, "Walk", False),
        ("Magic Kingdom - Red Flag Launch", "Magic Kingdom", 1, "Walk", False),

        ("Ticket & Transportation Center", "Ticket & Transportation Center - Resort Monorail", 7, "Walk", False),
        ("Ticket & Transportation Center", "Ticket & Transportation Center - Express Monorail", 7, "Walk", False),
        ("Ticket & Transportation Center", "Ticket & Transportation Center - Epcot Monorail", 7, "Walk", False),
        ("Ticket & Transportation Center - Resort Monorail", "Ticket & Transportation Center", 1, "Walk", False),
        ("Ticket & Transportation Center - Express Monorail", "Ticket & Transportation Center", 1, "Walk", False),
        ("Ticket & Transportation Center - Epcot Monorail", "Ticket & Transportation Center", 1, "Walk", False),
        ("Ticket & Transportation Center", "Ticket & Transportation Center - Ferry", 11, "Walk", False),
        ("Ticket & Transportation Center - Ferry", "Ticket & Transportation Center", 1, "Walk", False),

        ("Disney's Polynesian Village Resort", "Disney's Polynesian Village Resort - Resort Monorail", 7, "Walk", False),
        ("Disney's Polynesian Village Resort - Resort Monorail", "Disney's Polynesian Village Resort", 1, "Walk", False),
        ("Disney's Polynesian Village Resort", "Disney's Polynesian Village Resort - Gold Flag Launch", 11, "Walk", False),
        ("Disney's Polynesian Village Resort - Gold Flag Launch", "Disney's Polynesian Village Resort", 1, "Walk", False),

        ("Disney's Grand Floridian Resort & Spa", "Disney's Grand Floridian Resort & Spa - Resort Monorail", 7, "Walk", False),
        ("Disney's Grand Floridian Resort & Spa - Resort Monorail", "Disney's Grand Floridian Resort & Spa", 1, "Walk", False),
        ("Disney's Grand Floridian Resort & Spa", "Disney's Grand Floridian Resort & Spa - Gold Flag Launch", 11, "Walk", False),
        ("Disney's Grand Floridian Resort & Spa - Gold Flag Launch", "Disney's Grand Floridian Resort & Spa", 1, "Walk", False),

        ("Disney's Contemporary Resort", "Disney's Contemporary Resort - Resort Monorail", 7, "Walk", False),
        ("Disney's Contemporary Resort - Resort Monorail", "Disney's Contemporary Resort", 1, "Walk", False),
        ("Disney's Contemporary Resort", "Contemporary Resort - Blue Flag Launch", 15, "Walk", False),
        ("Disney's Contemporary Resort - Blue Flag Launch", "Contemporary Resort", 1, "Walk", False),

        ("Disney's Fort Wilderness Resort & Campground", "Disney's Fort Wilderness Resort & Campground - Green Flag Launch", 15, "Walk", False),
        ("Disney's Fort Wilderness Resort & Campground - Green Flag Launch", "Disney's Fort Wilderness Resort & Campground", 1, "Walk", False),
        ("Disney's Fort Wilderness Resort & Campground", "Disney's Fort Wilderness Resort & Campground - Blue Flag Launch", 15, "Walk", False),
        ("Disney's Fort Wilderness Resort & Campground - Blue Flag Launch", "Fort Wilderness Resort & Campground", 1, "Walk", False),

        ("Disney's Wilderness Lodge Resort", "Disney's Wilderness Lodge Resort - Red Flag Launch", 20, "Walk", False),
        ("Disney's Wilderness Lodge Resort - Red Flag Launch", "Disney's Wilderness Lodge Resort", 1, "Walk", False),
        ("Disney's Wilderness Lodge Resort", "Disney's Wilderness Lodge Resort - Red Flag Launch", 20, "Walk", False),
        ("Disney's Wilderness Lodge Resort - Red Flag Launch", "Disney's Wilderness Lodge Resort", 1, "Walk", False),
        ("Disney's Wilderness Lodge Resort", "Disney's Wilderness Lodge Resort - Blue Flag Launch", 15, "Walk", False),
        ("Disney's Wilderness Lodge Resort - Blue Flag Launch", "Disney's Wilderness Lodge Resort", 1, "Walk", False),

        ("Generation Gap Bridge - Pop Century/Art of Animation Skyliner", "Disney's Pop Century Resort", 10, "Walk", True),
        ("Generation Gap Bridge - Pop Century/Art of Animation Skyliner", "Disney's Art of Animation Resort", 10, "Walk", True),

        ("Disney's Caribbean Beach Resort", "Disney's Caribbean Beach Resort - Epcot Skyliner", 1, "Walk", True),
        ("Disney's Caribbean Beach Resort", "Disney's Caribbean Beach Resort - Hollywood Studios Skyliner", 1, "Walk", True),
        ("Disney's Caribbean Beach Resort", "Disney's Caribbean Beach Resort - Pop Century/Art of Animation Skyliner", 1, "Walk", True),
        ("Disney Vacation Club Riviera Resort", "Disney Vacation Club Riviera Resort - Epcot Skyliner", 1, "Walk", True),

        ("Epcot International Gateway", "Epcot - Epcot Monorail", 25, "Walk", True),
        ("Epcot International Gateway", "Epcot International Gateway - Epcot Skyliner", 1, "Walk", True),
        ("Epcot International Gateway - Crescent Lake Friendship Boat to Epcot", "Epcot International Gateway", 1, "Walk", False),
        ("Epcot International Gateway", "Epcot International Gateway - Crescent Lake Friendship Boat to Hollywood Studios", 7, "Walk", False),

        ("Hollywood Studios", "Hollywood Studios - Crescent Lake Friendship Boat to Epcot", 7, "Walk", False),
        ("Hollywood Studios - Crescent Lake Friendship Boat to Hollywood Studios", "Hollywood Studios", 1, "Walk", False),

    ]
    transit_types = [monorails, busses, boats, skyliners, connections]

    paths = []
    for transit_type in transit_types:
        for route in transit_type:
            if route[0] not in locs:
                locs.append(route[0])
            if route[1] not in locs:
                locs.append(route[1])
            if route[4]: # Is not direction-dependent.
                paths.append( (route[1], route[0], route[2], route[3] ) )

            paths.append( (route[0], route[1], route[2], route[3] ) )

    data = {"locations": locs, "paths": paths}
    with open('db.json', 'w') as file:
        json.dump(data, file, indent=4)

    WDW = TransitGraph(len(locs))
    for i in range(len(locs)):
        WDW.add_node(i, locs[i], "")

    for path in paths:
        WDW.add_adj(locs.index(path[0]), locs.index(path[1]), path[2], path[3])
    #distances = WDW.dijkstra("Disney's Grand Floridian Resort & Spa")
    distances = WDW.dijkstra("Ticket & Transportation Center")
    #print(distances["Disney's Polynesian Village Resort"])

    for key, value in distances.items():
        print(f"{key}: {value} \n\n")

