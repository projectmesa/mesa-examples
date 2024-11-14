from mesa.examples.advanced.epstein_civil_violence.agents import Citizen, Cop

from .utility import move


class CitizenRL(Citizen):
    def step(self):
        # Get action from action_dict
        action_tuple = self.model.action_dict[self.unique_id]
        # If in jail decrease sentence, else update condition
        if self.jail_sentence > 0:
            self.jail_sentence -= 1
        else:
            # RL Logic
            # Update condition and postion based on action
            self.condition = "Active" if action_tuple[0] == 1 else "Quiescent"
            # Update neighbors for updated empty neighbors
            self.update_neighbors()
            if self.model.movement:
                move(
                    self,
                    action_tuple[1],
                    self.empty_neighbors,
                )

        # Update the neighbors for observation space
        self.update_neighbors()


class CopRL(Cop):
    def step(self):
        # RL Logics
        # Arrest if active citizen is indicated in action
        action_tuple = self.model.action_dict[self.unique_id]
        arrest_pos = self.neighborhood[action_tuple[0]]
        for agent in self.model.grid.get_cell_list_contents(self.neighborhood):
            if (
                isinstance(agent, CitizenRL)
                and agent.condition == "Active"
                and agent.jail_sentence == 0
                and agent.pos == arrest_pos
            ):
                agent.jail_sentence = self.random.randint(1, self.model.max_jail_term)
                agent.condition = "Quiescent"
                self.arrest_made = True
                break
            else:
                self.arrest_made = False
        # Update neighbors for updated empty neighbors
        self.update_neighbors()
        # Move based on action
        if self.model.movement:
            move(self, action_tuple[1], self.empty_neighbors)
        # Update the neighbors for observation space
        self.update_neighbors()
