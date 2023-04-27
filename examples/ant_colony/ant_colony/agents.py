import mesa
from ant_colony.random_walk import RandomWalker

class Ant(RandomWalker):

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None, color='red'):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.color = color

    def step(self):
        self.random_move()
        living = True