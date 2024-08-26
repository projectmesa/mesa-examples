# Tutorial: Reinforcement Learning with Mesa Environments

Welcome to this comprehensive guide on integrating reinforcement learning (RL) with Mesa environments. Mesa, an agent-based modeling framework, offers an excellent platform to experiment with RL algorithms. In this tutorial, we'll explore several examples of how RL can be applied to various Mesa environments, starting with the **Epstein Civil Violence model**.

### Getting Started

Before diving into the implementation, take a moment to familiarize yourself with the [Epstein Civil Violence model](./epstein_civil_violence/README.md). This will give you a solid understanding of the environment we’ll be working with.

Next, ensure all dependencies are installed by following the instructions in the `README.md`.

### Step 1: Importing the Necessary Modules

To begin, let’s import the required modules for the Epstein Civil Violence model:

```python
from epstein_civil_violence.model import EPSTEINCIVILVIOLENCE_RL
from epstein_civil_violence.server import run_model
from epstein_civil_violence.train import config
from train import train_model
```

Here’s a breakdown of the modules:

- `EPSTEINCIVILVIOLENCE_RL`: Contains the core model and environment.
- `run_model`: Configures and runs the model for inference.
- `config`: Defines the parameters for training the model.
- `train_model`: Includes functions for training the RL agent using RLlib.

### Step 2: Initializing the Environment

Let's load and reset the environment. This also allows us to inspect the observation space:

```python
env = EPSTEINCIVILVIOLENCE_RL()
observation, info = env.reset(seed=42)
```

### Step 3: Running the Environment with Random Actions

To get a feel for how the environment operates, let's run it for a few steps using random actions. We’ll sample the action space for these actions:

```python
for _ in range(10):
    action_dict = {}
    for agent in env.schedule.agents:
        action_dict[agent.unique_id] = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action_dict)

    if terminated or truncated:
        observation, info = env.reset()
```

### Step 4: Training the Model

Now that you're familiar with the environment, let's train the RL model using the preset configuration:

```python
train_model(config, num_iterations=1, result_path='results.txt', checkpoint_dir='checkpoints')
```

Feel free to modify the training parameters in the `train_config.py` file to experiment with different outcomes.

### Step 5: Visualizing the Results

After training, you can visualize the results by running inference on the model. Mesa's built-in visualization tools will help you launch a webpage to view the model's performance:

```python
server = run_model(path='checkpoints')
server.port = 6005
server.launch(open_browser=True)
```


### Alternative Approach: Using Stable-Baselines with Mesa
In the example above, we utilized RLlib to integrate reinforcement learning algorithms with the Mesa environment, which is particularly useful when you want different policies for different agents. However, if your use case requires a simpler setup where all agents follow the same policy, you can opt for Stable-Baselines. An example of integrating Stable-Baselines with Mesa can be found in the Boltzmann Money model.

### Implementing Your own cases
If you're ready to explore RL in different agent-based scenarios, you can start by experimenting with various examples we provide at [Mesa-Examples](https://github.com/projectmesa/mesa-examples). These examples cover a range of scenarios and offer a great starting point for understanding how to apply RL within Mesa environments.

If you have your own scenario in mind, you can create it as a Mesa model by following this series of [Tutorials](https://mesa.readthedocs.io/en/stable/tutorials/intro_tutorial.html). Once your scenario is set up as a Mesa model, you can refer to the code in the provided implementations to see how the RL components are built on top of the respective Mesa models.