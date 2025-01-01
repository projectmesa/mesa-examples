import solara
from cholera_voronoi.model import Cholera, Pump
from mesa.visualization import JupyterViz, Slider

SUSCEPTIBLE = 0
INFECTIOUS = 1
REMOVED = 2


def get_removed_people(model: Cholera):
    """
    Display a text count of how many people were removed.
    """
    return f"Number of removed people: {model.removed}"


def get_infectious_pumps(model: Cholera):
    """
    Display infected/total pumps count.
    """
    return f"Infected pumps: {model.infected_pumps}/{model.number_pumps}"


model_params = {
    # "cases_ratio_to_fix_pump": {
    #     'type': 'SliderFloat',
    #     'label': "Ratio of cases in a neighborhood / total person in system to fix pump",
    #     'value': 0.1,
    #     'min': 0,
    #     'max': 0.3,
    #     'step': 0.001
    # ),
    "pumps_neighbor_contamination_chance": Slider(
        label="Neighbor contamination ratio",
        value=2e-1,
        min=0,
        max=1,
        step=0.05,
    ),
    "pumps_person_contamination_chance": Slider(
        label="Person contamination ratio",
        value=2e-1,
        min=0,
        max=1,
        step=0.05,
    ),
    "recovery_chance": Slider(
        label="Recovery chance",
        value=2e-1,
        min=0,
        max=1,
        step=0.05,
    ),
    "mortality_chance": Slider(
        label="Mortality chance",
        value=1e-1,
        min=0,
        max=1,
        step=0.05,
    ),
}


def agent_portrayal(agent):
    if isinstance(agent, Pump):
        if agent.state == INFECTIOUS:
            return {"size": 50, "color": "tab:orange"}
        elif agent.state == SUSCEPTIBLE:
            return {"size": 50, "color": "tab:blue"}
    return {"size": 0, "color": "tab:blue"}


@solara.component
def Page():
    JupyterViz(
        Cholera,
        model_params,
        name="Cholera Model",
        agent_portrayal=agent_portrayal,
        measures=[["Susceptible", "Infectious", "Removed"]],
    )
