import numpy as np

import mesa
from mesa_models.epstein_civil_violence.portrayal import citizen_cop_portrayal
import ray
from ray import tune
from ray.rllib.algorithms.algorithm import Algorithm

from .agent import CITIZEN_RL
from .model import EPSTEINCIVILVIOLENCE_RL
from .utility import grid_to_observation

ray.init(local_mode=True)

class EpsteinCivilViolenceServer(EPSTEINCIVILVIOLENCE_RL):
    def __init__(
        self,
        height=20,
        width=20,
        citizen_density=0.5,
        cop_density=0.1,
        citizen_vision=4,
        cop_vision=4,
        legitimacy=0.82,
        max_jail_term=30,
        model_path=None,
    ):
        super().__init__(
            height,
            width,
            citizen_density,
            cop_density,
            citizen_vision,
            cop_vision,
            legitimacy,
            max_jail_term,
        )
        self.running = True
        self.iteration = 0

        def env_creator(_):
            return EPSTEINCIVILVIOLENCE_RL(
                height,
                width,
                citizen_density,
                cop_density,
                citizen_vision,
                cop_vision,
                legitimacy,
                max_jail_term,
            )

        tune.register_env("WorldcopModel-v0", env_creator)
        # Get the directory of the checkpoint
        checkpoint_path = model_path
        # Initialize the algorithm with the checkpoint
        algo = Algorithm.from_checkpoint(checkpoint_path)
        self.cop_policy = algo.get_policy("policy_cop")
        self.citizen_policy = algo.get_policy("policy_citizen")

    def step(self):
        if self.iteration == 0:
            self.reset()
        grid_to_observation(self, CITIZEN_RL)
        observation = {}
        for agent in self.schedule.agents:
            observation[agent.unique_id] = [
                self.obs_grid[neighbor[0]][neighbor[1]]
                for neighbor in agent.neighborhood
            ]

        action_dict = {}
        # Compute actions for each agent
        for agent in self.schedule.agents:
            if agent.unique_id.startswith("cop"):
                action_dict[agent.unique_id] = self.cop_policy.compute_single_action(
                    np.array(observation[agent.unique_id]).T, explore=False
                )[0]
            else:
                action_dict[agent.unique_id] = (
                    self.citizen_policy.compute_single_action(
                        np.array(observation[agent.unique_id]).T, explore=False
                    )[0]
                )
        self.action_dict = action_dict
        # Step the model
        self.schedule.step()
        self.datacollector.collect(self)
        self.iteration += 1
        if self.iteration > self.max_iters:
            self.running = False


model_params = {
    "height": 20,
    "width": 20,
    "model_path": None,
    "citizen_density": mesa.visualization.Slider(
        "Initial Agent Density", 0.5, 0.0, 0.9, 0.1
    ),
    "cop_density": mesa.visualization.Slider(
        "Initial Cop Density", 0.1, 0.0, 0.3, 0.01
    ),
    "citizen_vision": mesa.visualization.Slider("Citizen Vision", 4, 1, 10, 1),
    "cop_vision": mesa.visualization.Slider("Cop Vision", 4, 1, 10, 1),
    "legitimacy": mesa.visualization.Slider(
        "Government Legitimacy", 0.82, 0.0, 1, 0.01
    ),
    "max_jail_term": mesa.visualization.Slider("Max Jail Term", 10, 0, 50, 1),
}

canvas_element = mesa.visualization.CanvasGrid(citizen_cop_portrayal, 20, 20, 480, 480)
chart = mesa.visualization.ChartModule(
    [
        {"Label": "Quiescent", "Color": "#648FFF"},
        {"Label": "Active", "Color": "#FE6100"},
        {"Label": "Jailed", "Color": "#808080"},
    ],
    data_collector_name="datacollector",
)


def run_model(height=20, width=20, model_path=None):
    model_params["height"] = height
    model_params["width"] = width
    model_params["model_path"] = model_path
    server = mesa.visualization.ModularServer(
        EpsteinCivilViolenceServer,
        [canvas_element, chart],
        "Epstein Civil Violence",
        model_params,
    )
    return server
