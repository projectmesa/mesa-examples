# Pseudo-Warehouse Model (Meta-Agent Example)

## Summary

The  purpose of this model is to demonstrate Mesa's meta-agent capability and some of its implementation approaches, not to be an accurate warehouse simulation.

**Overview of meta agent:** Complex systems often have multiple levels of components. A city is not a single entity, but it is made of districts,neighborhoods, buildings, and people. A forest comprises an ecosystem of trees, plants, animals, and microorganisms. An organization is not one entity, but is made of departments, sub-departments, and people. A person is not a single entity, but it is made of micro biomes, organs and cells.

This reality is the motivation for meta-agents. It allows users to represent these multiple levels, where each level can have agents with sub-agents.

In this simulation, robots are given tasks to take retrieve inventory items and then take those items to the loading docks.

Each `RobotAgent` is made up of sub-components that are treated as separate agents. For this simulation, each robot as a `SensorAgent`, `RouterAgent`, and `WorkerAgent`.

This model demonstrates deliberate meta-agent creation. It shows the basics of meta-agent creation and different ways to use and reference sub-agent and meta-agent functions and attributes. (The alliance formation demonstrates emergent meta-agent creation.)

In its current configuration, agents being part of multiple meta-agents is not supported

An additional item of note is that to reference the RobotAgent created in model you will see `type(self.RobotAgent)` or `type(model.RobotAgent)` in various places. If you have any ideas for how to make this more user friendly please let us know or do a pull request.

## Installation

This model requires Mesa's recommended install

```
    $ pip install 'mesa[rec]>=3'
```

## How to Run

To run the model interactively, in this directory, run the following command

```
    $ solara run app.py
```

## Files

- `model.py`: Contains creation of agents, the network and management of agent execution.
- `agents.py`: Contains logic for forming alliances and creation of new agents
- `app.py`: Contains the code for the interactive Solara visualization.
- `make_warehouse`: Generates a warehouse numpy array with loading docks, inventory, and charging stations.