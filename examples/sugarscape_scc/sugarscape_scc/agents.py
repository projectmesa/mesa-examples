import math

import mesa


def get_distance(pos_1, pos_2):
    """Get the distance between two point

    Args:
        pos_1, pos_2: Coordinate tuples for both points.
    """
    x1, y1 = pos_1
    x2, y2 = pos_2
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)


class SsAgent(mesa.Agent):
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

        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision
        self.age = 0
        self.fertile = fertile
        self.age_of_death = self.random.randrange(60, 100)
        self.gender = self.random.randint(0, 1)  # 0 is FEMALE, 1 is MALE
        self.children = []  # maybe stores the IDs of the kids of the agent?

    def is_occupied(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        return any(isinstance(agent, SsAgent) for agent in this_cell)

    def is_fertile(self) -> bool:
        # reduced some of the randomness in determining when agents can no longer reproduce
        if self.age < 15:
            return False

        if (self.gender == 1) and (self.age > 60):
            return False

        if (self.gender == 0) and (self.age > 50):
            return False
        return self.sugar < self.fertile

    def get_sugar(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        for agent in this_cell:
            if type(agent) is Sugar:
                return agent

    def move(self):
        # Get neighborhood within vision
        neighbors = [
            i
            for i in self.model.grid.get_neighborhood(
                self.pos, self.moore, False, radius=self.vision
            )
            if not self.is_occupied(i)
        ]
        neighbors.append(self.pos)
        # Look for location with the most sugar
        max_sugar = max(self.get_sugar(pos).amount for pos in neighbors)
        candidates = [
            pos for pos in neighbors if self.get_sugar(pos).amount == max_sugar
        ]
        # Narrow down to the nearest ones
        min_dist = min(get_distance(self.pos, pos) for pos in candidates)
        final_candidates = [
            pos for pos in candidates if get_distance(self.pos, pos) == min_dist
        ]
        self.random.shuffle(final_candidates)
        self.model.grid.move_agent(self, final_candidates[0])

    def eat(self):
        sugar_patch = self.get_sugar(self.pos)
        self.sugar = self.sugar - self.metabolism + sugar_patch.amount
        sugar_patch.amount = 0

    def sex(self):
        """ """
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

    def inheritance():
        pass

    def step(self):
        self.move()
        self.eat()
        if self.is_fertile() is True:
            self.sex()  # reproduction condition

        if (self.sugar <= 0) or (self.age == self.age_of_death):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)  # death conditions
            self.inheritance()
        self.age += 1


class Sugar(mesa.Agent):
    def __init__(self, unique_id, pos, model, max_sugar, growback_rule=1):
        super().__init__(unique_id, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar
        self.growback = growback_rule

    def step(self):
        self.amount = min([self.max_sugar, self.amount + self.growback])
