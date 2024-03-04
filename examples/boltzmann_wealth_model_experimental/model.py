import mesa


def compute_gini(model):
    agent_wealths = model.agents.get("wealth")
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
        self.running = True  # TODO remove this line when at Mesa 3.0
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        )
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector.collect(self)

    def step(self):
        self.agents.shuffle().do("step")
        # Must be before data collection.
        self._advance_time()  # Temporary API; will be finalized by Mesa 3.0 release
        self.datacollector.collect(self)

    def run_model(self, n):
        for i in range(n):
            self.step()


class MoneyAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def move(self):
        possible_positions = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        self.model.grid.move_agent_to_one_of(self, possible_positions)

    def give_money(self):
        cellmates = [
            c
            for c in self.model.grid.get_cell_list_contents([self.pos])
            # Ensure agent is not giving money to itself
            if c is not self
        ]
        if len(cellmates) > 0:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()
