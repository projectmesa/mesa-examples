from mesa.visualization import SolaraViz, make_plot_measure
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

gol = GameOfLifeModel(10, 10)

AlivePlot = make_plot_measure("Cells alive", "Fraction alive")


page = SolaraViz(
    gol,
    components=[AlivePlot],
    model_params=model_params,
    name="Game of Life Model",
)
page  # noqa
