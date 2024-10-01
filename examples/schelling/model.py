import mesa

class SchellingAgent(mesa.Agent):

    def __init__(self, unique_id, model, agent_type):
        """
        Create a new Schelling agent.

        Args:
           unique_id: A unique identifier for the agent.
           agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(unique_id, model)
        self.type = agent_type

    def step(self):
        similar = 0
        for neighbor in self.model.grid.iter_neighbors(
            self.pos, moore=True, radius=self.model.radius
        ):
            if neighbor.type == self.type:
                similar += 1

        # If unhappy, decide whether to move:
        if similar < self.model.homophily:
            if self.random.random() < self.model.move_probability:  # Add randomness to moving
                self.model.grid.move_to_empty(self)
            else:
                # Agent decides to stay even if unhappy
                pass
        else:
            self.model.happy += 1



class Schelling(mesa.Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(
        self,
        height=20,
        width=20,
        homophily=3,
        radius=1,
        density=0.8,
        minority_pc=0.2,
        move_probability=0.9,
        seed=None,
    ):
        super().__init__(seed=seed)
        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily
        self.radius = radius
        self.move_probability = move_probability  

        self.grid = mesa.space.SingleGrid(width, height, torus=True)

        self.happy = 0
        self.datacollector = mesa.DataCollector(
            model_reporters={"happy": "happy"},  # Model-level count of happy agents
        )

        # Set up agents with unique IDs
        unique_id = 0  # Initialize unique_id counter
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                agent_type = 1 if self.random.random() < self.minority_pc else 0
                agent = SchellingAgent(unique_id, self, agent_type)  # Pass unique_id
                self.grid.place_agent(agent, pos)
                unique_id += 1  # Increment the unique_id for the next agent

        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.agents.shuffle_do("step")

        self.datacollector.collect(self)

        if self.happy == len(self.agents):
            self.running = False
