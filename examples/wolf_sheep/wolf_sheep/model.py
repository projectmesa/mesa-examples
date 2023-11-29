"""
Wolf-Elk Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

import mesa

from .agents import GrassPatch, Elk, Wolf, WateringHole
from .scheduler import RandomActivationByTypeFiltered


class WolfElk(mesa.Model):
    """
    Wolf-Elk Predation Model
    """

    height = 50
    width = 50

    initial_elk = 1700
    initial_wolves = 14

    elk_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    elk_gain_from_food = 4
    water = True

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating wolf and elk (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        width=50,
        height=30,
        initial_elk=1700,
        initial_wolves=14,
        elk_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=False,
        grass_regrowth_time=30,
        elk_gain_from_food=4,
        water=True
    ):
        """
        Create a new Wolf-Elk model with the given parameters.

        Args:
            initial_elk: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            elk_reproduce: Probability of each elk reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the elk eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            elk_gain_from_food: Energy elk gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_elk = initial_elk
        self.initial_wolves = initial_wolves
        self.elk_reproduce = elk_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.elk_gain_from_food = elk_gain_from_food
        self.water = water

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_type_count(Wolf),
                "Elk": lambda m: m.schedule.get_type_count(Elk),
                "Grass": lambda m: m.schedule.get_type_count(
                    GrassPatch, lambda x: x.fully_grown
                ),
            }
        )

        # Create elk:
        for i in range(self.initial_elk):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.elk_gain_from_food)
            elk = Elk(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(elk, (x, y))
            self.schedule.add(elk)

        # Create wolves
        for i in range(self.initial_wolves):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            wolf = Wolf(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create grass patches
        if self.grass:
            for agent, (x, y) in self.grid.coord_iter():
                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)
                
        # Create watering holes
        if self.water:
            for x in range(0,5):
                for y in range(0,7):
          
                    waterhole = WateringHole(self.next_id(), (x,y), self)
                    self.grid.place_agent(waterhole, (x,y))
                    self.schedule.add(waterhole)
                    
            for x in range(45,50):
                for y in range(22,30):
          
                    waterhole = WateringHole(self.next_id(), (x,y), self)
                    self.grid.place_agent(waterhole, (x,y))
                    self.schedule.add(waterhole)
            
            

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_type_count(Wolf),
                    self.schedule.get_type_count(Elk),
                    self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown),
                    self.schedule.get_type_count(WateringHole)
                ]
            )

    def run_model(self, step_count=200):
        if self.verbose:
            print("Initial number wolves: ", self.schedule.get_type_count(Wolf))
            print("Initial number elk: ", self.schedule.get_type_count(Elk))
            print(
                "Initial number grass: ",
                self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown),
            )

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number wolves: ", self.schedule.get_type_count(Wolf))
            print("Final number elk: ", self.schedule.get_type_count(Elk))
            print(
                "Final number grass: ",
                self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown),
            )
