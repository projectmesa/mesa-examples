import numpy as np
from agents import Termite
from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid, PropertyLayer


class TermiteModel(Model):
    """
    A simulation that depicts behavior of termite agents gathering wood chips into piles.
    """

    def __init__(
        self, num_termites=50, width=60, height=60, wood_chip_density=0.4, seed=None
    ):
        """Initialize the model.

        Args:
            num_termites: Number of Termite Agents,
            width: Grid width.
            height: Grid heights.
            wood_chip_density: Density of wood chips in the grid.
        """
        super().__init__(seed=seed)
        self.num_termites = num_termites
        self.wood_chip_density = wood_chip_density

        # Initializing a OrthogonalMooreGrid: each cell has 8 neighbors
        self.grid = OrthogonalMooreGrid((width, height), torus=True)

        # Initializing up a PropertyLayer(woodcell) for wood_chips
        self.wood_chips_layer = PropertyLayer(
            "woodcell", (width, height), default_value=False, dtype=bool
        )
        self.wood_chips_layer.data = np.random.choice(
            [True, False],
            size=(width, height),
            p=[self.wood_chip_density, 1 - self.wood_chip_density],
        )

        # Adding PropertyLayer to the grid"""
        self.grid.add_property_layer(self.wood_chips_layer)

        # Creating and adding termite agents to the grid
        Termite.create_agents(
            self,
            self.num_termites,
            self.random.sample(self.grid.all_cells.cells, k=self.num_termites),
        )

    def step(self):
        self.agents.shuffle_do("step")
