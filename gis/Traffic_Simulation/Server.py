# Server.py
import mesa
import mesa_geo as mg
from mesa_geo import GeoAgent
from model import TrafficModel
import osmnx as ox
from mesa.visualization.ModularVisualization import ModularServer
from flask import Flask


def vehicle_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Color": "red",
        "Filled": "true",
        "Layer": 1,
        "r": 3,
    }

    return portrayal


def road_portrayal(road):
    return {
        "Shape": "line",
        "Color": "red",
        "Layer": 0,
        "opacity": 0.5,
        "coordinates": [(coord[1], coord[0]) for coord in road.shape.coords],
    }


class RoadAgent(GeoAgent):
    def __init__(self, unique_id, model, shape, crs):
        super().__init__(unique_id, model, shape, crs)


def create_road_agents(model):
    edges = ox.graph_to_gdfs(model.graph, nodes=False, edges=True)
    for i, row in edges.iterrows():
        road = RoadAgent(i, model, row["geometry"], crs="epsg:4326")
        model.space.add_agents(road)


map_module = mg.visualization.MapModule(
    portrayal_method=vehicle_portrayal,
    view=[40.755, -73.987],  # Center view on a critical point
    zoom=15,
    map_height=800,
    map_width=800,
    scale_options={"imperial": False},
)

model_params = {
    "num_vehicles": mesa.visualization.Slider("Number of Vehicles", 5, 1, 100, 1),
    "north": mesa.visualization.NumberInput("North", 40.759),
    "south": mesa.visualization.NumberInput("South", 40.748),
    "east": mesa.visualization.NumberInput("East", -73.984),
    "west": mesa.visualization.NumberInput("West", -73.994),
    "steps": mesa.visualization.Slider("Simulation Steps", 10, 1, 100, 1),
}


class CustomModularServer(ModularServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flask_app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.flask_app.route("/")
        def index():
            return self.render("index.html")

        @self.flask_app.route("/simulate", methods=["POST"])
        def simulate():
            self.simulate()
            return "", 204

    def reset_model(self):
        super().reset_model()
        create_road_agents(self.model)

    def simulate(self):
        self.model.running = True
        for _ in range(self.model.steps):
            self.model.step()
        self.model.running = False


server = CustomModularServer(
    TrafficModel, [map_module], "Traffic Simulation", model_params
)

server.port = 8522  # Change to a different port if necessary

# Modify the index.html to include the Simulate button
index_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Traffic Simulation</title>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body { font-family: Arial, sans-serif; }
        #map { height: 800px; width: 800px; margin: 0 auto; }
        #controls { text-align: center; }
    </style>
</head>
<body>
    <div id="map"></div>
    <div id="controls">
        <input type="button" value="Simulate" onclick="simulate()">
        <input type="button" value="Reset" onclick="reset()">
    </div>
    <script>
        var map = L.map('map').setView([40.755, -73.987], 15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        var simulate = function() {
            fetch('/simulate', { method: 'POST' });
        };

        var reset = function() {
            fetch('/reset', { method: 'POST' });
        };
    </script>
</body>
</html>
"""

with open("index.html", "w") as file:
    file.write(index_html)

server.launch()
