from mesa.discrete_space import CellAgent


class Termite(CellAgent):
    """
    A Termite agent that has ability to carry woodchip.

    Attributes:
        hasWoodChip(bool): True if the agent is carrying a wood chip.

    The termite will:
      1. Search for a cell with a wood chip (search_for_chip).
      2. Once it picks up the chip, search for a pile (find_new_pile).
      3. Put the chip down on an empty cell (put_down_chip), then move away (get_away).
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

    def wiggle(self):
        # Move the agent to a random neighboring cell.
        self.cell = self.cell.get_neighborhood(radius=3).select_random_cell()

    def search_for_chip(self):
        """
        If the current cell has a wood chip, pick it up and move forward.
        Otherwise, wiggle and continue searching.
        """
        # Check if current cell has a wood chip
        if self.cell.woodcell:
            # Pick up the wood chip
            self.cell.woodcell = False
            self.hasWoodChip = True

            # Move forward
            for _ in range(30):
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
        """
        If current cell is empty (no wood chip), drop the chip.
        Otherwise, move forward, then try again.
        """
        if not self.hasWoodChip:
            return True  # Nothing to put down

        if not self.cell.woodcell:
            # Drop the chip
            self.cell.woodcell = True
            self.hasWoodChip = False

            # Get away from the pile
            self.get_away()
            return True
        else:
            # Move to a random neighbor
            empty_neighbors = [c for c in self.cell.neighborhood if c.is_empty]
            if empty_neighbors:
                self.cell = self.model.random.choice(empty_neighbors)
            return False

    def get_away(self):

        # Move 20 steps forward randomly untill on a cell with no wood chip.
        empty_neighbors = [c for c in self.cell.get_neighborhood(radius=3) if c.is_empty]
        if empty_neighbors:
            self.cell = self.model.random.choice(empty_neighbors)

        for _ in range(20):
            new_cell = self.cell.neighborhood.select_random_cell()
            if new_cell.is_empty:
                self.cell = new_cell
                # If still on a wood chip, keep going
                if self.cell.woodcell:
                    return self.get_away()
                break

    def step(self):
        """
        Protocol which termite follows:
          1. Search for a wood chip if not carrying one.
          2. Find a new pile (a cell with a wood chip) if carrying a chip.
          3. Put down the chip if a suitable location is found.
        """
        if not self.hasWoodChip:
            # Keep searching until termite find a chip
            while not self.search_for_chip():
                pass

        # Keep looking for a pile until termite find one
        while not self.find_new_pile():
            pass

        # Keep trying to put down the chip until successful
        while not self.put_down_chip():
            pass
