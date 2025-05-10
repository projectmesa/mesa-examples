from mesa.discrete_space import CellAgent


class MoneyAgent(CellAgent):
    """An agent with fixed initial wealth"""

    def __init__(self, model):
        super().__init__(model)
        self.wealth = 1

    def give_money(self):
        neighbours = list(self.cell.neighborhood.agents)
        if len(neighbours) > 0:
            other = self.random.choice(neighbours)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        if self.wealth > 0:
            self.give_money()
