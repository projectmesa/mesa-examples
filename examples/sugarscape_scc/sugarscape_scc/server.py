import mesa
from mesa_models.sugarscape_cg.agents import Sugar

# TODO implement age graph as well
from .agents import SsAgent3 as SsAgent

from .model import SugarscapeScc

color_dic = {4: "#005C00", 3: "#008300", 2: "#00AA00", 1: "#00F800"}


def SsAgent_portrayal(agent):
    if agent is None:
        return

    if type(agent) is SsAgent:
        return {"Shape": "sugarscape_scc/resources/ant.png", "scale": 0.9, "Layer": 1}

    elif type(agent) is Sugar:
        color = color_dic[agent.amount] if agent.amount != 0 else "#D6F5D6"
        return {
            "Color": color,
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "w": 1,
            "h": 1,
        }

    return {}


canvas_element = mesa.visualization.CanvasGrid(SsAgent_portrayal, 50, 50, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [{"Label": "SsAgent", "Color": "#AA0000"}], data_collector_name="datacollector"
)
bar_graph = mesa.visualization.BarChartModule(
    [{"Label": "age", "Color": "#AAAAAA"}], data_collector_name="datacollector"
)
server = mesa.visualization.ModularServer(
    SugarscapeScc, [canvas_element, chart_element, bar_graph], "Sugarscape 3 SCC"
)
