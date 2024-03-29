"""
Sugarscape: Sex, Culture & Conflict.

TODO
1. calculate gini coeff
2. create trigger buttons that switch factors such as inheritance on/off.
"""


import mesa
from mesa_models.sugarscape_cg.model import SugarscapeCg

from .agents import SsAgent3 as SsAgent


class SugarscapeScc(SugarscapeCg):
    """
    Sugarscape 3 SCC
    """

    verbose = True  # Print-monitoring

    def __init__(self, width=50, height=50, initial_population=100):
        """
        Args:
            initial_population: Number of population to start with
        """
        super().__init__(width, height, initial_population)
        # ADD agent reporters to the datacollector

        self.datacollector = mesa.DataCollector(
            model_reporters={"SsAgent": lambda m: m.schedule.get_type_count(SsAgent)},
            agent_reporters={"age": "age"},
        )

