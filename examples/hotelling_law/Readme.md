# Hotelling's Law Mesa Simulation

## Overview

This project is an agent-based model implemented using the Mesa framework in Python. It simulates market dynamics based on Hotelling's Law, exploring the behavior of stores in a competitive market environment. Stores adjust their prices and locations to maximize revenue, providing insights into the effects of competition and customer behavior on market outcomes.

## Hotelling's Law

Hotelling's Law is an economic theory that predicts competitors in a market will end up in a state of minimum differentiation, often referred to as the "principle of minimum differentiation" or "Hotelling's linear city model". This model explores how businesses choose their location in relation to competitors and how this affects pricing and consumer choice.

## Installation

To run this simulation, you will need Python 3.x and the following Python libraries:

- Mesa
- Pandas
- Matplotlib
- Numpy

You can install all required libraries by running:

```bash
pip install -r requirements.txt 
```

## Project Structure

```plaintext
hotelling-law-mesa/
├── analysis/
│   └── analyze_simulation.py
├── agents/
│   └── agents.py
├── models/
│   └── model.py
├── server/
│   └── server.py
├── visualization/
│   └── visualization.py
├── requirements.txt
└── run.py
```

## Running the Simulation

To start the simulation, navigate to the project directory and execute the following command:

```bash
python run.py
```


