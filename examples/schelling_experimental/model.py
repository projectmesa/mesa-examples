import mesa

from mesa.experimental.cell_space import CellAgent, OrthogonalMooreGrid

class SchellingAgent(CellAgent):
    """
    Schelling segregation agent
    """

    def __init__(self, model, agent_type):
        """
        Create a new Schelling agent.

        Args:
           agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(model)
        self.type = agent_type

    def step(self):
        similar = 0
        for neighbor in self.cell.neighborhood.agents:
            if neighbor.type == self.type:
                similar += 1

        # If unhappy, move:
        if similar < self.model.homophily:
            self.cell = self.model.grid.select_random_empty_cell()
        else:
            self.model.happy += 1


class Schelling(mesa.Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, width=20, height=20, density=0.8, minority_pc=0.2, homophily=3):
        super().__init__()
        self.width = width
        self.height = height
        self.homophily = homophily

        self.grid = OrthogonalMooreGrid((width, height), torus=True)

        self.happy = 0
        self.datacollector = mesa.DataCollector(
            {"happy": "happy"},  # Model-level count of happy agents
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.all_cells:
            if self.random.random() < density:
                agent_type = 1 if self.random.random() < minority_pc else 0
                agent = SchellingAgent(self, agent_type)
                agent.cell = cell

        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.agents.shuffle_do("step")
        # collect data
        self.datacollector.collect(self)

        if self.happy == len(self.agents):
            self.running = False
