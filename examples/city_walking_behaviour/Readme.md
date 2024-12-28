# Walking Behavior Agent-Based Model

## Introduction

This agent-based model (ABM) simulates walking behavior patterns in a hypothetical city. It examines how socioeconomic status (SES), built environment, and social factors influence walking patterns by modeling dynamic interactions between individual attributes and environmental factors. The model incorporates feedback mechanisms and individual-environment interactions to simulate realistic walking patterns across different socioeconomic groups.

## Model Architecture

### Core Components

#### Initialization Parameters

- Grid dimensions (width and height)
- Workplace distribution (Grocery Stores, Social Places, etc.)
- Population demographics (couples and singles)

#### Simulation Scenarios

1. **RR (Random-Random)**

   - Random land use distribution
   - Random safety values

2. **RS (Random-Safety)**

   - Random land use distribution
   - Lower safety values in core areas

3. **CR (Centralized-Random)**

   - Centralized land use
   - Random safety values

4. **CS (Centralized-Safety)**
   - Centralized land use
   - Lower safety values in core areas

### Environmental Systems

#### Environmental Layers

1. **Safety Layer** (`safety_cell_layer`)

   - Dynamic values based on scenario
   - Influences walking behavior and route selection

2. **Aesthetic Layer** (`aesthetic_cell_layer`)
   - Center-based value distribution
   - Impacts route preferences

#### Agent Placement System

- Scenario-based workplace distribution
- Household-based agent spawning
- SES-correlated positioning (lower SES centrally located)

### Data Collection System

Tracks metrics across five SES levels (1-5):

- Average daily walking trips
- Work-related trips
- Basic needs trips (grocery and retail)
- Leisure walks

## Agent Implementation

### Human Agent Characteristics

#### Demographics

- Gender (50/50 distribution)
- Age (18-87 years, random distribution)
- Family Size (1-2 members)
- Pet Ownership (20% dog ownership rate)

#### Personal Attributes

- Walking Ability
- Walking Attitude
- Employment Status
- Social Networks

#### Behavioral Feedback Mechanisms

Walking attitudes influenced by:

- Social network dynamics
- Environmental conditions
- Pedestrian density
- Walking history

### Walking Behavior Model

- Activity probability modeling
- Distance threshold management
- Schedule optimization
- Destination planning

### Workplace Hierarchy

1. Base Workplace (Abstract)
2. GroceryStore
3. NonFoodShop
4. SocialPlace
5. Other

## Usage

### Running the Simulation

```python
solara run app.py
```

## Project Structure

- `city_walking_behaviour/model.py`: Core simulation engine
- `city_walking_behaviour/agents.py`: Agent class definitions

## References

1. [A Spatial Agent-Based Model for the Simulation of Adults' Daily Walking Within a City](https://pmc.ncbi.nlm.nih.gov/articles/PMC3306662/)
