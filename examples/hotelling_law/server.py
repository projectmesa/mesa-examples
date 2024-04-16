# Import necessary components from the Mesa visualization modules.
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import Choice, Slider

# Import the model and visualization elements defined
# in other files of the project.
from .model import HotellingModel
from .visualization import (
    agent_portrayal, average_price_chart, total_revenue_chart)

# Define the size of the grid that will be used for visualizing
# the simulation in the web interface.
grid_width, grid_height = 20, 20
# Create a CanvasGrid visualization, which uses the agent_portrayal
# function to determine how agents are drawn.
grid = CanvasGrid(agent_portrayal, grid_width, grid_height, 862, 400)

# Define the model parameters that can be adjusted
# in the web interface.
# These include sliders and choices for the number of stores,
# the simulation mode, and the environment type.
model_params = {
    "N": Slider(
        "Number of Stores", 10, 2, 20, 1
    ),  # Slider to adjust the number of store agents.
    "width": grid_width,  # The width of the simulation grid.
    "height": grid_height,  # The height of the simulation grid.
    "mode": Choice(
        "Rules",
        value="default",
        choices=["default", "pricing_only", "moving_only"],
    ),  # Choice between
    # different operation modes of the simulation.
    "environment_type": Choice(
        "Layout", value="grid", choices=["grid", "line"]
    ),  # Choice of environment: a
    # full grid or a single line.
    "mobility_rate": Slider(
        "Mobility Rate (%)", 100, 1, 100, 1
    ),  # Slider to adjust the mobility rate of the agents.
}

# Instantiate the ModularServer with the HotellingModel,
# the visualization modules (grid, charts),
# the name of the model for the web interface,
# and the adjustable model parameters.
server = ModularServer(
    HotellingModel,
    [grid, average_price_chart, total_revenue_chart],
    "Hotelling's Law Model",
    model_params,
)
