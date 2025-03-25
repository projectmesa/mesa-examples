
from agents import Person
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)
from model import BankReservesModel

"""
Citation:
The following code was adapted from server.py at
https://github.com/projectmesa/mesa/blob/main/examples/wolf_sheep/wolf_sheep/server.py
Accessed on: November 2, 2017
Author of original code: Taylor Mutch
"""

def person_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    # update portrayal characteristics for each Person object
    if isinstance(agent, Person):
        color = "tab:blue"
        # set agent color based on savings and loans
        if agent.savings > agent.model.rich_threshold:
            color = "green"
        if agent.savings < 10 and agent.loans < 10:
            color = "tab:blue"
        if agent.loans > 10:
            color = "tab:red"

        portrayal["color"] = color

    return portrayal

model_params = {
    "init_people": Slider(
        label="People",
        value=25,
        min=1,
        max=200,
    ),
    "rich_threshold": Slider(
        label="Rich Threshold",
        value=10,
        min=1,
        max=20,
    ),
    "reserve_percent":Slider(
        label="Reserves",
        value=50,
        min=1,
        max=100,
    )
}

SpacePlot = make_space_component(person_portrayal)
CategoryPlot = make_plot_component(["Rich","Poor","Middle Class"])
model = BankReservesModel()

page = SolaraViz(
    BankReservesModel(),
    components=[SpacePlot,CategoryPlot],
    model_params=model_params,
    name="Bank Reserves",
)
