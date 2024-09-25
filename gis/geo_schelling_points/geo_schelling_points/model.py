import random
from pathlib import Path

import mesa
import mesa_geo as mg

from .agents import PersonAgent, RegionAgent
from .space import Nuts2Eu

script_directory = Path(__file__).resolve().parent


class GeoSchellingPoints(mesa.Model):
    def __init__(self, red_percentage=0.5, similarity_threshold=0.5):
        super().__init__()

        self.red_percentage = red_percentage
        PersonAgent.SIMILARITY_THRESHOLD = similarity_threshold

        self.schedule = mesa.time.RandomActivation(self)
        self.space = Nuts2Eu()

        self.datacollector = mesa.DataCollector(
            {"unhappy": "unhappy", "happy": "happy"}
        )

        # Set up the grid with patches for every NUTS region
        ac = mg.AgentCreator(RegionAgent, model=self)
        data_path = script_directory / "../data/nuts_rg_60M_2013_lvl_2.geojson"
        regions = ac.from_file(data_path, unique_id="NUTS_ID")
        self.space.add_regions(regions)

        for region in regions:
            for _ in range(region.init_num_people):
                person = PersonAgent(
                    model=self,
                    crs=self.space.crs,
                    geometry=region.random_point(),
                    is_red=random.random() < self.red_percentage,
                    region_id=region.unique_id,
                )
                self.space.add_person_to_region(person, region_id=region.unique_id)
                self.schedule.add(person)

        self.datacollector.collect(self)

    @property
    def unhappy(self):
        num_unhappy = 0
        for agent in self.space.agents:
            if isinstance(agent, PersonAgent) and agent.is_unhappy:
                num_unhappy += 1
        return num_unhappy

    @property
    def happy(self):
        return self.space.num_people - self.unhappy

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        if not self.unhappy:
            self.running = False
