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
from .agents import SsAgent, Sugar
import numpy as np

class SugarscapeCg(mesa.Model):
    """
    Sugarscape 2 Constant Growback
    """

    verbose = True  # Print-monitoring

    def __init__(self, width=50, height=50, initial_population=100):
        """
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
        """
        super().__init__()

        # Set parameters
        self.width = width
        self.height = height
        self.initial_population = initial_population

        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)

        # Initialize agents by type
        self.agents_by_type = {SsAgent: [], Sugar: []}

        # Set up data collector
        self.datacollector = mesa.DataCollector(
            {"SsAgent": lambda m: len(m.agents_by_type[SsAgent])}
        )
        self.steps = 0

        # Create sugar
        sugar_distribution = np.genfromtxt(Path(__file__).parent / "sugar-map.txt")
        sugar_id = 1
        for (contents, x, y) in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar(sugar_id, self, max_sugar)
            self.grid.place_agent(sugar, (x, y))
            self.agents_by_type[Sugar].append(sugar)  # Track sugar agents
            sugar_id += 1

        # Create agents
        agent_id = 1
        for i in range(self.initial_population):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            sugar = self.random.randrange(6, 25)
            metabolism = self.random.randrange(2, 4)
            vision = self.random.randrange(1, 6)
            ssa = SsAgent(agent_id, self, False, sugar, metabolism, vision)
            self.grid.place_agent(ssa, (x, y))
            self.agents_by_type[SsAgent].append(ssa)  # Track SsAgent agents
            agent_id += 1

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        # Step sugar and agents
        for sugar in self.agents_by_type[Sugar]:
            sugar.step()
        for agent in self.agents_by_type[SsAgent]:
            agent.step()

        # Collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(f"Step: {self.steps}, SsAgents: {len(self.agents_by_type[SsAgent])}")
        self.steps += 1

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
