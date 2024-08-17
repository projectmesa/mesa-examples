

# GIS-Based Traffic Simulation with Mesa
![bangalore_traffic_congestion](https://github.com/user-attachments/assets/861218c2-3bc0-4f74-a2a7-41eb892a9e61)


## Overview

This project simulates urban traffic congestion using the Mesa agent-based modeling framework and OSMnx for extracting road network data from OpenStreetMap. It visualizes traffic patterns and congestion in a critical urban area in Bangalore, India. The simulation includes different vehicle types and their movement on the road network, and the results are animated into a GIF to showcase the traffic dynamics over time.

## Why We Need This

### Problem Definition

High vehicle density and complex road networks are significant contributors to traffic congestion in Indian cities, especially in densely populated urban areas. This issue affects millions of travelers, leading to:

- Increased travel duration
- Higher fuel consumption
- Elevated pollution levels

In cities like Bangalore, also known as the Tech Hub or Silicon Valley of India, these problems are exacerbated by rapid urbanization and technological growth.

### Objective

By developing and refining this traffic simulation project, we aim to deliver more effective and adaptable solutions for managing traffic congestion in Indian cities. The project has the potential to:

- Improve traffic flow and reduce congestion
- Decrease travel time and fuel consumption
- Lower pollution levels
- Enhance the overall quality of life for urban residents

## Features

- **Urban Traffic Simulation**: Models traffic flow using various vehicle types (cars, trucks, bikes).
- **OSMnx Integration**: Utilizes OSMnx to extract and visualize road networks from OpenStreetMap.
- **Animated Visualization**: Generates an animated GIF showing traffic patterns and vehicle movements.
- **Dynamic Visualization**: Updates the visualization in real-time to reflect vehicle positions on the map.

## Requirements

- **Python 3.11**
- **OSMnx**: `pip install osmnx`
- **NetworkX**: `pip install networkx`
- **Folium**: `pip install folium`
- **Mesa**: `pip install mesa`
- **PIL**: `pip install pillow`



1. **Update Bounding Box Coordinates**

   Modify the `north`, `south`, `east`, and `west` variables in the script to reflect the area you want to simulate.

2. **Run the Simulation**

   Execute the script to run the traffic simulation and generate the animated GIF:



3. **View the Results**

   The resulting animated GIF will be saved in the `Data` directory. You can view it directly from your file explorer or display it within a Jupyter Notebook using:



## Code Overview

- **TrafficGeoSpace**: Defines the space in which the agents move, based on the road network graph.
- **VehicleAgent**: Represents individual vehicles, including their routes and movement.
- **TrafficModel**: Manages the simulation, creating vehicles and stepping through the simulation.
- **Visualization**: Uses Folium to create maps and convert HTML maps to PNG images, which are then compiled into an animated GIF.

## Future Work

The project can be extended to address the following aspects:

- **Advanced Traffic Management**: Incorporate real-time traffic data and predictive analytics for dynamic traffic management.
- **Integration with Smart City Solutions**: Connect with IoT sensors and smart traffic lights for a more integrated approach.
- **Scenario Testing**: Simulate various scenarios such as road closures, construction, or major events to evaluate their impact on traffic.

## Acknowledgments

- **OSMnx**: For providing easy access to OpenStreetMap data.
- **Mesa**: For the agent-based modeling framework.
- **Folium**: For interactive map visualizations.
