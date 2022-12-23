# Caching and Replaying Schelling

## Summary

This example applies caching on the Mesa [Schelling example](https://github.com/projectmesa/mesa-examples/tree/main/examples/Schelling).
It enables a simulation run to be "cached" or in other words recorded. The recorded simulation run is persisted on the local file system and can be replayed at any later point.

It uses the [Mesa-Replay](https://github.com/Logende/mesa-replay) library and puts the Schelling model inside a so-called `CachableModel` wrapper that we name `CachableSchelling`.
From the outside perspective, the new model behaves the same way as the original Schelling model, but additionally supports caching.

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

After running a regular simulation, you can **replay** your latest simulation run by first enabling the Replay switch and then pressing Reset.
Note that this **requires the previous simulation run to have finished** (e.g. all agents are happy, no more new steps are simulated).

## Files

* ``run.py``: Launches a model visualization server and uses `CachableModelSchelling` as simulation model
* ``cachablemodel.py``: Implements `CachableModelSchelling` to make the original Schelling model cachable
* ``model.py``: Taken from the original Mesa Schelling example
* ``server.py``: Taken from the original Mesa Schelling example

## Further Reading

* [Mesa-Replay library](https://github.com/Logende/mesa-replay)
* [More caching and replay examples](https://github.com/Logende/mesa-replay/tree/main/examples)
