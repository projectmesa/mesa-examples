from mesa.discrete_space import CellAgent


class Termite(CellAgent):
    """A Termite agent starts wandering randomly.
    If it bumps into a wood chip, it finds a nearby empty space and puts its wood chip down.

    Attributes:
        hasWoodChip(bool): True if the agent is carrying a wood chip.
    """

    def __init__(self, model, cell):
        """
        Args:
            model: The model instance.
            cell: The starting cell (position) of the agent.
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
            # Termite agent is not carrying any woodchip
            if not self.hasWoodChip:
                # Pick up the woodchip
                self.hasWoodChip = True
                # Remove the wood chip from the cell
                self.cell.woodcell = False
            else:
                """
                Termite agent is already carrying a woodchip and has bumped into another wood chip
                then search for an empty space (no agent and no woodcell) in its neighbourhood and drop the wood chip
                """
                empty_cell_neighbors = [
                    x for x in self.cell.neighborhood if x.is_empty and not x.woodcell
                ]

                if empty_cell_neighbors:
                    # Move to random empty cell
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
                    # Count wood chips in each neighbor's neighborhood to find denser clusters
                    neighbor_scores = {}
                    for neighbor in self.cell.neighborhood:
                        if not neighbor.woodcell and neighbor.is_empty:
                            # Count wood chips in this neighbor's neighborhood
                            count = sum(1 for n in neighbor.neighborhood if n.woodcell)
                            if count > 0:  # Only consider cells with at least one wood chip nearby
                                neighbor_scores[neighbor] = count

                    if neighbor_scores:
                        # Choose the cell with the highest wood chip density in its neighborhood
                        best_cell = max(neighbor_scores.items(), key=lambda x: x[1])[0]
                        self.cell = best_cell
                        self.hasWoodChip = False
                        self.cell.woodcell = True
                    else:
                        # If no good location found, use the original method
                        self.hasWoodChip = False
                        self.cell.woodcell = True
