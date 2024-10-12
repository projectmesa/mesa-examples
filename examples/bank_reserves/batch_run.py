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
import pandas as pd
from bank_reserves.agents import Bank, Person
from bank_reserves.model import (
    get_num_mid_agents,
    get_num_poor_agents,
    get_num_rich_agents,
    get_total_loans,
    get_total_money,
    get_total_savings,
    get_total_wallets,
)


def track_params(model):
    return (model.init_people, model.rich_threshold, model.reserve_percent)


def track_run(model):
    return model.uid


class BankReservesModel(mesa.Model):
    # id generator to track run number in batch run data

    # grid height
    grid_h = 20
    # grid width
    grid_w = 20

    """init parameters "init_people", "rich_threshold", and "reserve_percent"
       are all set via Slider"""

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

        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        # rich_threshold is the amount of savings a person needs to be considered "rich"
        self.rich_threshold = rich_threshold
        self.reserve_percent = reserve_percent
        # see datacollector functions above
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
            agent_reporters={"Wealth": "wealth"},
        )

        # create a single bank object for the model
        self.bank = Bank(self, self.reserve_percent)

        # create people for the model according to number of people set by user
        for i in range(self.init_people):
            # set x coordinate as a random number within the width of the grid
            x = self.random.randrange(self.width)
            # set y coordinate as a random number within the height of the grid
            y = self.random.randrange(self.height)
            p = Person(i, (x, y), self, True, self.bank, self.rich_threshold)
            # place the Person object on the grid at coordinates (x, y)
            self.grid.place_agent(p, (x, y))

        self.running = True

    def step(self):
        # collect data
        self.datacollector.collect(self)
        # tell all the agents in the model to run their step function
        self.agents.shuffle_do("step")

    def run_model(self):
        for i in range(self.run_time):
            self.step()


# parameter lists for each parameter to be tested in batch run
br_params = {
    "init_people": [25, 100],
    "rich_threshold": [5, 10],
    "reserve_percent": 5,
}


def main():
    # The existing batch run logic here
    data = mesa.batch_run(
        BankReservesModel,
        br_params,
    )
    br_df = pd.DataFrame(data)
    br_df.to_csv("BankReservesModel_Data.csv")


if __name__ == "__main__":
    main()
