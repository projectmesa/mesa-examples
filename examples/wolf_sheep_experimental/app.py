import time
import solara
from mesa.visualization.solara_viz import SolaraViz, make_text
from .model import WolfSheep
from .agents import Sheep, Wolf, GrassPatch


def agent_portrayal(agent):
    if isinstance(agent, Sheep):
        portrayal = {
            "color": "tab:blue",
            "size": 50,
        }
    elif isinstance(agent, Wolf):
        portrayal = {
            "color": "tab:red",
            "size": 50,
        }
    elif isinstance(agent, GrassPatch):
        color = "tab:green" if agent.fully_grown else "tab:brown"
        portrayal = {
            "color": color,
            "size": 50,
        }
    return portrayal


def get_wolf_sheep_ratio(model):
    wolf_count = sum(isinstance(agent, Wolf) for agent in model.schedule.agents)
    sheep_count = sum(isinstance(agent, Sheep) for agent in model.schedule.agents)
    ratio = wolf_count / sheep_count if sheep_count > 0 else float("inf")
    return f"Wolf/Sheep Ratio: {ratio:.2f}"


model_params = {
    "width": 20,
    "height": 20,
    "initial_sheep": 100,
    "initial_wolves": 50,
    "sheep_reproduce": 0.04,
    "wolf_reproduce": 0.05,
    "wolf_gain_from_food": 20,
    "grass": True,
    "grass_regrowth_time": 30,
    "sheep_gain_from_food": 4,
}

page = SolaraViz(
    model_class=WolfSheep,
    model_params=model_params,
    measures=[
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

    # Add color legend
    solara.Markdown("""
    ## Color Legend
    - Blue: Sheep
    - Red: Wolves
    - Green: Fully grown grass
    - Brown: Eaten grass (regrowing)
    """)

    page.show()


if __name__ == "__main__":
    model = WolfSheep(25, 25, 60, 40, 0.2, 0.1, 20)
    start_time = time.perf_counter()
    for _ in range(100):
        model.step()
    print("Time:", time.perf_counter() - start_time)
    App()
