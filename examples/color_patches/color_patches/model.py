"""
The model - a 2D lattice where agents live and have an opinion
"""

from collections import Counter

import mesa


class ColorCell(mesa.experimental.cell_space.CellAgent):
    """
    Represents a cell's opinion (visualized by a color)
    """

    OPINIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def __init__(self, model, initial_state):
        """
        Create a cell, in the given state, at the given row, col position.
        """
        super().__init__(model)
        self.state = initial_state
        self.next_state = None

    def get_col(self):
        """Return the col location of this cell."""
        return self.cell.coordinate[0]

    def get_row(self):
        """Return the row location of this cell."""
        return self.cell.coordinate[1]

    def determine_opinion(self):
        """
        Determines the agent opinion for the next step by polling its neighbors
        The opinion is determined by the majority of the 8 neighbors' opinion
        A choice is made at random in case of a tie
        The next state is stored until all cells have been polled
        """
        neighbors = self.cell.neighborhood.agents
        neighbors_opinion = Counter(n.state for n in neighbors)
        # Following is a a tuple (attribute, occurrences)
        polled_opinions = neighbors_opinion.most_common()
        tied_opinions = []
        for neighbor in polled_opinions:
            if neighbor[1] == polled_opinions[0][1]:
                tied_opinions.append(neighbor)

        self.next_state = self.random.choice(tied_opinions)[0]

    def assume_opinion(self):
        """
        Set the state of the agent to the next state
        """
        self.state = self.next_state


class ColorPatches(mesa.Model):
    """
    represents a 2D lattice where agents live
    """

    def __init__(self, width=20, height=20):
        """
        Create a 2D lattice with strict borders where agents live
        The agents next state is first determined before updating the grid
        """
        super().__init__()
        self._grid = mesa.experimental.cell_space.OrthogonalMooreGrid(
            (width, height), torus=False, random=self.random
        )

        # self._grid.coord_iter()
        #  --> should really not return content + col + row
        #  -->but only col & row
        # for (contents, col, row) in self._grid.coord_iter():
        # replaced content with _ to appease linter
        for cell in self._grid.all_cells:
            agent = ColorCell(self, ColorCell.OPINIONS[self.random.randrange(0, 16)])
            agent.move_to(cell)

        self.running = True

    def step(self):
        """
        Perform the model step in two stages:
        - First, all agents determine their next opinion based on their neighbors current opinions
        - Then, all agents update their opinion to the next opinion
        """
        self.agents.do("determine_opinion")
        self.agents.do("assume_opinion")

    @property
    def grid(self):
        """
        /mesa/visualization/modules/CanvasGridVisualization.py
        is directly accessing Model.grid
             76     def render(self, model):
             77         grid_state = defaultdict(list)
        ---> 78         for y in range(model.grid.height):
             79             for x in range(model.grid.width):
             80                 cell_objects = model.grid.get_cell_list_contents([(x, y)])

        AttributeError: 'ColorPatches' object has no attribute 'grid'
        """
        return self._grid
