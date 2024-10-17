import mesa_geo as mg
import solara
from mesa.visualization import SolaraViz
from mesa_geo.visualization import make_geospace_leaflet
from population.model import Population
from population.space import UgandaCell
from shapely.geometry import Point, Polygon


def make_plot_num_agents(model):
    return solara.Markdown(f"**Number of Agents: {len(model.space.agents)}**")


def agent_portrayal(agent):
    if isinstance(agent, mg.GeoAgent):
        if isinstance(agent.geometry, Point):
            return {
                "stroke": False,
                "color": "Green",
                "radius": 2,
                "fillOpacity": 0.3,
            }
        elif isinstance(agent.geometry, Polygon):
            return {
                "fillColor": "Blue",
                "fillOpacity": 1.0,
            }
    elif isinstance(agent, UgandaCell):
        return (agent.population, agent.population, agent.population, 1)


model = Population()
page = SolaraViz(
    model,
    [
        make_geospace_leaflet(agent_portrayal),
        make_plot_num_agents,
    ],
    name="Population Model",
)

page  # noqa
