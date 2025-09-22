from .agents import GrassPatch, SheepRL, WolfRL


def create_initial_agents(self):
    # Create sheep:
    for _ in range(self.initial_sheep):
        x = self.random.randrange(self.width)
        y = self.random.randrange(self.height)
        energy = self.random.randrange(2 * self.sheep_gain_from_food)
        unique_id_str = f"sheep_{self.next_id()}"
        sheep = SheepRL(unique_id_str, None, self, True, energy)
        self.grid.place_agent(sheep, (x, y))
        self.add(sheep)

    # Create wolves
    for _ in range(self.initial_wolves):
        x = self.random.randrange(self.width)
        y = self.random.randrange(self.height)
        energy = self.random.randrange(2 * self.wolf_gain_from_food)
        unique_id_str = f"wolf_{self.next_id()}"
        wolf = WolfRL(unique_id_str, None, self, True, energy)
        self.grid.place_agent(wolf, (x, y))
        self.add(wolf)

    # Create grass patches
    if self.grass:
        for _, (x, y) in self.grid.coord_iter():
            fully_grown = self.random.choice([True, False])

            if fully_grown:
                countdown = self.grass_regrowth_time
            else:
                countdown = self.random.randrange(self.grass_regrowth_time)

            unique_id_str = f"grass_{self.next_id()}"
            patch = GrassPatch(unique_id_str, None, self, fully_grown, countdown)
            self.grid.place_agent(patch, (x, y))
            self.add(patch)


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


def grid_to_observation(self):
    # Convert grid to matrix for better representation
    self.obs_grid = []
    for i in self.grid._grid:
        row = []
        for j in i:
            value = [0, 0, 0]
            for agent in j:
                if isinstance(agent, SheepRL):
                    value[0] = 1
                elif isinstance(agent, WolfRL):
                    value[1] = 1
                elif isinstance(agent, GrassPatch) and agent.fully_grown:
                    value[2] = 1
            row.append(value)
        self.obs_grid.append(row)
