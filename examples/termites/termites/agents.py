from mesa.discrete_space import CellAgent


class Termite(CellAgent):
    """
    A Termite agent that has ability to carry woodchip.

    Attributes:
        has_woodchip(bool): True if the agent is carrying a wood chip.
    """

    def __init__(self, model, cell):
        """
        Args:
            model: The model instance.
            cell: The starting cell (position) of the agent.
        """
        super().__init__(model)
        self.cell = cell
        self.has_woodchip = False

    def wiggle(self):
        self.cell = self.model.random.choice(self.model.grid.all_cells.cells)

    def search_for_chip(self):
        if self.cell.woodcell:
            self.cell.woodcell = False
            self.has_woodchip = True

            for _ in range(10):
                new_cell = self.cell.neighborhood.select_random_cell()
                if new_cell.is_empty:
                    self.cell = new_cell
                    break
            return True
        else:
            # No chip found, wiggle and return False to continue searching
            self.wiggle()
            return False

    def find_new_pile(self):
        # Continue wiggling until finding a cell with a wood chip.
        if not self.cell.woodcell:
            self.wiggle()
            return False
        return True

    def put_down_chip(self):
        if not self.has_woodchip:
            return True

        if not self.cell.woodcell:
            self.cell.woodcell = True
            self.has_woodchip = False

            self.get_away()
            return True
        else:
            empty_neighbors = [c for c in self.cell.neighborhood if c.is_empty]
            if empty_neighbors:
                self.cell = self.model.random.choice(empty_neighbors)
            return False

    def get_away(self):
        for _ in range(10):
            new_cell = self.cell.neighborhood.select_random_cell()
            if new_cell.is_empty:
                self.cell = new_cell
                if self.cell.woodcell:
                    return self.get_away()
                break

    def step(self):
        """
        Protocol which termite agent follows:
          1. Search for a wood chip if not carrying one.
          2. Find a new pile (a cell with a wood chip) if carrying a chip.
          3. Put down the chip if a suitable location is found.
        """
        if not self.has_woodchip:
            while not self.search_for_chip():
                pass

        while not self.find_new_pile():
            pass

        while not self.put_down_chip():
            pass
