# Pseudo-Warehouse Model (Meta-Agent Example)

## Summary

The  purpose of this model is to demonstrate Mesa's meta-agent capability and some of its implementation approaches, not to be an accurate warehouse simulation.

**Overview of meta agent:** Complex systems often have multiple levels of components. A city is not a single entity, but it is made of districts,neighborhoods, buildings, and people. A forest comprises an ecosystem of trees, plants, animals, and microorganisms. An organization is not one entity, but is made of departments, sub-departments, and people. A person is not a single entity, but it is made of micro biomes, organs and cells.

This reality is the motivation for meta-agents. It allows users to represent these multiple levels, where each level can have agents with sub-agents.

In this simulation, robots are given tasks to take retrieve inventory items and then take those items to the loading docks.

Each `RobotAgent` is assembled with `MetaAgents.create` from sub-components treated as separate agents: a `SensorAgent`, `RouteAgent`, and `WorkerAgent`, with typed memberships (`router` / `sensor` / `worker`).

This model demonstrates deliberate meta-agent creation. It shows the basics of meta-agent creation and different ways to use and reference sub-agent and meta-agent functions and attributes. (The alliance formation demonstrates emergent meta-agent creation.)

The membership backend supports overlapping memberships (agents in multiple meta-agents); this example still creates one group per robot.

Robots are tracked via `model.robots` (explicit list) and are created with unique names `RobotAgent_0`, `RobotAgent_1` so string lookups are unambiguous. Each robot has typed memberships (`router`/`sensor`/`worker`) queried via `model.meta_agents.members_of(robot, relation=…)` and `groups_of(agent)`.

The membership backend (`model.membership_backend` / `model.meta_agents.backend`) tracks every `(agent, group, relation)` triplet. The app shows a shallow use: `len(model.membership_backend.as_triplets())` (6 triplets for 2 robots × 3 relations) and `model.meta_agents.query_memberships(robot)` in the “Memberships” panel.

Layout is fully driven by `WarehouseScenario` (`rows`, `cols`, `height`, `rng`) and exposed as Solara sliders; `make_warehouse.get_warehouse_coords(rows, cols)` adapts dock/station placement to the scenario size.

## Installation

This model requires Mesa 4.0+ (meta-agents moved from `mesa.experimental` to `mesa.meta_agents`).

```
    $ pip install -U --pre "mesa[rec]>=4.0.0a0"
```

## How to Run

To run the model interactively, in this directory, run the following command

```
    $ solara run app.py
```

## Files

- `model.py`: Contains creation of agents, the network and management of agent execution.
- `agents.py`: Contains inventory, routing, sensing, and worker agent logic for robots.
- `app.py`: Contains the code for the interactive Solara visualization.
- `make_warehouse`: Generates a warehouse numpy array with loading docks, inventory, and charging stations.
