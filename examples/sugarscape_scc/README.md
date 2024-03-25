# Sugarscape: Sex, Culture, and Conflict : The Emergence of History

## Summary

This is a work-in-progress implementation of Chapter 3 from *Growing Artificial Societies: Social Science from the Bottom Up.*, adding mechanics such as sexual reproduction, cultural exchange and combat.

This model greatly increases the complexity of interactions between agents, following on from Chapter 2's model.

## Mechanics Introduced

### Sexual Reproduction

We assign agents a trait, **Fertility**, according to which they can perform Agent Rule **S**:
- Select a neighbour at random
- If the neighbor is fertile and of the opposite sex and at least one of the agents has an empty neighboring site (for the baby), then a child is born
- Repeat for all neighbors

###  Cultural Processes (WIP)

### Combat (WIP)

This model demonstrates visualisation of agent attributes.
## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

`$ mesa runserver`

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press **Reset**, then **Run**.

## Files

* `sugarscape_scc/agents.py`: Adds chapter-specific mechanics to `sugarscape_cg/agent.py`
* `sugarscape_scc/server.py`: Sets up the interactive server with charts visualising data.
* `sugarscape_scc/model.py`: Defines the Sugarscape model itself
* `run.py`: Launches a model visualization server.

## Further Reading

Epstein, J. M., & Axtell, R. (n.d.). *Growing Artificial Societies*: Social science from the bottom up. Brookings Institution Press, Chapter 3.


The ant sprite is taken from https://openclipart.org/detail/229519/ant-silhouette, with CC0 1.0 license.
