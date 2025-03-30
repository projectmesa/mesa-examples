# Termite WoodChip Behaviour
This model simulates termites interacting with wood chips, inspired by the [NetLogo Termites model](https://ccl.northwestern.edu/netlogo/models/Termites). It explores emergent behavior in decentralized systems, demonstrating how simple agents (termites) collectively organize wood chips into piles without centralized coordination.

## Summary


In this simulation, multiple termite agents move randomly on a grid containing scattered wood chips. Each termite follows simple rules:

1. Move randomly.
2. If carrying a wood chip and encountering another, place the carried chip in a nearby empty space.
3. If not carrying a chip and encountering one, pick it up.

Over time, these simple interactions lead to the formation of wood chip piles, illustrating decentralized organization without a central coordinator.


## Installation

Make sure that you have installed the `latest` version of mesa i.e `3.2.0.dev0`

## Usage

To run the simulation:

```bash
solara run app.py
```


## Model Details

### Agents

- **Termite:** An agent that moves within the grid environment, capable of carrying a single wood chip at a time.

### Environment

- **Grid:** A two-dimensional toroidal grid where termites interacts with the wood chips. The toroidal nature means agents exiting one edge re-enter from the opposite edge,

- **PropertyLayer:** A data structure overlaying the grid, storing  the presence of wood chips at each cell.

## References

- Wilensky, U. (1997). NetLogo Termites model. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL. Available at: [NetLogo Termites Model](https://ccl.northwestern.edu/netlogo/models/Termites)
---



