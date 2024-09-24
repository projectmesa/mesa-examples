import mesa
import numpy as np

from .spin import Spin


class IsingModel(mesa.Model):
    def __init__(
        self,
        width=50,
        height=50,
        spin_up_probability: float = 0.7,
        temperature: float = 1,
    ):
        super().__init__()
        self.temperature = temperature
        self.grid = mesa.space.SingleGrid(width, height, torus=True)

        for contents, (x, y) in self.grid.coord_iter():
            cell = Spin((x, y), self, Spin.DOWN)
            if self.random.random() < spin_up_probability:
                cell.state = cell.UP
            self.grid.place_agent(cell, (x, y))

        self.running = True

    def step(self):
        agents_list = list(self.agents)
        for i in range(1000):
            random_spin = self.random.choice(agents_list)
            dE = self.get_energy_change(random_spin)
            if dE < 0 or self.random.random() < self.boltzmann_factor(dE):
                random_spin.state *= -1

    def get_energy_change(self, spin: Spin):
        neighbors = spin.neighbors()
        sum_over_neighbors = 0
        for neighbor in neighbors:
            sum_over_neighbors += neighbor.state
        return sum_over_neighbors * 2 * spin.state

    def boltzmann_factor(self, dE):
        return np.exp(-dE / self.temperature)
