# Boltzmann Wealth Model with Network

## Summary

This is the same Boltzmann Wealth Model, but with a network grid implementation.

A simple model of agents exchanging wealth. All agents start with the same amount of money. Every step, each agent with one unit of money or more gives one unit of wealth to another random agent. This is the model described in the [Intro Tutorial](https://mesa.readthedocs.io/latest/tutorials/0_first_model.html).

In this network implementation, agents must be located on a node, with a limit of one agent per node. In order to give or receive the unit of money, the agent must be directly connected to the other agent (there must be a direct link between the nodes).

As the model runs, the distribution of wealth among agents goes from being perfectly uniform (all agents have the same starting wealth), to highly skewed -- a small number have high wealth, more have none at all.


## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``solara run app.py`` in this directory.

```
    $ solara run app.py
```

Then open your browser to [http://127.0.0.1:8765/](http://127.0.0.1:8765/) and press Reset, then Run.

## Files

* ``agent.py``: Defines the agent class.
* ``model.py``: Defines the model class.
* ``app.py``  : Defines the visualization and spins up a solara server.

## Further Reading

This model is drawn from econophysics and presents a statistical mechanics approach to wealth distribution. Some examples of further reading on the topic can be found at:

[Milakovic, M. A Statistical Equilibrium Model of Wealth Distribution. February, 2001.](https://editorialexpress.com/cgi-bin/conference/download.cgi?db_name=SCE2001&paper_id=214)

[Dragulescu, A and Yakovenko, V. Statistical Mechanics of Money, Income, and Wealth: A Short Survey. November, 2002](http://arxiv.org/pdf/cond-mat/0211175v1.pdf)
