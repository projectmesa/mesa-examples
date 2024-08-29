import numpy as np
from mesa import Model
from mesa.space import PropertyLayer
from scipy.signal import convolve2d

# fmt: off
class GameOfLifeModel(Model):
    def __init__(self, width=10, height=10, alive_fraction=0.2):
        super().__init__()
        # Initialize the property layer for cell states
        self.cell_layer = PropertyLayer("cells", width, height, False, dtype=bool)
        # Randomly set cells to alive
        self.cell_layer.data = np.random.choice([True, False], size=(width, height), p=[alive_fraction, 1 - alive_fraction])

    def step(self):
        self._advance_time()
        # Define a kernel for counting neighbors. The kernel has 1s around the center cell (which is 0).
        # This setup allows us to count the live neighbors of each cell when we apply convolution.
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])

        # Count neighbors using convolution.
        # convolve2d applies the kernel to each cell of the grid, summing up the values of neighbors.
        # boundary="wrap" ensures that the grid wraps around, simulating a toroidal surface.
        neighbor_count = convolve2d(self.cell_layer.data, kernel, mode="same", boundary="wrap")

        # Apply Game of Life rules:
        # 1. A live cell with 2 or 3 live neighbors survives, otherwise it dies.
        # 2. A dead cell with exactly 3 live neighbors becomes alive.
        # These rules are implemented using logical operations on the grid.
        self.cell_layer.data = np.logical_or(
            np.logical_and(self.cell_layer.data, np.logical_or(neighbor_count == 2, neighbor_count == 3)),
            # Rule for live cells
            np.logical_and(~self.cell_layer.data, neighbor_count == 3)  # Rule for dead cells
        )
