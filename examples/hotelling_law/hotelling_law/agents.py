import random

import numpy as np
from mesa import Agent


class StoreAgent(Agent):
    """An agent representing a store with a price and ability to move
    and adjust prices."""

    def __init__(self, unique_id, model, price=10, can_move=True):
        # Initializes the store agent with a unique ID,
        # the model it belongs to,its initial price,
        # and whether it can move.
        super().__init__(unique_id, model)
        self.price = price  # Initial price of the store.
        self.can_move = can_move  # Indicates if the agent can move.

    def move(self):
        # Defines how the store agent moves in the environment.
        if self.can_move:
            # For a grid / line  environment, find neighboring positions and
            # randomly move to one.
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False
            )
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

    def adjust_price(self):
        # Randomly adjusts the price of the store
        # by +/- 1 within a defined range.
        self.price += self.random.choice([-1, 1])
        self.price = max(
            5, min(self.price, 15)
        )  # Ensures the price stays between 5 and 15.

    # adjust price dynamics based on neighbouring store
    def adjust_price_by_neighbour_store(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False
        )
        if not neighbors:
            return  # No adjustment if there are no neighbors

        avg_neighbor_price = np.mean([neighbor.price for neighbor in neighbors])
        price_difference = self.price - avg_neighbor_price

        # Strategy: Narrow the price gap if it's significantly
        # higher or lower than the average neighbor price
        if abs(price_difference) > 2:
            if price_difference > 0:
                # Price is significantly higher, attempt to
                # become more competitive without drastic drops
                self.price -= 1
            else:
                # Price is significantly lower, cautiously
                # increase price while remaining competitive
                self.price += 1
        else:
            # Prices are already competitive,
            # subtle adjustments for optimization
            # Random chance to slightly adjust price
            # for dynamic market response
            if random.random() < 0.1:  # 10% chance for random minor adjustment
                self.price += np.random.choice([-1, 1])

        # Ensure price stays within a reasonable range, promoting stability
        self.price = max(5, min(self.price, 15))

        # Random external factors influencing the market,
        # less frequent but can cause sudden changes
        if random.random() < 0.02:  # 2% chance for a market event
            if self.price > avg_neighbor_price:
                # Market event benefits lower-priced stores,
                # slight chance to capitalize
                self.price -= 2
            else:
                # Market event benefits higher-priced stores,
                # slight chance to capitalize
                self.price += 2

        # Re-normalize to ensure the price is
        # within bounds after adjustments
        self.price = max(5, min(self.price, 15))

    def step(self):
        # Defines the actions the store agent takes
        # in each step of the simulation.
        if self.model.mode == "default":
            # In default mode, the agent can move and
            # adjust prices if allowed.
            self.move()
            self.adjust_price_by_neighbour_store()
        elif self.model.mode == "moving_only":
            # In moving_only mode, the agent only moves if it can.
            self.move()
        elif self.model.mode == "pricing_only":
            # In pricing_only mode, the agent only adjusts its price.
            self.adjust_price_by_neighbour_store()
