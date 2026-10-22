from hex_snowflake.model import HexSnowflake
from mesa.visualization import SolaraViz, make_space_component


def agent_portrayal(agent):
    """Portrayal for the Cell agents: black when alive, white when dead."""
    return {"color": "black" if agent.is_alive else "white"}


model = HexSnowflake()

page = SolaraViz(
    model,
    components=[make_space_component(agent_portrayal=agent_portrayal)],
    name="Hex Snowflake",
)
