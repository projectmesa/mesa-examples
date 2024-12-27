from city_walking_behaviour.agents import Human, GroceryStore, SocialPlace, NonFoodShop, Other
from city_walking_behaviour.model import WalkingModel
from mesa.experimental.devs import ABMSimulator
from mesa.visualization import (
    SolaraViz,
    make_space_component,
    make_plot_component,
)

# Define the scenarios
SCENARIOS = [
    ("random_random", "Random Land Use, Random Safety"),
    ("random_safe", "Random Land Use, Low Safety in Core"),
    ("central_random", "Centralized Land Use, Random Safety"),
    ("central_safe", "Centralized Land Use, Low Safety in Core"),
]


def agent_portrayal(agent):
    """Determine visual portrayal details for each agent."""
    if agent is None:
        return

    portrayal = {
        "size": 25,
    }

    if isinstance(agent, GroceryStore):
        portrayal["color"] = "tab:green"
        portrayal["marker"] = "s"
        portrayal["zorder"] = 2
    elif isinstance(agent, SocialPlace):
        portrayal["color"] = "tab:purple"
        portrayal["marker"] = "s"
        portrayal["zorder"] = 2
    elif isinstance(agent, NonFoodShop):
        portrayal["color"] = "tab:olive"
        portrayal["marker"] = "s"
        portrayal["zorder"] = 2
    elif isinstance(agent, Other):
        portrayal["color"] = "tab:brown"
        portrayal["marker"] = "s"
        portrayal["zorder"] = 2
    elif isinstance(agent, Human):
        portrayal["color"] = "tab:red"
        portrayal["marker"] = "v"
        portrayal["zorder"] = 2

    return portrayal


model_params = {
    "width": 40,
    "height": 40,
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "no_of_couples": {
        "type": "SliderInt",
        "value": 2400,
        "label": "Number of Couples:",
        "min": 2000,
        "max": 3000,
        "step": 100,
    },
    "no_of_singles": {
        "type": "SliderInt",
        "value": 600,
        "label": "Number of Singles:",
        "min": 300,
        "max": 1000,
        "step": 20,
    },
    "no_of_grocery_stores": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of Grocery Stores:",
        "min": 5,
        "max": 20,
        "step": 1,
    },
    "no_of_social_places": {
        "type": "SliderInt",
        "value": 75,
        "label": "Number of Social Places:",
        "min": 50,
        "max": 90,
        "step": 1,
    },
    "no_of_non_food_shops": {
        "type": "SliderInt",
        "value": 40,
        "label": "Number of Non-Food Shops:",
        "min": 25,
        "max": 55,
        "step": 1,
    },
    "no_of_others": {
        "type": "SliderInt",
        "value": 475,
        "label": "Number of Other Places:",
        "min": 405,
        "max": 600,
        "step": 1,
    },
    "scenario": {
        "type": "Select",
        "value": "random_random",
        "label": "Scenario",
        "values": [s[0] for s in SCENARIOS],
    },
}


def post_process_space(ax):
    """Ensure consistent scaling for visual grid."""
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.get_figure().set_size_inches(10, 10)


def post_process_lines_walk(ax):
    """Configure the average walking trips plot."""
    handles, labels = ax.get_legend_handles_labels()
    new_labels = []
    for label in labels:
        if label == "avg_walk_ses1":
            new_labels.append("SES 1")
        elif label == "avg_walk_ses2":
            new_labels.append("SES 2")
        elif label == "avg_walk_ses3":
            new_labels.append("SES 3")
        elif label == "avg_walk_ses4":
            new_labels.append("SES 4")
        elif label == "avg_walk_ses5":
            new_labels.append("SES 5")
        else:
            new_labels.append(label)
    ax.legend(handles, new_labels, loc="center left", bbox_to_anchor=(1, 0.9))
    ax.set_ylabel("Average Walking Trips", fontsize=12, fontweight="normal")


def post_process_lines_work(ax):
    """Configure the work trips plot."""
    handles, labels = ax.get_legend_handles_labels()
    new_labels = []
    for label in labels:
        if label == "avg_work_ses1":
            new_labels.append("SES 1")
        elif label == "avg_work_ses2":
            new_labels.append("SES 2")
        elif label == "avg_work_ses3":
            new_labels.append("SES 3")
        elif label == "avg_work_ses4":
            new_labels.append("SES 4")
        elif label == "avg_work_ses5":
            new_labels.append("SES 5")
        else:
            new_labels.append(label)
    ax.legend(handles, new_labels, loc="center left", bbox_to_anchor=(1, 0.9))
    ax.set_ylabel("Average Work Trips", fontsize=12, fontweight="normal")


def post_process_lines_basic(ax):
    """Configure the basic needs trips plot."""
    handles, labels = ax.get_legend_handles_labels()
    new_labels = []
    for label in labels:
        if label == "avg_basic_ses1":
            new_labels.append("SES 1")
        elif label == "avg_basic_ses2":
            new_labels.append("SES 2")
        elif label == "avg_basic_ses3":
            new_labels.append("SES 3")
        elif label == "avg_basic_ses4":
            new_labels.append("SES 4")
        elif label == "avg_basic_ses5":
            new_labels.append("SES 5")
        else:
            new_labels.append(label)
    ax.legend(handles, new_labels, loc="center left", bbox_to_anchor=(1, 0.9))
    ax.set_ylabel("Average Trips for Basic Needs", fontsize=12, fontweight="normal")


def post_process_lines_leisure(ax):
    """Configure the leisure trips plot."""
    handles, labels = ax.get_legend_handles_labels()
    new_labels = []
    for label in labels:
        if label == "avg_leisure_ses1":
            new_labels.append("SES 1")
        elif label == "avg_leisure_ses2":
            new_labels.append("SES 2")
        elif label == "avg_leisure_ses3":
            new_labels.append("SES 3")
        elif label == "avg_leisure_ses4":
            new_labels.append("SES 4")
        elif label == "avg_leisure_ses5":
            new_labels.append("SES 5")
        else:
            new_labels.append(label)
    ax.legend(handles, new_labels, loc="center left", bbox_to_anchor=(1, 0.9))
    ax.set_ylabel("Average Trips for Leisure", fontsize=12, fontweight="normal")


def post_process_buildings_legend(ax):
    import matplotlib.lines as mlines
    # Create legend entries for each building/agent
    grocery_store = mlines.Line2D([], [], color="tab:green", marker="s", linestyle="None", markersize=10, label="Grocery Store")
    social_place = mlines.Line2D([], [], color="tab:purple", marker="s", linestyle="None", markersize=10, label="Social Place")
    non_food_shop = mlines.Line2D([], [], color="tab:olive", marker="s", linestyle="None", markersize=10, label="Non-Food Shop")
    other_building = mlines.Line2D([], [], color="tab:brown", marker="s", linestyle="None", markersize=10, label="Other")
    human = mlines.Line2D([], [], color="tab:red", marker="v", linestyle="None", markersize=10, label="Human")

    ax.legend(
        handles=[grocery_store, social_place, non_food_shop, other_building, human],
        loc="center",
        bbox_to_anchor=(0.5, 0.5)
    )
    ax.axis("off")

space_component = make_space_component(
    agent_portrayal, draw_grid=True, post_process=post_process_space
)

plot_component_a = make_plot_component(
    {
        "avg_walk_ses1": "tab:red",
        "avg_walk_ses2": "tab:blue",
        "avg_walk_ses3": "tab:green",
        "avg_walk_ses4": "tab:purple",
        "avg_walk_ses5": "tab:cyan",
    },
    post_process=post_process_lines_walk,
)

plot_component_b = make_plot_component(
    {
        "avg_work_ses1": "tab:red",
        "avg_work_ses2": "tab:blue",
        "avg_work_ses3": "tab:green",
        "avg_work_ses4": "tab:purple",
        "avg_work_ses5": "tab:cyan",
    },
    post_process=post_process_lines_work,
)

plot_component_c = make_plot_component(
    {
        "avg_basic_ses1": "tab:red",
        "avg_basic_ses2": "tab:blue",
        "avg_basic_ses3": "tab:green",
        "avg_basic_ses4": "tab:purple",
        "avg_basic_ses5": "tab:cyan",
    },
    post_process=post_process_lines_basic,
)

plot_component_d = make_plot_component(
    {
        "avg_leisure_ses1": "tab:red",
        "avg_leisure_ses2": "tab:blue",
        "avg_leisure_ses3": "tab:green",
        "avg_leisure_ses4": "tab:purple",
        "avg_leisure_ses5": "tab:cyan",
    },
    post_process=post_process_lines_leisure,
)

plot_component_legend = make_plot_component({}, post_process=post_process_buildings_legend)

# Initialize and run the model
simulator = ABMSimulator()
model = WalkingModel(simulator=simulator)

# server = mesa.visualization(
#     WalkingModel,
#     [space_component, plot_component_legend, plot_component_a, plot_component_b, plot_component_c, plot_component_d],
#     "Walking Model",
#     model_params,
# )

page = SolaraViz(
    model,
    components=[
        space_component,
        plot_component_legend,
        plot_component_a,
        plot_component_b,
        plot_component_c,
        plot_component_d,
    ],
    model_params=model_params,
    name="Walking Model",
    simulator=simulator,
)
page
