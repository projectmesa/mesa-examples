import mesa


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B


class BoltzmannWealthModel(mesa.Model):
    """A simple model of an economy where agents exchange currency at random.

    All the agents begin with one unit of currency, and each time step can give
    a unit of currency to another agent. Note how, over time, this produces a
    highly skewed distribution of wealth.
    """

    def __init__(self, N=100, width=10, height=10):
        super().__init__()
        self.num_agents = N
        self.grid = mesa.spaces.OrthogonalMooreGrid(
            (width, height), torus=True, random=self.random
        )

        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        )
        # Create agents
        for _ in range(self.num_agents):
            agent = MoneyAgent(self)

            # Add the agent to a random grid cell
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            agent.move_to(self.grid[(x, y)])

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.agents.shuffle().do("step")
        # collect data
        self.datacollector.collect(self)

    def run_model(self, n):
        for i in range(n):
            self.step()


class MoneyAgent(mesa.spaces.CellAgent):
    """An agent with fixed initial wealth."""

    def __init__(self, model):
        super().__init__(model)
        self.wealth = 1

    def give_money(self):
        cellmates = [agent for agent in self.cell.agents if agent is not self]
        if len(cellmates) > 0:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        self.move_to(self.cell.neighborhood().select_random_cell())
        if self.wealth > 0:
            self.give_money()
