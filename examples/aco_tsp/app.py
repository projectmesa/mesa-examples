"""
Configure visualization elements and instantiate a server
"""
import solara
from matplotlib.figure import Figure
import networkx as nx

from mesa.visualization import SolaraViz

from aco_tsp.model import AcoTspModel  # noqa


def circle_portrayal_example(agent):
    # return {
    #     "size": 40,
    #     # This is Matplotlib's color
    #     "color": "tab:blue",
    # }
    return {}


model_params = {"num_agents": 2, "num_cities": 5}

def make_graph(model):
    # Note: you must initialize a figure using this method instead of
    # plt.figure(), for thread safety purpose
    fig = Figure()
    ax = fig.subplots()
    graph = model.grid.G
    pos = model.pos
    # Set edge-width based on 1/distance between nodes
    weights = [graph[u][v]['weight'] for u, v in graph.edges()]

    nx.draw(
        graph,
        ax=ax,
        pos=pos,
        width=weights,
        edge_color="gray",
    )
    
    solara.FigureMatplotlib(fig)

page = SolaraViz(
    AcoTspModel,
    model_params,
    measures=["num_steps", make_graph],
    agent_portrayal=circle_portrayal_example
)
