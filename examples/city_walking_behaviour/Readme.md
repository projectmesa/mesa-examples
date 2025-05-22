# Walking Behavior Agent-Based Model

An agent-based model (ABM) that simulates how people walk in cities based on socioeconomic status, environment, and social factors.

## What This Model Shows

This simulation demonstrates how different city layouts and social factors affect walking patterns. Key insights include:

- How safety perceptions influence route choices
- Impact of socioeconomic status on walking frequency
- Effects of centralized vs distributed city planning
- Relationship between social networks and walking behavior

## Features

- Four simulation scenarios:

  - Random layout with random safety (RR)
  - Random layout with core safety gradient (RS)
  - Centralized layout with random safety (CR)
  - Centralized layout with core safety gradient (CS)

- Agent behaviors include:
  - Work commutes
  - Shopping trips
  - Social visits
  - Leisure walks

## Outcomes in different scenarios

#### RR
![image](https://github.com/user-attachments/assets/fddda37d-d0d5-40f7-9e6d-89fa9b37898a)

#### RS
![image](https://github.com/user-attachments/assets/67112dbb-056d-4bd5-b668-a1bb389c262d)

#### CR
![image](https://github.com/user-attachments/assets/aee37477-7693-46a8-848e-5a5986db0e95)

#### CS
![image](https://github.com/user-attachments/assets/f9e58239-19a2-4fa4-bbea-2b7ccbe36c8f)

## Quick Start

1. Run the simulation:

```python
solara run app.py
```

## Technical Details

### Model Architecture (`model.py`)

#### Initialization Parameters

- Grid dimensions (width and height)
- Number of workplaces (categorized into Grocery Stores, Social Places, etc.)
- Population composition (number of couples and singles)

#### Environmental Layers

1. **Safety Layer** (`safety_cell_layer`)

   - Values vary based on selected scenario
   - Impacts walking behavior and route choices

2. **Aesthetic Layer** (`aesthetic_cell_layer`)
   - Values decrease with distance from center
   - Reflects personal preferences in route selection

### Agent Implementation (`agents.py`)

#### Human Class Attributes

- **Demographics**: Gender, Age (18-87), Family Size (1-2), Pet Ownership (20% probability)
- **Personal**: Walking Ability, Walking Attitude, Employment Status
- **Social**: Network of friends and family members

#### Behavioral System

Walking attitude influenced by:

- Social network (family and friends' attitudes)
- Environmental factors (safety and aesthetics)
- Local pedestrian density
- Cumulative walking distance

### Data Collection

Tracks metrics across five SES levels (1-5):

1. Average daily walking trips
2. Work-related trips
3. Basic needs trips
4. Leisure trips

## File Structure

- `city_walking_behaviour/model.py`: Core simulation engine
- `city_walking_behaviour/agents.py`: Agent behavior definitions

## Based On

This model extends research from ["A Spatial Agent-Based Model for the Simulation of Adults' Daily Walking Within a City"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3306662/)
