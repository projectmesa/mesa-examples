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

import mesa
import pandas as pd
from bank_reserves.model import BankReservesModel


def main():
    # parameter lists for each parameter to be tested in batch run
    br_params = {
        "init_people": [25, 100],
        "rich_threshold": [5, 10],
        "reserve_percent": 5,
    }

    # The existing batch run logic here
    data = mesa.batch_run(
        BankReservesModel,
        br_params,
    )
    br_df = pd.DataFrame(data)
    br_df.to_csv("BankReservesModel_Data.csv")


if __name__ == "__main__":
    main()
