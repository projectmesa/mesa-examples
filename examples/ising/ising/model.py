import mesa
import numpy as np

from .spin import Spin


class IsingModel(mesa.Model):
    BOLTZMANN_CONSTANT = 1.380649e-23

    def __init__(
        self,
        width=50,
        height=50,
        spin_up_probability: float = 0.5,
        temperature: float = 2.27,
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
        random_spin = self.random.choice(agents_list)
        dE = self.get_energy_change(random_spin)
        if dE < 0:
            random_spin.state *= -1
        else:
            if self.random.random() < self.boltzmann(dE):
                random_spin.state *= -1

    def get_energy_change(self, spin: Spin):
        neighbors = spin.neighbors()
        sum_over_neighbors = 0
        for neighbor in neighbors:
            sum_over_neighbors += spin.state * neighbor.state
        return -1 * sum_over_neighbors

    def boltzmann(self, dE):
        return np.exp(-dE / (self.BOLTZMANN_CONSTANT * self.temperature))
