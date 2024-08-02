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


model_params = {"num_agents": 20, "num_cities": 20}


def make_graph(model):
    # Note: you must initialize a figure using this method instead of
    # plt.figure(), for thread safety purpose
    fig = Figure()
    ax = fig.subplots()
    graph = model.grid.G
    pos = model.pos
    # Set edge-width based on 1/distance between nodes
    weights = [graph[u][v]["weight"] for u, v in graph.edges()]

    nx.draw(
        graph,
        ax=ax,
        pos=pos,
        width=weights,
        edge_color="gray",
    )

    solara.FigureMatplotlib(fig)


def extract_data(model):
    fig = Figure()
    ax = fig.subplots()
    ant_distances = model.datacollector.get_agent_vars_dataframe()
    # Plot so that the step index is the x-axis, there's a line for each agent,
    # and the y-axis is the distance traveled
    ant_distances["traveled_distance"].unstack(level=1).plot(ax=ax)
    # print(ant_distances)
    solara.FigureMatplotlib(fig)


page = SolaraViz(
    AcoTspModel,
    model_params,
    measures=["num_steps", make_graph, extract_data],
    agent_portrayal=circle_portrayal_example,
)
