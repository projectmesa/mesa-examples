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

def post_process_lineplot(ax):
    ax.set_ylim(ymin=0)
    ax.set_ylabel("# total degree")
    ax.set_xlim(xmin=0)
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")

SpacePlot = make_space_component(node_portrayal)
StatePlot = make_plot_component(measure = "Degree",post_process=post_process_lineplot)
model = AgentNetwork()

page = SolaraViz(
    model,
    components=[SpacePlot,StatePlot],
    # model_params=model_params,
    name= "Agent Network"
)
