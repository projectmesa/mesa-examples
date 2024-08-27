import solara
from ising.model import IsingModel
from ising.portrayal import portray_spin
from mesa.visualization import JupyterViz
from mesa.visualization.UserParam import Slider

model_params = {
    "temperature": Slider(
        label="Temperature", value=2, min=0.01, max=10, step=0.06, dtype=float
    ),
    "spin_up_probability": Slider(
        label="Spin Up Probability",
        value=0.5,
        min=0,
        max=1,
        step=0.05,
    ),
}


@solara.component
def Page():
    JupyterViz(
        IsingModel,
        model_params,
        name="Ising Model",
        agent_portrayal=portray_spin,
    )
