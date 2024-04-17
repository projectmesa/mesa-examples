import numpy as np
import solara
from hotelling_law.model import HotellingModel
from matplotlib.figure import Figure
from mesa.experimental import JupyterViz


# This function defines how agents are visually
# represented in the simulation.
def agent_portrayal(agent):
    size = 50  # Default size
    color = "grey"  # Default color for agents

    # Check if the agent has a 'price' attribute.
    # This is to ensure compatibility
    # with different types of agents.
    if hasattr(agent, "price"):
        # Adjust color based on the price attribute of the StoreAgent
        if agent.price > 12:
            color = "#FF0000"  # Higher prices in red
        elif agent.price > 8:
            color = "#FFA500"  # Moderate prices in orange
        else:
            color = "#00FF00"  # Lower prices in green
    # Construct and return the portrayal dictionary
    portrayal = {
        "size": size,
        "color": color,
    }
    return portrayal  # Return the portrayal dictionary to be used by
    # the visualization engine.


def space_drawer(model, agent_portrayal):
    # Create a new figure
    fig = Figure(figsize=(8, 5), dpi=100)
    ax = fig.subplots()

    # Define grid lines
    ticks = np.arange(0, model.grid.width + 1, 1)
    ax.set_xticks(ticks, minor=False)
    ax.set_yticks(ticks, minor=False)
    ax.grid(which="both", color="gray", linestyle="-", linewidth=0.5)
    ax.tick_params(which="both", size=0)  # Hide grid ticks

    # Set axis limits and aspect
    ax.set_xlim(0, model.grid.width)
    ax.set_ylim(0, model.grid.height)
    ax.set_aspect("equal")

    # Hide major tick labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Plotting agents using portrayal
    for agent in model.schedule.agents:
        portrayal = agent_portrayal(agent)
        x, y = agent.pos
        # Adjust plot call for object-oriented API
        ax.scatter(
            x + 0.5,
            y + 0.5,
            c=portrayal.get("color", "black"),
            s=portrayal.get("size", 100),
            linewidths=0.5,
            edgecolors="black",
            alpha=0.6,
        )

    # Invert y-axis to match grid origin (bottom-left)
    ax.invert_yaxis()

    # Adjust layout properly for embedded plots
    fig.tight_layout()

    return solara.FigureMatplotlib(fig)


model_params = {
    "N": {
        "type": "SliderInt",
        "value": 20,
        "label": "Number of stores:",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "mode": {
        "type": "Select",
        "value": "default",
        "label": "Mode:",
        "values": ["default", "pricing_only", "moving_only"],
    },
    "environment_type": {
        "type": "Select",
        "value": "grid",
        "label": "Environment Type:",
        "values": ["grid", "line"],
    },
    "mobility_rate": {
        "type": "SliderInt",
        "value": 100,
        "label": "Mobility Rate (%):",
        "min": 10,
        "max": 100,
        "step": 5,
    },
    "width": {
        "type": "SliderInt",
        "value": 20,  # Adjusted from 10 to 20 for wider grid
        "label": "Grid Width:",
        "min": 10,
        "max": 50,
        "step": 5,
    },
    "height": {
        "type": "SliderInt",
        "value": 20,  # Adjusted from 10 to 20 for taller grid
        "label": "Grid Height:",
        "min": 10,
        "max": 50,
        "step": 5,
    },
}

# Instantiate the JupyterViz component with your model
page = JupyterViz(
    model_class=HotellingModel,
    model_params=model_params,
    measures=["Average Price", "Total Revenue", "Price Variance"],
    name="Hotelling's Law Model",
    agent_portrayal=agent_portrayal,
    space_drawer=space_drawer,
)

# Display the visualization in the Jupyter Notebook
page  # noqa
