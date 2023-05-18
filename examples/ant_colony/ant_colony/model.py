"""
Ant Adaptation Model
================================

Replication of the model found in NetLogo:
    Martin, K. and Wilensky, U. (2019). NetLogo Ant Adaptation model.
    http://ccl.northwestern.edu/netlogo/models/AntAdaptation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

import mesa
import numpy as np

from ant_colony.scheduler import RandomActivationByTypeFiltered
from ant_colony.agents import Ant


class AntColony(mesa.Model):
    """
    Ant Predation Model
    """

    height = 50
    width = 50

    initial_red_ants = 7
    initial_blue_ants = 7

    red_cost = 7
    blue_cost = 7

    red_size = 6
    blue_size = 6

    red_aggression = 30
    blue_aggression = 30

    red_starting_energy = 2000
    blue_starting_energy = 2000

    pheromone_evaporation_rate = 1.0

    verbose = False  # Print-monitoring

    description = (
        "A model with two ant colonies who send out their foragers to move around and find food."
    )

    def __init__(
        self,
        width=50,
        height=50,
        initial_red_ants=7,
        initial_blue_ants=7,
        red_cost=7,
        blue_cost=7,
        red_size=6,
        blue_size=6,
        red_aggression=30,
        blue_aggression=30,
        red_starting_energy=2000,
        blue_starting_energy=2000,
        pheromone_evaporation_rate=1.0
    ):
        """
        Create a new Ant Adaptation model with the given parameters.

        Args:
            initial_red_ants: Number of red ants to start with
            initial_blue_ants: Number of blue ants to start with
            red_cost: The amount of food needed to make a new red ant
            blue_cost: The amount of food needed to make a new blue ant
            red_size: The size of the red ants
            blue_size: The size of the blue ants
            red_aggression: Aggression level of red ants
            blue_aggression: Aggression level of blue ants
            red_starting_energy: Starting energy of red ants.
            blue_starting_energy: Starting energy of blue ants.
            pheromone_evaporation_rate:
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_red_ants = initial_red_ants
        self.initial_blue_ants = initial_blue_ants
        self.red_cost = red_cost
        self.blue_cost = blue_cost
        self.red_size = red_size
        self.blue_size = blue_size
        self.red_aggression = red_aggression
        self.blue_aggression = blue_aggression
        self.red_starting_energy = red_starting_energy
        self.blue_starting_energy = blue_starting_energy
        self.pheromone_evaporation_rate = pheromone_evaporation_rate
        self.space = mesa.space.ContinuousSpace(width, height, True)
        self.schedule = RandomActivationByTypeFiltered(self)
        self.datacollector = mesa.DataCollector(
            {
                "Ants": lambda m: m.schedule.get_type_count(Ant)
            }
        )

        # Create red ants:
        for i in range(self.initial_red_ants):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.red_starting_energy
            ant = Ant(self.next_id(), (x, y), self, moore=True)
            self.space.place_agent(ant, np.array((x, y)))
            self.schedule.add(ant)

        # Create blue ants:
        for i in range(self.initial_blue_ants):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.red_starting_energy
            ant = Ant(self.next_id(), (x, y), self, moore=True, color='blue')
            self.space.place_agent(ant, np.array((x, y)))
            self.schedule.add(ant)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_type_count(Ant)
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number wolves: ", self.schedule.get_type_count(Ant))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number wolves: ", self.schedule.get_type_count(Ant))
