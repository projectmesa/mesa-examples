from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.logger import pretty_print


# Custom function to get the configuration
def get_config(custom_config):
    config = (
        PPOConfig()
        .environment(custom_config["env_name"])
        .framework(custom_config["framework"])
        .training(train_batch_size=custom_config["train_batch_size"])
        .multi_agent(
            policies=custom_config["policies"],
            policy_mapping_fn=custom_config["policy_mapping_fn"],
            policies_to_train=custom_config["policies_to_train"],
        )
        .resources(num_gpus=custom_config["num_gpus"])
        .learners(num_learners=custom_config["num_learners"])
        .env_runners(
            num_env_runners=custom_config["num_env_runners"],
            num_envs_per_env_runner=custom_config["num_envs_per_env_runner"],
            batch_mode=custom_config["batch_mode"],
            rollout_fragment_length=custom_config["rollout_fragment_length"],
        )
    )
    return config


# Training the model
def train_model(
    config, num_iterations=5, result_path="results.txt", checkpoint_dir="checkpoints"
):
    tune.register_env(config["env_name"], config["env_creator"])

    algo_config = get_config(config)
    algo = algo_config.build()

    for _ in range(num_iterations):
        result = algo.train()
        print(pretty_print(result))

    with open(result_path, "w") as file:
        file.write(pretty_print(result))

    checkpoint_dir = algo.save(checkpoint_dir).checkpoint.path
    print(f"Checkpoint saved in directory {checkpoint_dir}")
