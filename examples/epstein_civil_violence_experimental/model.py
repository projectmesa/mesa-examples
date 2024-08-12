import sys
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid

# Add the mesa-examples-main directory to the Python path
sys.path.append('mesa-examples\\examples\\epstein_civil_violence_experimental')

from agent import Citizen, Cop

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

        self.max_iters = max_iters

        self.grid = SingleGrid(self.width, self.height, torus=True)
        self.schedule = RandomActivation(self)

        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.cop_density:
                agent = Cop(
                    self.next_id(),
                    self,
                    cop_vision,
                    movement,
                    max_jail_term,
                )
            elif self.random.random() < (self.cop_density + self.citizen_density):
                agent = Citizen(
                    self.next_id(),
                    self,
                    citizen_vision,
                    movement,
                    hardship=self.random.random(),
                    regime_legitimacy=legitimacy,
                    risk_aversion=self.random.random(),
                    threshold=active_threshold,
                    arrest_prob_constant=arrest_prob_constant,
                )
            else:
                continue
            self.grid.place_agent(agent, pos)
            self.schedule.add(agent)

        self.active_agents = self.schedule.agents

    def step(self):
        self.schedule.step()
