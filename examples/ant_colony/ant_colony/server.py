import mesa

from ant_colony.agents import Ant
from ant_colony.model import AntColony
from .SimpleContinuousModule import SimpleCanvas


boid_canvas = SimpleCanvas(Ant, 500, 500)

def ant_colony_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Ant:
        portrayal["Shape"] = f"ant_colony/resources/{agent.color}_ant.png"
        # https://icons8.com/icons/set/ant
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal

canvas_element = SimpleCanvas(ant_colony_portrayal, 500, 500)

chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Red Ants", "Color": "#AA0000"},
        {"Label": "Blue Ants", "Color": "#0000FF"},
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:")
}


server = mesa.visualization.ModularServer(
    AntColony, [canvas_element, chart_element], "Ant Adaptation", model_params
)
server.port = 8521