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

model = GameOfLifeModel(10, 10)

page = SolaraViz(
    model,
    components=[make_plot_measure(["Cells alive", "Fraction alive"])],
    name="Game of Life Model",
)
page  # noqa
