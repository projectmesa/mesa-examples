# Reinforcement Learning Implementations with Mesa

This repository demonstrates various applications of reinforcement learning (RL) using the Mesa agent-based modeling framework. These implementations were developed as part of my Google Summer of Code 2024 (GSoC'24) project under Project Mesa.

<p align="center">
<img src="wolf_sheep/resources/wolf_sheep.gif" width="500" height="400">
</p>

## Getting Started

### Installation

*Given the number of dependencies required, we recommend starting by creating a Conda environment or a Python virtual environment.*
1. **Install Mesa Models**  
   Begin by installing the Mesa models:

   ```bash
   pip install -U -e git+https://github.com/projectmesa/mesa-examples@mesa-2.x#egg=mesa-models
   ```

2. **Install RLlib for Multi-Agent Training**  
   Next, install RLlib along with TensorFlow and PyTorch to support multi-agent training algorithms:

   ```bash
   pip install "ray[rllib]" tensorflow torch
   ```

3. **Install Additional Dependencies**  
   Finally, install any remaining dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Examples

To test the code, simply execute `example.py`:

```bash
python example.py
```

*Note: Pre-trained models might not work in some cases because of different library versions. In such cases, you can train your own model and use it.*

To learn about individual implementations, please refer to the README files of specific environments.


## Tutorials

For detailed tutorials on how to use these implementations and guidance on starting your own projects, please refer to [Tutorials.md](./Tutorials.md).

Here's a refined version of your contribution guide:


## Contribution Guide

We welcome contributions to our project! A great way to get started is by implementing the remaining examples listed in the [Mesa-Examples](https://github.com/projectmesa/mesa-examples) repository with reinforcement learning (RL). 

Additionally, if you have your own Mesa environments that you think would benefit from RL integration, we encourage you to share them with us. Simply start an issue on our GitHub repository with your suggestion, and we can collaborate on bringing it to life!

Your contributions are invaluable in enhancing the project and helping us build a robust library of RL-integrated Mesa environments. 
