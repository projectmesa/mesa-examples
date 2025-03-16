from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)
from model import BoltzmannWealthModelNetwork


def agent_portrayal(agent):
    return {
        "color": "red" if agent.wealth == 0 else "green",
        "size": 30,
    }


model_params = {
    "num_agents": Slider(
        label="Number of agents",
        value=10,
        min=5,
        max=20,
        step=1,
    ),
    "num_nodes": Slider(
        label="Number of nodes",
        value=10,
        min=5,
        max=20,
        step=1,
    ),
}


def post_process_lineplot(ax):
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)


SpacePlot = make_space_component(agent_portrayal)
GiniPlot = make_plot_component("Gini", post_process=post_process_lineplot)

model = BoltzmannWealthModelNetwork()

page = SolaraViz(
    model,
    components=[GiniPlot, SpacePlot],
    model_params=model_params,
    name="Boltzmann_wealth_model_network",
)
