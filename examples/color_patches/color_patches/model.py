from collections import Counter
from random import random

import mesa


class ColorCell(mesa.Agent):
    """
    Represents a cell's opinion (visualized by a color)
    """

    # test
    OPINIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def __init__(self, unique_id, model, initial_state, mutation_prob=0.1):
        """
        Create a cell with the given opinion state.
        """
        super().__init__(unique_id, model)
        self.state = initial_state
        self.next_state = None
        self.mutation_prob = mutation_prob

    def determine_opinion(self):
        """
        Determines the agent's opinion for the next step by polling its neighbors.
        The opinion is determined by the majority of the 8 neighbors' opinions.
        A choice is made at random in case of a tie.
        The next state is stored until all cells have been polled.
        """
        if random() < 0.5:
            self.next_state = self.state
            return

        if random() < self.mutation_prob:
            # Зміна кольору на випадковий незалежно від сусідів
            self.next_state = self.random.choice(ColorCell.OPINIONS)
        else:
            # Стандартний процес визначення "думки" на основі сусідів
            neighbors = self.model.grid.get_neighbors(
                self.pos, moore=True, include_center=False
            )
            neighbors_opinion = Counter(neighbor.state for neighbor in neighbors)
            polled_opinions = neighbors_opinion.most_common()

            # Збираємо всі зв'язані думки (якщо є кілька з однаковою частотою)
            tied_opinions = [
                opinion[0]
                for opinion in polled_opinions
                if opinion[1] == polled_opinions[0][1]
            ]
            self.next_state = self.random.choice(tied_opinions)

    def assume_opinion(self):
        """
        Set the state of the agent to the next state.
        """
        self.state = self.next_state


class ColorPatches(mesa.Model):
    """
    Represents a 2D lattice where agents live.
    """

    def __init__(self, width=20, height=20):
        """
        Create a 2D lattice with strict borders where agents live.
        The agents' next state is determined first, and then the grid is updated.
        """
        super().__init__()
        self.width = width
        self.height = height
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)

        # Create agents
        for content, x, y in self.grid.coord_iter():
            initial_state = ColorCell.OPINIONS[
                self.random.randrange(0, len(ColorCell.OPINIONS))
            ]
            agent = ColorCell(self.next_id(), self, initial_state, mutation_prob=0.01)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

        self.running = True

    def step(self):
        """
        Perform the model step in two stages:
        - First, all agents determine their next opinion based on their neighbors' current opinions.
        - Then, all agents update their opinion to the next opinion.
        """
        for agent in self.schedule.agents:
            agent.determine_opinion()
        for agent in self.schedule.agents:
            agent.assume_opinion()
        self.schedule.step()
