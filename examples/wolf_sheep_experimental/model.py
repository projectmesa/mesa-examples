from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agent import Sheep, Wolf, GrassPatch


class WolfSheepPredation(Model):
    def __init__(
        self,
        width,
        height,
        initial_sheep,
        initial_wolves,
        sheep_reproduce,
        wolf_reproduce,
        sheep_gain_from_food,
        wolf_gain_from_food,
    ):
        self.width = width
        self.height = height
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.sheep_gain_from_food = sheep_gain_from_food
        self.wolf_gain_from_food = wolf_gain_from_food

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus=True)

        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: self.count_type(m, Wolf),
                "Sheep": lambda m: self.count_type(m, Sheep),
                "Grass": lambda m: self.count_type(m, GrassPatch),
            }
        )

        for _ in range(self.initial_sheep):
            sheep = Sheep(self.next_id(), self)
            self.grid.place_agent(
                sheep,
                (self.random.randrange(self.width), self.random.randrange(self.height)),
            )
            self.schedule.add(sheep)

        for _ in range(self.initial_wolves):
            wolf = Wolf(self.next_id(), self)
            self.grid.place_agent(
                wolf,
                (self.random.randrange(self.width), self.random.randrange(self.height)),
            )
            self.schedule.add(wolf)

        for agent, x, y in self.grid.coord_iter():
            grass_patch = GrassPatch(self.next_id(), self)
            self.grid.place_agent(grass_patch, (x, y))
            self.schedule.add(grass_patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    @staticmethod
    def count_type(model, agent_type):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, agent_type):
                count += 1
        return count
