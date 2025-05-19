from pathlib import Path

import mesa
from cacheablemodel import CacheableSchelling
from server import canvas_element, get_happy_agents, happy_chart, model_params

# As 'replay' is a simulation model parameter in this example, we need to make it available as such
model_params["replay"] = mesa.visualization.Checkbox("Replay cached run?", False)
model_params["cache_file_path"] = "./my_cache_file_path.cache"


def get_cache_file_status(_):
    """Display an informational text about caching and the status of the cache file (existing versus not existing)"""
    cache_file = Path(model_params["cache_file_path"])
    return (
        f"Only activate the 'Replay cached run?' switch when a cache file already exists, otherwise it will fail. "
        f"Cache file existing: '{cache_file.exists()}'."
    )


server = mesa.visualization.ModularServer(
    model_cls=CacheableSchelling,  # Note that Schelling was replaced by CacheableSchelling here
    visualization_elements=[
        get_cache_file_status,
        canvas_element,
        get_happy_agents,
        happy_chart,
    ],
    name="Schelling Segregation Model",
    model_params=model_params,
)

server.launch()
