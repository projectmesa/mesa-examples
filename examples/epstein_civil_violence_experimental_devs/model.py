import mesa
import random
import numpy as np
from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from .agent import AgentState, Citizen, Cop


def compute_gini(model):
    agent_hardships = [
        agent.hardship for agent in model.schedule.agents if isinstance(agent, Citizen)
    ]
    if len(agent_hardships) == 0:
        return 0
    sorted_hardships = sorted(agent_hardships)
    N = len(agent_hardships)
    cumulative_hardship = np.cumsum(sorted_hardships)
    B = sum(cumulative_hardship) / (N * cumulative_hardship[-1])
    return 1 + (1 / N) - 2 * B


class EpsteinCivilViolence(Model):
    def __init__(
        self,
        width=40,
        height=40,
        citizen_density=0.7,
        cop_density=0.074,
        citizen_vision=7,
        cop_vision=7,
        legitimacy=0.8,
        max_jail_term=1000,
        active_threshold=0.1,
        arrest_prob_constant=2.3,
        movement=True,
        max_iters=1000,
        seed=None,
    ):
        super().__init__(seed)
        if cop_density + citizen_density > 1:
            raise ValueError("Cop density + citizen density must be less than 1")

        self.width = width
        self.height = height
        self.citizen_density = citizen_density
        self.cop_density = cop_density
        self.citizen_vision = citizen_vision
        self.cop_vision = cop_vision
        self.legitimacy = legitimacy
        self.max_jail_term = max_jail_term
        self.active_threshold = active_threshold
        self.arrest_prob_constant = arrest_prob_constant
        self.movement = movement
        self.max_iters = max_iters
        self.iteration = 0
        self.random = random.Random(seed)
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(self.width, self.height, torus=True)

        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Hardship": "hardship"},
        )

        unique_id = 0
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < self.cop_density:
                cop = Cop(
                    unique_id,
                    self,
                    vision=self.cop_vision,
                    movement=self.movement,
                    max_jail_term=self.max_jail_term,
                )
                unique_id += 1
                self.grid.place_agent(cop, (x, y))
                self.schedule.add(cop)
            elif self.random.random() < (self.cop_density + self.citizen_density):
                citizen = Citizen(
                    unique_id,
                    self,
                    vision=self.citizen_vision,
                    movement=self.movement,
                    hardship=self.random.random(),
                    regime_legitimacy=self.legitimacy,
                    risk_aversion=self.random.random(),
                    threshold=self.active_threshold,
                    arrest_prob_constant=self.arrest_prob_constant,
                )
                unique_id += 1
                self.grid.place_agent(citizen, (x, y))
                self.schedule.add(citizen)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.iteration += 1
        if self.iteration >= self.max_iters:
            self.running = False

    @staticmethod
    def count_type_citizens(model, condition, exclude_jailed=True):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Citizen) and agent.condition == condition:
                if exclude_jailed and agent.condition == AgentState.ARRESTED:
                    continue
                count += 1
        return count

    @staticmethod
    def count_jailed(model):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Citizen) and agent.condition == AgentState.ARRESTED:
                count += 1
        return count

    @staticmethod
    def count_cops(model):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Cop):
                count += 1
        return count
