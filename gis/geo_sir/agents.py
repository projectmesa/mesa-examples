import mesa_geo as mg
from shapely.geometry import Point


class PersonAgent(mg.GeoAgent):
    """Person Agent."""

    def __init__(
        self,
        unique_id,
        model,
        geometry,
        crs,
        agent_type="susceptible",
        mobility_range=100,
        recovery_rate=0.2,
        death_risk=0.1,
        init_infected=0.1,
    ):
        """
        Create a new person agent.
        :param unique_id:   Unique identifier for the agent
        :param model:       Model in which the agent runs
        :param geometry:    Shape object for the agent
        :param agent_type:  Indicator if agent is infected
                            ("infected", "susceptible", "recovered" or "dead")
        :param mobility_range:  Range of distance to move in one step
        """
        super().__init__(unique_id, model, geometry, crs)
        # Agent parameters
        self.atype = agent_type
        self.mobility_range = mobility_range
        self.recovery_rate = recovery_rate
        self.death_risk = death_risk

        # Random choose if infected
        if self.random.random() < init_infected:
            self.atype = "infected"
            self.model.counts["infected"] += 1  # Adjust initial counts
            self.model.counts["susceptible"] -= 1

    def move_point(self, dx, dy):
        """
        Move a point by creating a new one
        :param dx:  Distance to move in x-axis
        :param dy:  Distance to move in y-axis
        """
        return Point(self.geometry.x + dx, self.geometry.y + dy)

    def step(self):
        """Advance one step."""
        # If susceptible, check if exposed
        if self.atype == "susceptible":
            neighbors = self.model.space.get_neighbors_within_distance(
                self, self.model.exposure_distance
            )
            for neighbor in neighbors:
                if (
                    neighbor.atype == "infected"
                    and self.random.random() < self.model.infection_risk
                ):
                    self.atype = "infected"
                    break

        # If infected, check if it recovers or if it dies
        elif self.atype == "infected":
            if self.random.random() < self.recovery_rate:
                self.atype = "recovered"
            elif self.random.random() < self.death_risk:
                self.atype = "dead"

        # If not dead, move
        if self.atype != "dead":
            move_x = self.random.randint(-self.mobility_range, self.mobility_range)
            move_y = self.random.randint(-self.mobility_range, self.mobility_range)
            self.geometry = self.move_point(move_x, move_y)  # Reassign geometry

        self.model.counts[self.atype] += 1  # Count agent type

    def __repr__(self):
        return "Person " + str(self.unique_id)


class NeighbourhoodAgent(mg.GeoAgent):
    """Neighbourhood agent. Changes color according to number of infected inside it."""

    def __init__(
        self, unique_id, model, geometry, crs, agent_type="safe", hotspot_threshold=1
    ):
        """
        Create a new Neighbourhood agent.
        :param unique_id:   Unique identifier for the agent
        :param model:       Model in which the agent runs
        :param geometry:    Shape object for the agent
        :param agent_type:  Indicator if agent is infected
                            ("infected", "susceptible", "recovered" or "dead")
        :param hotspot_threshold:   Number of infected agents in region
                                    to be considered a hot-spot
        """
        super().__init__(unique_id, model, geometry, crs)
        self.atype = agent_type
        self.hotspot_threshold = (
            hotspot_threshold  # When a neighborhood is considered a hot-spot
        )
        self.color_hotspot()

    def step(self):
        """Advance agent one step."""
        self.color_hotspot()
        self.model.counts[self.atype] += 1  # Count agent type

    def color_hotspot(self):
        # Decide if this region agent is a hot-spot
        # (if more than threshold person agents are infected)
        neighbors = self.model.space.get_intersecting_agents(self)
        infected_neighbors = [
            neighbor for neighbor in neighbors if neighbor.atype == "infected"
        ]
        if len(infected_neighbors) >= self.hotspot_threshold:
            self.atype = "hotspot"
        else:
            self.atype = "safe"

    def __repr__(self):
        return "Neighborhood " + str(self.unique_id)
