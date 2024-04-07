from collections.abc import Sequence

import mesa

from .agents import Person, Pump

SUSCEPTIBLE = 0
INFECTIOUS = 1
REMOVED = 2

cell_population = [400] * 8

points = [
    (9.909976449792431, 11.542846828417543),
    (0.40972334441912234, 14.266853186123692),
    (0.0, 20.0),
    (20.0, 5.111991897435429),
    (12.566609556906684, 1.57960921165571),
    (5.232766132031835, 0.0),
    (10.196872670067446, 4.1842030053700165),
    (16.553612933660478, 4.449943091510793),
]

is_pump_contaminated = [True, False, False, False, False, False, False, False]


class Cholera(mesa.Model):
    def __init__(
        self,
        cell_population: Sequence[int] = cell_population,
        pumps_location: Sequence[Sequence[float]] = points,
        is_pump_contaminated: Sequence[bool] = is_pump_contaminated,
        cases_ratio_to_fix_pump: float = 9e-1,
        pumps_neighbor_contamination_chance: float = 2e-1,
        pumps_person_contamination_chance: float = 2e-1,
        recovery_chance: float = 2e-1,
        mortality_chance: float = 1e-1,
    ):
        super().__init__()
        self.susceptible = 0
        for population in cell_population:
            self.susceptible += population
        self.infectious = 0
        self.removed = 0

        self.infected_pumps = 0
        self.number_pumps = len(cell_population)

        self.schedule = mesa.time.RandomActivation(self)

        self.grid = mesa.experimental.cell_space.VoronoiGrid(
            centroids_coordinates=pumps_location,
            capacity=int(self.susceptible + 1),
            random=self.random,
        )

        for population, cell, contaminated in zip(
            cell_population, list(self.grid.all_cells), is_pump_contaminated
        ):
            pump_state = INFECTIOUS if contaminated else SUSCEPTIBLE
            self.infected_pumps += pump_state
            pump = Pump(
                self.next_id(),
                self,
                pump_state,
                pumps_person_contamination_chance,
                pumps_neighbor_contamination_chance,
                cases_ratio_to_fix_pump,
            )
            self.schedule.add(pump)
            cell.add_agent(pump)
            pump.move_to(cell)
            for i in range(population):
                person = Person(self.next_id(), self, mortality_chance, recovery_chance)
                self.schedule.add(person)
                cell.add_agent(person)
                person.move_to(cell)

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Susceptible": "susceptible",
                "Infectious": "infectious",
                "Removed": "removed",
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
