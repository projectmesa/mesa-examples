from .agent import CitizenRL, CopRL


def create_initial_agents(self):
    # Create agents
    unique_id = 0
    if self.cop_density + self.citizen_density > 1:
        raise ValueError("CopRL density + citizen density must be less than 1")
    cops = []
    citizens = []
    for _, (x, y) in self.grid.coord_iter():
        if self.random.random() < self.cop_density:
            unique_id_str = f"cop_{unique_id}"
            cop = CopRL(unique_id_str, self, (x, y), vision=self.cop_vision)
            unique_id += 1
            self.grid[x][y] = cop
            cops.append(cop)
        elif self.random.random() < (self.cop_density + self.citizen_density):
            unique_id_str = f"citizen_{unique_id}"
            citizen = CitizenRL(
                unique_id_str,
                self,
                (x, y),
                hardship=self.random.random(),
                regime_legitimacy=self.legitimacy,
                risk_aversion=self.random.random(),
                threshold=0,
                vision=self.citizen_vision,
            )
            unique_id += 1
            self.grid[x][y] = citizen
            citizens.append(citizen)
    # Initializing cops then citizens
    # This ensures cops act out their step before citizens
    for cop in cops:
        self.add(cop)
    for citizen in citizens:
        self.add(citizen)


def grid_to_observation(self):
    # Convert neighborhood to observation grid
    self.obs_grid = []
    for i in self.grid._grid:
        row = []
        for j in i:
            if j is None:
                row.append(0)  # Empty cell
            elif isinstance(j, CitizenRL):
                if j.condition == "Quiescent":
                    row.append(
                        3 if j.jail_sentence > 0 else 1
                    )  # Quiescent citizen (jailed or not)
                elif j.condition == "Active":
                    row.append(2)  # Active citizen
            else:
                row.append(4)  # Cop
        self.obs_grid.append(row)


def move(self, action, empty_neighbors):
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
