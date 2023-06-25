from typing import Tuple

import mesa
import mesa_geo as mg

from .model import Rainfall
from .space import LakeCell

model_params = {
    "rain_rate": mesa.visualization.Slider("rain rate", 500, 0, 500, 5),
    "water_height": mesa.visualization.Slider("water height", 5, 1, 5, 1),
    "num_steps": mesa.visualization.Slider("total number of steps", 20, 1, 100, 1),
    "export_data": mesa.visualization.Checkbox("export data after simulation", False),
}


def cell_portrayal(cell: LakeCell) -> Tuple[float, float, float, float]:
    if cell.water_level == 0:
        return cell.elevation, cell.elevation, cell.elevation, 1
    else:
        # return a blue color gradient based on the normalized water level
        # from the lowest water level colored as RGBA: (74, 141, 255, 1)
        # to the highest water level colored as RGBA: (0, 0, 255, 1)
        return (
            (1 - cell.water_level_normalized) * 74,
            (1 - cell.water_level_normalized) * 141,
            255,
            1,
        )


map_module = mg.visualization.MapModule(
    portrayal_method=cell_portrayal,
    map_height=341,
    map_width=498,
)
water_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Total Amount of Water", "Color": "Black"},
        {"Label": "Total Contained", "Color": "Blue"},
        {"Label": "Total Outflow", "Color": "Orange"},
    ]
)

server = mesa.visualization.ModularServer(
    Rainfall, [map_module, water_chart], "Rainfall Model", model_params
)
