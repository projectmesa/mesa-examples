"""
The following code was adapted from the Bank Reserves model included in Netlogo
Model information can be found at:
http://ccl.northwestern.edu/netlogo/models/BankReserves
Accessed on: November 2, 2017
Author of NetLogo code:
    Wilensky, U. (1998). NetLogo Bank Reserves model.
    http://ccl.northwestern.edu/netlogo/models/BankReserves.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.

This version of the model has a BatchRunner at the bottom. This
is for collecting data on parameter sweeps. It is not meant to
be run with run.py, since run.py starts up a server for visualization, which
isn't necessary for the BatchRunner. To run a parameter sweep, call
batch_run.py in the command line.

The BatchRunner is set up to collect step by step data of the model. It does
this by collecting the DataCollector object in a model_reporter (i.e. the
DataCollector is collecting itself every step).

The end result of the batch run will be a CSV file created in the same
directory from which Python was run. The CSV file will contain the data from
every step of every run.
"""


import itertools
import mesa
import numpy as np
import pandas as pd
from .agents import Bank, Person

# Start of datacollector functions

def get_num_rich_agents(model):
    """list of rich agents"""
    rich_agents = [a for a in model.schedule.agents if a.savings > model.rich_threshold]
    return len(rich_agents)

def get_num_poor_agents(model):
    """list of poor agents"""
    poor_agents = [a for a in model.schedule.agents if a.loans > 10]
    return len(poor_agents)

def get_num_mid_agents(model):
    """list of middle class agents"""
    mid_agents = [
        a
        for a in model.schedule.agents
        if a.loans < 10 and a.savings < model.rich_threshold
    ]
    return len(mid_agents)

def get_total_savings(model):
    """list of amounts of all agents' savings"""
    agent_savings = [a.savings for a in model.schedule.agents]
    return np.sum(agent_savings)

def get_total_wallets(model):
    """list of amounts of all agents' wallets"""
    agent_wallets = [a.wallet for a in model.schedule.agents]
    return np.sum(agent_wallets)

def get_total_money(model):
    """sum of all agents' wallets"""
    wallet_money = get_total_wallets(model)
    savings_money = get_total_savings(model)
    return wallet_money + savings_money

def get_total_loans(model):
    """list of amounts of all agents' loans"""
    agent_loans = [a.loans for a in model.schedule.agents]
    return np.sum(agent_loans)

def track_params(model):
    return (model.init_people, model.rich_threshold, model.reserve_percent)

def track_run(model):
    return model.uid

class BankReservesModel(mesa.Model):
    id_gen = itertools.count(1)
    grid_h = 20
    grid_w = 20

    def __init__(
        self,
        height=grid_h,
        width=grid_w,
        init_people=2,
        rich_threshold=10,
        reserve_percent=50,
    ):
        super().__init__()
        self.uid = next(self.id_gen)
        self.height = height
        self.width = width
        self.init_people = init_people
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.rich_threshold = rich_threshold
        self.reserve_percent = reserve_percent
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Rich": get_num_rich_agents,
                "Poor": get_num_poor_agents,
                "Middle Class": get_num_mid_agents,
                "Savings": get_total_savings,
                "Wallets": get_total_wallets,
                "Money": get_total_money,
                "Loans": get_total_loans,
                "Model Params": track_params,
                "Run": track_run,
            },
            agent_reporters={"wealth": "wealth"},
        )

        self.bank = Bank(1, self, self.reserve_percent)

        for i in range(self.init_people):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            p = Person(i, (x, y), self, True, self.bank, self.rich_threshold)
            self.grid.place_agent(p, (x, y))
            self.schedule.add(p)

        self.running = True

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def run_model(self):
        for i in range(self.run_time):
            self.step()

br_params = {
    "init_people": [25, 100],
    "rich_threshold": [5, 10],
    "reserve_percent": [5, 10, 20, 50],
}

def custom_batch_run(model_cls, parameters, iterations, max_steps, model_reporters, agent_reporters):
    results = []
    for params in (dict(zip(parameters, x)) for x in itertools.product(*parameters.values())):
        for i in range(iterations):
            model = model_cls(**params)
            for step in range(max_steps):
                model.step()
            model_data = {var: reporter(model) for var, reporter in model_reporters.items()}
            agent_data = [{var: getattr(agent, var) for var in agent_reporters} for agent in model.schedule.agents]
            results.append({**model_data, "Agent Data": agent_data})
    return results

def main():

    data = custom_batch_run(
        BankReservesModel,
        br_params,
        iterations=5,
        max_steps=100,
        model_reporters={
            "Rich": get_num_rich_agents,
            "Poor": get_num_poor_agents,
            "Middle Class": get_num_mid_agents,
            "Savings": get_total_savings,
            "Wallets": get_total_wallets,
            "Money": get_total_money,
            "Loans": get_total_loans,
            "Model Params": track_params,
            "Run": track_run,
        },
        agent_reporters={"wealth": "wealth"},
    )

    br_df = pd.DataFrame(data)
    br_df.to_csv("BankReservesModel_Data.csv")

if __name__ == "__main__":
    main()
