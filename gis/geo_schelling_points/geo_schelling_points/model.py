import random
from pathlib import Path

import geopandas as gpd
import libpysal
import mesa
import mesa_geo as mg

from .agents import PersonAgent, RegionAgent
from .space import Nuts2Eu

script_directory = Path(__file__).resolve().parent


def get_largest_connected_components(gdf):
    """Get the largest connected component of a GeoDataFrame."""
    # create spatial weights matrix
    W = libpysal.weights.Queen.from_dataframe(
        gdf, use_index=True, silence_warnings=True
    )
    # get component labels
    gdf["component"] = W.component_labels
    # get the largest component
    largest_component = gdf["component"].value_counts().idxmax()
    # subset the GeoDataFrame
    gdf = gdf[gdf["component"] == largest_component]
    return gdf


class GeoSchellingPoints(mesa.Model):
    def __init__(self, red_percentage=0.5, similarity_threshold=0.5):
        super().__init__()

        self.red_percentage = red_percentage
        PersonAgent.SIMILARITY_THRESHOLD = similarity_threshold

        self.space = Nuts2Eu()

        self.datacollector = mesa.DataCollector(
            {"unhappy": "unhappy", "happy": "happy"}
        )

        # Set up the grid with patches for every NUTS region
        ac = mg.AgentCreator(RegionAgent, model=self)
        data_path = script_directory / "../data/nuts_rg_60M_2013_lvl_2.geojson"
        regions_gdf = gpd.read_file(data_path)
        regions_gdf = get_largest_connected_components(regions_gdf)
        regions = ac.from_GeoDataFrame(regions_gdf)
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
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

        if not self.unhappy:
            self.running = False
