"""
Sugarscape Constant Growback Model
================================

Replication of the model found in Netlogo:
Li, J. and Wilensky, U. (2009). NetLogo Sugarscape 2 Constant Growback model.
http://ccl.northwestern.edu/netlogo/models/Sugarscape2ConstantGrowback.
Center for Connected Learning and Computer-Based Modeling,
Northwestern University, Evanston, IL.
"""

from pathlib import Path

import mesa
from mesa.experimental.cell_space import OrthogonalVonNeumannGrid

from .agents import SsAgent, Sugar


class SugarscapeCg(mesa.Model):
    """
    Sugarscape 2 Constant Growback
    """

    verbose = True  # Print-monitoring

    def __init__(self, width=50, height=50, initial_population=100, seed=None):
        """
        Create a new constant grow back model with the given parameters.

        Args:
            width (int): Width of the Sugarscape 2 Constant Growback model.
            height (int): Height of the Sugarscape 2 Constant Growback model.
            initial_population: Number of population to start with
            seed (int): Seed for the random number generator

        """
        super().__init__(seed=seed)

        # Set parameters
        self.width = width
        self.height = height
        self.initial_population = initial_population

        self.grid = OrthogonalVonNeumannGrid((self.width, self.height), torus=True)
        self.datacollector = mesa.DataCollector(
            {"SsAgent": lambda m: len(m.agents_by_type[SsAgent])}
        )

        # Create sugar
        import numpy as np

        sugar_distribution = np.genfromtxt(Path(__file__).parent / "sugar-map.txt")
        for cell in self.grid.all_cells:
            max_sugar = sugar_distribution[cell.coordinate]
            Sugar(self, max_sugar, cell)

        # Create agent:
        for i in range(self.initial_population):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            sugar = self.random.randrange(6, 25)
            metabolism = self.random.randrange(2, 4)
            vision = self.random.randrange(1, 6)
            cell = self.grid[(x, y)]
            SsAgent(self, cell, sugar, metabolism, vision)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        # Step suger and agents
        self.agents_by_type[Sugar].do("step")
        self.agents_by_type[SsAgent].shuffle_do("step")
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(f"Step: {self.steps}, SsAgents: {len(self.agents_by_type[SsAgent])}")

    def run_model(self, step_count=200):
        if self.verbose:
            print(
                f"Initial number Sugarscape Agents: {len(self.agents_by_type[SsAgent])}"
            )

        for i in range(step_count):
            self.step()

        if self.verbose:
            print(
                f"\nFinal number Sugarscape Agents: {len(self.agents_by_type[SsAgent])}"
            )
