# model.py
import osmnx as ox
import networkx as nx
import random
from shapely.geometry import Point
from mesa import Model
from mesa.time import SimultaneousActivation
from mesa_geo import GeoAgent, GeoSpace

# Define critical points (e.g., intersections) prone to congestion
critical_points = [
    (40.755, -73.990),
    (40.752, -73.987),
]


class VehicleAgent(GeoAgent):
    def __init__(self, unique_id, model, shape, start_node, end_node, crs):
        super().__init__(unique_id, model, shape, crs)
        self.start_node = start_node
        self.end_node = end_node
        try:
            self.route = nx.shortest_path(
                model.graph, source=start_node, target=end_node, weight="length"
            )
        except nx.NetworkXNoPath:
            self.route = []  # Empty route if no path found
        self.current_step = 0

    def step(self):
        if self.current_step < len(self.route) - 1:
            self.current_step += 1
            node = self.route[self.current_step]
            self.shape = Point(
                (self.model.graph.nodes[node]["x"], self.model.graph.nodes[node]["y"])
            )


class TrafficModel(Model):
    def __init__(self, num_vehicles, north, south, east, west, steps):
        super().__init__()
        self.num_vehicles = num_vehicles
        self.steps = steps
        self.graph = ox.graph_from_bbox(north, south, east, west, network_type="drive")
        self.schedule = SimultaneousActivation(self)
        self.space = GeoSpace(crs="epsg:4326")

        self.simulate_congestion(critical_points)

        for i in range(self.num_vehicles):
            start_node = random.choice(list(self.graph.nodes))
            end_node = random.choice(list(self.graph.nodes))
            start_point = Point(
                (self.graph.nodes[start_node]["x"], self.graph.nodes[start_node]["y"])
            )
            vehicle = VehicleAgent(
                i, self, start_point, start_node, end_node, crs="epsg:4326"
            )
            if vehicle.route:  # Only add vehicles with valid routes
                self.space.add_agents(vehicle)
                self.schedule.add(vehicle)

    def simulate_congestion(self, critical_points):
        for point in critical_points:
            node = ox.distance.nearest_nodes(self.graph, X=point[1], Y=point[0])
            if node in self.graph.nodes:
                for u, v, key, data in self.graph.edges(node, keys=True, data=True):
                    data["length"] *= (
                        5  # Simulating congestion by increasing travel time
                    )

    def step(self):
        self.schedule.step()
