import mesa
import networkx as nx


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.agents]
    x = sorted(agent_wealths)
    N = model.num_agents  # noqa: N806
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))  # noqa: N806
    return 1 + (1 / N) - 2 * B


class BoltzmannWealthModelNetwork(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, num_agents=7, num_nodes=10):
        super().__init__()
        self.num_agents = num_agents
        self.num_nodes = num_nodes if num_nodes >= self.num_agents else self.num_agents
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=0.5)
        self.grid = mesa.experimental.cell_space.Network(
            self.G, random=self.random, capacity=1
        )

        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": lambda _: _.wealth},
        )

        list_of_random_nodes = self.random.sample(list(self.G), self.num_agents)

        # Create agents
        for position in list_of_random_nodes:
            agent = MoneyAgent(self)

            # Add the agent to a random node
            agent.move_to(self.grid[position])

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.agents.shuffle_do("step")
        # collect data
        self.datacollector.collect(self)

    def run_model(self, n):
        for _ in range(n):
            self.step()


class MoneyAgent(mesa.experimental.cell_space.CellAgent):
    """An agent with fixed initial wealth."""

    def __init__(self, model):
        super().__init__(model)
        self.wealth = 1

    def give_money(self):
        neighbors = [agent for agent in self.cell.neighborhood.agents if not self]
        if len(neighbors) > 0:
            other = self.random.choice(neighbors)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        empty_neighbors = [cell for cell in self.cell.neighborhood if cell.is_empty]
        if empty_neighbors:
            self.cell = self.random.choice(empty_neighbors)

        if self.wealth > 0:
            self.give_money()
