from mesa.visualization.modules import ChartModule


# This function defines how agents are visually represented in the simulation.
def agent_portrayal(agent):
    # Basic portrayal with agents shown as circles.
    portrayal = {
        "Shape": "circle",  # The shape of the agent in the visualization.
        "r": 0.8,  # Radius of the circle, determining the size of the agent.
        "Filled": "true",  # Specifies that the shape should be filled.
        "Layer": 0,  # The layer on which the agent is drawn.
        # Lower numbers are drawn first.
    }

    # Check if the agent has a 'price' attribute.
    # This is to ensure compatibility
    # with different types of agents.
    if hasattr(agent, "price"):
        # The color of the agent is determined by its price to visualize
        # the pricing strategy dynamically.
        if agent.price > 12:
            portrayal[
                "Color"
            ] = "#FF0000"  # Agents with a price above 12 are colored red,
            # indicating higher prices.
        elif agent.price > 8:
            portrayal["Color"] = "#FFFF00"  # Agents with a price above 8 and
            # up to 12 are colored yellow,indicating moderate prices.
        else:
            portrayal["Color"] = "#00FF00"  # Agents with a price of 8 or below
            # are colored green,indicating lower prices.

    return portrayal  # Return the portrayal dictionary to be used by
    # the visualization engine.


# Define a chart to visualize the average price of agents
# over time in the simulation.
average_price_chart = ChartModule(  # The data series label and color.
    [{"Label": "Average Price", "Color": "Black"}],
    data_collector_name="datacollector",  # The name of the DataCollector
    # object from which to retrieve the data.
)

# Similarly, define a chart to visualize the total revenue over time.
total_revenue_chart = ChartModule(
    [
        {"Label": "Total Revenue", "Color": "Blue"}
    ],  # The data series label and color for total revenue.
    data_collector_name="datacollector",  # Again, specifying the
    # DataCollector object to use.
)
