import mesa
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.experimental.devs.simulator import ABMSimulator

from .agents import Bank, Person

# Start of datacollector functions


def get_num_rich_agents(model):
    """return number of rich agents"""
    rich_agents = [
        a
        for a in model.schedule.agents
        if isinstance(a, Person) and a.savings > model.rich_threshold
    ]
    return len(rich_agents)


def get_num_poor_agents(model):
    """return number of poor agents"""
    poor_agents = [
        a for a in model.schedule.agents if isinstance(a, Person) and a.loans > 10
    ]
    return len(poor_agents)


def get_num_mid_agents(model):
    """return number of middle class agents"""
    mid_agents = [
        a
        for a in model.schedule.agents
        if isinstance(a, Person) and a.loans <= 10 and a.savings <= model.rich_threshold
    ]
    return len(mid_agents)


def get_total_savings(model):
    """sum of all agents' savings"""
    return sum(a.savings for a in model.schedule.agents if isinstance(a, Person))


def get_total_wallets(model):
    """sum of amounts of all agents' wallets"""
    return sum(a.wallet for a in model.schedule.agents if isinstance(a, Person))


def get_total_money(model):
    return get_total_wallets(model) + get_total_savings(model)


def get_total_loans(model):
    return sum(a.loans for a in model.schedule.agents if isinstance(a, Person))


class BankReserves(mesa.Model):
    grid_h = 20
    grid_w = 20

    def __init__(
        self,
        height=grid_h,
        width=grid_w,
        init_people=2,
        rich_threshold=10,
        reserve_percent=50,
        seed=None,
    ):
        super().__init__(seed=seed)
        self.height = height
        self.width = width
        self.init_people = init_people
        self.rich_threshold = rich_threshold
        self.reserve_percent = reserve_percent

        self.grid = SingleGrid(self.width, self.height, torus=True)
        self.schedule = RandomActivation(self)

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Rich": get_num_rich_agents,
                "Poor": get_num_poor_agents,
                "Middle Class": get_num_mid_agents,
                "Savings": get_total_savings,
                "Wallets": get_total_wallets,
                "Money": get_total_money,
                "Loans": get_total_loans,
            },
            agent_reporters={
                "Wealth": lambda x: getattr(x, "wealth", None)
                if isinstance(x, Person)
                else None
            },
        )

        # Create the bank and place it on the grid
        bank_pos = (self.width // 2, self.height // 2)  # Place bank at the center
        self.bank = Bank(1, self, self.reserve_percent)
        self.grid.place_agent(self.bank, bank_pos)
        # Note: We're not adding the bank to the schedule anymore

        # Create people
        for i in range(self.init_people):
            self.create_person(i + 2)

        self.running = True
        self.datacollector.collect(self)

    def create_person(self, unique_id):
        x = self.random.randrange(self.width)
        y = self.random.randrange(self.height)
        pos = (x, y)
        while not self.grid.is_cell_empty(pos):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            pos = (x, y)

        person = Person(unique_id, pos, self, True, self.bank, self.rich_threshold)
        self.grid.remove_agent(person)
        self.grid.place_agent(person, pos)
        self.schedule.add(person)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run_model(self):
        for i in range(self.run_time):
            self.step()
