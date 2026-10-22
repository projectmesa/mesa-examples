"""Generate a compact warehouse layout for the meta-agent example."""

from __future__ import annotations

import random
import string
from random import Random

import numpy as np


def get_warehouse_coords(
    rows: int, cols: int
) -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    """Return loading-dock and charging-station coordinates for a size.

    Keeps the two dock/station pairs used by the example but adapts column
    placement when ``cols`` differs from the default 8. Inventory lives at
    ``cols 1,4,7,...`` (see ``range(1, cols, 3)``), so docks at ``0`` and ``2``
    and stations at ``cols-1`` and ``cols-3`` avoid direct overlap.
    """
    if rows < 4 or cols < 4:
        raise ValueError(f"Warehouse too small: rows={rows} cols={cols} need >=4")

    # Loading docks on the north edge (row 0). Keep two, spaced by 2.
    docks: list[tuple[int, int, int]] = [(0, 0, 0)]
    if cols > 2:
        docks.append((0, 2, 0))
    # For wider warehouses we could add more, but the example is fixed at 2.
    docks = docks[:2]

    # Charging stations on the south edge (row rows-1), right side.
    stations: list[tuple[int, int, int]] = []
    if cols >= 2:
        stations.append((rows - 1, cols - 1, 0))
    if cols >= 4:
        stations.append((rows - 1, cols - 3, 0))
    # Ensure ordering matches docks (first dock ↔ last station spacing)
    stations = list(reversed(stations[:2]))
    if len(stations) == 1 and len(docks) == 2:
        # Degenerate narrow warehouse - duplicate the single station.
        stations.append(stations[0])

    return docks, stations


def generate_item_code(rng: Random) -> str:
    """Generate a short random inventory code."""
    letter = rng.choice(string.ascii_uppercase)
    number = rng.randint(10, 99)
    return f"{letter}{number}"


def make_warehouse(
    rows: int,
    cols: int,
    height: int,
    rng: Random | None = None,
) -> np.ndarray:
    """Generate a 3D warehouse array with loading docks and inventory.

    Sizes come from ``WarehouseScenario`` (``rows``, ``cols``, ``height``);
    this module holds no independent defaults.
    """
    rng = rng or random.Random(0)

    warehouse = np.full((rows, cols, height), " ", dtype=object)

    docks, stations = get_warehouse_coords(rows, cols)

    for r, c, h in docks:
        warehouse[r, c, h] = "LD"

    for r, c, h in stations:
        warehouse[r, c, h] = "CS"

    for r in range(2, rows - 1, 3):
        for c in range(1, cols, 3):
            for h in range(height):
                # Don't overwrite docks/stations (edge rows/cols already handled,
                # but keep guard for small warehouses).
                if warehouse[r, c, h] != " ":
                    continue
                warehouse[r, c, h] = generate_item_code(rng)

    return warehouse
