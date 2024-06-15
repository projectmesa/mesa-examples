from mesa_models.sugarscape_cg.agents import SsAgent


class SsAgent3(SsAgent):
    def __init__(
        self,
        unique_id,
        pos,
        model,
        moore=False,
        sugar=0,
        metabolism=0,
        vision=0,
        fertile=40,
    ):
        # first generation agents are randomly assigned metabolism and vision,
        # children get a contribution from their parents

        super().__init__(unique_id, pos, model, moore, sugar, metabolism, vision)
        self.age = 0
        self.fertile = fertile
        self.age_of_death = self.random.randrange(60, 100)
        self.gender = self.random.randint(0, 1)  # 0 is FEMALE, 1 is MALE
        self.children = []  # maybe stores the IDs of the kids of the agent?
        self.age_of_death = self.random.randrange(60, 100)
        self.gender = self.random.randint(0, 1)  # 0 is FEMALE, 1 is MALE

    def is_fertile(self) -> bool:
        # reduced some of the randomness in determining when agents can no longer reproduce
        if self.age < 15:
            return False

        if (self.gender == 1) and (self.age > 60):
            return False

        if (self.gender == 0) and (self.age > 50):
            return False
        return self.sugar < self.fertile

      def sex(self):
        potential_mates = [
            i
            for i in self.model.grid.get_neighbors(
                self.pos, self.moore, include_center=False, radius=self.vision
            )
            if (
                (type(i) is SsAgent)
                and (i.is_fertile() is True)
                and (i.gender != self.gender)
            )
        ]

        # check for empty spots next to self
        empty_cells = [
            i
            for i in self.model.grid.get_neighborhood(
                self.pos, self.moore, include_center=False, radius=1
            )
            if not self.is_occupied(i)
        ]
        self.random.shuffle(empty_cells)
        for neighbor in potential_mates:
            if self.sugar < self.fertile:
                break

            if len(empty_cells) == 0:
                continue  # placeholder
                # check for first empty spot next to neighbor
                # if none found iterate to next neighbor
            endowment = (self.sugar / 2) + (neighbor.sugar / 2)
            self.sugar -= self.sugar / 2
            neighbor.sugar -= neighbor.sugar / 2
            ssa = SsAgent(
                self.model.next_id(),
                empty_cells[0],
                self.model,
                False,
                sugar=endowment,
                metabolism=self.random.choice([neighbor.metabolism, self.metabolism]),
                vision=self.random.choice([neighbor.vision, self.vision]),
            )
            self.model.grid.place_agent(ssa, empty_cells[0])
            self.model.schedule.add(ssa)

        # iterate through list

    def inheritance(self):
        for i in self.children:
            i.sugar += self.sugar / len(self.children)


    def step(self):
        self.move()
        self.eat()
        if self.is_fertile() is True:
            self.sex()  # reproduction condition

        if (self.sugar <= 0) or (self.age == self.age_of_death):
            self.inheritance()
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)  # death conditions
        self.age += 1


