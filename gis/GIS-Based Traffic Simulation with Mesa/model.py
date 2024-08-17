import mesa
import networkx as nx
import random
import osmnx as ox
from agent import VehicleAgent

class TrafficGeoSpace(mesa.space.ContinuousSpace):
    def __init__(self, G, min_x, min_y, max_x, max_y, crs="EPSG:3857"):
        x_max = max_x - min_x
        y_max = max_y - min_y
        super().__init__(x_max, y_max, False)
        self.G = G  # Assign the OSMnx graph to the space
        self.crs = crs  # Coordinate Reference System


class TrafficModel(mesa.Model):
    def __init__(self, G, num_vehicles, min_x, min_y, max_x, max_y):
        super().__init__()
        self.schedule = mesa.time.RandomActivation(self)
        self.space = TrafficGeoSpace(G, min_x, min_y, max_x, max_y)
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.create_vehicles(num_vehicles)

    def create_vehicles(self, num_vehicles):
        vehicle_types = ["car", "truck", "bike"]
        for i in range(num_vehicles):
            start_point = (
                random.uniform(self.min_y, self.max_y),
                random.uniform(self.min_x, self.max_x),
            )
            end_point = (
                random.uniform(self.min_y, self.max_y),
                random.uniform(self.min_x, self.max_x),
            )
            start_node = ox.distance.nearest_nodes(
                self.space.G, X=start_point[1], Y=start_point[0]
            )
            end_node = ox.distance.nearest_nodes(
                self.space.G, X=end_point[1], Y=end_point[0]
            )

            try:
                route = nx.shortest_path(
                    self.space.G, source=start_node, target=end_node, weight="length"
                )
                vehicle_type = random.choice(vehicle_types)
                vehicle = VehicleAgent(i, self, vehicle_type=vehicle_type, route=route)
                start_position = (
                    self.space.G.nodes[start_node]["x"] - self.min_x,
                    self.space.G.nodes[start_node]["y"] - self.min_y,
                )  # Adjust coordinates
                self.space.place_agent(vehicle, start_position)
                self.schedule.add(vehicle)
            except nx.NetworkXNoPath:
                pass  # Skip this vehicle if no route is found

    def step(self):
        self.schedule.step()
