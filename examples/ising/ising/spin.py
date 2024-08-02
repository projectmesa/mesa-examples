import mesa


class Spin(mesa.Agent):
    """Represents a single ALIVE or DEAD cell in the simulation."""

    UP = 1
    DOWN = -1

    def __init__(self, pos, model, init_state):
        """
        Create a cell, in the given state, at the given x, y position.
        """
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state

    def neighbors(self):
        return self.model.grid.iter_neighbors((self.x, self.y), True)
