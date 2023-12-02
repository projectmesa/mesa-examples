import mesa

from .random_walk import RandomWalker


class Elk(RandomWalker):
    """
    A elk that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        living = True

        if self.model.grass:
            # Reduce energy
            self.energy -= 1

            # If there is grass available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.elk_gain_from_food
                grass_patch.fully_grown = False

            # Death
            if self.energy < 0:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                living = False

        if living and self.random.random() < self.model.elk_reproduce:
            # Create a new elk:
            if self.model.grass:
                self.energy /= 2
            calf = Elk(
                self.model.next_id(), self.pos, self.model, self.moore, self.energy
            )
            self.model.grid.place_agent(calf, self.pos)
            self.model.schedule.add(calf)
            
            
        # if there is water present, drink it

#         x, y = self.pos
#         this_cell = self.model.grid.get_cell_list_contents([self.pos])
        water = [obj for obj in this_cell if isinstance(obj, WateringHole)]
        if len(water) > 0:
            self.energy += 1


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats elk.
    """

    energy = None
    threshold = 0.5

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1
        
    # probability wolf eats elk upon encounter        
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        elk = [obj for obj in this_cell if isinstance(obj, Elk)]

        if len(elk) > 0:
            elk_to_eat = self.random.choice(elk)

            # Check probability of eating the elk
            wolf_eats_prob = self.random.random()
            if wolf_eats_prob < self.threshold:
                # Wolf eats the elk
                self.energy += self.model.wolf_gain_from_food

                # Kill the elk
                self.model.grid.remove_agent(elk_to_eat)
                self.model.schedule.remove(elk_to_eat)
            else:
                # Wolf moves away a random number of spaces
                self.random_move()
                self.energy -= 1
                
        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.wolf_reproduce:
                # Create a new wolf cub
                self.energy /= 2
                cub = Wolf(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)


class GrassPatch(mesa.Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by elk
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1
class WateringHole(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        
        super().__init__(unique_id, model)
        self.pos=pos
    
    def step(self):
        pass

                 

