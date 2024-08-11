import enum
from mesa import Agent


class AgentState(enum.IntEnum):
    QUIESCENT = enum.auto()
    ARRESTED = enum.auto()
    ACTIVE = enum.auto()


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
        self.arrest_prob_constant = arrest_prob_constant
        self.condition = AgentState.QUIESCENT

    def step(self):
        # Implement the behavior of Citizen agents here
        pass

    def sent_to_jail(self, jail_term):
        self.condition = AgentState.ARRESTED
        self.jail_term = jail_term


class Cop(EpsteinAgent):
    def __init__(self, unique_id, model, vision, movement, max_jail_term):
        super().__init__(unique_id, model, vision, movement)
        self.max_jail_term = max_jail_term

    def step(self):
        self.update_neighbors()
        active_neighbors = [
            agent
            for agent in self.neighbors
            if isinstance(agent, Citizen) and agent.condition == AgentState.ACTIVE
        ]
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
