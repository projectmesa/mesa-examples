import solara
from ising.model import IsingModel
from mesa.visualization import SolaraViz

model_params = {
    "temperature": {
        "type": "SliderFloat",
        "label": "Temperature",
        "value": 2,
        "min": 0.01,
        "max": 10,
        "step": 0.06,
    },
    "spin_up_probability": {
        "type": "SliderFloat",
        "label": "Spin Up Probability",
        "value": 0.5,
        "min": 0,
        "max": 1,
        "step": 0.05,
    },
}


@solara.component
def Page():
    SolaraViz(
        IsingModel,
        model_params,
        name="Ising Model",
        # agent_portrayal=portray_spin,
    )
