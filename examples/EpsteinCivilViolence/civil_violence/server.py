from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.TextVisualization import (
    TextData, TextGrid, TextVisualization
)

from .model import CivilViolenceModel
from .agent import Citizen, Cop


COP_COLOR = "#000000"
AGENT_QUIET_COLOR = "#0066CC"
AGENT_REBEL_COLOR = "#CC0000"
JAIL_COLOR = "#757575"


def citizen_cop_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "x": agent.pos[0], "y": agent.pos[1],
                 "Filled": "true"}

    if type(agent) is Citizen:
        color = AGENT_QUIET_COLOR if agent.condition == "Quiescent" else \
            AGENT_REBEL_COLOR
        color = JAIL_COLOR if agent.jail_sentence else color
        portrayal["Color"] = color
        portrayal["r"] = 0.8
        portrayal["Layer"] = 0

    elif type(agent) is Cop:
        portrayal["Color"] = COP_COLOR
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Shape"] = "rect"
    return portrayal

canvas_element = CanvasGrid(citizen_cop_portrayal, 40, 40, 500, 500)
active_chart = ChartModule([{"Label": "Active", "Color": "Red"}, {"Label": "Jailed", "Color": "Black"}, {"Label": "Quiescent", "Color": "Orange"}], data_collector_name="dc")
leg_slider = UserSettableParameter('slider', "legitimacy", 0.8, 0., 1., 0.001)
cit_vis_slider = UserSettableParameter('slider', "Citizen vision", 3, 1, 10, 1)
cop_vis_slider = UserSettableParameter('slider', "Cop vision", 2, 1, 10, 1)
act_slider = UserSettableParameter('slider', "Active treshold", 0.1, 0., .5, 0.001)
#hom_slider = UserSettableParameter('slider', "Schelling homophily", 3, 1, 9, 1)
nb_choice = UserSettableParameter('choice', 'Neighbourhood vision setup', value='Neumann',
                                              choices=['Neumann', 'Moore'])
jail_slider = UserSettableParameter('slider', "Max jail time", 30, 0., 150, 1)
server = ModularServer(CivilViolenceModel, [canvas_element, active_chart],
                       "Epstein Civil Violence",
                       {"height": 40,
                       "width": 40,
                       "citizen_density": .7,

                      # Original article uses 0.04 and 0.074
                       "cop_density": .074,

                       "citizen_vision": cit_vis_slider,
                       "cop_vision": cop_vis_slider,
                       "legitimacy": leg_slider,
                       "max_jail_term": jail_slider,
                       "active_threshold": act_slider,
                       "moore": nb_choice})
