# GeoSchelling Model (Points & Polygons)

[![](https://img.youtube.com/vi/iLMU6jfmir8/0.jpg)](https://www.youtube.com/watch?v=iLMU6jfmir8)

## Summary

This is a geoversion of a simplified Schelling example.

### GeoSpace

The NUTS-2 regions are considered as a shared definition of neighborhood among all people agents, instead of a locally defined neighborhood such as Moore or von Neumann.

### GeoAgent

There are two types of GeoAgents: people and regions. Each person resides in a randomly assigned region, and checks the color ratio of its region against a pre-defined "happiness" threshold at every time step. If the ratio falls below a certain threshold (e.g., 40%), the agent is found to be "unhappy", and randomly moves to another region. People are represented as points, with locations randomly chosen within their regions. The color of a region depends on the color of the majority population it contains (i.e., point in polygon calculations).

## How to Run

To run the model interactively, run `solara run app.py` in this directory. e.g.

```bash
solara run app.py
```

Then open your browser to [http://127.0.0.1:8765/](http://127.0.0.1:8765/) and press the play button `▶`.
