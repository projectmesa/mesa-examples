import mesa

from server import (
    canvas_element,
    get_happy_agents,
    happy_chart,
    model_params,
)
from cacheablemodel import CacheableSchelling

# As 'replay' is a simulation model parameter in this example, we need to make it available as such
model_params["replay"] = mesa.visualization.Checkbox("Replay last run?", False)

server = mesa.visualization.ModularServer(
    # Note that Schelling was replaced by CacheableSchelling here
    CacheableSchelling,
    [canvas_element, get_happy_agents, happy_chart],
    "Schelling",
    model_params,
)

server.launch()
