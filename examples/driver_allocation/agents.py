import networkx as nx
import mesa


class DriverAgent(mesa.Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.available = True
        self.path = None
        self.ride = None

    def step(self):
        if not self.available:
            self.move_along_path()

    def move_along_path(self):
        if self.path and len(self.path) > 0:
            self.pos = self.path.pop(0)
            if self.pos == self.ride.dropoff:
                self.complete_ride()

    def complete_ride(self):
        self.available = True
        self.ride = None
        self.path = None


class RideAgent(mesa.Agent):
    def __init__(self, unique_id, model, pickup, dropoff):
        super().__init__(unique_id, model)
        self.pickup = pickup
        self.dropoff = dropoff
        self.assigned_driver = None

    def step(self):
        if self.assigned_driver is None:
            self.assign_driver()

    def assign_driver(self):
        closest_driver = min(
            (
                driver
                for driver in self.model.schedule.agents
                if isinstance(driver, DriverAgent) and driver.available
            ),
            key=lambda driver: nx.shortest_path_length(
                self.model.G, source=self.pickup, target=driver.pos, weight="length"
            ),
            default=None,
        )
        if closest_driver:
            self.assigned_driver = closest_driver
            closest_driver.available = False
            closest_driver.ride = self
            closest_driver.path = nx.shortest_path(
                self.model.G,
                source=closest_driver.pos,
                target=self.dropoff,
                weight="length",
            )
