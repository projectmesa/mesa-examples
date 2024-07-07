### README.md

# GIS-Based Traffic Simulation with Mesa-Geo

![alt text](Road_traffic_congestion-1.gif) ![alt text](<Screenshot 2024-07-07 at 12.40.38 AM.png>)

## Overview

This project is a GIS-based traffic simulation platform developed using the Mesa-Geo extension for Mesa. The application models and visualizes vehicle movements on a road network, providing insights into traffic patterns and enabling the analysis of traffic management strategies. This simulation tool is valuable for urban planners, researchers, and policymakers in understanding and optimizing traffic flow in cities.




## Why GIS-Based Traffic Simulation?

Traffic congestion is a significant issue in urban areas, leading to increased travel times, higher fuel consumption, and elevated pollution levels. By simulating traffic congestion, urban planners, researchers, and policymakers can:

- **Identify Congestion Points:** Pinpoint critical areas prone to traffic jams.
- **Analyze Traffic Patterns:** Understand how vehicles move through the city.
- **Evaluate Traffic Management Strategies:** Test the effectiveness of different traffic management strategies.
- **Optimize Traffic Flow:** Improve the overall efficiency of the road network.

## Features

- **Realistic Road Networks:** Uses OSMnx to import real road networks.
- **Dynamic Traffic Simulation:** Simulates vehicle movements and congestion points dynamically.
- **Interactive Visualization:** Provides an interactive map for visualizing the simulation in real-time.
- **Customizable Parameters:** Allows users to input specific parameters, such as the number of vehicles and their routes.

## Installation

### Prerequisites

- Python 3.x
- Mesa
- Mesa-Geo
- OSMnx
- NetworkX
- mesa visualization
- shapely.geometry
- open streets


## Usage

1. **Enter Simulation Parameters:** Specify the number of vehicles, start coordinates, and end coordinates.
2. **Run Simulation:** Start the simulation to see how traffic flows and where congestion occurs.
3. **View Results:** Analyze the simulation results using the interactive map and graphical outputs.

## How It Works

1. **Import Road Network:** Uses OSMnx to import a road network from OpenStreetMap based on bounding box coordinates.
2. **Initialize Simulation:** Sets up the simulation environment using Mesa and Mesa-Geo.
3. **Simulate Traffic Flow:** Vehicles move through the network following the shortest paths calculated by NetworkX.
4. **Visualize Results:** Uses mesa own visuvalization Tornado visualize the road network and vehicle movements on an interactive map.



## Future Enhancements

- **Dynamic Traffic Data:** Incorporate real-time traffic data for more accurate simulations.
- **Advanced Visualization:** Enhance the visualization with heatmaps and traffic density graphs.
- **Interactive Controls:** Add more interactive controls for users to adjust simulation parameters on the fly.
- **Extended Simulation Scenarios:** Support more complex scenarios like traffic incidents, road closures, and traffic light effects.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, please open an issue to discuss what you would like to change.

## License

This project is licensed under the MIT License.