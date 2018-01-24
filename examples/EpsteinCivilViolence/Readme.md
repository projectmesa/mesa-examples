# Epstein Civil Violence Model
##### Adapted by Daniel Muysken, Zazo Meijs, Cornelis Boon, Tamika van 't Hoff and Julia Anten

## Summary

This model is based on Joshua Epstein's simulation of how civil unrest grows and is suppressed. Citizen agents wander the grid randomly, and are endowed with individual risk aversion and hardship levels; there is also a universal regime legitimacy value. There are also Cop agents, who work on behalf of the regime. Cops arrest Citizens who are actively rebelling; Citicens decide whether to rebel based on their hardship and the regime legitimacy, and their perceived probability of arrest. 

The model generates mass uprising as self-reinforcing proceses: if enough agents are rebelling, the probability of any individual agent being arrested is reduced, making more agents more likely to join the uprising. However, the more rebelling Citizens the Cops arrest, the less likely additional agents become to join.

## Improvements
- Vision parameter implemented.
- Added sliders to make the model easier to use. 

## How to Run

To run the model interactively, run ``run.py`` in this directory. e.g.

```
    $ python run.py
``` 

Then open your browser to [http://127.0.0.1:8888/](http://127.0.0.1:8888/) and press Reset, then Run. 

## Files

* ``Agent.py``: Agent code.
* ``Model.py``: Core model code.
* ``Server.py``: Sets up the interactive visualisation.
* ``Epstein Civil Violence.ipynb``: Jupyter notebook conducting some preliminary analysis of the model.

## Further Reading

This model is adapted from:

[Epstein, J. “Modeling civil violence: An agent-based computational approach”, Proceedings of the National Academy of Sciences, Vol. 99, Suppl. 3, May 14, 2002](http://www.pnas.org/content/99/suppl.3/7243.short)

A similar model is also included with NetLogo:

Wilensky, U. (2004). NetLogo Rebellion model. http://ccl.northwestern.edu/netlogo/models/Rebellion. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL. <br>
Although, in this model, it is possible for agents to occupy the same space.
