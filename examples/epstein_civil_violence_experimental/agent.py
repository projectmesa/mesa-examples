import enum
import math
from mesa import Agent


class EpsteinAgent(Agent):
    def __init__(self, unique_id, model, vision, movement):
        super().__init__(unique_id, model)
        self.vision = vision
        self.movement = movement


class AgentState(enum.IntEnum):
    QUIESCENT = enum.auto()
    ARRESTED = enum.auto()
    ACTIVE = enum.auto()


class Citizen(EpsteinAgent):
    """
    A member of the general population, may or may not be in active rebellion.
    Summary of rule: If grievance - risk > threshold, rebel.

    Attributes:
        unique_id: unique int
        model :
        hardship: Agent's 'perceived hardship (i.e., physical or economic
            privation).' Exogenous, drawn from U(0,1).
        regime_legitimacy: Agent's perception of regime legitimacy, equal
            across agents.  Exogenous.
        risk_aversion: Exogenous, drawn from U(0,1).
        threshold: if (grievance - (risk_aversion * arrest_probability)) >
            threshold, go/remain Active
        vision: number of cells in each direction (N, S, E and W) that agent
            can inspect
        condition: Can be "Quiescent" or "Active;" deterministic function of
            greivance, perceived risk, and
        grievance: deterministic function of hardship and regime_legitimacy;
            how aggrieved is agent at the regime?
        arrest_probability: agent's assessment of arrest probability, given
            rebellion
    """

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
        """
        Create a new Citizen.
        Args:
            unique_id: unique int
            model : model instance
            hardship: Agent's 'perceived hardship (i.e., physical or economic
                privation).' Exogenous, drawn from U(0,1).
            regime_legitimacy: Agent's perception of regime legitimacy, equal
                across agents.  Exogenous.
            risk_aversion: Exogenous, drawn from U(0,1).
            threshold: if (grievance - (risk_aversion * arrest_probability)) >
                threshold, go/remain Active
            vision: number of cells in each direction (N, S, E and W) that
                agent can inspect. Exogenous.
        """
        super().__init__(unique_id, model, vision, movement)
        self.hardship = hardship
        self.regime_legitimacy = regime_legitimacy
        self.risk_aversion = risk_aversion
        self.threshold = threshold
        self.condition = AgentState.QUIESCENT
        self.grievance = self.hardship * (1 - self.regime_legitimacy)
        self.arrest_probability = None
        self.arrest_prob_constant = arrest_prob_constant

    def step(self):
        """
        Decide whether to activate, then move if applicable.
        """
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
        """
        Look around and see who my neighbors are
        """
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, radius=self.vision
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]

    def update_estimated_arrest_probability(self):
        """
        Based on the ratio of cops to actives in my neighborhood, estimate the
        p(Arrest | I go active).
        """
        cops_in_vision = len([c for c in self.neighbors if isinstance(c, Cop)])
        actives_in_vision = 1.0  # citizen counts herself
        for c in self.neighbors:
            if isinstance(c, Citizen) and c.condition == AgentState.ACTIVE:
                actives_in_vision += 1
        self.arrest_probability = 1 - math.exp(
            -1 * self.arrest_prob_constant * (cops_in_vision / actives_in_vision)
        )

    def sent_to_jail(self, value):
        self.model.active_agents.remove(self)
        self.condition = AgentState.ARRESTED
        self.model.simulator.schedule_event_relative(self.release_from_jail, value)

    def release_from_jail(self):
        self.model.active_agents.add(self)
        self.condition = AgentState.QUIESCENT


class Cop(EpsteinAgent):
    """
    A cop for life.  No defection.
    Summary of rule: Inspect local vision and arrest a random active agent.

    Attributes:
        unique_id: unique int
        x, y: Grid coordinates
        vision: number of cells in each direction (N, S, E and W) that cop is
            able to inspect
    """

    def __init__(self, unique_id, model, vision, movement, max_jail_term):
        super().__init__(unique_id, model, vision, movement)
        self.max_jail_term = max_jail_term

    def step(self):
        """
        Inspect local vision and arrest a random active agent. Move if
        applicable.
        """
        self.update_neighbors()
        active_neighbors = []
        for agent in self.neighbors:
            if isinstance(agent, Citizen) and agent.condition == "Active":
                active_neighbors.append(agent)
        if active_neighbors:
            arrestee = self.random.choice(active_neighbors)
            arrestee.sent_to_jail(self.random.randint(0, self.max_jail_term))
        if self.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.model.grid.move_agent(self, new_pos)

    def update_neighbors(self):
        """
        Look around and see who my neighbors are.
        """
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, radius=self.vision
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]
