import mesa
import mesa_geo.geoexperimental as mge
from model import GeoSchelling


class HappyElement(mesa.visualization.TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Happy agents: " + str(model.happy)


"""
model_params = {
    "density": mesa.visualization.Slider("Agent density", 0.6, 0.1, 1.0, 0.1),
    "minority_pc": mesa.visualization.Slider("Fraction minority", 0.2, 0.00, 1.0, 0.05),
    "export_data": mesa.visualization.Checkbox("Export data after simulation", False),
}
"""


def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    portrayal = {}
    if agent.atype is None:
        portrayal["color"] = "Grey"
    elif agent.atype == 0:
        portrayal["color"] = "Red"
    else:
        portrayal["color"] = "Blue"
    return portrayal


model_params = {
    "density": {
        "type": "SliderFloat",
        "value": 0.6,
        "label": "Population Density",
        "min": 0.0,
        "max": 1.0,
        "step": 0.1,
    },
    "minority_pc": {
        "type": "SliderFloat",
        "value": 0.2,
        "label": "Fraction Minority",
        "min": 0.0,
        "max": 1.0,
        "step": 0.05,
    },
    "export_data": {
        "type": "Checkbox",
        "value": False,
        "description": "Export Data",
        "disabled": False,
    },
}

page = mge.JupyterViz(
    GeoSchelling,
    model_params,
    measures=["happy"],
    name="Geo-Schelling Model",
    agent_portrayal=schelling_draw,
    zoom=3,
    center_point=[52, 12],
)

page  # noqa: B018
