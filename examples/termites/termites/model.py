import numpy as np
from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid, PropertyLayer

from .agents import Termite


class TermiteModel(Model):
    """
    A simulation that depicts behavior of termite agents gathering wood chips into piles.
    """

    def __init__(
        self, num_termites=100, width=100, height=100, wood_chip_density=0.1, seed=42
    ):
        """Initialize the model.

        Args:
            num_termites: Number of Termite Agents,
            width: Grid width.
            height: Grid heights.
            wood_chip_density: Density of wood chips in the grid.
            seed : Random seed for reproducibility.
        """
        super().__init__(seed=seed)
        self.num_termites = num_termites
        self.wood_chip_density = wood_chip_density

        self.grid = OrthogonalMooreGrid((width, height), torus=True)

        self.wood_chips_layer = PropertyLayer(
            "woodcell", (width, height), default_value=False, dtype=bool
        )
        self.wood_chips_layer.data = np.random.choice(
            [True, False],
            size=(width, height),
            p=[self.wood_chip_density, 1 - self.wood_chip_density],
        )

        self.grid.add_property_layer(self.wood_chips_layer)

        Termite.create_agents(
            self,
            self.num_termites,
            self.random.sample(self.grid.all_cells.cells, k=self.num_termites),
        )

    def step(self):
        self.agents.shuffle_do("step")
