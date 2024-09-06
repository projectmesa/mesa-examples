import mesa


class Walker(mesa.Agent):
    def __init__(self, model, heading=(1, 0)):
        super().__init__(model)
        self.heading = heading
        self.headings = {(1, 0), (0, 1), (-1, 0), (0, -1)}


class ShapeExample(mesa.Model):
    def __init__(self, N=2, width=20, height=10):
        super().__init__()
        self.N = N  # num of agents
        self.headings = ((1, 0), (0, 1), (-1, 0), (0, -1))  # tuples are fast
        self.grid = mesa.space.SingleGrid(width, height, torus=False)

        self.make_walker_agents()
        self.running = True

    def make_walker_agents(self):
        unique_id = 0
        while True:
            if unique_id == self.N:
                break
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            pos = (x, y)
            heading = self.random.choice(self.headings)
            # heading = (1, 0)
            if self.grid.is_cell_empty(pos):
                print(f"Creating agent {unique_id} at ({x}, {y})")
                a = Walker(self, heading)

                self.grid.place_agent(a, pos)
                unique_id += 1

    def step(self):
        self.agents.shuffle().do("step")
