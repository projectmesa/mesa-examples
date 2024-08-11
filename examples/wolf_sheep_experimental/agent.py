import mesa
from .random_walk import RandomWalker


class GrassPatch(mesa.Agent):
    def __init__(self, unique_id, model, fully_grown, countdown):
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1


class Animal(mesa.Agent):
    def __init__(self, unique_id, model, moore, energy, p_reproduce, energy_from_food):
        super().__init__(unique_id, model)
        self.energy = energy
        self.p_reproduce = p_reproduce
        self.energy_from_food = energy_from_food
        self.moore = moore

    def random_move(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def spawn_offspring(self):
        self.energy /= 2
        offspring = self.__class__(
            self.model.next_id(),
            self.model,
            self.moore,
            self.energy,
            self.p_reproduce,
            self.energy_from_food,
        )
        self.model.grid.place_agent(offspring, self.pos)

    def feed(self):
        pass

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def step(self):
        self.random_move()
        self.energy -= 1

        self.feed()

        if self.energy < 0:
            self.die()
        elif self.random.random() < self.p_reproduce:
            self.spawn_offspring()


class Sheep(Animal):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.
    """

    def feed(self):
        # If there is grass available, eat it
        agents = self.model.grid.get_cell_list_contents(self.pos)
        grass_patch = next(obj for obj in agents if isinstance(obj, GrassPatch))
        if grass_patch.fully_grown:
            self.energy += self.energy_from_food
            grass_patch.fully_grown = False


class Wolf(Animal):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    def feed(self):
        agents = self.model.grid.get_cell_list_contents(self.pos)
        sheep = [obj for obj in agents if isinstance(obj, Sheep)]
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            self.energy += self.energy_from_food

            # Kill the sheep
            sheep_to_eat.die()
