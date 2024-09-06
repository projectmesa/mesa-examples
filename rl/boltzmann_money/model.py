# This code implements a multi-agent model called MoneyModel using the Mesa library.
# The model simulates the distribution of wealth among agents in a grid environment.
# Each agent has a randomly assigned wealth and can move to neighboring cells.
# Agents can also give money to other agents in the same cell if they have greater wealth.
# The model is trained by a scientist who believes in an equal society and wants to minimize the Gini coefficient, which measures wealth inequality.
# The model is trained using the Proximal Policy Optimization (PPO) algorithm from the stable-baselines3 library.
# The trained model is saved as "ppo_money_model".

import random

import gymnasium
import matplotlib.pyplot as plt

# Import mesa
import mesa

# Import necessary libraries
import numpy as np
import seaborn as sns
from mesa_models.boltzmann_wealth_model.model import (
    BoltzmannWealthModel,
    MoneyAgent,
    compute_gini,
)

NUM_AGENTS = 10


# Define the agent class
class MoneyAgentRL(MoneyAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = np.random.randint(1, NUM_AGENTS)

    def move(self, action):
        empty_neighbors = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        # Define the movement deltas
        moves = {
            0: (1, 0),  # Move right
            1: (-1, 0),  # Move left
            2: (0, -1),  # Move up
            3: (0, 1),  # Move down
            4: (0, 0),  # Stay in place
        }

        # Get the delta for the action, defaulting to (0, 0) if the action is invalid
        dx, dy = moves.get(int(action), (0, 0))

        # Calculate the new position and wrap around the grid
        new_position = (
            (self.pos[0] + dx) % self.model.grid.width,
            (self.pos[1] + dy) % self.model.grid.height,
        )

        # Move the agent if the new position is in empty_neighbors
        if new_position in empty_neighbors:
            self.model.grid.move_agent(self, new_position)

    def take_money(self):
        # Get all agents in the same cell
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            # Choose a random agent from the cellmates
            other_agent = random.choice(cellmates)
            if other_agent.wealth > self.wealth:
                # Transfer money from other_agent to self
                other_agent.wealth -= 1
                self.wealth += 1

    def step(self):
        # Get the action for the agent
        action = self.model.action_dict[self.unique_id]
        # Move the agent based on the action
        self.move(action)
        # Take money from other agents in the same cell
        self.take_money()


# Define the model class
class BoltzmannWealthModelRL(BoltzmannWealthModel, gymnasium.Env):
    def __init__(self, N, width, height):
        super().__init__(N, width, height)
        # Define the observation and action space for the RL model
        # The observation space is the wealth of each agent and their position
        self.observation_space = gymnasium.spaces.Box(low=0, high=10 * N, shape=(N, 3))
        # The action space is a MultiDiscrete space with 5 possible actions for each agent
        self.action_space = gymnasium.spaces.MultiDiscrete([5] * N)
        self.is_visualize = False

    def step(self, action):
        self.action_dict = action
        # Perform one step of the model
        self.schedule.step()
        # Collect data for visualization
        self.datacollector.collect(self)
        # Compute the new Gini coefficient
        new_gini = compute_gini(self)
        # Compute the reward based on the change in Gini coefficient
        reward = self.calculate_reward(new_gini)
        self.prev_gini = new_gini
        # Get the observation for the RL model
        obs = self._get_obs()
        if self.schedule.time > 5 * NUM_AGENTS:
            # Terminate the episode if the model has run for a certain number of timesteps
            done = True
            reward = -1
        elif new_gini < 0.1:
            # Terminate the episode if the Gini coefficient is below a certain threshold
            done = True
            reward = 50 / self.schedule.time
        else:
            done = False
        info = {}
        truncated = False
        return obs, reward, done, truncated, info

    def calculate_reward(self, new_gini):
        if new_gini < self.prev_gini:
            # Compute the reward based on the decrease in Gini coefficient
            reward = (self.prev_gini - new_gini) * 20
        else:
            # Penalize for increase in Gini coefficient
            reward = -0.05
        self.prev_gini = new_gini
        return reward

    def visualize(self):
        # Visualize the Gini coefficient over time
        gini = self.datacollector.get_model_vars_dataframe()
        g = sns.lineplot(data=gini)
        g.set(title="Gini Coefficient over Time", ylabel="Gini Coefficient")
        plt.show()

    def reset(self, *, seed=None, options=None):
        if self.is_visualize:
            # Visualize the Gini coefficient before resetting the model
            self.visualize()
        super().reset()
        self.grid = mesa.space.MultiGrid(self.grid.width, self.grid.height, True)
        self.schedule = mesa.time.RandomActivation(self)
        for i in range(self.num_agents):
            # Create MoneyAgentRL instances and add them to the schedule
            a = MoneyAgentRL(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        self.prev_gini = compute_gini(self)
        return self._get_obs(), {}

    def _get_obs(self):
        # The observation is the wealth of each agent and their position
        obs = []
        for a in self.schedule.agents:
            obs.append([a.wealth, *list(a.pos)])
        return np.array(obs)
