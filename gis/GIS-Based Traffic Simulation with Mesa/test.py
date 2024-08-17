import os
import osmnx as ox
import networkx as nx
import folium
import io
from PIL import Image
from model import TrafficModel, VehicleAgent

# Bounding box coordinates for Bangalore
north, south, east, west = 12.976, 12.961, 77.599, 77.579
bbox = (north, south, east, west)

# Create a graph from the bounding box using the bbox parameter
G = ox.graph_from_bbox(north, south, east, west, network_type='drive')

# Extract graph bounds for the TrafficGeoSpace
min_x = min(nx.get_node_attributes(G, 'x').values())
max_x = max(nx.get_node_attributes(G, 'x').values())
min_y = min(nx.get_node_attributes(G, 'y').values())
max_y = max(nx.get_node_attributes(G, 'y').values())

# Running the TrafficModel simulation
num_vehicles = 51
model = TrafficModel(G, num_vehicles, min_x, min_y, max_x, max_y)

# Ensure the directory exists
gif_dir = 'Data/'
os.makedirs(gif_dir, exist_ok=True)

# Running the simulation and updating the Folium map
map_images = []
for step in range(10):  # Run for 10 steps
    model.step()

    # Create a new map for each step
    temp_map = folium.Map(location=[(north + south) / 2, (east + west) / 2], zoom_start=15)

    # Add the road network to the map
    edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
    for _, row in edges.iterrows():
        points = [(row['geometry'].coords[i][1], row['geometry'].coords[i][0]) for i in range(len(row['geometry'].coords))]
        folium.PolyLine(points, color='blue', weight=2.5, opacity=1).add_to(temp_map)

    # Add vehicles to the map
    for vehicle in model.schedule.agents:
        if isinstance(vehicle, VehicleAgent):
            if vehicle.current_step > 0:
                # Ensure vehicle has moved
                position_node = vehicle.route[vehicle.current_step - 1]
                vehicle_position = (model.space.G.nodes[position_node]['y'],
                                    model.space.G.nodes[position_node]['x'])
                color = 'red' if vehicle.vehicle_type == 'car' else 'blue' if vehicle.vehicle_type == 'truck' else 'green'
                folium.CircleMarker(location=vehicle_position, radius=5, color=color, fill=True).add_to(temp_map)
            else:
                print(f"Vehicle {vehicle.unique_id} has not started its route yet.")

    # Save the map state as an image
    img_data = temp_map._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    map_images.append(img)
    print(f"Step {step} image captured.")

# Create an animated GIF from the saved map images
gif_path = os.path.join(gif_dir, 'bangalore_traffic_congestion.gif')
map_images[0].save(gif_path, save_all=True, append_images=map_images[1:], duration=500, loop=0)

print("Simulation complete. Check the Data/ directory for the Bangalore traffic congestion animation.")
