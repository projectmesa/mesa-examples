from mesa.experimental.cell_space import FixedAgent


class TreeCell(FixedAgent):
    """
    A tree cell.

    Attributes:
        condition: Can be "Fine", "On Fire", or "Burned Out"

    """

    def __init__(self, model, cell):
        """
        Create a new tree.
        Args:
            model: standard model reference for agent.
        """
        super().__init__(model)
        self.condition = "Fine"
        self.cell = cell

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "On Fire":
            for neighbor in self.cell.neighborhood.agents:
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"
