from epstein_civil_violence.model import EpsteinCivilViolenceRL
from epstein_civil_violence.server import run_model
from epstein_civil_violence.train_config import config
from train import train_model

# Load the environment
env = EpsteinCivilViolenceRL()
observation, info = env.reset(seed=42)
# Running the environment on some random actions
for _ in range(10):
    action_dict = {}
    for agent in env.schedule.agents:
        action_dict[agent.unique_id] = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action_dict)

    if terminated or truncated:
        observation, info = env.reset()

# Training a model
train_model(
    config, num_iterations=1, result_path="results.txt", checkpoint_dir="checkpoints"
)

# Running the model and visualizing it
server = run_model(path="checkpoints")
# You can also try running pre-trained checkpoints present in model folder
# server = run_model(path='model/epstein_civil_violence')
server.port = 6005
server.launch(open_browser=True)
