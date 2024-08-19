import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.experimental.devs.simulator import ABMSimulator
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from .agent import GrassPatch, Sheep, Wolf


def get_wolf_sheep_ratio(model):
    wolf_count = sum(isinstance(agent, Wolf) for agent in self.schedule.agents)
    sheep_count = sum(isinstance(agent, Sheep) for agent in self.schedule.agents)
    ratio = wolf_count / sheep_count if sheep_count > 0 else float("inf")
    return ratio


def compute_gini(model):
    agent_energies = [
        agent.energy
        for agent in model.schedule.agents
        if isinstance(agent, (Sheep, Wolf))
    ]
    if len(agent_energies) == 0:
        return 0
    sorted_energies = sorted(agent_energies)
    N = len(agent_energies)
    cumulative_energy = np.cumsum(sorted_energies)
    B = sum(cumulative_energy) / (N * cumulative_energy[-1])
    return 1 + (1 / N) - 2 * B


class WolfSheep(Model):
    """Wolf-Sheep Predation Model"""

    def __init__(
        self,
        width=20,
        height=20,
        initial_sheep=100,
        initial_wolves=50,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=False,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=True)

        self.datacollector = DataCollector(
            model_reporters={
                "Wolf/Sheep Ratio": get_wolf_sheep_ratio,
                "Gini": compute_gini,
            },
            agent_reporters={"Energy": "energy"},
        )

        self.simulator = ABMSimulator()
        self.simulator.setup(self)

        self._init_population()

        self.running = True
        self.datacollector.collect(self)

    def _init_population(self):
        # Create sheep
        for i in range(self.initial_sheep):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.sheep_gain_from_food)
            sheep = Sheep(
                self.next_id(),
                self,
                True,
                energy,
                self.sheep_reproduce,
                self.sheep_gain_from_food,
            )
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create wolves
        for i in range(self.initial_wolves):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            wolf = Wolf(
                self.next_id(),
                self,
                True,
                energy,
                self.wolf_reproduce,
                self.wolf_gain_from_food,
            )
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create grass patches
        if self.grass:
            for agent, (x, y) in self.grid.coord_iter():
                fully_grown = self.random.choice([True, False])
                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)
                patch = GrassPatch(self.next_id(), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run_model(self, step_count=200):
        self.simulator.run_for(time_delta=step_count)
