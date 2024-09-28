# GeoSIR Epidemics Model

[![](https://img.youtube.com/vi/oZShtptaIg4/0.jpg)](https://www.youtube.com/watch?v=oZShtptaIg4)

## Summary

This is a geoversion of a simple agent-based pandemic SIR model, as an example to show the capabilities of mesa-geo.

It uses geographical data of Toronto's regions on top of a an Leaflet map to show the location of agents (in a continuous space).

Person agents are initially located in random positions in the city, then start moving around unless they die.
A fraction of agents start with an infection and may recover or die in each step.
Susceptible agents (those who have never been infected) who come in proximity with an infected agent may become infected.

Neighbourhood agents represent neighbourhoods in the Toronto, and become hot-spots (colored red) if there are infected agents inside them.
Data obtained from [this link](http://adamw523.com/toronto-geojson/).

## How to Run

To run the model interactively, run `solara run app.py` in this directory. e.g.

```bash
solara run app.py
```

Then open your browser to [http://127.0.0.1:8765/](http://127.0.0.1:8765/) and press the play button `▶`.
