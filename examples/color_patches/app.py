"""
handles the definition of the canvas parameters and
the drawing of the model representation on the canvas
"""

# import webbrowser
from color_patches.model import ColorPatches
from mesa.visualization import (
    SolaraViz,
    make_space_component,
)

_COLORS = [
    "Aqua",
    "Blue",
    "Fuchsia",
    "Gray",
    "Green",
    "Lime",
    "Maroon",
    "Navy",
    "Olive",
    "Orange",
    "Purple",
    "Red",
    "Silver",
    "Teal",
    "White",
    "Yellow",
]


grid_rows = 50
grid_cols = 25
cell_size = 10
canvas_width = grid_rows * cell_size
canvas_height = grid_cols * cell_size


def color_patch_draw(cell):
    """
    This function is registered with the visualization server to be called
    each tick to indicate how to draw the cell in its current state.

    :param cell:  the cell in the simulation

    :return: the portrayal dictionary.
    """
    if cell is None:
        raise AssertionError
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    portrayal["x"] = cell.get_row()
    portrayal["y"] = cell.get_col()
    portrayal["color"] = _COLORS[cell.state]
    return portrayal


space_component = make_space_component(
    color_patch_draw,
    draw_grid=False,
)
model = ColorPatches()
page = SolaraViz(
    model,
    components=[space_component],
    model_params={"width": grid_rows, "height": grid_cols},
    name="Color Patches",
)
# webbrowser.open('http://127.0.0.1:8521')  # TODO: make this configurable
