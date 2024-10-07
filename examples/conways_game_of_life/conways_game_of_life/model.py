import mesa

from .cell import Cell


class ConwaysGameOfLife(mesa.Model):
    """
    Represents the 2-dimensional array of cells in Conway's
    Game of Life.
    """

    def __init__(self, width=50, height=50):
        """
        Create a new playing area of (width, height) cells.
        """
        super().__init__()
        # Use a simple grid, where edges wrap around.
        self.grid = mesa.experimental.cell_space.OrthogonalMooreGrid(
            (width, height), torus=True
        )

        # Place a cell at each location, with some initialized to
        # ALIVE and some to DEAD.
        for cell in self.grid.all_cells:
            cell_agent = Cell(self)
            if self.random.random() < 0.1:
                cell_agent.state = cell_agent.ALIVE
            cell_agent.move_to(cell)

        self.running = True

    def step(self):
        """
        Perform the model step in two stages:
        - First, all cells assume their next state (whether they will be dead or alive)
        - Then, all cells change state to their next state
        """
        self.agents.do("determine_state")
        self.agents.do("assume_state")
