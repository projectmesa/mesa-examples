import os

import mesa

from server import (
    canvas_element,
    get_happy_agents,
    happy_chart,
    model_params,
)
from cacheablemodel import CacheableSchelling

# As 'replay' is a simulation model parameter in this example, we need to make it available as such
model_params["replay"] = mesa.visualization.Checkbox("Replay cached run?", False)


def get_cache_file_status(_):
    """
    Display an informational text about caching and the status of the cache file (existing versus not existing)
    """
    return (
        f"This example writes every simulation run into a cache file. Cached runs can be replayed later. "
        f"Activate the 'Replay cached run?' toggle to replay the latest cached run. "
        f"Only activate the replay when a cache file already exists, otherwise it will fail. Cache file existing: "
        f"'{os.path.exists('my_cache_file_path.cache')}'."
    )


server = mesa.visualization.ModularServer(
    # Note that Schelling was replaced by CacheableSchelling here
    CacheableSchelling,
    [get_cache_file_status, canvas_element, get_happy_agents, happy_chart],
    "Schelling",
    model_params,
)

server.launch()
