import pandas as pd
import math
import heapq

# Load data from the CSV file
df = pd.read_csv('water_data.csv')

# Create a dictionary to store node information
nodes = {}
for index, row in df.iterrows():
    node_id = row['Node']
    node_type = row['type']
    x = row['x']
    y = row['y']
    linked_node = row['linked']
    nodes[node_id] = {'type': node_type, 'x': x, 'y': y, 'linked': linked_node}

# Build a graph representing connections between nodes and their distances
graph = {}
for node_id, node_info in nodes.items():
    if node_info['type'] == 'junction':
        graph[node_id] = {}
        linked_node = node_info['linked']
        distance = math.sqrt((nodes[linked_node]['x'] - node_info['x']) ** 2 + (nodes[linked_node]['y'] - node_info['y']) ** 2)
        graph[node_id][linked_node] = distance
        graph[linked_node] = {node_id: distance}

# Function to find the shortest path using Dijkstra's algorithm
def shortest_path(graph, start, end):
    visited = set()
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {}

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    current_node = end

    while current_node != start:
        path.append(current_node)
        current_node = previous_nodes[current_node]

    path.append(start)
    path.reverse()

    return path

# Function to find the shortest path within a specified range
def shortest_path_within_range(graph, start, end, x1, x2, y1, y2, dam_node=None):
    # Filter nodes within the specified x and y range
    filtered_nodes = [node_id for node_id, node_info in nodes.items() if x1 <= node_info['x'] <= x2 and y1 <= node_info['y'] <= y2]

    # Find the shortest path that covers all filtered nodes
    shortest_path_result = None
    shortest_path_length = float('inf')

    for node in filtered_nodes:
        if dam_node:
            # If a dam node is provided, insert it into the graph temporarily
            original_graph = graph.copy()
            original_linked_nodes = nodes[node]['linked']

            graph[dam_node] = {}
            graph[dam_node][node] = math.sqrt((nodes[dam_node]['x'] - nodes[node]['x']) ** 2 + (nodes[dam_node]['y'] - nodes[node]['y']) ** 2)
            graph[node][dam_node] = math.sqrt((nodes[dam_node]['x'] - nodes[node]['x']) ** 2 + (nodes[dam_node]['y'] - nodes[node]['y']) ** 2)
            nodes[node]['linked'] = dam_node

            path = shortest_path(graph, start, node)

            # Restore the original graph and linked nodes
            graph = original_graph
            nodes[node]['linked'] = original_linked_nodes
        else:
            path = shortest_path(graph, start, node)

        length = sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1))

        if length < shortest_path_length:
            shortest_path_result = path
            shortest_path_length = length

    return shortest_path_result

# Function to find the shortest path between two points with an optional dam location
def shortest_path_search(start_point, end_point, dam_loc=None):
    # Extract coordinates from start_point and end_point
    x1, y1 = start_point
    x2, y2 = end_point

    if dam_loc:
        dam_x, dam_y = dam_loc

        # Insert the dam as a temporary node
        dam_node_id = max(nodes.keys()) + 1
        nodes[dam_node_id] = {'type': 'dam', 'x': dam_x, 'y': dam_y, 'linked': None}

        # Find the shortest path considering the dam
        result = shortest_path_within_range(graph, 1, 3, x1, x2, y1, y2, dam_node_id)

        # Print the shortest path with the dam
        print("Shortest path considering the dam:")
        previous_node = None  # To keep track of the previous node

        for i, node_id in enumerate(result):
            node_info = nodes[node_id]
            print(f"{i + 1}. Node {node_id}: Type - {node_info['type']}, Coordinates - ({node_info['x']}, {node_info['y']})")

            # Check for backtracking and print a message
            if node_id == previous_node:
                print("Backtracking: Do not recheck this site.")
            
            previous_node = node_id
    else:
        # Find the shortest path without considering the dam
        result = shortest_path_within_range(graph, 1, 3, x1, x2, y1, y2)

        # Print the shortest path, noting backtracking
        print("Shortest path without considering the dam:")
        previous_node = None  # To keep track of the previous node

    for i, node_id in enumerate(result):
        node_info = nodes[node_id]
        print(f"{i+1}. Node {node_id}: Type - {node_info['type']}, Coordinates - ({node_info['x']}, {node_info['y']})")
        
        # Check for backtracking and print a message
        if node_id == previous_node:
           print("Backtracking: Do not recheck this site.")
            
        previous_node = node_id
            
# Specify the start and end points
start_point = (100, 100)
end_point = (400, 400)

# Specify the dam location (before a junction)
dam_location = (200, 250)

# Find the shortest path with and without the dam
shortest_path_search(start_point, end_point)  # Without dam
shortest_path_search(start_point, end_point, dam_location)  # With dam
