"""
The model - a 2D lattice where agents live and have an opinion
"""

from collections import Counter

import mesa
import random


class ColorCell(mesa.Agent):
    """
    Represents a cell's opinion (visualized by a color)
    """

    OPINIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def __init__(self, pos, unique_id, model, initial_state):
        """
        Create a cell, in the given state, at the given row, col position and stubbornness.
        """
        super().__init__(unique_id, model)
        self._row = pos[0]
        self._col = pos[1]
        self._state = initial_state
        self.stubbornness = random.uniform(0, 0.99)
        self._next_state = None

    def get_col(self):
        """Return the col location of this cell."""
        return self._col

    def get_row(self):
        """Return the row location of this cell."""
        return self._row

    def get_state(self):
        """Return the current state (OPINION) of this cell."""
        return self._state

    def determine_opinion(self):
        """
        Determines the agent opinion for the next step by polling its neighbors
        The opinion is determined by the majority of the 8 neighbors' opinion
        A choice is made at random in case of a tie
        The next state is stored until all cells have been polled
        The last opinion is determined by the stubbornness parameter of the agent
        """
        _neighbor_iter = self.model.grid.iter_neighbors((self._row, self._col), True)
        neighbors_opinion = Counter(n.get_state() for n in _neighbor_iter)
        # Following is a a tuple (attribute, occurrences)
        polled_opinions = neighbors_opinion.most_common()
        tied_opinions = []
        for neighbor in polled_opinions:
            if neighbor[1] == polled_opinions[0][1]:
                tied_opinions.append(neighbor)

        if self.random.random() > self.stubbornness:
            self._next_state = self.random.choice(tied_opinions)[0]
        else:
            self._next_state = self._state

    def assume_opinion(self):
        """
        Set the state of the agent to the next state
        """
        self._state = self._next_state

    def set_next_state(self, opinion):
        """
        Set the next state for the agent.
        """
        self._next_state = opinion


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
        self._grid = mesa.space.SingleGrid(width, height, torus=False)

        # self._grid.coord_iter()
        #  --> should really not return content + col + row
        #  -->but only col & row
        # for (contents, col, row) in self._grid.coord_iter():
        # replaced content with _ to appease linter
        for _, (row, col) in self._grid.coord_iter():
            cell = ColorCell(
                (row, col),
                row + col * row,
                self,
                ColorCell.OPINIONS[self.random.randrange(0, 16)],
            )
            self._grid.place_agent(cell, (row, col))

        self.running = True

    def step(self):
        """
        Perform the model step in three stages:
        - First, all agents determine their next opinion based on their neighbors current opinions
        - A random event is introduced to potentially influence agent opinions.
        - Then, all agents update their opinion to the next opinion
        """
        self.agents.do("determine_opinion")
        self.random_event()
        self.agents.do("assume_opinion")

    def random_event(self, event_chance=0.001):
        """
        Introduce a random event that may influence agent opinions.
        If a randomly generated value is less than `event_chance`, a change in opinion will be triggered for agents by
        calling `change_opinion`.
        """
        if self.random.random() < event_chance:
            self.change_opinion()

    def change_opinion(self, radius=2):
        """
        Apply an opinion change to agents within a specified radius around a random grid location.
        - Select random coordinates (x, y) within the grid boundaries.
        - Retrieve agents located within a Moore neighborhood of (x, y) using the specified radius (default is 2),
            which includes all agents within this distance as well as the center cell.
        - Randomly choose an opinion from `ColorCell.OPINIONS`.
        - Set each agent's `next_state` within this neighborhood to the selected opinion.
        """
        x, y = (
            self.random.randrange(self.grid.width),
            self.random.randrange(self.grid.height),
        )
        agents = list(
            self.grid.iter_neighbors(
                (x, y), moore=True, include_center=True, radius=radius
            )
        )
        opinion = ColorCell.OPINIONS[self.random.randrange(0, 16)]

        for agent in agents:
            agent.set_next_state(opinion)

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
