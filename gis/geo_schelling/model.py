import random

import mesa
import mesa_geo as mg


class SchellingAgent(mg.GeoAgent):
    """Schelling segregation agent."""

    def __init__(self, unique_id, model, geometry, crs, agent_type=None):
        """Create a new Schelling agent.

        Args:
            unique_id: Unique identifier for the agent.
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(unique_id, model, geometry, crs)
        self.atype = agent_type

    def step(self):
        """Advance agent one step."""
        similar = 0
        different = 0
        neighbors = self.model.space.get_neighbors(self)
        if neighbors:
            for neighbor in neighbors:
                if neighbor.atype is None:
                    continue
                elif neighbor.atype == self.atype:
                    similar += 1
                else:
                    different += 1

        # If unhappy, move:
        if similar < different:
            # Select an empty region
            empties = [a for a in self.model.space.agents if a.atype is None]
            # Switch atypes and add/remove from scheduler
            new_region = random.choice(empties)
            new_region.atype = self.atype
            self.model.schedule.add(new_region)
            self.atype = None
            self.model.schedule.remove(self)
        else:
            self.model.happy += 1

    def __repr__(self):
        return "Agent " + str(self.unique_id)


class GeoSchelling(mesa.Model):
    """Model class for the Schelling segregation model."""

    def __init__(self, density=0.6, minority_pc=0.2, export_data=False):
        self.density = density
        self.minority_pc = minority_pc
        self.export_data = export_data

        self.schedule = mesa.time.RandomActivation(self)
        self.space = mg.GeoSpace(warn_crs_conversion=False)

        self.happy = 0
        self.datacollector = mesa.DataCollector({"happy": "happy"})

        self.running = True

        # Set up the grid with patches for every NUTS region
        ac = mg.AgentCreator(SchellingAgent, model=self)
        agents = ac.from_file("data/nuts_rg_60M_2013_lvl_2.geojson")
        self.space.add_agents(agents)

        # Set up agents
        for agent in agents:
            if random.random() < self.density:
                if random.random() < self.minority_pc:
                    agent.atype = 1
                else:
                    agent.atype = 0
                self.schedule.add(agent)

    def export_agents_to_file(self) -> None:
        self.space.get_agents_as_GeoDataFrame(agent_cls=SchellingAgent).to_crs(
            "epsg:4326"
        ).to_file("data/schelling_agents.geojson", driver="GeoJSON")

    def step(self):
        """Run one step of the model.

        If All agents are happy, halt the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False

        if not self.running and self.export_data:
            self.export_agents_to_file()
