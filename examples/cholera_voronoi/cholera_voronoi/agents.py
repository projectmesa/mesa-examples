from mesa.experimental.cell_space import CellAgent

SUSCEPTIBLE = 0
INFECTIOUS = 1
REMOVED = 2


class Person(CellAgent):
    def __init__(self, unique_id, model, mortality_chance, recovery_chance):
        super().__init__(unique_id, model)
        self.state = SUSCEPTIBLE
        self.mortality_chance = mortality_chance
        self.recovery_chance = recovery_chance

    def step(self):
        if self.state == REMOVED:
            return

        if (
            self.state == INFECTIOUS
            and self.model.random.random() < self.recovery_chance
        ):
            self.state = SUSCEPTIBLE
            self.model.infectious -= 1
            self.model.susceptible += 1

        if (
            self.state == INFECTIOUS
            and self.model.random.random() < self.mortality_chance
        ):
            self.state = REMOVED
            self.model.infectious -= 1
            self.model.removed += 1


class Pump(CellAgent):
    def __init__(
        self,
        unique_id,
        model,
        contaminated,
        pumps_person_contamination_chance,
        pumps_neighbor_contamination_chance,
        cases_ratio_to_fix_pump,
    ):
        super().__init__(unique_id, model)
        self.state = contaminated
        self.pumps_person_contamination_chance = pumps_person_contamination_chance
        self.pumps_neighbor_contamination_chance = pumps_neighbor_contamination_chance
        self.cases_ratio_to_fix_pump = cases_ratio_to_fix_pump

    def step(self):
        if self.state is INFECTIOUS:
            # Infect people in the cell
            people = [
                obj
                for obj in self.cell.agents
                if isinstance(obj, Person) and obj.state is not REMOVED
            ]
            for person in people:
                if (
                    person.state is SUSCEPTIBLE
                    and self.model.random.random()
                    < self.pumps_person_contamination_chance
                ):
                    person.state = INFECTIOUS
                    self.model.susceptible -= 1
                    self.model.infectious += 1

            # Infect neighbor cells
            if self.model.random.random() < self.pumps_neighbor_contamination_chance:
                neighbor_cell = self.random.choice(list(self.cell._connections))
                neighbor_pump = neighbor_cell.agents[0]
                if neighbor_pump.state is SUSCEPTIBLE:
                    neighbor_pump.state = INFECTIOUS
                    self.model.infected_pumps += 1

            # If cases in total is too high, fix pump
            cases = sum(1 for a in people if a.state is INFECTIOUS)
            cases_ratio = cases / (
                self.model.susceptible + self.model.infectious + 1e-1
            )
            self.cell.properties["cases_ratio"] = cases_ratio
            if cases_ratio > self.cases_ratio_to_fix_pump:
                self.state = SUSCEPTIBLE
                self.model.infected_pumps -= 1
