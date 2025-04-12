# Termite WoodChip Behaviour

This model simulates termites interacting with wood chips, inspired by the [NetLogo Termites model](https://ccl.northwestern.edu/netlogo/models/Termites). It explores emergent behavior in decentralized systems, demonstrating how simple agents (termites) collectively organize wood chips into piles without centralized coordination.

## Summary

In this simulation, multiple termite agents move randomly on a grid containing scattered wood chips. Each termite follows simple rules:

1. Search for a wood chip. If found, pick it up and move away.
2. When carrying a wood chip, search for a pile (another wood chip).
3. When a pile is found, find a nearby empty space to place the carried chip.
4. After dropping a chip, move away from the pile.

Over time, these simple interactions lead to the formation of wood chip piles, illustrating decentralized organization without a central coordinator.

## Installation

Make sure that you have installed the `latest` version of mesa i.e `3.2` onwards.

## Usage

To run the simulation:
```bash
solara run app.py
```

## Model Details

### Agents

- **Termite:** An agent that moves within the grid environment, capable of carrying a single wood chip at a time. The termite follows the precise logic of the original NetLogo model, with each behavior (searching, finding piles, dropping chips) continuing until successful.

### Environment

- **Grid:** A two-dimensional toroidal grid where termites interact with the wood chips. The toroidal nature means agents exiting one edge re-enter from the opposite edge.
- **PropertyLayer:** A data structure overlaying the grid, storing the presence of wood chips at each cell.

### Agent Behaviors

- **wiggle():** Simulates random movement by selecting a random neighboring cell.
- **search_for_chip():** Looks for a wood chip. If found, picks it up and moves forward significantly.
- **find_new_pile():** When carrying a chip, searches for a cell that already has a wood chip.
- **put_down_chip():** Attempts to place the carried wood chip in an empty cell near a pile.
- **get_away():** After dropping a chip, moves away from the pile to prevent clustering.

## References

- Wilensky, U. (1997). NetLogo Termites model. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL. Available at: [NetLogo Termites Model](https://ccl.northwestern.edu/netlogo/models/Termites)