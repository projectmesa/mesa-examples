import solara 
from model import AgentNetwork
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)

def node_portrayal(agent):
    return{
        "color": "blue",
        "size": 30
    }

SpacePlot = make_space_component(node_portrayal)

model = AgentNetwork()

page = SolaraViz(
    model,
    components=[SpacePlot],
    # model_params=model_params,
    name= "Agent Network"
)
