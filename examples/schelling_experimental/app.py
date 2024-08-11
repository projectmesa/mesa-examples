from mesa.visualization.solara_viz.py import Slider, SolaraViz, make_text
from model import Schelling


def get_happy_agents(model):
    """
    Display a text count of how many happy agents there are.
    """
    return f"Happy agents: {model.happy}"


def agent_portrayal(agent):
    return {"color": "tab:orange" if agent.type == 0 else "tab:blue"}


model_params = {
    "density": Slider("Agent density", 0.8, 0.1, 1.0, 0.1),
    "minority_pc": Slider("Fraction minority", 0.2, 0.0, 1.0, 0.05),
    "homophily": Slider("Homophily", 3, 0, 8, 1),
    "width": 20,
    "height": 20,
}

page = SolaraViz(
    Schelling,
    model_params,
    measures=["happy", make_text(get_happy_agents)],
    agent_portrayal=agent_portrayal,
)
page  # noqa
