import networkx as nx

import mesa


class AntTSP(mesa.Agent):  # noqa
    """
    An agent
    """

    def __init__(self, unique_id, model):
        """
        Customize the agent
        """
        self.unique_id = unique_id
        super().__init__(unique_id, model)
        self.cities_visited = set()

    def decide_next_city(self):
        # Random
        # new_city = self.random.choice(list(self.model.all_cities - self.cities_visited))
        # Choose closest city
        g = self.model.grid.G
        current_city = self.pos
        neighbors = list(g.neighbors(current_city))
        min_distance = float('inf')
        new_city = None
        for neighbor in neighbors:
            if neighbor in self.cities_visited:
                continue
            distance = g[current_city][neighbor]['distance']
            if distance < min_distance:
                min_distance = distance
                new_city = neighbor
        if new_city is None:
            # No unvisited neighbors, so stay put
            new_city = current_city
        return new_city

    def step(self):
        """
        Modify this method to change what an individual agent will do during each step.
        Can include logic based on neighbors states.
        """
        # Pick a random city that isn't in the list of cities visited
        new_city = self.decide_next_city()
        print(f"Moving Ant {self.unique_id} from city {self.pos} to {new_city}")
        self.cities_visited.add(new_city)
        self.model.grid.move_agent(self, new_city)
        

class AcoTspModel(mesa.Model):
    """
    The model class holds the model-level attributes, manages the agents, and generally handles
    the global level of our model.

    There is only one model-level parameter: how many agents the model contains. When a new model
    is started, we want it to populate itself with the given number of agents.

    The scheduler is a special model component which controls the order in which agents are activated.
    """

    def __init__(self, num_agents, num_cities):
        super().__init__()
        self.num_agents = num_agents
        self.num_cities = num_cities
        self.all_cities = set(range(self.num_cities))
        self.schedule = mesa.time.RandomActivation(self)
        g = self.create_graph(num_cities)
        self.grid = mesa.space.NetworkGrid(g)

        for i in range(self.num_agents):
            agent = AntTSP(i, self)
            self.schedule.add(agent)

            city = self.random.randrange(self.num_cities)
            self.grid.place_agent(agent, city)
            agent.cities_visited.add(city)

        # example data collector
        self.num_steps = 0
        self.datacollector = mesa.datacollection.DataCollector({"num_steps": "num_steps"})

        self.running = True
        self.datacollector.collect(self)

    def create_graph(self, num_cities):
        g = nx.random_geometric_graph(num_cities, 2.).to_directed()
        self.pos = {k: v['pos'] for k, v in dict(g.nodes.data()).items()}

        for u, v in g.edges():
            u_x, u_y = g.nodes[u]['pos']
            v_x, v_y = g.nodes[v]['pos']
            g[u][v]['distance'] = ((u_x - v_x) ** 2 + (u_y - v_y) ** 2) ** 0.5
            g[u][v]['weight'] = 1 / g[u][v]['distance']

        return g

    
    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
        self.datacollector.collect(self)
        self.schedule.step()
        self.num_steps += 1

        # Check len of cities visited by an agent
        for agent in self.schedule.agents:
            if len(agent.cities_visited) == self.num_cities:
                print(f"Ant {agent.unique_id} has visited all cities")
                self.running = False