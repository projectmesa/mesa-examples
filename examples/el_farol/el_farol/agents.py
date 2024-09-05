import mesa
import numpy as np


class BarCustomer(mesa.Agent):
    def __init__(self, model, memory_size, crowd_threshold, num_strategies):
        super().__init__(model)
        # Random values from -1.0 to 1.0
        self.strategies = np.random.rand(num_strategies, memory_size + 1) * 2 - 1
        self.best_strategy = self.strategies[0]
        self.attend = False
        self.memory_size = memory_size
        self.crowd_threshold = crowd_threshold
        self.utility = 0
        self.update_strategies()

    def update_attendance(self):
        prediction = self.predict_attendance(
            self.best_strategy, self.model.history[-self.memory_size :]
        )
        if prediction <= self.crowd_threshold:
            self.attend = True
            self.model.attendance += 1
        else:
            self.attend = False

    def update_strategies(self):
        # Pick the best strategy based on new history window
        best_score = float("inf")
        for strategy in self.strategies:
            score = 0
            for week in range(self.memory_size):
                last = week + self.memory_size
                prediction = self.predict_attendance(
                    strategy, self.model.history[week:last]
                )
                score += abs(self.model.history[last] - prediction)
            if score <= best_score:
                best_score = score
                self.best_strategy = strategy
        should_attend = self.model.history[-1] <= self.crowd_threshold
        if should_attend != self.attend:
            self.utility -= 1
        else:
            self.utility += 1

    def predict_attendance(self, strategy, subhistory):
        # This is extracted from the source code of the model in
        # https://ccl.northwestern.edu/netlogo/models/ElFarol.
        # This reports an agent's prediction of the current attendance
        # using a particular strategy and portion of the attendance history.
        # More specifically, the strategy is then described by the formula
        # p(t) = x(t - 1) * a(t - 1) + x(t - 2) * a(t - 2) +..
        #      ... + x(t - memory_size) * a(t - memory_size) + c * 100,
        # where p(t) is the prediction at time t, x(t) is the attendance of the
        # bar at time t, a(t) is the weight for time t, c is a constant, and
        # MEMORY-SIZE is an external parameter.

        # The first element of the strategy is the constant, c, in the
        # prediction formula. one can think of it as the the agent's prediction
        # of the bar's attendance in the absence of any other data then we
        # multiply each week in the history by its respective weight.
        return strategy[0] * 100 + np.dot(strategy[1:], subhistory)
