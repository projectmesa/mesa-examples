# Epstein Civil Violence Model

This is an experimental implementation of the Epstein Civil Violence Model, which simulates the dynamics of civil violence with agents representing citizens and cops.


## Summary

This model is based on Joshua Epstein's simulation of how civil unrest grows and is suppressed. Citizen agents wander the grid randomly, and are endowed with individual risk aversion and hardship levels; there is also a universal regime legitimacy value. There are also Cop agents, who work on behalf of the regime. Cops arrest Citizens who are actively rebelling; Citizens decide whether to rebel based on their hardship and the regime legitimacy, and their perceived probability of arrest.

The model generates mass uprising as self-reinforcing processes: if enough agents are rebelling, the probability of any individual agent being arrested is reduced, making more agents more likely to join the uprising. However, the more rebelling Citizens the Cops arrest, the less likely additional agents become to join.

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    # First, we clone the Mesa repo
    $ git clone https://github.com/projectmesa/mesa.git
    $ cd mesa
    # Then we cd to the example directory
    $ cd examples/epstein_civil_violence_experimental
    $ pip install -r requirements.txt
```

## How to Run

You can run the batch model directly by executing the `app.py` file. as 

```
    python app.py
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/)

## Files

* `epstein_civil_violence_experimental/agent.py`: Defines the Citizen and Cop agent classes.
* `epstein_civil_violence_experimental/model.py`: Defines the Epstein Civil Violence model itself, including the initialization of the grid, agents, and data collection.
* `epstein_civil_violence_experimental/app.py`: Sets up the interactive visualization server for the model using SolaraViz and launches a batch run of the model.
* `epstein_civil_violence_experimental/requirements.txt`: Lists the dependencies required to run the model.
* `epstein_civil_violence_experimental/Readme.md`: Provides an overview and instructions for the model.

## Further Reading

This model is based adapted from:

[Epstein, J. “Modeling civil violence: An agent-based computational approach”, Proceedings of the National Academy of Sciences, Vol. 99, Suppl. 3, May 14, 2002](http://www.pnas.org/content/99/suppl.3/7243.short)

A similar model is also included with NetLogo:

Wilensky, U. (2004). NetLogo Rebellion model. http://ccl.northwestern.edu/netlogo/models/Rebellion. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.
