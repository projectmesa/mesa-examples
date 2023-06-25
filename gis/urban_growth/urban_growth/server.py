from typing import Tuple

import mesa
import mesa_geo as mg

from .model import UrbanGrowth
from .space import UrbanCell


def cell_portrayal(cell: UrbanCell) -> Tuple[float, float, float, float]:
    if cell.urban:
        if cell.old_urbanized:
            return 0, 0, 255, 1
        else:
            return 255, 0, 0, 1
    else:
        return 0, 0, 0, 0


class UrbanizedText(mesa.visualization.TextElement):
    def render(self, model):
        return f"Percentage Urbanized: {model.pct_urbanized:.2f}%"


model_params = {
    "max_coefficient": mesa.visualization.NumberInput("max_coefficient", 100),
    "dispersion_coefficient": mesa.visualization.Slider(
        "dispersion_coefficient", 20, 0, 100, 1
    ),
    "spread_coefficient": mesa.visualization.Slider(
        "spread_coefficient", 27, 0, 100, 1
    ),
    "breed_coefficient": mesa.visualization.Slider("breed_coefficient", 5, 0, 100, 1),
    "rg_coefficient": mesa.visualization.Slider("rg_coefficient", 10, 0, 100, 1),
    "slope_coefficient": mesa.visualization.Slider("slope_coefficient", 50, 0, 100, 1),
    "critical_slope": mesa.visualization.Slider("critical_slope", 25, 0, 100, 1),
    "road_influence": mesa.visualization.Choice(
        "road_influence", False, choices=[True, False]
    ),
}


map_module = mg.visualization.MapModule(
    portrayal_method=cell_portrayal,
    view=[12.904598815296707, -8.027435210420451],
    zoom=12.1,
    map_height=394,
    map_width=531,
    scale_options={"imperial": False},
)
urbanized_text = UrbanizedText()
urbanized_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Percentage Urbanized", "Color": "Black"},
    ]
)

server = mesa.visualization.ModularServer(
    UrbanGrowth,
    [map_module, urbanized_text, urbanized_chart],
    "Urban Growth Model",
    model_params,
)
