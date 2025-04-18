"""
Virus/Antibody Model
===================
A mesa implementation of the Virus/Antibody model, where antibodies and viruses interact in a continuous space.
"""

import os
import sys

sys.path.insert(0, os.path.abspath("../../mesa"))

import numpy as np
from agents import AntibodyAgent, VirusAgent
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.experimental.continuous_space import ContinuousSpace


class VirusAntibodyModel(Model):
    """
    Virus/Antibody model.

    Handles agent creation, placement and scheduling.
    """

    def __init__(
        # General parameters
        self,
        seed=None,
        initial_antibody=20,
        initial_viruses=20,
        width=100,
        height=100,
        # Antibody parameters
        antibody_duplication_rate=0.01,
        antibody_sight_range=10,
        antibody_ko_timeout=15,
        antibody_memory_capacity=3,
        # Virus parameters
        virus_duplication_rate=0.01,
        virus_mutation_rate=0.01,
    ):
        """Create a new Virus/Antibody  model.

        Args:
            seed: Random seed for reproducibility
            initial_antibody: Number of Antibodies in the simulation
            initial_viruses: Number of viruses in the simulation
            width: Width of the space
            height: Height of the space
            antibody_duplication_rate: Probability of duplication for antibodies
            virus_duplication_rate: Probability of duplication for viruses
            virus_mutation_rate: Probability of mutation for viruses

        Indirect Args (not chosen in the graphic interface for clarity reasons):
            antibody_memory_capacity: Number of virus DNA an antibody can remember
            antibody_sight_range: Radius within which antibodies can detect viruses
            antibody_ko_timeout : Number of step after which an antibody can move after a KO

        """

        super().__init__(seed=seed)

        # Model parameters
        self.initial_antibody = initial_antibody
        self.initial_viruses = initial_viruses
        self.width = width
        self.height = height

        # antibody parameters
        self.antibody_duplication_rate = antibody_duplication_rate
        self.antibody_sight_range = antibody_sight_range
        self.antibody_ko_timeout = antibody_ko_timeout
        self.antibody_memory_capacity = antibody_memory_capacity

        # virus parameters
        self.virus_duplication_rate = virus_duplication_rate
        self.virus_mutation_rate = virus_mutation_rate

        # Statistics
        self.antibodies_killed = 0
        self.virus_killed = 0
        self.running = True

        # Set up data collection
        model_reporters = {
            "Antibodies": lambda m: len(m.agents_by_type[AntibodyAgent]),
            "Viruses": lambda m: len(m.agents_by_type[VirusAgent]),
        }

        self.datacollector = DataCollector(model_reporters=model_reporters)

        # Set up the space
        self.space = ContinuousSpace(
            [[0, width], [0, height]],
            torus=True,  # change to false and make checks (currently fails)
            random=self.random,
            # n_agents=initial_antibody + initial_viruses,
        )

        # Create and place the Antibody agents
        antibodies_positions = self.rng.random(
            size=(self.initial_antibody, 2)
        ) * np.array(self.space.size)
        directions = self.rng.uniform(-1, 1, size=(self.initial_antibody, 2))
        self.antibodies_set = AntibodyAgent.create_agents(
            self,
            self.initial_antibody,
            self.space,
            initial_position=antibodies_positions,
            direction=directions,
            sight_range=self.antibody_sight_range,
            duplication_rate=self.antibody_duplication_rate,
            ko_timeout=self.antibody_ko_timeout,
            memory_capacity=self.antibody_memory_capacity,
        )

        # Create and place the Virus agents
        dna = [self.random.randint(0, 9) for _ in range(3)]
        viruses_positions = self.rng.random(size=(self.initial_viruses, 2)) * np.array(
            self.space.size
        )
        directions = self.rng.uniform(-1, 1, size=(self.initial_viruses, 2))

        self.viruses_set = VirusAgent.create_agents(
            self,
            self.initial_viruses,
            self.space,
            position=viruses_positions,
            duplication_rate=self.virus_duplication_rate,
            mutation_rate=self.virus_mutation_rate,
            dna=dna,
        )

        self.datacollector.collect(self)

    def step(self):
        """Run one step of the model."""
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

        if (
            len(self.agents_by_type[AntibodyAgent]) > 200
            or len(self.agents_by_type[VirusAgent]) > 200
        ):
            print("Too many agents, stopping the simulation")
            self.running = False
        elif len(self.agents_by_type[AntibodyAgent]) == 0:
            self.running = False
            print("All antibodies are dead")
        elif len(self.agents_by_type[VirusAgent]) == 0:
            self.running = False
            print("All viruses are dead")
