import solara
from mesa.visualization import SolaraViz, make_text, make_plot
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from .model import WolfSheep
from .agents import Sheep, Wolf, GrassPatch

def agent_portrayal(agent):
    if isinstance(agent, Sheep):
        portrayal = {
            "Shape": "circle",
            "Color": "white",
            "Filled": "true",
            "r": 0.5,
            "Layer": 1
        }
    elif isinstance(agent, Wolf):
        portrayal = {
            "Shape": "circle",
            "Color": "black",
            "Filled": "true",
            "r": 0.5,
            "Layer": 1
        }
    elif isinstance(agent, GrassPatch):
        portrayal = {
            "Shape": "rect",
            "Color": "green" if agent.fully_grown else "brown",
            "Filled": "true",
            "w": 1,
            "h": 1,
            "Layer": 0
        }
    return portrayal

def get_wolf_sheep_ratio(model):
    wolf_count = sum(isinstance(agent, Wolf) for agent in model.schedule.agents)
    sheep_count = sum(isinstance(agent, Sheep) for agent in model.schedule.agents)
    ratio = wolf_count / sheep_count if sheep_count > 0 else float('inf')
    return f"Wolf/Sheep Ratio: {ratio:.2f}"

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

model_params = {
    "width": 20,
    "height": 20,
    "initial_sheep": 100,
    "initial_wolves": 50,
    "sheep_reproduce": 0.04,
    "wolf_reproduce": 0.05,
    "wolf_gain_from_food": 20,
    "grass": False,
    "grass_regrowth_time": 30,
    "sheep_gain_from_food": 4,
}

page = SolaraViz(
    model_class=WolfSheep,
    model_params=model_params,
    measures=[
        make_plot,
        make_text(get_wolf_sheep_ratio),
    ],
    name="Wolf-Sheep Predation Model",
    agent_portrayal=agent_portrayal,
)

@solara.component
def App():
    solara.Title("Wolf-Sheep Predation Model")
    solara.Markdown("# Wolf-Sheep Predation Model")
    solara.Markdown("This is a visualization of the Wolf-Sheep Predation Model.")
    page.show()

if __name__ == "__main__":
    solara.run(App)
