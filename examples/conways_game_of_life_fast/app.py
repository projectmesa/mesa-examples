from mesa.visualization import SolaraViz, make_plot_measure, make_space_matplotlib
from model import GameOfLifeModel

propertylayer_portrayal = {
    "cell_layer": {
        "color": "Black",
        "alpha": 1,
    },
}

model_params = {
    "width": {
        "type": "SliderInt",
        "value": 20,
        "label": "Width",
        "min": 5,
        "max": 40,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 20,
        "label": "Height",
        "min": 5,
        "max": 40,
        "step": 1,
    },
}

gol = GameOfLifeModel()

layer_viz = make_space_matplotlib(propertylayer_portrayal=propertylayer_portrayal)
TotalAlivePlot = make_plot_measure("Cells alive")
FractionAlivePlot = make_plot_measure("Fraction alive")

page = SolaraViz(
    gol,
    components=[layer_viz, TotalAlivePlot, FractionAlivePlot],
    model_params=model_params,
    name="Game of Life Model",
)
