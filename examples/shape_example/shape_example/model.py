import mesa


from mesa.experimental.cell_space import OrthogonalMooreGrid

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
        self.grid = OrthogonalMooreGrid((width, height), torus=True)

        self.make_walker_agents()
        self.running = True

    def make_walker_agents(self):
        for _ in range(self.N):
            x = self.random.randrange(self.grid.dimensions[0])
            y = self.random.randrange(self.grid.dimensions[1])
            cell = self.grid[(x, y)]
            heading = self.random.choice(self.headings)
            # heading = (1, 0)
            if cell.is_empty:
                a = Walker(self, heading)
                a.cell = cell

    def step(self):
        self.agents.shuffle_do("step")
