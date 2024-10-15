import math

from mesa.experimental.cell_space import CellAgent, FixedAgent


def get_distance(cell_1, cell_2):
    """Get the distance between two point

    Args:
        pos_1, pos_2: Coordinate tuples for both points.
    """
    x1, y1 = cell_1.coordinate
    x2, y2 = cell_2.coordinate
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)


class SsAgent(CellAgent):
    def __init__(self, model, cell, sugar=0, metabolism=0, vision=0):
        super().__init__(model)
        self.cell = cell
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision

    def get_sugar(self, cell):
        for agent in cell.agents:
            if isinstance(agent, Sugar):
                return agent

    def is_occupied(self, cell):
        return any(isinstance(agent, SsAgent) for agent in cell.agents)

    def move(self):
        # Get neighborhood within vision
        neighbors = [
            cell
            for cell in self.cell.get_neighborhood(radius=self.vision)
            if not self.is_occupied(cell)
        ]
        neighbors.append(self.cell)
        # Look for location with the most sugar
        max_sugar = max(self.get_sugar(cell).amount for cell in neighbors)
        candidates = [
            cell for cell in neighbors if self.get_sugar(cell).amount == max_sugar
        ]
        # Narrow down to the nearest ones
        min_dist = min(get_distance(self.cell, cell) for cell in candidates)
        final_candidates = [
            cell for cell in candidates if get_distance(self.cell, cell) == min_dist
        ]
        self.random.shuffle(final_candidates)
        self.cell = final_candidates[0]

    def eat(self):
        sugar_patch = self.get_sugar(self.cell)
        self.sugar = self.sugar - self.metabolism + sugar_patch.amount
        sugar_patch.amount = 0

    def step(self):
        self.move()
        self.eat()
        if self.sugar <= 0:
            self.remove()


class Sugar(FixedAgent):
    def __init__(self, model, max_sugar, cell):
        super().__init__(model)
        self.amount = max_sugar
        self.max_sugar = max_sugar
        self.cell = cell

    def step(self):
        self.amount = min([self.max_sugar, self.amount + 1])
