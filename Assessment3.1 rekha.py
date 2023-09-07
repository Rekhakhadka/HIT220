# Question 1
# Load the dataset
data = pd.read_csv('Assessment3.csv') #read the csv data you need here instead of Assessment3,csv
# data for location of each point with their type of location
locations = [
    { "point": 1, 'type': "headwater", "latitude": 70, "longitude": 100},
    { "point": 2, 'type': "junction",  "latitude": 230, "longitude": 190},
    { "point": 3, 'type': "headwater", "latitude": 140, "longitude": 265},
    # from the dataset "Assessment3.csv add remaining location
    { "point": 58, 'type': "junction", "latitude": 380, "longitude": 220},
]

# When accessing data for a specific location
print(locations[0]["point"], locations[0]["latitude"], locations[0]["longitude"], locations[0]["type"])

# Iterating over all locations
for point in locations:
    print(point["point"], ":", point["latitude"], point["longitude"], point["type"])

# Question 2
   
# Create a graph representation of the river system with distance (weight) between points using DFs
river_system = {
    1: [(2, 30)],        # Point 1 connects to Point 2 with a distance of 30 units
    2: [(3, 25)],        # Point 2 "         "   "   3  "    "   "     "  25 units
    3: [(58, 50)],       # Point 3 "         "   "   58 "    "   "     "  50 units
    58: []               # Point 58 is the end point and has no outgoing connections as it finishes there
}

# Create a dictionary to store terrain data for each point
terrain_data = {
    1: "mountain",
    2: "terrai",
    3: "hills",
    # add other points and locations if needed
    58: "himalyans"
}

# Print out a traversal to show the order of nodes in the river system
def traverse_river_system(graph, start_node):
    visited = set()
    stack = [(start_node, 0)]  # Use a tuple to track both the node and total distance

    while stack:
        node, total_distance = stack.pop()
        if node not in visited:
            print(f"Point {node} ({terrain_data[node]}), Distance: {total_distance} units")
            visited.add(node)
            for neighbor, distance in graph[node]:
                if neighbor not in visited:
                    stack.append((neighbor, total_distance + distance))

# Perform a traversal starting from Point 1 our starting point to our ending point point 58
print("Traversal of the river system:")
traverse_river_system(river_system, 1)

