from mesa.visualization import SolaraViz, make_plot_measure, make_space_matplotlib
from model import GameOfLifeModel

propertylayer_portrayal = {
    "cell_layer": {
        "color": "Black",
        "alpha": 1,
        "colorbar": False,
    },
}

model_params = {
    "width": {
        "type": "SliderInt",
        "value": 30,
        "label": "Width",
        "min": 5,
        "max": 60,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 30,
        "label": "Height",
        "min": 5,
        "max": 60,
        "step": 1,
    },
    "alive_fraction": {
        "type": "SliderFloat",
        "value": 0.2,
        "label": "Cells alive",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "randomize_new_cells": {  # Новий параметр для ручного регулювання
        "type": "SliderFloat",
        "value": 0.05,  # Початкова ймовірність оживлення нових клітин
        "label": "New Cells Randomization",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
}


gol = GameOfLifeModel(
    width=model_params["width"]["value"],
    height=model_params["height"]["value"],
    alive_fraction=model_params["alive_fraction"]["value"],
    randomize_new_cells=model_params["randomize_new_cells"]["value"],
)


layer_viz = make_space_matplotlib(propertylayer_portrayal=propertylayer_portrayal)
TotalAlivePlot = make_plot_measure("Cells alive")

page = SolaraViz(
    gol,
    components=[layer_viz, TotalAlivePlot],
    model_params=model_params,
    name="Game of Life Model",
)
