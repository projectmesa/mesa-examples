import mesa
import networkx as nx
from .agents.py import DriverAgent, RideAgent


class CityModel(mesa.Model):
    def __init__(self, num_drivers, num_rides, width, height):
        self.num_drivers = num_drivers
        self.num_rides = num_rides
        self.width = width
        self.height = height

        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.NetworkGrid(nx.grid_2d_graph(width, height))

        self.G = nx.grid_2d_graph(width, height)

        for i in range(self.num_drivers):
            x, y = self.random.choice(list(self.G.nodes))
            driver = DriverAgent(i, self, (x, y))
            self.grid.place_agent(driver, (x, y))
            self.schedule.add(driver)

        for i in range(self.num_rides):
            pickup = self.random.choice(list(self.G.nodes))
            dropoff = self.random.choice(list(self.G.nodes))
            ride = RideAgent(self.num_drivers + i, self, pickup, dropoff)
            self.grid.place_agent(ride, pickup)
            self.schedule.add(ride)

    def step(self):
        self.schedule.step()
