# Walking Behavior Agent-Based Model

This repository contains an agent-based model (ABM) that simulates walking behavior in a hypothetical city, examining how socioeconomic status (SES), built environment, and social factors influence walking patterns.

# Walking Behavior Simulation Model Documentation

## Overview

## Model Architecture (`model.py`)

### Initialization Parameters

- Grid dimensions (width and height)
- Number of workplaces (categorized into Grocery Stores, Social Places, etc.)
- Population composition (number of couples and singles)

### Simulation Scenarios

The model implements four distinct scenarios:

1. **RR (Random-Random)**: Random land use distribution with random safety values
2. **RS (Random-Safety)**: Random land use distribution with lower safety values in core areas
3. **CR (Centralized-Random)**: Centralized land use with random safety values
4. **CS (Centralized-Safety)**: Centralized land use with lower safety values in core areas

### Environmental Layers

1. **Safety Layer** (`safety_cell_layer`)

   - Values vary based on selected scenario
   - Impacts walking behavior and route choices

2. **Aesthetic Layer** (`aesthetic_cell_layer`)
   - Values decrease with distance from center
   - Reflects personal preferences in route selection

### Agent Placement

- Workplaces are distributed according to scenario parameters
- Households serve as spawn locations for human agents
- Agent placement correlates with Socioeconomic Status (SES) - lower SES values correspond to more central locations

### Data Collection

The model tracks the following metrics across five SES levels (1-5):

1. Average daily walking trips
2. Work-related trips
3. Basic needs trips (grocery and non-food shopping)
4. Leisure trips (non-purposeful neighborhood walks)

## Agent Implementation (`agents.py`)

### Human Class

Extends the CellAgent class with the following attributes:

#### Demographic Characteristics

- Gender: Equal probability of male/female
- Age: Random distribution (18-87 years)
- Family Size: 1 or 2 (based on `SINGLE_HOUSEHOLD_PROBABILITY`)
- Pet Ownership: 20% probability of dog ownership (increases leisure walking frequency)

#### Personal Attributes

- Walking Ability: Determined by `get_walking_ability` function
- Walking Attitude: Calculated via `get_walking_attitude` function
- Employment Status:
  - Automatic retirement above `RETIREMENT_AGE`
  - 95% employment probability for working-age population
- Social Network: Maintains lists of friends and family members

#### Behavioral Feedback System

Walking attitude is influenced by:

- Social network (family and friends' attitudes)
- Environmental factors (safety and aesthetics)
- Local pedestrian density
- Cumulative walking distance

### WalkingBehaviourModel Class

Manages walking behavior simulation with:

- Activity probability distributions
- Maximum distance thresholds
- Daily walk scheduling based on destination distances
- Activity and destination planning algorithms

### Workplace Classes

A hierarchy of workplace types:

1. **Base Workplace**: Abstract class for workplace definition
2. **GroceryStore**: Essential food retail
3. **NonFoodShop**: General retail
4. **SocialPlace**: Community gathering locations
5. **Other**: Miscellaneous workplace types

All workplace classes inherit from both `Workplace` and `FixedAgent` base classes.

## How to Run

To run a basic simulation:

```python

solara run app.py

```

# Files

- [city_walking_behaviour/model.py](city_walking_behaviour/model.py): Core model file.
- [city_walking_behaviour/agents.py](city_walking_behaviour/agents.py): The agent class.

## Further Reading

1. A Spatial Agent-Based Model for the Simulation of Adults’ Daily Walking Within a City [article](https://pmc.ncbi.nlm.nih.gov/articles/PMC3306662/)
