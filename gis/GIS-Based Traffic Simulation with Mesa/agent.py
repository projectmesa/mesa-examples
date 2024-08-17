# agent.py

import mesa


class VehicleAgent(mesa.Agent):
    def __init__(self, unique_id, model, vehicle_type, route=None):
        super().__init__(unique_id, model)
        self.vehicle_type = vehicle_type  # Assign vehicle type (car, truck, bike)
        self.route = route  # Assign the route for the vehicle
        self.current_step = 0  # Initialize the current step in the route

    def step(self):
        if self.route and self.current_step < len(self.route):
            next_node = self.route[self.current_step]
            x = self.model.space.G.nodes[next_node]["x"] - self.model.space.min_x
            y = self.model.space.G.nodes[next_node]["y"] - self.model.space.min_y
            self.model.space.move_agent(self, (x, y))
            self.current_step += 1  # Move to the next step in the route
        else:
            pass  # Optionally, handle reaching the end of the route
