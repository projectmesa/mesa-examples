"""
Mesa implementation of Virus/Antibody model: Agents module.
"""

import copy
import os
import sys
import weakref
from collections import deque

import numpy as np

sys.path.insert(0, os.path.abspath("../../mesa"))
from mesa.experimental.continuous_space import ContinuousSpaceAgent


class AntibodyAgent(ContinuousSpaceAgent):
    """An Antibody agent. They move randomly until they see a virus, go fight it.
    If they lose, stay KO for a bit, lose health and back to random moving.
    """

    def __init__(
        self,
        model,
        space,
        sight_range,
        duplication_rate,
        ko_timeout,
        memory_capacity,
        initial_position=(0, 0),
        direction=(1, 1),
    ):
        super().__init__(model=model, space=space)

        # Movement & state
        self.position = initial_position
        self.speed = 1.5
        self.direction = np.array(direction, dtype=float)

        # Characteristics
        self.sight_range = sight_range
        self.health = 2
        self.duplication_rate = duplication_rate

        # Memory
        self.st_memory: deque = deque()
        self.lt_memory: list = []
        self.memory_capacity = memory_capacity

        # Target & KO state
        self.target = None  # will hold a weakref.ref or None
        self.ko_timeout = ko_timeout
        self.ko_steps_left = 0

    def step(self):
        # Acquire a virus target if we don't already have one
        if self.target is None:
            closest = self.find_closest_virus()
            if closest:
                self.target = weakref.ref(closest)

        # Communicate and maybe duplicate
        self.communicate()
        if self.random.random() < self.duplication_rate:
            self.duplicate()

        # Then move
        self.move()

    def find_closest_virus(self):
        agents, _ = self.space.get_agents_in_radius(self.position, self.sight_range)
        viruses = [a for a in agents if isinstance(a, VirusAgent)]
        return viruses[0] if viruses else None

    def communicate(self) -> bool:
        agents, _ = self.space.get_agents_in_radius(self.position, self.sight_range)
        peers = [
            a
            for a in agents
            if isinstance(a, AntibodyAgent) and a.unique_id != self.unique_id
        ]
        if not peers:
            return False

        for other in peers:
            to_share = [
                dna for dna in self.st_memory if dna and dna not in other.lt_memory
            ]
            if to_share:
                other.st_memory.extend(to_share)
                other.lt_memory.extend(to_share)
                while len(other.st_memory) > self.memory_capacity:
                    other.st_memory.popleft()
        return True

    def duplicate(self):
        clone = AntibodyAgent(
            self.model,
            self.space,
            sight_range=self.sight_range,
            duplication_rate=self.duplication_rate,
            ko_timeout=self.ko_timeout,
            memory_capacity=self.memory_capacity,
            initial_position=self.position,
            direction=self.direction,
        )
        # Copy over memory
        clone.st_memory = deque(item for item in self.st_memory if item)
        clone.lt_memory = [item for item in self.lt_memory if item]
        clone.target = None
        clone.ko_steps_left = 0

        self.model.antibodies_set.add(clone)

    def move(self):
        # If we've been removed from the space, bail out
        if getattr(self, "space", None) is None:
            return

        # Dereference weakref if needed
        target = (
            self.target()
            if isinstance(self.target, weakref.ReferenceType)
            else self.target
        )

        new_pos = None

        # KO state: target refers back to self
        if target is self:
            self.ko_steps_left -= 1
            if self.ko_steps_left <= 0:
                self.target = None

        # Random walk if no target
        elif target is None:
            perturb = np.array(
                [
                    self.random.uniform(-0.5, 0.5),
                    self.random.uniform(-0.5, 0.5),
                ]
            )
            self.direction = self.direction + perturb
            norm = np.linalg.norm(self.direction)
            if norm > 0:
                self.direction /= norm
            new_pos = self.position + self.direction * self.speed

        # Chase a valid virus target
        else:
            if getattr(target, "space", None) is not None:
                vec = np.array(target.position) - np.array(self.position)
                dist = np.linalg.norm(vec)
                if dist > self.speed:
                    self.direction = vec / dist
                    new_pos = self.position + self.direction * self.speed
                else:
                    self.engage_virus(target)
            else:
                self.target = None

        if new_pos is not None:
            self.position = new_pos

    def engage_virus(self, virus) -> str:
        # If it's already gone
        if virus not in self.model.agents:
            self.target = None
            return "no_target"

        dna = copy.deepcopy(virus.dna)
        if dna in self.st_memory or dna in self.lt_memory:
            virus.remove()
            self.target = None
            return "win"
        else:
            # KO (or death)
            self.health -= 1
            if self.health <= 0:
                self.remove()
                return "dead"

            self.st_memory.append(dna)
            self.lt_memory.append(dna)
            self.ko_steps_left = self.ko_timeout
            # mark KO state by weak-ref back to self
            self.target = weakref.ref(self)
            return "ko"


class VirusAgent(ContinuousSpaceAgent):
    """A virus agent: random movement, mutation, duplication, passive to antibodies."""

    def __init__(
        self,
        model,
        space,
        mutation_rate,
        duplication_rate,
        position=(0, 0),
        dna=None,
    ):
        super().__init__(model=model, space=space)

        self.position = position
        self.mutation_rate = mutation_rate
        self.duplication_rate = duplication_rate
        self.speed = 1
        self.direction = np.array((1, 1), dtype=float)
        self.dna = dna if dna is not None else self.generate_dna()

    def step(self):
        # If already removed from the space, don't do anything
        if getattr(self, "space", None) is None:
            return
        if self.random.random() < self.duplication_rate:
            self.duplicate()
        self.move()

    def duplicate(self):
        clone = VirusAgent(
            self.model,
            self.space,
            mutation_rate=self.mutation_rate,
            duplication_rate=self.duplication_rate,
            position=self.position,
            dna=self.generate_dna(self.dna),
        )
        self.model.viruses_set.add(clone)

    def generate_dna(self, dna=None):
        if dna is None:
            return [self.random.randint(0, 9) for _ in range(3)]
        idx = self.random.randint(0, 2)
        chance = self.random.random()
        if chance < self.mutation_rate / 2:
            dna[idx] = (dna[idx] + 1) % 10
        elif chance < self.mutation_rate:
            dna[idx] = (dna[idx] - 1) % 10
        return dna

    def move(self):
        if getattr(self, "space", None) is None:
            return

        # Random walk
        perturb = np.array(
            [
                self.random.uniform(-0.5, 0.5),
                self.random.uniform(-0.5, 0.5),
            ]
        )
        self.direction = self.direction + perturb
        norm = np.linalg.norm(self.direction)
        if norm > 0:
            self.direction /= norm

        # Step
        self.position = self.position + self.direction * self.speed
