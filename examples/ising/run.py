import solara
from ising.model import IsingModel
from ising.portrayal import portraySpin
from mesa.visualization import JupyterViz


@solara.component
def Page():
    JupyterViz(
        IsingModel,
        {},
        name="Ising Model Model",
        agent_portrayal=portraySpin,
    )
