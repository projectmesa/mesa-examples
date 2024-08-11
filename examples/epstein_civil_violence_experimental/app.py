import solara
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import EpsteinCivilViolence
from agent import Citizen, Cop, AgentState


def agent_portrayal(agent):
    if isinstance(agent, Citizen):
        portrayal = {
            "Shape": "circle",
            "Color": "blue" if agent.condition == AgentState.QUIESCENT else "red",
            "Filled": "true",
            "r": 0.5,
        }
    elif isinstance(agent, Cop):
        portrayal = {
            "Shape": "rect",
            "Color": "black",
            "Filled": "true",
            "w": 0.5,
            "h": 0.5,
        }
    return portrayal


grid = CanvasGrid(agent_portrayal, 40, 40, 500, 500)

server = ModularServer(
    EpsteinCivilViolence,
    [grid],
    "Epstein Civil Violence Model",
    {
        "width": 40,
        "height": 40,
        "citizen_density": 0.7,
        "cop_density": 0.074,
        "citizen_vision": 7,
        "cop_vision": 7,
        "legitimacy": 0.8,
        "max_jail_term": 1000,
        "active_threshold": 0.1,
        "arrest_prob_constant": 2.3,
        "movement": True,
        "max_iters": 1000,
    },
)


@solara.component
def App():
    solara.Title("Epstein Civil Violence Model")
    solara.Markdown("# Epstein Civil Violence Model")
    solara.Markdown("This is a visualization of the Epstein Civil Violence Model.")
    server.launch()


if __name__ == "__main__":
    solara.run(App)
