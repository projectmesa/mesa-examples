"""
Determines where wolves and elk will move. Called random_walk because originally in mesa, movement was totally random
"""

import mesa
import math
import random


# +
class RandomWalker(mesa.Agent):
    """
    Class implementing random walker methods in a generalized manner.

    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    grid = None
    x = None
    y = None
    moore = True
    water = True

    def __init__(self, unique_id, pos, model, moore=True, target_location_1=(0,0), target_location_2=(49,29)):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        target_location: watering hole locations
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.target_location_1 = target_location_1
        self.target_location_2 = target_location_2
        
        
    def calculate_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def find_closest_neighbor(self, agent_position, neighborhood):
        closest_neighbor = None
        min_distance = float('inf')  # Initialize with a large value

        for neighbor_cell in neighborhood:
            distance_to_target = self.calculate_distance(neighbor_cell, self.target_location_1)
            if distance_to_target < min_distance:
                min_distance = distance_to_target
                closest_neighbor = neighbor_cell
            distance_to_target = self.calculate_distance(neighbor_cell, self.target_location_2)
            if distance_to_target < min_distance:
                min_distance = distance_to_target
                closest_neighbor = neighbor_cell

        return closest_neighbor, min_distance
        
        
    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        closest_neighbor_to_target, min_distance = self.find_closest_neighbor(self.pos, next_moves)
        
        #probability that it moves towards watering hole if it's far away from a watering hole
        prob_to_water = self.random.uniform(0, 1)
        
        
        if min_distance > 10:
            
            if prob_to_water > 0.8:
                next_move = closest_neighbor_to_target
            else:
                next_move = self.random.choice(next_moves)
                
        else:
            next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)
        

        
#Kaitlyn notes
# mesa.Agent seems to be an built in functionality of mesa used to establish agents. In this example, agents are created
# first by ascribing how they move with RandomWalker, then wolf and sheep inherit the attributes of an agent and 
# walking pattern from random walker so the sub class tree goes mesa.Agent -> RandomWalker -> wolf/sheep, and that's why
# the grass just inherits mesa.Agent because it doesn't need to move
# -

# #If we wanted to implement movement towards watering holes
# # little worried about the reel life application - what is our justification for doing this mathmatically?
# import math
#
# # Define the target location
# target_location = (0,0) # location of watering hole in bottom left corner
#
# # Function to calculate Euclidean distance between two points
# def calculate_distance(point1, point2):
#     x1, y1 = point1
#     x2, y2 = point2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
#
# # Example function to find the closest neighboring cell to the target location
# def find_closest_neighbor(agent_position, neighborhood):  #neighborhood would be next moves from above?
#     closest_neighbor = None
#     min_distance = float('inf')  # Initialize with a large value
#
#     for neighbor_cell in neighborhood:
#         distance_to_target = calculate_distance(neighbor_cell, target_location)
#         if distance_to_target < min_distance:
#             min_distance = distance_to_target
#             closest_neighbor = neighbor_cell
#
#     return closest_neighbor
#
# # wouldn't need this but would use closest_neighbor_to_target in random_move method above
# # I'm thinking we give it some probabillity it moves towards watering hole?
# # Example agent's position
# agent_position = (3, 4)  # Example agent's position coordinates
#
# # Example agent's neighborhood (can be obtained depending on the grid system or neighborhood definition)
# neighborhood = [(2, 4), (4, 4), (3, 3), (3, 5)]  # Example neighboring cells
#
# # Find the closest neighbor to the target location
# closest_neighbor_to_target = find_closest_neighbor(agent_position, neighborhood)
#
# if closest_neighbor_to_target:
#     print(f"The closest neighboring cell to the target location is {closest_neighbor_to_target}.")
# else:
#     print("No neighboring cell found.")
#     
# # from GPT 3.5, prompt: is there a way to ask if one of neighborhood is closer to a specific location on the grid?
# # Accessed 11/22/23, chat.openai.com
