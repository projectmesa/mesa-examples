import mesa

from wolf_sheep.agents import GrassPatch, Elk, Wolf, WateringHole
from wolf_sheep.model import WolfElk


def wolf_elk_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Elk:
        portrayal["Shape"] = "wolf_sheep/resources/icons8-deer-50.png"
        # https://icons8.com/icon/5038/deer
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2

    elif type(agent) is Wolf:
        portrayal["Shape"] = "wolf_sheep/resources/wolf.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        
    elif type(agent) is WateringHole:
        portrayal["Color"] = ["#728cff", "#0000FF"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(wolf_elk_portrayal, 50, 30, 1000, 600)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Wolves", "Color": "#AA0000"},
        {"Label": "Elk", "Color": "#666666"},
        {"Label": "Grass", "Color": "#00AA00"},
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:"),
    "grass": mesa.visualization.Checkbox("Grass Enabled", True),
    "water": mesa.visualization.Checkbox("Water Enabled", True),
    "grass_regrowth_time": mesa.visualization.Slider("Grass Regrowth Time", 20, 1, 50),
    "initial_elk": mesa.visualization.Slider(
        "Initial Elk Population", 1700, 10, 2000
    ),
    "elk_reproduce": mesa.visualization.Slider(
        "Elk Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    ),
    "initial_wolves": mesa.visualization.Slider("Initial Wolf Population", 14, 5, 300),
    "wolf_reproduce": mesa.visualization.Slider(
        "Wolf Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which wolf agents reproduce.",
    ),
    "wolf_gain_from_food": mesa.visualization.Slider(
        "Wolf Gain From Food Rate", 20, 1, 50
    ),
    "elk_gain_from_food": mesa.visualization.Slider("Elk Gain From Food", 4, 1, 10),
}

server = mesa.visualization.ModularServer(
    WolfElk, [canvas_element, chart_element], "Wolf Elk Predation", model_params
)
server.port = 8521
