import numpy as np
from mesa.experimental import JupyterViz, prepare_matplotlib_space
from sugarscape_g1mt.model import SugarscapeG1mt
from sugarscape_g1mt.resource_agents import Sugar
from sugarscape_g1mt.trader_agents import Trader


@prepare_matplotlib_space
def space_drawer(viz, fig, ax):
    def portray(g):
        layers = {
            "sugar": [[np.nan for j in range(g.height)] for i in range(g.width)],
            "spice": [[np.nan for j in range(g.height)] for i in range(g.width)],
            "trader": {"x": [], "y": [], "c": "tab:red", "marker": "o", "s": 10},
        }

        for content, (i, j) in g.coord_iter():
            for agent in content:
                if isinstance(agent, Trader):
                    layers["trader"]["x"].append(i)
                    layers["trader"]["y"].append(j)
                else:
                    # Don't visualize resource with value <= 1.
                    value = agent.amount if agent.amount > 1 else np.nan
                    if isinstance(agent, Sugar):
                        layers["sugar"][i][j] = value
                    else:
                        layers["spice"][i][j] = value
        return layers

    out = portray(viz.model.grid)
    # Sugar
    # Important note: imshow by default draws from upper left. You have to
    # always explicitly specify origin="lower".
    im = ax.imshow(out["sugar"], cmap="spring", origin="lower")
    fig.colorbar(im, orientation="vertical")
    # Spice
    ax.imshow(out["spice"], cmap="winter", origin="lower")
    # Trader
    ax.scatter(**out["trader"])


model_params = {
    "width": 50,
    "height": 50,
}

page = JupyterViz(
    SugarscapeG1mt,
    model_params,
    measures=["Trader", "Price"],
    name="Sugarscape {G1, M, T}",
    space_drawer=space_drawer,
    play_interval=1500,
)
page  # noqa
