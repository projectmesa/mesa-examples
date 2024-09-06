import gymnasium as gym
import mesa
import numpy as np
from mesa_models.wolf_sheep.agents import GrassPatch
from mesa_models.wolf_sheep.model import WolfSheep
from mesa_models.wolf_sheep.scheduler import RandomActivationByTypeFiltered
from ray.rllib.env import MultiAgentEnv

from .agents import Sheep_RL, Wolf_RL
from .utility import create_intial_agents, grid_to_observation


class WolfSheep_RL(WolfSheep, MultiAgentEnv):
    """
    Wolf_RL-Sheep Predation Model
    """

    def __init__(
        self,
        width=20,
        height=20,
        initial_sheep=100,
        initial_wolves=25,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=True,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
        vision=4
    ):
        """
        Create a new Wolf_RL-Sheep model with the given parameters.
        """
        super().__init__(width, height, initial_sheep, initial_wolves, sheep_reproduce, wolf_reproduce, wolf_gain_from_food, grass, grass_regrowth_time, sheep_gain_from_food)
        # Defining RL specific attributes 
        self.vision = vision
        # The observation space is a dictionary containing the grid and energy of the agent
        self.observation_space = gym.spaces.Dict({
            'grid': gym.spaces.Box(low=0, high=1, shape=((self.vision*2+1)**2 - 1, 3), dtype=int),  # 3 for sheep, wolf, grass
            'energy': gym.spaces.Box(low=-1, high=np.inf, shape=(1,), dtype=np.float32)
        })
        # The action space is a discrete space with 5 actions of moving up, down, left, right
        self.action_space =  gym.spaces.Discrete(4)
        self.max_steps = 500
        self.datacollector = mesa.DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_type_count(Wolf_RL),
                "Sheep": lambda m: m.schedule.get_type_count(Sheep_RL),
                "Grass": lambda m: m.schedule.get_type_count(
                    GrassPatch, lambda x: x.fully_grown
                ),
            }
        )

    def step(self, action_dict):

        self.action_dict = action_dict
        self.schedule.step()
        self.datacollector.collect(self)
        
        # Get rewards
        rewards = self.cal_reward()

        # Get observations
        # We convert grid to a matrix and then neighbors of each agent is extracted
        grid_to_observation(self, Sheep_RL, Wolf_RL, GrassPatch)
        obs = { }
        for agent in self.schedule.agents:
            if isinstance(agent, (Sheep_RL, Wolf_RL)):
                neighbors = agent.model.grid.get_neighborhood(
                            agent.pos, moore=True, radius=self.vision)

                obs[agent.unique_id] = {
                    'grid': np.array([self.obs_grid[neighbor[0]][neighbor[1]] for neighbor in neighbors]),
                    'energy': np.array([agent.energy])}        
        
        # Either time finishes or either wolves or sheep are extinct
        done = {a.unique_id: False for a in self.schedule.agents if isinstance(a, (Sheep_RL, Wolf_RL))}

        # Check if either wolves or sheep are extinct
        if self.schedule.get_type_count(Wolf_RL) == 0 or self.schedule.get_type_count(Sheep_RL) == 0 or self.schedule.time > self.max_steps:
            done['__all__'] = True
        else:
            done['__all__'] = False

        # Prepare info dictionary
        truncated = {a.unique_id: False for a in self.schedule.agents if isinstance(a, (Sheep_RL, Wolf_RL))}
        truncated['__all__'] = np.all(list(truncated.values()))

        # All the agents that dies during this step are marked as done and rewarded penalty
        sample = next(iter(obs.values()))  
        for agent_id in action_dict.keys():
            if agent_id not in rewards.keys():
                done[agent_id] = True
                rewards[agent.unique_id] = -20 
                truncated[agent.unique_id] = False
                # generate a sample observation with 0 -1

                obs[agent_id] = {
                    'grid': np.zeros_like(sample["grid"]),
                    'energy': np.array([-1])
                }

        return obs, rewards, done, truncated, {}

    def cal_reward(self):
        rewards = {}
        # Calculate rewards
        # Agents are rewarded for being alive and having energy
        for agent in self.schedule.agents:
            if isinstance(agent, (Sheep_RL, Wolf_RL)):
                if isinstance(agent, Sheep_RL):
                    rewards[agent.unique_id] = min(4, agent.energy - 4)
                else:
                    rewards[agent.unique_id] = min(4, agent.energy/5 - 4)
        return rewards
    
    def reset(self, *, seed=None, options=None):
        # Reset your environment here
        super().reset()
        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.current_id = 0
        create_intial_agents(self, Sheep_RL, Wolf_RL, GrassPatch)
        grid_to_observation(self, Sheep_RL, Wolf_RL, GrassPatch)
        obs = {}
        for agent in self.schedule.agents:
            if isinstance(agent, (Sheep_RL, Wolf_RL)):
                neighbors = agent.model.grid.get_neighborhood(
                            agent.pos, moore=True, radius=self.vision)

                obs[agent.unique_id] = {
                    'grid': np.array([self.obs_grid[neighbor[0]][neighbor[1]] for neighbor in neighbors]),
                    'energy': np.array([agent.energy])}        
        return obs , {}

