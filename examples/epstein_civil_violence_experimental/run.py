from model import EpsteinCivilViolence
from mesa.experimental.devs.simulator import ABMSimulator

if __name__ == "__main__":
    model = EpsteinCivilViolence(seed=15)
    simulator = ABMSimulator()

    simulator.setup(model)

    simulator.run(time_delta=100)
