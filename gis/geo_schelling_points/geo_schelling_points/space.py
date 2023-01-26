import random
from typing import Dict

import mesa_geo as mg

from .agents import RegionAgent


class Nuts2Eu(mg.GeoSpace):
    _id_region_map: Dict[str, RegionAgent]
    num_people: int

    def __init__(self):
        super().__init__(warn_crs_conversion=False)
        self._id_region_map = {}
        self.num_people = 0

    def add_regions(self, agents):
        super().add_agents(agents)
        total_area = 0
        for agent in agents:
            self._id_region_map[agent.unique_id] = agent
            total_area += agent.SHAPE_AREA
        for _, agent in self._id_region_map.items():
            agent.SHAPE_AREA = agent.SHAPE_AREA / total_area * 100.0

    def add_person_to_region(self, person, region_id):
        person.region_id = region_id
        person.geometry = self._id_region_map[region_id].random_point()
        self._id_region_map[region_id].add_person(person)
        super().add_agents(person)
        self.num_people += 1

    def remove_person_from_region(self, person):
        self._id_region_map[person.region_id].remove_person(person)
        person.region_id = None
        super().remove_agent(person)
        self.num_people -= 1

    def get_random_region_id(self) -> str:
        return random.choice(list(self._id_region_map.keys()))

    def get_region_by_id(self, region_id) -> RegionAgent:
        return self._id_region_map.get(region_id)
