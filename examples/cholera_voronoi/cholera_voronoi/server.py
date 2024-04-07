import mesa
from cholera.model import Cholera


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
    "cases_ratio_to_fix_pump": mesa.visualization.Slider(
        name="Ratio of cases in a neighborhood / total person in system to fix pump",
        value=0.1,
        min_value=0,
        max_value=0.3,
        step=0.001,
    ),
    "pumps_neighbor_contamination_chance": mesa.visualization.Slider(
        name="Pump chance of contaminate a neighbor",
        value=2e-1,
        min_value=0,
        max_value=1,
        step=0.05,
    ),
    "pumps_person_contamination_chance": mesa.visualization.Slider(
        name="Pump chance of contaminate a person",
        value=2e-1,
        min_value=0,
        max_value=1,
        step=0.05,
    ),
    "recovery_chance": mesa.visualization.Slider(
        name="Infected person recovery chance",
        value=2e-1,
        min_value=0,
        max_value=1,
        step=0.05,
    ),
    "mortality_chance": mesa.visualization.Slider(
        name="Infected person mortality chance",
        value=1e-1,
        min_value=0,
        max_value=1,
        step=0.05,
    ),
}

chart = mesa.visualization.ChartModule(
    [
        {"Label": "Susceptible", "Color": "#008000"},
        {"Label": "Infectious", "Color": "#FF0000"},
        {"Label": "Removed", "Color": "#808080"},
    ]
)

server = mesa.visualization.ModularServer(
    Cholera,
    [chart, get_removed_people, get_infectious_pumps],
    model_params=model_params,
)
