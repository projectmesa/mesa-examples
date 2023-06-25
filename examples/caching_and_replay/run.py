from pathlib import Path

import mesa
from cacheablemodel import CacheableSchelling
from server import canvas_element, get_happy_agents, happy_chart, model_params

# As 'replay' is a simulation model parameter in this example, we need to make it available as such
model_params["replay"] = mesa.visualization.Checkbox("Replay cached run?", False)


def get_cache_file_status(_):
    """
    Display an informational text about caching and the status of the cache file (existing versus not existing)
    """
    cache_file = Path("./my_cache_file_path.cache")
    return (
        f"Only activate the 'Replay cached run?' switch when a cache file already exists, otherwise it will fail. "
        f"Cache file existing: '{cache_file.exists()}'."
    )


server = mesa.visualization.ModularServer(
    # Note that Schelling was replaced by CacheableSchelling here
    CacheableSchelling,
    [get_cache_file_status, canvas_element, get_happy_agents, happy_chart],
    "Schelling",
    model_params,
)

server.launch()
