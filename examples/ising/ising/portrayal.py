def portray_spin(spin):
    """
    This function is registered with the visualization server to be called
    each tick to indicate how to draw the cell in its current state.
    :param cell:  the cell in the simulation
    :return: the portrayal dictionary.
    """
    if spin is None:
        raise AssertionError
    return {
        "shape": "s",
        "x": spin.x,
        "y": spin.y,
        "color": "grey" if spin.state is spin.UP else "black",
    }
