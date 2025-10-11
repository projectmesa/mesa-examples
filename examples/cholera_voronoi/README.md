# Disease dynamics on Voronoi Grid

This folder contains a implementation of Cholera spread analyzed by John Snow at London Soho district during the 19th century. The physicist discovered contaminated water from Broad Street Pump was the source of disease by drawing a Voronoi diagram around pumps and mapping cholera cases.

The model has two agents: people and pumps. Pumps can infect people and neighbor pumps. People start as susceptible, can be infected by pumps and recover or die, according to a simple SIR model. Each cell has only one pump and is connected to neighbor cells according to Voronoi's diagram. The model aims to investigate how fast actions oriented by Voronoi diagrams can prevent disease spread.

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press ``run``.

## Files

* ``cholera_voronoi/agents.py``: Defines Pump and Person agents.
* ``cholera_voronoi/model.py``: Defines the model itself, initialized with John Snow study about Cholera Spread pump locations.
* ``cholera_voronoi/server.py``: Defines an interactive visualization.
* ``run.py``: Launches the visualization

## Further reading
- [R Package for Analyzing John Snow's 1854 Cholera Map ](https://github.com/lindbrook/cholera)
- [Why this pattern shows up everywhere in nature | Voronoi Cell Pattern](https://www.youtube.com/watch?v=GafRRl5XRPM&t=183s)
- [John Snow, Cholera, the Broad Street Pump; Waterborne Diseases Then and Now](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7150208/)