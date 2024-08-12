import enum
import math
from mesa import Agent

class AgentState(enum.IntEnum):
    QUIESCENT = 0
    ARRESTED = 1
    ACTIVE = 2

class EpsteinAgent(Agent):
    def __init__(self, unique_id, model, vision, movement):
        super().__init__(unique_id, model)
        self.vision = vision
        self.movement = movement

class Citizen(EpsteinAgent):
    def __init__(
        self,
        unique_id,
        model,
        vision,
        movement,
        hardship,
        regime_legitimacy,
        risk_aversion,
        threshold,
        arrest_prob_constant,
    ):
        super().__init__(unique_id, model, vision, movement)
        self.hardship = hardship
        self.regime_legitimacy = regime_legitimacy
        self.risk_aversion = risk_aversion
        self.threshold = threshold
        self.condition = AgentState.QUIESCENT
        self.grievance = self.hardship * (1 - self.regime_legitimacy)
        self.arrest_probability = None
        self.arrest_prob_constant = arrest_prob_constant
        self.jail_time_remaining = 0

    def step(self):
        if self.condition == AgentState.ARRESTED:
            self.jail_time_remaining -= 1
            if self.jail_time_remaining <= 0:
                self.release_from_jail()
            return

        self.update_neighbors()
        self.update_estimated_arrest_probability()
        net_risk = self.risk_aversion * self.arrest_probability
        if self.grievance - net_risk > self.threshold:
            self.condition = AgentState.ACTIVE
        else:
            self.condition = AgentState.QUIESCENT
        if self.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.model.grid.move_agent(self, new_pos)

    def update_neighbors(self):
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, radius=self.vision
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]

    def update_estimated_arrest_probability(self):
        cops_in_vision = len([c for c in self.neighbors if isinstance(c, Cop)])
        actives_in_vision = 1.0  # citizen counts herself
        for c in self.neighbors:
            if isinstance(c, Citizen) and c.condition == AgentState.ACTIVE:
                actives_in_vision += 1
        self.arrest_probability = 1 - math.exp(
            -1 * self.arrest_prob_constant * (cops_in_vision / actives_in_vision)
        )

    def sent_to_jail(self, jail_time):
        self.model.schedule.remove(self)
        self.condition = AgentState.ARRESTED
        self.jail_time_remaining = jail_time

    def release_from_jail(self):
        self.model.schedule.add(self)
        self.condition = AgentState.QUIESCENT

class Cop(EpsteinAgent):
    def __init__(self, unique_id, model, vision, movement, max_jail_term):
        super().__init__(unique_id, model, vision, movement)
        self.max_jail_term = max_jail_term

    def step(self):
        self.update_neighbors()
        active_neighbors = []
        for agent in self.neighbors:
            if isinstance(agent, Citizen) and agent.condition == AgentState.ACTIVE:
                active_neighbors.append(agent)
        if active_neighbors:
            arrestee = self.random.choice(active_neighbors)
            arrestee.sent_to_jail(self.random.randint(0, self.max_jail_term))
        if self.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.model.grid.move_agent(self, new_pos)

    def update_neighbors(self):
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, radius=self.vision
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]
