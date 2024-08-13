from mesa.visualization import Slider, SolaraViz

from epstein_civil_violence.agent import Citizen, Cop
from epstein_civil_violence.model import EpsteinCivilViolence


COP_COLOR = "#000000"
AGENT_QUIET_COLOR = "#648FFF"
AGENT_REBEL_COLOR = "#FE6100"
JAIL_COLOR = "#808080"
JAIL_SHAPE = "rect"

def citizen_cop_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "x": agent.pos[0],
        "y": agent.pos[1],
        "Filled": "true",
    }

    if isinstance(agent, Citizen):
        color = (
            AGENT_QUIET_COLOR if agent.condition == "Quiescent" else AGENT_REBEL_COLOR
        )
        color = JAIL_COLOR if agent.jail_sentence else color
        shape = JAIL_SHAPE if agent.jail_sentence else "circle"
        portrayal["color"] = color
        portrayal["Shape"] = shape
        # TODO add marker to SolaraViz to display rectangle.
        portrayal["size"] = 0.5
        portrayal["Filled"] = "false"

    else:
        assert isinstance(agent, Cop)
        portrayal["color"] = COP_COLOR
        portrayal["size"] = 0.9

    return portrayal


model_params = {
    "height": 40,
    "width": 40,
    "citizen_density": Slider(
        "Initial Agent Density", 0.7, 0.0, 0.9, 0.1
    ),
    "cop_density": Slider(
        "Initial Cop Density", 0.04, 0.0, 0.1, 0.01
    ),
    "citizen_vision": Slider("Citizen Vision", 7, 1, 10, 1),
    "cop_vision": Slider("Cop Vision", 7, 1, 10, 1),
    "legitimacy": Slider(
        "Government Legitimacy", 0.82, 0.0, 1, 0.01
    ),
    "max_jail_term": Slider("Max Jail Term", 30, 0, 50, 1),
}
page = SolaraViz(
    EpsteinCivilViolence,
    model_params,
    measures=[{"Quiescent": "#648FFF", "Active": "#FE6100", "Jailed": "#808080"}],
    agent_portrayal=citizen_cop_portrayal,
)
page  # noqa
