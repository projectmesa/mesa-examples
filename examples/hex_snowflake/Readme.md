# Conway's Game Of "Life" on a hexagonal grid

## Summary

In this model, each dead cell will become alive if it has exactly one neighbor. Alive cells stay alive forever.


## How to Run

```bash
solara run app.py
```

## Files

* ``hex_snowflake/cell.py``: Defines the behavior of an individual cell, which can be in two states: DEAD or ALIVE.
* ``hex_snowflake/model.py``: Defines the model itself, initialized with one alive cell at the center.
* ``app.py``: Defines and launches the interactive visualization.

## Further Reading
[Explanation of how hexagon neighbors are calculated. (The method is slightly different for Cartesian coordinates)](http://www.redblobgames.com/grids/hexagons/#neighbors-offset)
