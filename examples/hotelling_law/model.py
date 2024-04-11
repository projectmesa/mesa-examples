# Adjust the import statement based on your project structure
import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid, SingleGrid
from mesa.time import RandomActivation

from examples.hotelling_law.agents import (
    StoreAgent,
)


# Function to compute the average price of all store agents in the model.
def compute_average_price(model):
    """Compute the average price of all stores."""
    return np.mean(model.agents.get("price"))


# Function to compute the total revenue for all store agents,
# assuming revenue is proportional to price.
def compute_total_revenue(model):
    """Compute the total revenue of all stores,
    simplified as price * market share."""
    return sum(model.agents.get("price"))


# The main model class that sets up and runs the simulation.
class HotellingModel(Model):
    """
    A model simulating competition and pricing strategies among stores
    within a defined environment. This simulation
    explores the dynamics of market competition, specifically focusing
    on how pricing and location strategies affect
    market outcomes in accordance with Hotelling's Law.

    Parameters:
        N (int): The number of store agents participating in the simulation.
        Each agent acts as an individual store competing in the market.
        width (int), height (int): The dimensions of the simulation grid.
        These dimensions define the size of the environment in which the
        store agents operate.
        mode (str): Defines the operation mode of the simulation,
        influencing agent behavior. The available modes are:
        - 'default': In this mode, agents have the ability to both move
        (if enabled) and adjust their pricing in response
        to market conditions.
        - 'pricing_only': Agents focus solely on adjusting their prices
        to optimize market positioning and do not move regardless of
        their mobility settings.
        - 'moving_only': Agents can change their locations if they are
        enabled to move but will not adjust their prices. This mode
        is useful for studying the effects of spatial distribution
        without pricing competition.
        mobility_rate (int): Represents the percentage of agents that
        are allowed to move in the simulation environment. This parameter
        is a percentage of the total number of agents (N),
        determining how many of them have the capability to relocate.
        For example, a mobility rate of 80 means 80% of the store agents
        can change their locations if the operation mode permits movement.
        This allows for the exploration of market dynamics under
        varying degrees of agent mobility.

    Key Components:
        HotellingModel: The class encapsulating the simulation environment,
        responsible for initializing the agents, setting up the grid,
        and managing data collection for analysis.
        compute_average_price(model),compute_total_revenue(model):
        Functions that calculate key economic metrics from the
        simulation data for analysis.

    The model leverages Mesa's framework capabilities to simulate agent
    interactions, environmental constraints,and the emergent phenomena
    resulting from individual agent strategies within the
    market context defined by Hotelling's Law.
    """

    def __init__(
        self,
        N=10,
        width=20,
        height=20,
        mode="default",
        environment_type="grid",
        mobility_rate=80,
    ):
        # Initialize the model with parameters for number of agents,
        # grid size, mode of operation,environment type,
        # and mobility rate.
        super().__init__()
        self.num_agents = N  # Total number of store agents in the model.
        self.mobility_rate = mobility_rate  # Percentage of agents that can move.
        self.mode = mode  # Operational mode of the simulation
        # (affects agents' behavior).
        self.environment_type = (
            environment_type  # Type of environment ('grid' or 'line').
        )
        self.schedule = RandomActivation(
            self
        )  # Scheduler to activate agents one at a time, in random order.

        # Initialize the spatial grid based on the specified environment type.
        if environment_type == "grid":
            self.grid = MultiGrid(
                width, height, True
            )  # A grid where multiple agents can occupy the same cell.
        elif environment_type == "line":
            self.grid = SingleGrid(
                width, height, True
            )  # A grid representing a line (single occupancy per cell).

        self._initialize_agents()

        # DataCollector to gather simulation data for analysis.
        self.datacollector = DataCollector(
            model_reporters={
                "Average Price": compute_average_price,
                "Total Revenue": compute_total_revenue,
                "Price Variance": lambda m: np.var([agent.price for agent in m.agents]),
            }
        )

    # Private method to initialize and place agents on the grid.
    def _initialize_agents(self):
        num_mobile_agents = int(
            self.num_agents * (self.mobility_rate / 100)
        )  # Calculate number of mobile agents.
        mobile_agents_assigned = 0

        # Different logic for placing agents based on the environment type.
        if self.environment_type == "line":
            middle_x = (
                self.grid.width // 2
            )  # For a line environment, agents are placed along
            # the middle axis.
            available_positions = set(
                range(self.grid.height)
            )  # Track available positions for placement.

            for unique_id in range(self.num_agents):
                if not available_positions:
                    raise ValueError("No more available positions to place agents.")

                can_move = mobile_agents_assigned < num_mobile_agents
                if can_move:
                    mobile_agents_assigned += 1

                agent = StoreAgent(unique_id, self, can_move=can_move)
                self.schedule.add(agent)

                y_position = self.random.choice(list(available_positions))
                available_positions.remove(y_position)
                initial_position = (middle_x, y_position)
                self.grid.place_agent(agent, initial_position)
        else:
            for unique_id in range(self.num_agents):
                can_move = mobile_agents_assigned < num_mobile_agents
                if can_move:
                    mobile_agents_assigned += 1

                agent = StoreAgent(unique_id, self, can_move=can_move)
                self.schedule.add(agent)

                # Randomly place agents on the grid for a grid environment.
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))

    # Method to advance the simulation by one step.
    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)  # Collect data for the current step.
        self.schedule.step()  # Activate the next agent in the schedule.

    # Utility method to run the model for a specified number of steps.
    def run_model(self, step_count=200):
        """Run the model for a certain number of steps."""
        for i in range(step_count):
            self.step()

    # Method to export collected data to CSV files for further analysis.
    def export_data(self):
        """Export collected data to a CSV file."""
        model_data = self.datacollector.get_model_vars_dataframe()
        agent_data = self.datacollector.get_agent_vars_dataframe()
        # Adjust the file paths if necessary to match your project structure
        model_data.to_csv("output/model_data.csv")
        agent_data.to_csv("output/agent_data.csv")
