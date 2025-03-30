from mesa.visualization import SolaraViz
from mesa.visualization.components.matplotlib_components import make_mpl_space_component
from model import TermiteModel

wood_chip_portrayal = {
    "woodcell": {
        "color": "blue",
        "alpha": 0.6,
        "colorbar": False,
        "vmin": 0,
        "vmax": 2,
    },
}


def agent_portrayal(agent):
    return {"marker": ">", "color": "red" if agent.hasWoodChip else "black", "size": 10}


model_params = {
    "num_termites": {
        "type": "SliderInt",
        "value": 50,
        "label": "No. of Termites",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "wood_chip_density": {
        "type": "SliderFloat",
        "value": 0.1,
        "label": "Wood Chip Density",
        "min": 0.01,
        "max": 1,
        "step": 0.1,
    },
    "width": 60,
    "height": 60,
}

model = TermiteModel(num_termites=400, width=100, height=100, wood_chip_density=0.1)


def post_process(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


woodchips_space = make_mpl_space_component(
    agent_portrayal=agent_portrayal,
    propertylayer_portrayal=wood_chip_portrayal,
    post_process=post_process,
    draw_grid=False,
)

page = SolaraViz(
    model,
    components=[woodchips_space],
    model_params=model_params,
    name="Termites Model",
    play_interval=1,
    render_interval=15,
)
