# Wolf-Sheep Experimental Model

This is an experimental implementation of the Wolf-Sheep Predation Model, which simulates the dynamics of predator-prey interactions between wolves and sheep, including factors such as energy expenditure, reproduction, and grass regrowth.

## Summary

This model consists of three agent types: wolves, sheep, and grass. The wolves and the sheep wander around the grid at random. Wolves and sheep both expend energy moving around and replenish it by eating. Sheep eat grass, and wolves eat sheep if they end up on the same grid cell.

If wolves and sheep have enough energy, they reproduce, creating a new wolf or sheep (in this simplified model, only one parent is needed for reproduction). The grass on each cell regrows at a constant rate. If any wolves and sheep run out of energy, they die.

The model tests and demonstrates several Mesa concepts and features:
 - MultiGrid
 - Multiple agent types (wolves, sheep, grass)
 - Overlay arbitrary text (wolf's energy) on agent's shapes while drawing on CanvasGrid
 - Agents inheriting a behavior (random movement) from an abstract parent
 - Writing a model composed of multiple files
 - Dynamically adding and removing agents from the schedule

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    # First, we clone the Mesa repo
    $ git clone https://github.com/projectmesa/mesa.git
    $ cd mesa
    # Then we cd to the example directory
    $ cd examples/wolf_sheep_experimental
    $ pip install -r requirements.txt
```

## How to Run

You can run the batch model directly by executing the `app.py` file. e.g.

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

```
    python app.py
```

## Files

* `wolf_sheep_experimental/agents.py`: Defines the Wolf, Sheep, and GrassPatch agent classes.
* `wolf_sheep_experimental/model.py`: Defines the Wolf-Sheep Predation model itself, including the initialization of the grid, agents, and data collection.
* `wolf_sheep_experimental/app.py`: Sets up the interactive visualization server for the model and launches a batch run of the model and visualizes the results using matplotlib.
* `wolf_sheep_experimental/requirements.txt`: Lists the dependencies required to run the model.
* `wolf_sheep_experimental/Readme.md`: Provides an overview and instructions for the model.

## Further Reading

This model is closely based on the NetLogo Wolf-Sheep Predation Model:

Wilensky, U. (1997). NetLogo Wolf Sheep Predation model. http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

See also the [Lotka–Volterra equations
](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations) for an example of a classic differential-equation model with similar dynamics.
