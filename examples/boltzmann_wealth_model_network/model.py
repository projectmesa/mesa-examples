import mesa
import networkx as nx
from .agent import MoneyAgent
from mesa.experimental.cell_space import Network


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B


class BoltzmannWealthModelNetwork(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, num_agents=10, num_nodes=10):
        super().__init__()
        self.num_agents = num_agents
        self.num_nodes = num_nodes if num_nodes >= self.num_agents else self.num_agents
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=0.5)
        self.grid = Network(self.G, random=self.random, capacity=1)

        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini},
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
