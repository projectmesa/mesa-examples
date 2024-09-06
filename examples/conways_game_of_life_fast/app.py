from mesa.visualization import SolaraViz
from model import GameOfLifeModel

model_params = {
    "width": {
        "type": "SliderInt",
        "value": 10,
        "label": "Width",
        "min": 5,
        "max": 25,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 10,
        "label": "Height",
        "min": 5,
        "max": 25,
        "step": 1,
    },
}

page = SolaraViz(
    GameOfLifeModel,
    model_params,
    measures=["Cells alive", "Fraction alive"],
    space_drawer=None,
    name="Game of Life Model",
)
page  # noqa
