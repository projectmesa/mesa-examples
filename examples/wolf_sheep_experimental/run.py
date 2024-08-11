from model import WolfSheepPredation
from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt


def run_model():
    model_params = {
        "width": 20,
        "height": 20,
        "initial_sheep": 50,
        "initial_wolves": 50,
        "sheep_reproduce": 0.04,
        "wolf_reproduce": 0.05,
        "sheep_gain_from_food": 4,
        "wolf_gain_from_food": 20,
    }

    batch_run = BatchRunner(
        WolfSheepPredation,
        model_params,
        iterations=5,
        max_steps=200,
        model_reporters={
            "Wolves": lambda m: m.count_type(m, Wolf),
            "Sheep": lambda m: m.count_type(m, Sheep),
            "Grass": lambda m: m.count_type(m, GrassPatch),
        },
    )

    batch_run.run_all()

    run_data = batch_run.get_model_vars_dataframe()
    run_data.plot()
    plt.show()


if __name__ == "__main__":
    run_model()
