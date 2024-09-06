import os

import mesa
import numpy as np
from mesa_models.wolf_sheep.agents import GrassPatch
from ray import tune
from ray.rllib.algorithms.algorithm import Algorithm

from .agents import SheepRL, WolfRL
from .model import WolfSheepRL
from .utility import grid_to_observation


class WolfSheepServer(WolfSheepRL):
    def __init__(self, width=20, height=20, initial_sheep=100, initial_wolves=25, sheep_reproduce=0.04, wolf_reproduce=0.05, wolf_gain_from_food=20, grass=True, grass_regrowth_time=30, sheep_gain_from_food=4, model_path=None):
        super().__init__(width, height, initial_sheep, initial_wolves, sheep_reproduce, wolf_reproduce, wolf_gain_from_food, grass, grass_regrowth_time, sheep_gain_from_food)
        def env_creator(_):
            return WolfSheepRL(width, height, initial_sheep, initial_wolves, sheep_reproduce, wolf_reproduce, wolf_gain_from_food, grass, grass_regrowth_time, sheep_gain_from_food)
        tune.register_env("WorldSheepModel-v0", env_creator)
        self.iteration = 0
        # Load the model from checkpoint
        checkpoint_path = model_path
        algo = Algorithm.from_checkpoint(checkpoint_path)
        self.wolf_policy = algo.get_policy("policy_wolf")
        self.sheep_policy = algo.get_policy("policy_sheep")
    
    def step(self):
        if self.iteration == 0:
            self.reset()
        self.datacollector.collect(self)
        # Get the observation for each agent
        grid_to_observation(self, SheepRL, WolfRL, GrassPatch)
        obs = {}
        for agent in self.schedule.agents:
            if isinstance(agent, (SheepRL, WolfRL)):
                neighbors = agent.model.grid.get_neighborhood(agent.pos, moore=True, radius=self.vision)
                obs[agent.unique_id] = {'grid': np.array([self.obs_grid[neighbor[0]][neighbor[1]] for neighbor in neighbors]), 'energy': np.array([agent.energy])}    
        action_dict = {}
        # Get the action for each agent
        for agent in self.schedule.agents:
            if isinstance(agent, SheepRL):
                action_dict[agent.unique_id] = self.sheep_policy.compute_single_action(obs[agent.unique_id], explore=False)[0]
            elif isinstance(agent, WolfRL):
                action_dict[agent.unique_id] = self.wolf_policy.compute_single_action(obs[agent.unique_id], explore=False)[0]
        self.action_dict = action_dict
        # Take a step in the environment
        self.schedule.step()
        self.iteration += 1
        if self.schedule.get_type_count(WolfRL) == 0 or self.schedule.get_type_count(SheepRL) == 0 or self.schedule.time > self.max_steps:
            self.running = False

def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    file_path = os.path.dirname(os.path.abspath(__file__))
    resources_path = os.path.join(file_path, "resources")

    if type(agent) is SheepRL:
        portrayal["Shape"] = os.path.join(resources_path, "sheep.png")
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        
    elif type(agent) is WolfRL:
        portrayal["Shape"] = os.path.join(resources_path, "wolf.png")
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is GrassPatch:
        portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"] if agent.fully_grown else ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
    return portrayal

canvas_element = mesa.visualization.CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = mesa.visualization.ChartModule([
    {"Label": "Wolves", "Color": "#AA0000"},
    {"Label": "Sheep", "Color": "#666666"},
    {"Label": "Grass", "Color": "#00AA00"}
])

model_params = {
    "height": 20,
    "width": 20,
    "model_path": None,
    "title": mesa.visualization.StaticText("Parameters:"),
    "grass": mesa.visualization.Checkbox("Grass Enabled", True),
    "grass_regrowth_time": mesa.visualization.Slider("Grass Regrowth Time", 20, 1, 50),
    "initial_sheep": mesa.visualization.Slider("Initial Sheep Population", 100, 10, 300),
    "sheep_reproduce": mesa.visualization.Slider("Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01),
    "initial_wolves": mesa.visualization.Slider("Initial Wolf Population", 25, 10, 300),
    "wolf_reproduce": mesa.visualization.Slider("Wolf Reproduction Rate", 0.05, 0.01, 1.0, 0.01, description="The rate at which wolf agents reproduce."),
    "wolf_gain_from_food": mesa.visualization.Slider("Wolf Gain From Food Rate", 20, 1, 50),
    "sheep_gain_from_food": mesa.visualization.Slider("Sheep Gain From Food", 4, 1, 10),
}

def run_model(height=20, width=20, model_path=None):
    model_params["height"] = height
    model_params["width"] = width
    model_params["model_path"] = model_path
    server = mesa.visualization.ModularServer(
        WolfSheepServer,
        [canvas_element, chart_element],
        "Wolf Sheep Predation",
        model_params,
    )
    return server