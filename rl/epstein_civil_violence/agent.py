from . utility import move
from mesa_models.epstein_civil_violence.agent import Citizen, Cop

class Citizen_RL(Citizen):

    def step(self):
        # If in jail decrease sentence, else update condition
        if self.jail_sentence:
            self.jail_sentence -= 1
        else:
            # RL Logic
            # Update condition and postion based on action
            self.condition = "Active" if self.model.action_dict[self.unique_id][0] == 1 else "Quiescent"
            # Update neighbors for updated empty neighbors
            self.update_neighbors()
            if self.model.movement:
                move(self, self.model.action_dict[self.unique_id][1], self.empty_neighbors)

        # Update the neighbors for observation space
        self.update_neighbors()

class Cop_RL(Cop):
    
    def step(self):
        # RL Logics
        # Arrest if active citizen is indicated in action
        action_tuple = self.model.action_dict[self.unique_id]
        arrest_pos = self.neighborhood[action_tuple[0]]
        for agent in self.model.grid.get_cell_list_contents(self.neighborhood):
            if agent.breed == "citizen" and agent.condition == "Active" and agent.jail_sentence == 0 and agent.pos == arrest_pos:
                sentence = self.random.randint(1, self.model.max_jail_term)
                agent.jail_sentence = sentence
                agent.condition = "Quiescent"
                self.arrest_made = True
                break
            else:
                self.arrest_made = False
        # Update neighbors for updated empty neighbors
        self.update_neighbors()
        # Move based on action
        if self.model.movement:
            move(self, self.model.action_dict[self.unique_id][1], self.empty_neighbors)
        # Update the neighbors for observation space
        self.update_neighbors()
