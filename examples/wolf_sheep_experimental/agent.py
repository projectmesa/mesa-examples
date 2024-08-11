from mesa import Agent

class Sheep(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.energy = self.random.randint(2, 4)

    def step(self):
        self.move()
        self.eat_grass()
        self.reproduce()
        self.die()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def eat_grass(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        grass_patch = [obj for obj in cell_contents if isinstance(obj, GrassPatch)][0]
        if grass_patch.fully_grown:
            self.energy += self.model.sheep_gain_from_food
            grass_patch.fully_grown = False

    def reproduce(self):
        if self.random.random() < self.model.sheep_reproduce:
            lamb = Sheep(self.model.next_id(), self.model)
            self.model.grid.place_agent(lamb, self.pos)
            self.model.schedule.add(lamb)

    def die(self):
        self.energy -= 1
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


class Wolf(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.energy = self.random.randint(2, 4)

    def step(self):
        self.move()
        self.eat_sheep()
        self.reproduce()
        self.die()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def eat_sheep(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in cell_contents if isinstance(obj, Sheep)]
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            self.energy += self.model.wolf_gain_from_food
            self.model.grid.remove_agent(sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)

    def reproduce(self):
        if self.random.random() < self.model.wolf_reproduce:
            cub = Wolf(self.model.next_id(), self.model)
            self.model.grid.place_agent(cub, self.pos)
            self.model.schedule.add(cub)

    def die(self):
        self.energy -= 1
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


class GrassPatch(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.fully_grown = True
        self.countdown = self.random.randint(2, 10)

    def step(self):
        if not self.fully_grown:
            self.countdown -= 1
            if self.countdown <= 0:
                self.fully_grown = True
                self.countdown = self.random.randint(2, 10)
