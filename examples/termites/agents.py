from mesa.discrete_space import CellAgent


class Termite(CellAgent):
    """A Termite agent starts wandering randomly.
    If it bumps into a wood chip, it finds a nearby empty space and puts its wood chip down.

    Attributes:
        hasWoodChip(bool): True if the agent is carrying a wood chip.
    """

    def __init__(self,model,cell):
        """
        Args:
            model: The model instance.
            cell: The startin cell (position) of the agent.
        """
        super().__init__(model)
        self.cell = cell
        self.hasWoodChip = False

    def move(self):
        # Move the agent to a random neighboring cell.
        self.cell = self.cell.neighborhood.select_random_cell()

    def step(self):
        # Move to a random neighboring cell
        self.move()

        # Check if Woodchip is present on the cell
        if self.cell.woodcell:
            # Termite agnet is not carrying any woodchip
            if not self.hasWoodChip:
                # Pick up the woodchip
                self.hasWoodChip = True
                # Remove the wood chip from the cell
                self.cell.woodcell = False
            else:
                """
                Termite agent is already carrying a woodchip and has bumped into another wood chip
                then search for a empty space (no agent and no woodcell) in it's neighbourhood and drop the wood chip
                """
                empty_cell_neighbors = [x for x in self.cell.neighborhood if x.is_empty and not x.woodcell]

                if empty_cell_neighbors:
                    # Moving to random empty cell
                    self.cell = self.cell.random.choice(empty_cell_neighbors)
                    # Drop the woodchip
                    self.hasWoodChip = False
                    self.cell.woodcell = True
        else:
            # Termite agent has a wood chip
            if self.hasWoodChip:
                # search for neighbors
                wood_chip_neighbors = [x for x in self.cell.neighborhood if x.woodcell]
                if wood_chip_neighbors:
                    # drop the Wood chip
                    self.hasWoodChip = False
                    self.cell.woodcell = True
