import mesa


def compute_gini(model):
    # Compute Gini coefficient based on agents' wealth
    agent_wealths = [agent.wealth for agent in model.agents]
    x = sorted(agent_wealths)  # Sort the wealth values
    N = model.num_agents
    # Calculate the Gini coefficient using the sorted wealth values
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B


class BoltzmannWealthModel(mesa.Model):
    def __init__(self, N=100, width=10, height=10, tax_rate=0.1):
        super().__init__()
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.tax_fund = 0
        self.tax_rate = tax_rate  # Store the tax rate

        # Data collector to track Gini coefficient and agents' wealth
        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        )

        # Create and place agents on the grid
        for _ in range(self.num_agents):
            a = MoneyAgent(self)  # Instantiate a MoneyAgent
            x = self.random.randrange(self.grid.width)  # Random x position
            y = self.random.randrange(self.grid.height)  # Random y position
            self.grid.place_agent(a, (x, y))  # Place agent on the grid

        self.running = True
        self.datacollector.collect(self)

    def distribute_taxes(self):
        # Distribute the tax fund among agents with zero wealth
        for agent in self.agents:
            if agent.wealth == 0 and self.tax_fund > 0:
                agent.receive_aid()
                self.tax_fund -= 1

    def pay_taxes(self):
        for agent in self.agents:
            if agent.wealth > 0:
                agent.pay_taxes()  # Call pay_taxes method for each agent

    def step(self):
        self.agents.shuffle_do("step")  # Randomize agent execution order
        self.distribute_taxes()
        self.datacollector.collect(self)


class MoneyAgent(mesa.Agent):
    """Agent with initial wealth and taxation function."""

    def __init__(self, model):
        super().__init__(model)
        self.wealth = 1  # Initialize wealth

    def move(self):
        # Get possible neighboring positions to move
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(
            possible_steps
        )  # Randomly choose a new position
        self.model.grid.move_agent(self, new_position)  # Move agent to new position

    def give_money(self):
        # Give money to a random neighbor (cellmate)
        cellmates = self.model.grid.get_cell_list_contents(
            [self.pos]
        )  # Get agents in the same cell
        cellmates.pop(cellmates.index(self))  # Remove self from the list of cellmates
        if len(cellmates) > 0 and self.wealth > 0:
            other = self.random.choice(
                cellmates
            )  # Choose a random agent to give money to
            other.wealth += 1
            self.wealth -= 1

    def pay_taxes(self):
        tax_rate = 0.1
        tax_amount = self.wealth * tax_rate  # Calculate tax amount
        if tax_amount > self.wealth:  # Ensure agent has enough wealth to pay taxes
            tax_amount = self.wealth  # Pay what they have
        self.wealth -= tax_amount
        self.model.tax_fund += tax_amount

    def receive_aid(self):
        # Aid is received if the agent's wealth is zero
        if self.wealth == 0:
            self.wealth += 1

    def step(self):
        self.move()
        self.pay_taxes()  # Pay taxes based on current wealth
        if self.wealth > 0:
            self.give_money()  # Give money to another agent if wealthy
