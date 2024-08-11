import solara
from mesa.experimental import JupyterViz, make_text
from model import WolfSheepPredation
from agents import (
    Sheep,
    Wolf,
    GrassPatch,
)  # Assuming these classes are defined in agents.py


def agent_portrayal(agent):
    if isinstance(agent, Sheep):
        return {"size": 10, "color": "tab:green"}
    elif isinstance(agent, Wolf):
        return {"size": 10, "color": "tab:red"}
    elif isinstance(agent, GrassPatch):
        return {"size": 5, "color": "tab:blue" if agent.fully_grown else "tab:brown"}


model_params = {
    "width": 20,
    "height": 20,
    "initial_sheep": {
        "type": "SliderInt",
        "value": 50,
        "label": "Initial number of sheep",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "initial_wolves": {
        "type": "SliderInt",
        "value": 50,
        "label": "Initial number of wolves",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "sheep_reproduce": {
        "type": "SliderFloat",
        "value": 0.04,
        "label": "Sheep reproduction rate",
        "min": 0.01,
        "max": 0.1,
        "step": 0.01,
    },
    "wolf_reproduce": {
        "type": "SliderFloat",
        "value": 0.05,
        "label": "Wolf reproduction rate",
        "min": 0.01,
        "max": 0.1,
        "step": 0.01,
    },
    "sheep_gain_from_food": {
        "type": "SliderInt",
        "value": 4,
        "label": "Sheep gain from food",
        "min": 1,
        "max": 10,
        "step": 1,
    },
    "wolf_gain_from_food": {
        "type": "SliderInt",
        "value": 20,
        "label": "Wolf gain from food",
        "min": 1,
        "max": 50,
        "step": 1,
    },
}

page = JupyterViz(
    WolfSheepPredation,
    model_params,
    measures=["Wolves", "Sheep", "Grass"],
    name="Wolf-Sheep Predation Model",
    agent_portrayal=agent_portrayal,
)

# If you are in a Jupyter notebook, you might need to display the page
# For example:
# from IPython.display import display
# display(page)
