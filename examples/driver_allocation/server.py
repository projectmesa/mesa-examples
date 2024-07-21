import mesa
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model.simulation import CityModel


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Color": "red" if isinstance(agent, DriverAgent) else "blue",
        "Filled": "true",
        "r": 0.5,
    }
    return portrayal


grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = ModularServer(
    CityModel,
    [grid],
    "Driver Ride Allocation Model",
    {"num_drivers": 10, "num_rides": 5, "width": 20, "height": 20},
)

server.port = 8765
server.launch()
